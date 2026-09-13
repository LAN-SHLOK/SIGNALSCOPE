"""
SignalScope — EXIF Parser Interface (Role 5)
Convenience adapter bridging deep EXIF extraction and metadata auditing.
"""
from typing import Dict, Any
from .deep_exif import extract_deep_exif
from .exif_auditor import audit_metadata


def extract_exif_signals(image_source: Any) -> Dict[str, Any]:
    """
    Extract technical EXIF metadata and audit for AI footprints in one call.
    
    Args:
        image_source: Image file path, binary bytes, or PIL Image.
        
    Returns:
        Consolidated dictionary with EXIF tags, GPS, and AI audit flags.
    """
    exif_data = extract_deep_exif(image_source)
    audit_data = audit_metadata(exif_data)
    
    return {
        "has_exif": exif_data.get("has_exif", False),
        "camera_make": exif_data.get("camera_make"),
        "camera_model": exif_data.get("camera_model"),
        "software": exif_data.get("software"),
        "datetime_original": exif_data.get("datetime_original"),
        "exposure_time": exif_data.get("exposure_time"),
        "f_number": exif_data.get("f_number"),
        "iso": exif_data.get("iso"),
        "focal_length": exif_data.get("focal_length"),
        "gps_coords": exif_data.get("gps_coords"),
        "is_ai_software_detected": audit_data.get("is_ai_software_detected", False),
        "detected_ai_software": audit_data.get("detected_ai_software", []),
        "anomalies": audit_data.get("anomalies", []),
        "has_authentic_camera_tags": audit_data.get("has_authentic_camera_tags", False),
        "raw_tags": exif_data.get("raw_tags", {}),
    }


def parse_exif(image_source: Any) -> Dict[str, Any]:
    """Alias for extract_deep_exif."""
    return extract_deep_exif(image_source)
