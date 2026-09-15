"""
SignalScope — Provenance Report & Decision Combination Logic
Fuses Computer Vision confidence with Metadata/C2PA signals into a unified verdict.
"""
from typing import Any, Tuple
from .deep_exif import extract_deep_exif
from .exif_auditor import audit_metadata
from .c2pa_checker import check_c2pa_provenance
from app.schemas.contracts import MetadataReport


def generate_provenance_report(image_source: Any) -> MetadataReport:
    """
    Generate comprehensive MetadataReport combining Deep EXIF, Audit, and C2PA checks.
    
    Args:
        image_source: File path, bytes, or PIL Image.
        
    Returns:
        Structured MetadataReport object.
    """
    exif_dict = extract_deep_exif(image_source)
    audit_res = audit_metadata(exif_dict)
    c2pa_res = check_c2pa_provenance(image_source)

    # Determine unified Trust Signal
    if c2pa_res.get("status") == "VALID_AI_CREDENTIAL" or audit_res["is_ai_software_detected"]:
        trust_signal = "CONFIRMED_SYNTHETIC"
    elif c2pa_res.get("status") == "VALID_AUTHENTIC" and audit_res["has_authentic_camera_tags"]:
        trust_signal = "STRONG_AUTHENTIC"
    elif not exif_dict.get("has_exif") and not c2pa_res.get("present"):
        trust_signal = "SUSPICIOUS_STRIPPED"
    elif audit_res["has_authentic_camera_tags"]:
        trust_signal = "LIKELY_AUTHENTIC_HARDWARE"
    else:
        trust_signal = "NEUTRAL"

    return MetadataReport(
        has_exif=exif_dict.get("has_exif", False),
        camera_make=exif_dict.get("camera_make"),
        camera_model=exif_dict.get("camera_model"),
        software=exif_dict.get("software"),
        datetime_original=exif_dict.get("datetime_original"),
        exposure_time=exif_dict.get("exposure_time"),
        f_number=exif_dict.get("f_number"),
        iso=exif_dict.get("iso"),
        focal_length=exif_dict.get("focal_length"),
        gps_coords=exif_dict.get("gps_coords"),
        is_ai_software_detected=audit_res["is_ai_software_detected"],
        ai_software_names=audit_res["detected_ai_software"],
        c2pa_present=c2pa_res.get("present", False),
        c2pa_status=c2pa_res.get("status", "NOT_FOUND"),
        c2pa_issuer=c2pa_res.get("issuer"),
        c2pa_claim_generator=c2pa_res.get("claim_generator"),
        anomalies=audit_res["anomalies"],
        trust_signal=trust_signal,
        raw_tags=exif_dict.get("raw_tags", {}),
    )


def fuse_cv_with_provenance(
    cv_confidence: float,
    metadata_report: MetadataReport
) -> Tuple[float, str, str]:
    """
    Fuse raw Computer Vision confidence with Metadata/C2PA signals.
    
    Returns:
        (adjusted_confidence, label, action_note)
    """
    adjusted_conf = cv_confidence
    action_note = "Model prediction based on visual and spectral forensics."

    # Case 1: Definite cryptographic or software AI proof
    if metadata_report.c2pa_status == "VALID_AI_CREDENTIAL":
        adjusted_conf = max(0.985, cv_confidence)
        action_note = "Confirmed AI: Verified C2PA Content Credential indicates generative creation."
        return adjusted_conf, "AI-generated", action_note

    if metadata_report.is_ai_software_detected:
        adjusted_conf = max(0.960, cv_confidence)
        tools = ", ".join(metadata_report.ai_software_names)
        action_note = f"Confirmed AI: Found generative tool fingerprints in metadata ({tools})."
        return adjusted_conf, "AI-generated", action_note

    # Case 2: Cryptographic authentic camera capture
    if metadata_report.c2pa_status == "VALID_AUTHENTIC":
        if cv_confidence < 0.70:
            adjusted_conf = min(0.08, cv_confidence * 0.5)
            action_note = "High Authenticity: Validated C2PA hardware capture signature."
            return adjusted_conf, "Authentic Real", action_note
        else:
            # Conflict: C2PA says camera, but model strongly detects synthetic manipulation
            adjusted_conf = 0.50  # Push to uncertain
            action_note = "Forensic Conflict: Valid camera C2PA signature, but visual detector found high-confidence synthetic artifacts. Review for deepfake/face-swap."
            return adjusted_conf, "Uncertain — Forensic Conflict", action_note

    # Case 3: Complete camera hardware profile without anomalies
    if metadata_report.trust_signal in ("LIKELY_AUTHENTIC_HARDWARE", "STRONG_AUTHENTIC"):
        cam_info = f"{metadata_report.camera_make or ''} {metadata_report.camera_model or ''}".strip() or "Camera"
        if cv_confidence >= 0.75:
            # Forensic Conflict: Authentic optical camera hardware profile verified, but visual stream
            # flagged surface smoothing/compression typical of smartphone front-camera computational beauty/HDR processing.
            adjusted_conf = 0.50
            action_note = (
                f"Forensic Conflict: Hardware tags verified authentic ({cam_info}), but visual model "
                f"detected surface smoothing/noise anomalies typical of smartphone front-camera computational beauty/HDR processing. Human review recommended."
            )
            return adjusted_conf, "Uncertain — Forensic Conflict", action_note
        elif cv_confidence >= 0.35:
            adjusted_conf = cv_confidence * 0.40
            action_note = f"Authentic Profile: Consistent hardware tags ({cam_info})."
            return adjusted_conf, "Authentic Real", action_note
        else:
            adjusted_conf = min(0.05, cv_confidence * 0.5)
            action_note = f"Authentic Profile: Consistent hardware tags ({cam_info})."
            return adjusted_conf, "Authentic Real", action_note

    # Case 4: Stripped metadata
    elif metadata_report.trust_signal == "SUSPICIOUS_STRIPPED":
        # Stripped EXIF is very common on social media and AI; slight boost to confidence if leaning AI
        if cv_confidence > 0.60:
            adjusted_conf = min(0.98, cv_confidence * 1.05)
            action_note = "Caution: Metadata is stripped. Forensic assessment relies on pixel and frequency features."

    final_label = "AI-generated" if adjusted_conf >= 0.50 else "Authentic Real"
    return round(adjusted_conf, 4), final_label, action_note
