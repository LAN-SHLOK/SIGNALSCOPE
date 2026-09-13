"""
Tests for SignalScope Metadata & Provenance Engine (Role 5)
"""
import pytest
import io
from PIL import Image, PngImagePlugin
from src.metadata.deep_exif import extract_deep_exif
from src.metadata.exif_auditor import audit_metadata
from src.metadata.c2pa_checker import check_c2pa_provenance
from src.metadata.provenance_report import generate_provenance_report, fuse_cv_with_provenance
from app.schemas.contracts import MetadataReport


def create_blank_test_image(format="JPEG", metadata=None) -> io.BytesIO:
    """Helper to create an in-memory image."""
    img = Image.new("RGB", (100, 100), color=(255, 128, 64))
    buf = io.BytesIO()
    if metadata and format == "PNG":
        img.save(buf, format=format, pnginfo=metadata)
    else:
        img.save(buf, format=format)
    buf.seek(0)
    return buf


def test_stripped_metadata():
    """Verify that images without EXIF are correctly audited as stripped."""
    buf = create_blank_test_image(format="JPEG")
    report = generate_provenance_report(buf)
    
    assert report.has_exif is False
    assert report.is_ai_software_detected is False
    assert report.trust_signal == "SUSPICIOUS_STRIPPED"
    assert any("Stripped metadata" in a for a in report.anomalies)


def test_png_ai_parameters_detection():
    """Verify that generation parameters in PNG text chunks are caught."""
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", "cyberpunk detective, masterpiece, steps: 30, sampler: DPM++ 2M")
    buf = create_blank_test_image(format="PNG", metadata=pnginfo)

    report = generate_provenance_report(buf)
    assert report.is_ai_software_detected is True
    assert "diffusion_parameters" in report.ai_software_names or "automatic1111" in report.ai_software_names
    assert report.trust_signal == "CONFIRMED_SYNTHETIC"


def test_c2pa_binary_detection():
    """Verify fallback detection of C2PA JUMBF containers."""
    # Synthetic binary payload with C2PA and Firefly tags
    fake_c2pa_data = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xFF\xEB\x00\x40c2pa_manifest_Adobe Firefly_c2pa.ai_generated\xFF\xD9"
    res = check_c2pa_provenance(fake_c2pa_data)

    assert res["present"] is True
    assert res["status"] == "VALID_AI_CREDENTIAL"
    assert "Firefly" in res["claim_generator"]


def test_fuse_cv_with_provenance_ai_override():
    """Verify that confirmed AI credentials override marginal CV score."""
    report = MetadataReport(
        has_exif=False,
        c2pa_present=True,
        c2pa_status="VALID_AI_CREDENTIAL",
        is_ai_software_detected=True,
        ai_software_names=["midjourney"],
        trust_signal="CONFIRMED_SYNTHETIC",
    )
    # Model had weak score 0.55, but metadata has definite proof
    conf, label, note = fuse_cv_with_provenance(0.55, report)
    assert conf >= 0.98
    assert label == "AI-generated"
    assert "Confirmed AI" in note


def test_fuse_cv_with_provenance_conflict():
    """Verify that authentic camera C2PA with high-confidence AI CV triggers a review conflict."""
    report = MetadataReport(
        has_exif=True,
        c2pa_present=True,
        c2pa_status="VALID_AUTHENTIC",
        camera_make="Leica",
        camera_model="M11",
        trust_signal="STRONG_AUTHENTIC",
    )
    conf, label, note = fuse_cv_with_provenance(0.92, report)
    assert conf == 0.50
    assert "Conflict" in label or "Conflict" in note
