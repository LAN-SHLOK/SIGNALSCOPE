"""
SignalScope — Central Configuration.
All hyperparameters, paths, and constants in one place.
"""
from pathlib import Path
import torch

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = PROJECT_ROOT / "cache"           # Pre-extracted features (.npy)
WEIGHTS_DIR = PROJECT_ROOT / "model" / "weights"
OUTPUT_DIR = PROJECT_ROOT / "output"

# ── Device ─────────────────────────────────────────────────────────────────────
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ── DINOv2 Backbone ───────────────────────────────────────────────────────────
DINO_MODEL_NAME = "dinov2_vitl14_reg"        # ViT-L/14 with register tokens
DINO_INPUT_SIZE = 518                         # DINOv2 native resolution
DINO_EMBED_DIM = 1024                         # Per-layer embedding dimension
DINO_LAYER_INDICES = [8, 16, 20, 24]          # Multi-layer extraction points
DINO_CLS_DIM = DINO_EMBED_DIM * len(DINO_LAYER_INDICES)  # 4096
DINO_NUM_PATCHES = 37 * 37                    # 1369 patches at 518×518

# Fallback if GPU memory is tight (T4 16GB)
DINO_FALLBACK_MODEL = "dinov2_vitb14_reg"     # ViT-B/14: 768-dim, 50% less memory
DINO_FALLBACK_EMBED_DIM = 768

# ── Patch Statistics ───────────────────────────────────────────────────────────
PATCH_STATS_DIM = DINO_EMBED_DIM * 3 + 1     # mean + std + max + avg_sim = 3073
PATCH_SIM_NUM_SAMPLES = 200                   # Sampled pairs for avg_sim (memory-safe)

# ── Spectral Branch ───────────────────────────────────────────────────────────
SRM_NUM_COLORSPACES = 3                       # RGB, YCbCr, HSV
SRM_KERNELS_PER_SPACE = 3                     # 1st, 2nd, 3rd order
SRM_CHANNELS = SRM_NUM_COLORSPACES * SRM_KERNELS_PER_SPACE  # 9
SPECTRAL_CNN_OUT_DIM = 256
FFT_BINS = 128
FFT_MLP_OUT_DIM = 128
JPEG_QUALITY_RANGE = range(50, 100, 5)        # 10 quality levels
JPEG_FEATURES_DIM = len(JPEG_QUALITY_RANGE) * 2  # mean + std per level = 20
BAYER_FEATURES_DIM = 2

# ── Fusion Dimensions ─────────────────────────────────────────────────────────
TOTAL_FEATURE_DIM = (
    DINO_CLS_DIM +           # 4096
    PATCH_STATS_DIM +         # 3073
    SPECTRAL_CNN_OUT_DIM +    # 256
    FFT_MLP_OUT_DIM +         # 128
    JPEG_FEATURES_DIM +       # 20
    BAYER_FEATURES_DIM         # 2
)  # = 7575

# ── Training ──────────────────────────────────────────────────────────────────
BATCH_SIZE = 16                               # T4-safe; use 32 on A100
GRADIENT_ACCUMULATION_STEPS = 4               # Effective batch = 64
LEARNING_RATE = 3e-4
WEIGHT_DECAY = 0.01
EPOCHS = 15
EARLY_STOPPING_PATIENCE = 3
LABEL_SMOOTHING = 0.05
BINARY_LOSS_WEIGHT = 0.8
ATTRIBUTION_LOSS_WEIGHT = 0.2
WARMUP_STEPS = 500
NUM_WORKERS = 4

# ── Attribution Classes ───────────────────────────────────────────────────────
ATTRIBUTION_CLASSES = ["Real", "GAN-family", "Diffusion-family", "Unknown"]
NUM_ATTRIBUTION_CLASSES = len(ATTRIBUTION_CLASSES)

# ── Inference ─────────────────────────────────────────────────────────────────
TTA_NUM_VIEWS = 5
CONFIDENT_AI_THRESHOLD = 0.75
CONFIDENT_REAL_THRESHOLD = 0.25
MAX_FPR_CONSERVATIVE = 0.05

# ── ImageNet Normalization (used by DINOv2) ────────────────────────────────────
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# ── LightGBM Stacking ─────────────────────────────────────────────────────────
LGBM_N_ESTIMATORS = 500
LGBM_LEARNING_RATE = 0.05
LGBM_MAX_DEPTH = 6
LGBM_NUM_LEAVES = 31
LGBM_SUBSAMPLE = 0.8
LGBM_COLSAMPLE_BYTREE = 0.8

LGBM_PARAMS = {
    'n_estimators': LGBM_N_ESTIMATORS,
    'learning_rate': LGBM_LEARNING_RATE,
    'max_depth': LGBM_MAX_DEPTH,
    'num_leaves': LGBM_NUM_LEAVES,
    'subsample': LGBM_SUBSAMPLE,
    'colsample_bytree': LGBM_COLSAMPLE_BYTREE,
    'random_state': 42,
    'verbose': -1,
}

# ── Temperature Scaling ───────────────────────────────────────────────────────
TEMP_SCALING_INIT = 1.5
TEMP_SCALING_LR = 0.01
TEMP_SCALING_MAX_ITER = 50
INITIAL_TEMPERATURE = TEMP_SCALING_INIT
