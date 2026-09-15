"""
SignalScope — Domain Contracts & Typed Schemas
Strictly decoupled data contracts mirroring future React TypeScript interfaces.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple


class VerdictTier(str, Enum):
    CONFIDENT_AI = "confident_ai"
    CONFIDENT_REAL = "confident_real"
    UNCERTAIN = "uncertain"


@dataclass
class VerdictResult:
    """Primary classification verdict with responsible framing."""
    label: str                                   # "AI-generated" | "Authentic Real"
    confidence: float                            # 0.0 to 1.0 (calibrated)
    raw_confidence: float                        # Uncalibrated model output
    tier: VerdictTier
    badge_text: str                              # "LIKELY AI" | "LIKELY REAL" | "UNCERTAIN"
    badge_color: str                             # Hex code
    icon: str                                    # Unicode or emoji
    action_recommendation: str                   # Plain-English guideline for user
    optimal_threshold: float = 0.50

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "confidence": round(self.confidence, 4),
            "raw_confidence": round(self.raw_confidence, 4),
            "tier": self.tier.value,
            "badge_text": self.badge_text,
            "badge_color": self.badge_color,
            "icon": self.icon,
            "action_recommendation": self.action_recommendation,
            "optimal_threshold": self.optimal_threshold,
        }


@dataclass
class ForensicCue:
    """Individual explainability forensic cue grounded in model activations."""
    cue_type: str                                # e.g. "Texture Anomaly", "Spectral Grid"
    description: str                             # Human-readable forensic cue description
    severity: str                                # "high" | "medium" | "low" | "info"
    confidence: float                            # 0.0 to 1.0
    location: Optional[str] = None               # Sub-region description e.g. "Central object"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cue_type": self.cue_type,
            "description": self.description,
            "severity": self.severity,
            "confidence": round(self.confidence, 3),
            "location": self.location,
        }


@dataclass
class MetadataReport:
    """EXIF, GPS, camera hardware tags, and C2PA Content Credentials."""
    has_exif: bool
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    software: Optional[str] = None
    datetime_original: Optional[str] = None
    exposure_time: Optional[str] = None
    f_number: Optional[float] = None
    iso: Optional[int] = None
    focal_length: Optional[str] = None
    gps_coords: Optional[Dict[str, float]] = None
    is_ai_software_detected: bool = False
    ai_software_names: List[str] = field(default_factory=list)
    c2pa_present: bool = False
    c2pa_status: str = "NOT_FOUND"               # "VALID_AUTHENTIC" | "VALID_AI_CREDENTIAL" | "TAMPERED" | "NOT_FOUND"
    c2pa_issuer: Optional[str] = None
    c2pa_claim_generator: Optional[str] = None
    anomalies: List[str] = field(default_factory=list)
    trust_signal: str = "NEUTRAL"                # "STRONG_AUTHENTIC" | "PROBABLE_AI" | "SUSPICIOUS_STRIPPED" | "CONFIRMED_SYNTHETIC" | "NEUTRAL"
    raw_tags: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "has_exif": self.has_exif,
            "camera_make": self.camera_make,
            "camera_model": self.camera_model,
            "software": self.software,
            "datetime_original": self.datetime_original,
            "exposure_time": self.exposure_time,
            "f_number": self.f_number,
            "iso": self.iso,
            "focal_length": self.focal_length,
            "gps_coords": self.gps_coords,
            "is_ai_software_detected": self.is_ai_software_detected,
            "ai_software_names": self.ai_software_names,
            "c2pa_present": self.c2pa_present,
            "c2pa_status": self.c2pa_status,
            "c2pa_issuer": self.c2pa_issuer,
            "c2pa_claim_generator": self.c2pa_claim_generator,
            "anomalies": self.anomalies,
            "trust_signal": self.trust_signal,
        }


@dataclass
class SpectralData:
    """Radially-averaged FFT azimuthal spectrum and compression artifact data."""
    azimuthal_freqs: List[float] = field(default_factory=list)  # (128,) normalized curve
    jpeg_ghost_levels: List[int] = field(default_factory=list)  # Quality steps [50..95]
    jpeg_ghost_diffs: List[float] = field(default_factory=list) # Mean absolute diffs
    has_bayer_trace: bool = False
    bayer_confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "azimuthal_freqs": [round(x, 4) for x in self.azimuthal_freqs],
            "jpeg_ghost_levels": self.jpeg_ghost_levels,
            "jpeg_ghost_diffs": [round(x, 4) for x in self.jpeg_ghost_diffs],
            "has_bayer_trace": self.has_bayer_trace,
            "bayer_confidence": round(self.bayer_confidence, 3),
        }


@dataclass
class AnalysisResponse:
    """Complete diagnostic response payload for a single image."""
    filename: str
    image_size: Tuple[int, int]                  # (width, height)
    verdict: VerdictResult
    generator_family: str                        # "Diffusion-family" | "GAN-family" | "Autoregressive" | "Camera / Real" | "Unknown"
    cues: List[ForensicCue]
    metadata: MetadataReport
    spectral: SpectralData
    heatmap_array: Optional[Any] = None          # 2D normalized fused heatmap (H, W) or None
    attn_array: Optional[Any] = None             # 2D normalized DINOv2 attention rollout (H, W) or None
    srm_array: Optional[Any] = None              # 2D normalized SRM noise residual (H, W) or None
    summary_explanation: Optional[str] = None    # Grounded natural language summary from cue descriptors
    processing_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "image_size": self.image_size,
            "verdict": self.verdict.to_dict(),
            "generator_family": self.generator_family,
            "cues": [c.to_dict() for c in self.cues],
            "metadata": self.metadata.to_dict(),
            "spectral": self.spectral.to_dict(),
            "summary_explanation": self.summary_explanation,
            "processing_time_ms": round(self.processing_time_ms, 2),
        }


@dataclass
class BatchItemResult:
    """Row item summary for batch scanning."""
    filename: str
    label: str
    confidence: float
    tier: str
    generator_family: str
    c2pa_status: str
    anomaly_count: int
    processing_time_ms: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Filename": self.filename,
            "Verdict": self.label,
            "Confidence": f"{self.confidence * 100:.1f}%",
            "Tier": self.tier,
            "Generator": self.generator_family,
            "C2PA": self.c2pa_status,
            "Anomalies": self.anomaly_count,
            "Latency (ms)": f"{self.processing_time_ms:.1f}",
        }
