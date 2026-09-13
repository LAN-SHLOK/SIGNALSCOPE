"""
Test Suite for SignalScope FastAPI Server
Verifies REST endpoints for health check, single image scan, and batch audit.
"""
import io
import pytest
from PIL import Image
from starlette.testclient import TestClient

from api.server import app

client = TestClient(app)


def _create_dummy_image_bytes(format="JPEG", color=(100, 150, 200)) -> bytes:
    img = Image.new("RGB", (128, 128), color=color)
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


def test_health_check():
    """Verify /api/health endpoint returns 200 OK and healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "SignalScope" in data["service"]


def test_analyze_image_endpoint():
    """Verify /api/analyze endpoint accepts an image and returns full forensic report."""
    img_bytes = _create_dummy_image_bytes()
    files = {"file": ("test_sample.jpg", img_bytes, "image/jpeg")}

    response = client.post("/api/analyze", files=files)
    assert response.status_code == 200
    data = response.json()

    # Verify contracts
    assert "id" in data
    assert data["name"] == "test_sample.jpg"
    assert data["verdictTier"] in ["confident_ai", "confident_real", "uncertain"]
    assert "confidence" in data
    assert "imgUrl" in data and data["imgUrl"].startswith("data:image/")
    assert "heatmapOverlayUrl" in data and data["heatmapOverlayUrl"].startswith("data:image/")
    assert "attentionRolloutUrl" in data and data["attentionRolloutUrl"].startswith("data:image/")
    assert "srmResidualUrl" in data and data["srmResidualUrl"].startswith("data:image/")
    assert "fftSpectrumUrl" in data and data["fftSpectrumUrl"].startswith("data:image/")
    assert "exif" in data
    assert "c2pa" in data
    assert "cues" in data
    assert isinstance(data["cues"], list)
    assert "fftStats" in data


def test_batch_analyze_endpoint():
    """Verify /api/batch endpoint processes multiple files and returns summary rows."""
    img1 = _create_dummy_image_bytes(color=(255, 0, 0))
    img2 = _create_dummy_image_bytes(color=(0, 255, 0))

    files = [
        ("files", ("img1.jpg", img1, "image/jpeg")),
        ("files", ("img2.jpg", img2, "image/jpeg")),
    ]

    response = client.post("/api/batch", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert data["items"][0]["filename"] == "img1.jpg"
    assert data["items"][1]["filename"] == "img2.jpg"
