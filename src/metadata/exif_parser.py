"""
Module D: Provenance & Metadata Analysis for SignalScope.
Extracts and analyzes EXIF metadata, camera hardware provenance, 
AI generator signatures, and C2PA / Content Credentials.
"""

import os
from typing import Dict, Any, Optional
from PIL import Image, ExifTags


KNOWN_CAMERA_MAKES = {
    'apple', 'samsung', 'google', 'sony', 'canon', 'nikon', 'fujifilm',
    'olympus', 'panasonic', 'leica', 'xiaomi', 'oneplus', 'oppo', 'vivo',
    'huawei', 'motorola', 'realme', 'hasselblad', 'pentax'
}

AI_SOFTWARE_SIGNATURES = [
    'stable diffusion', 'midjourney', 'dall-e', 'dalle', 'automatic1111',
    'comfyui', 'novelai', 'invokeai', 'fooocus', 'adobe firefly', 'flux',
    'bing image creator', 'chatgpt', 'imagine'
]


def extract_exif_signals(image_path: str) -> Dict[str, Any]:
    """
    Extracts and evaluates forensic metadata from an image file.

    Args:
        image_path: Path to the image file.

    Returns:
        Dictionary containing extracted metadata fields, provenance classification,
        and an authenticity signal score (-1.0 to +1.0).
    """
    result = {
        "has_exif": False,
        "has_c2pa": False,
        "camera_make": None,
        "camera_model": None,
        "lens_model": None,
        "exposure_time": None,
        "f_number": None,
        "iso": None,
        "datetime_original": None,
        "software": None,
        "ai_tool_detected": None,
        "provenance_tier": "neutral",
        "provenance_score": 0.0
    }

    if not os.path.exists(image_path):
        return result

    try:
        with open(image_path, "rb") as f:
            header = f.read(65536)
            if b"c2pa" in header or b"urn:uuid:84966870-76" in header or b"JUMBF" in header:
                result["has_c2pa"] = True

        with Image.open(image_path) as img:
            if hasattr(img, "info") and isinstance(img.info, dict):
                info_str = " ".join([f"{k}: {v}" for k, v in img.info.items() if isinstance(v, str)]).lower()
                for sig in AI_SOFTWARE_SIGNATURES:
                    if sig in info_str:
                        result["ai_tool_detected"] = sig.title()
                        result["provenance_tier"] = "ai_watermark_detected"
                        result["provenance_score"] = -0.95
                        break

            exif_data = img._getexif() if hasattr(img, "_getexif") and img._getexif() else img.getexif()
            if exif_data:
                result["has_exif"] = True
                named_exif = {}
                for tag_id, val in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                    named_exif[tag_name] = val

                result["camera_make"] = str(named_exif.get("Make", "")).strip() or None
                result["camera_model"] = str(named_exif.get("Model", "")).strip() or None
                result["lens_model"] = str(named_exif.get("LensModel", "")).strip() or None
                result["software"] = str(named_exif.get("Software", "")).strip() or None
                result["datetime_original"] = str(named_exif.get("DateTimeOriginal", "")).strip() or None
                result["iso"] = named_exif.get("ISOSpeedRatings")

                exp = named_exif.get("ExposureTime")
                if exp is not None:
                    result["exposure_time"] = f"{float(exp):.4f}s" if isinstance(exp, (int, float)) else str(exp)

                fnum = named_exif.get("FNumber")
                if fnum is not None:
                    result["f_number"] = f"f/{float(fnum):.1f}" if isinstance(fnum, (int, float)) else str(fnum)

                if result["software"]:
                    soft_lower = result["software"].lower()
                    for sig in AI_SOFTWARE_SIGNATURES:
                        if sig in soft_lower:
                            result["ai_tool_detected"] = sig.title()
                            result["provenance_tier"] = "ai_watermark_detected"
                            result["provenance_score"] = -0.95
                            return result

                has_make = bool(result["camera_make"])
                has_model = bool(result["camera_model"])
                make_lower = (result["camera_make"] or "").lower()

                is_known_camera = any(k in make_lower for k in KNOWN_CAMERA_MAKES)
                has_optical_specs = (result["exposure_time"] is not None or 
                                     result["f_number"] is not None or 
                                     result["iso"] is not None)

                if has_make and has_model and (is_known_camera or has_optical_specs):
                    result["provenance_tier"] = "camera_verified"
                    result["provenance_score"] = 0.85
                elif has_make or has_model:
                    result["provenance_tier"] = "camera_verified"
                    result["provenance_score"] = 0.50

    except Exception:
        pass

    return result
