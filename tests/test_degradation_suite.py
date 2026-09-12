import pytest
import numpy as np
from src.robustness.degradation_suite import (
    degrade_image, 
    run_degradation_suite,
    evaluate_degradation_curve,
    get_planned_degradations
)

@pytest.fixture
def sample_image():
    # 64x64 RGB uint8 image
    return np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)

@pytest.fixture
def dataset_mock():
    # 4 mock images
    images = [np.random.randint(0, 256, (32, 32, 3), dtype=np.uint8) for _ in range(4)]
    labels = np.array([0, 1, 0, 1])
    return images, labels

def mock_eval_func(images):
    # Dummy evaluator returning random predictions
    # Deterministic if np seed is set
    return np.random.rand(len(images))


def test_degrade_image_all_types(sample_image):
    conditions = get_planned_degradations()
    for condition in conditions:
        deg = condition['degradation']
        sev = condition['severity']
        
        if deg == 'clean':
            continue
            
        degraded = degrade_image(sample_image.copy(), deg, sev, seed=42)
        
        assert degraded.shape == sample_image.shape
        assert degraded.dtype == np.uint8

def test_degrade_image_determinism(sample_image):
    deg = 'salt_pepper'
    sev = 0.1
    img1 = degrade_image(sample_image.copy(), deg, sev, seed=42)
    img2 = degrade_image(sample_image.copy(), deg, sev, seed=42)
    img3 = degrade_image(sample_image.copy(), deg, sev, seed=43)
    
    assert np.array_equal(img1, img2)
    assert not np.array_equal(img1, img3)

def test_run_degradation_suite(dataset_mock):
    images, labels = dataset_mock
    
    np.random.seed(42)
    results = run_degradation_suite(mock_eval_func, images, labels, seed=42)
    
    conditions = get_planned_degradations()
    assert len(results) == len(conditions)
    
    for r in results:
        assert 'degradation' in r
        assert 'severity' in r
        assert 'metric' in r
        assert r['metric'] == 'roc_auc'
        assert 'value' in r
        assert not np.isnan(r['value']), "AUC should not be NaN for mixed labels"
        assert r['n_samples'] == len(labels)

def test_evaluate_degradation_curve(dataset_mock):
    images, labels = dataset_mock
    np.random.seed(42)
    results = run_degradation_suite(mock_eval_func, images, labels, seed=42)
    
    curve = evaluate_degradation_curve(results, 'jpeg')
    
    # We should have 6 JPEG conditions
    assert len(curve) == 6
    # Curve is list of (severity, auc)
    for sev, auc in curve:
        assert isinstance(sev, int)
        assert isinstance(auc, float)
    
    # Should be sorted by severity
    severities = [c[0] for c in curve]
    assert severities == sorted(severities)

