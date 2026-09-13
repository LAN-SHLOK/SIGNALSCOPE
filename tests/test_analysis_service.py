"""
Tests for SignalScope Analysis Service Layer
"""
import io
import numpy as np
from PIL import Image
from app.services.analysis_service import AnalysisService
from app.schemas.contracts import AnalysisResponse, VerdictTier


def test_analysis_service_blank_image():
    """Verify that AnalysisService processes an image end-to-end and returns a valid contract."""
    service = AnalysisService()
    img = Image.new("RGB", (256, 256), color=(100, 150, 200))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    res: AnalysisResponse = service.analyze_image(buf.getvalue(), filename="test_sample.jpg")

    assert res.filename == "test_sample.jpg"
    assert res.image_size == (256, 256)
    assert res.verdict is not None
    assert 0.0 <= res.verdict.confidence <= 1.0
    assert res.verdict.tier in [VerdictTier.CONFIDENT_AI, VerdictTier.CONFIDENT_REAL, VerdictTier.UNCERTAIN]
    assert len(res.cues) > 0
    assert res.spectral is not None
    assert len(res.spectral.azimuthal_freqs) == 128
    assert len(res.spectral.jpeg_ghost_diffs) == 10
    assert res.processing_time_ms > 0


def test_analysis_service_batch():
    """Verify that batch processing returns valid BatchItemResults."""
    service = AnalysisService()
    img = Image.new("RGB", (128, 128), color=(20, 20, 20))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    data = buf.getvalue()

    items = [("img1.jpg", data), ("img2.jpg", data)]
    batch_res = service.batch_analyze(items)

    assert len(batch_res) == 2
    assert batch_res[0].filename == "img1.jpg"
    assert batch_res[1].filename == "img2.jpg"
