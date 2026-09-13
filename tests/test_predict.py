"""
Test Suite for SignalScope Predict Interface (Role 5)
Verifies end-to-end command-line prediction, explanation, and schema contracts.
"""
import io
import json
from pathlib import Path
import pytest
from PIL import Image

from predict import predict_single


@pytest.fixture
def dummy_image_file(tmp_path):
    """Create a temporary test JPEG image file."""
    img_path = tmp_path / "test_eval_img.jpg"
    img = Image.new("RGB", (256, 256), color=(120, 180, 240))
    img.save(img_path, format="JPEG")
    return img_path


def test_predict_single_base_schema(dummy_image_file):
    """Verify single image prediction returns all mandatory JSON contract keys."""
    result = predict_single(dummy_image_file, explain=False)
    
    assert "filename" in result
    assert result["filename"] == "test_eval_img.jpg"
    assert "label" in result
    assert result["label"] in ["AI-generated", "Authentic Real", "Uncertain — Forensic Conflict"]
    assert "confidence" in result
    assert 0.0 <= result["confidence"] <= 1.0
    assert "tier" in result
    assert result["tier"] in ["confident_ai", "confident_real", "uncertain"]
    assert "generator_family" in result
    assert "metadata" in result
    assert "has_exif" in result["metadata"]
    assert "has_c2pa" in result["metadata"]
    assert "spectral" in result
    assert "latency_ms" in result


def test_predict_single_with_explain(dummy_image_file, tmp_path):
    """Verify --explain generates visual heatmap overlay and grounded cue explanation."""
    out_dir = tmp_path / "test_output"
    result = predict_single(dummy_image_file, explain=True, output_dir=str(out_dir))
    
    assert "explanation" in result
    assert "verdict" in result["explanation"]
    assert "primary_cues" in result["explanation"]
    assert isinstance(result["explanation"]["primary_cues"], list)
    assert "caveat" in result["explanation"]
    assert "heatmap_path" in result
    assert result["heatmap_path"] is not None
    assert Path(result["heatmap_path"]).exists()
