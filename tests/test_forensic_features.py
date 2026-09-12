import torch
import pytest
import numpy as np

from src.features.srm_filters import SRMFilters
from src.features.frequency import FrequencyFeatures
from src.features.jpeg_ghost import JPEGGhostFeatures
from src.features.bayer_detection import BayerDetectionFeatures


@pytest.fixture
def random_batch():
    # Batch of 2, 3 channels, 64x64, values in [0, 1]
    return torch.rand(2, 3, 64, 64)

@pytest.fixture
def flat_batch():
    # Flat image (e.g. all 0.5)
    return torch.full((2, 3, 32, 32), 0.5)

@pytest.fixture
def small_batch():
    # Pathologically small image
    return torch.rand(2, 3, 2, 2)


class TestSRMFilters:
    def test_srm_output_shape(self, random_batch):
        model = SRMFilters()
        out = model(random_batch)
        assert out.shape == (2, 9, 64, 64), f"Expected (2, 9, 64, 64), got {out.shape}"
        
    def test_srm_no_nans(self, random_batch):
        model = SRMFilters()
        out = model(random_batch)
        assert not torch.isnan(out).any()
        assert not torch.isinf(out).any()
        
    def test_srm_flat_image(self, flat_batch):
        model = SRMFilters()
        out = model(flat_batch)
        # SRM of flat image should be mostly 0 except at boundaries where padding affects it
        # Actually, reflection/zero padding might produce non-zeros at edges, but it shouldn't crash
        assert not torch.isnan(out).any()

    def test_srm_determinism(self, random_batch):
        model = SRMFilters()
        out1 = model(random_batch)
        out2 = model(random_batch.clone())
        assert torch.allclose(out1, out2)


class TestFrequencyFeatures:
    def test_frequency_output_shape(self, random_batch):
        model = FrequencyFeatures(num_bins=128)
        out = model(random_batch)
        assert out.shape == (2, 128), f"Expected (2, 128), got {out.shape}"
        
    def test_frequency_no_nans(self, random_batch):
        model = FrequencyFeatures()
        out = model(random_batch)
        assert not torch.isnan(out).any()
        assert not torch.isinf(out).any()
        
    def test_frequency_flat_image(self, flat_batch):
        model = FrequencyFeatures()
        out = model(flat_batch)
        assert not torch.isnan(out).any()
        
    def test_frequency_small_image(self, small_batch):
        model = FrequencyFeatures()
        out = model(small_batch)
        assert out.shape == (2, 128)
        assert not torch.isnan(out).any()

    def test_frequency_determinism(self, random_batch):
        model = FrequencyFeatures()
        out1 = model(random_batch)
        out2 = model(random_batch.clone())
        assert torch.allclose(out1, out2)


class TestJPEGGhostFeatures:
    def test_jpeg_output_shape(self, random_batch):
        model = JPEGGhostFeatures()
        out = model(random_batch)
        assert out.shape == (2, 20), f"Expected (2, 20), got {out.shape}"
        
    def test_jpeg_no_nans(self, random_batch):
        model = JPEGGhostFeatures()
        out = model(random_batch)
        assert not torch.isnan(out).any()
        assert not torch.isinf(out).any()
        
    def test_jpeg_flat_image(self, flat_batch):
        model = JPEGGhostFeatures()
        out = model(flat_batch)
        assert not torch.isnan(out).any()
        
    def test_jpeg_small_image(self, small_batch):
        model = JPEGGhostFeatures()
        out = model(small_batch)
        assert out.shape == (2, 20)
        assert not torch.isnan(out).any()
        
    def test_jpeg_determinism(self, random_batch):
        model = JPEGGhostFeatures()
        out1 = model(random_batch)
        out2 = model(random_batch.clone())
        assert torch.allclose(out1, out2)


class TestBayerDetectionFeatures:
    def test_bayer_output_shape(self, random_batch):
        model = BayerDetectionFeatures(patch_size=32)
        out = model(random_batch)
        assert out.shape == (2, 2), f"Expected (2, 2), got {out.shape}"
        
    def test_bayer_no_nans(self, random_batch):
        model = BayerDetectionFeatures(patch_size=32)
        out = model(random_batch)
        assert not torch.isnan(out).any()
        assert not torch.isinf(out).any()
        
    def test_bayer_flat_image(self, flat_batch):
        model = BayerDetectionFeatures(patch_size=32)
        out = model(flat_batch)
        assert not torch.isnan(out).any()
        
    def test_bayer_small_image(self, small_batch):
        model = BayerDetectionFeatures(patch_size=32)
        out = model(small_batch)
        assert out.shape == (2, 2)
        assert not torch.isnan(out).any()
        
    def test_bayer_determinism(self, random_batch):
        model = BayerDetectionFeatures(patch_size=32)
        out1 = model(random_batch)
        out2 = model(random_batch.clone())
        assert torch.allclose(out1, out2)

