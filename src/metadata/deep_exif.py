"""
SignalScope — Deep EXIF & Hardware Metadata Extractor
Extracts and parses camera hardware, optical parameters, GPS, and low-level EXIF tags.
"""
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io
import logging

logger = logging.getLogger(__name__)


def _convert_to_serializable(val: Any) -> Any:
    """Recursively convert PIL IFDRational and byte values to JSON-serializable types."""
    if hasattr(val, "numerator") and hasattr(val, "denominator"):
        return float(val)
    if isinstance(val, bytes):
        try:
            return val.decode("utf-8", errors="replace").strip("\x00")
        except Exception:
            return str(val)
    if isinstance(val, tuple):
        return [_convert_to_serializable(v) for v in val]
    if isinstance(val, list):
        return [_convert_to_serializable(v) for v in val]
    if isinstance(val, dict):
        return {str(k): _convert_to_serializable(v) for k, v in val.items()}
    return val


def _convert_gps_dms_to_dd(dms: Any, ref: str) -> Optional[float]:
    """Convert degrees, minutes, seconds to decimal degrees."""
    try:
        if not dms or len(dms) < 3:
            return None
        deg = float(dms[0])
        minute = float(dms[1])
        sec = float(dms[2])
        dd = deg + (minute / 60.0) + (sec / 3600.0)
        if ref in ["S", "W"]:
            dd = -dd
        return round(dd, 6)
    except Exception as e:
        logger.debug(f"Failed to convert GPS coordinates: {e}")
        return None


def extract_deep_exif(image_source: Any) -> Dict[str, Any]:
    """
    Extract comprehensive EXIF, GPS, and technical hardware data.
    
    Args:
        image_source: File path (str/Path), file-like bytes buffer, or PIL.Image
        
    Returns:
        Dictionary containing parsed EXIF fields, GPS info, and raw tags.
    """
    img = None
    if isinstance(image_source, bytes):
        img = Image.open(io.BytesIO(image_source))
    elif isinstance(image_source, io.BytesIO):
        # Don't let PIL close the caller's buffer; copy bytes
        img = Image.open(io.BytesIO(image_source.getvalue()))
    elif isinstance(image_source, (str, Path)):
        img = Image.open(str(image_source))
    elif isinstance(image_source, Image.Image):
        img = image_source
    else:
        try:
            img = Image.open(image_source)
        except Exception as e:
            logger.error(f"Cannot open image source for EXIF extraction: {e}")
            return {"has_exif": False, "raw_tags": {}, "tag_count": 0}

    try:
        exif_data = img.getexif()
        has_exif = bool(exif_data and len(exif_data) > 0)
        
        raw_tags: Dict[str, Any] = {}
        gps_info: Dict[str, Any] = {}
        
        if has_exif:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, str(tag_id))
                raw_tags[tag_name] = _convert_to_serializable(value)
            
            # Check for Exif Sub-IFD (tag 0x8769)
            try:
                sub_ifd = exif_data.get_ifd(0x8769)
                for tag_id, value in sub_ifd.items():
                    tag_name = TAGS.get(tag_id, str(tag_id))
                    raw_tags[tag_name] = _convert_to_serializable(value)
            except Exception:
                pass
            
            # Check for GPS Sub-IFD (tag 0x8825)
            try:
                gps_ifd = exif_data.get_ifd(0x8825)
                for tag_id, value in gps_ifd.items():
                    tag_name = GPSTAGS.get(tag_id, str(tag_id))
                    gps_info[tag_name] = _convert_to_serializable(value)
            except Exception:
                pass

        # Extract PNG text chunks if PNG
        png_info: Dict[str, str] = {}
        if hasattr(img, "text") and isinstance(img.text, dict):
            for k, v in img.text.items():
                png_info[str(k)] = str(v)

        # Parse GPS coordinates
        gps_coords = None
        if gps_info:
            lat = _convert_gps_dms_to_dd(gps_info.get("GPSLatitude"), gps_info.get("GPSLatitudeRef", "N"))
            lon = _convert_gps_dms_to_dd(gps_info.get("GPSLongitude"), gps_info.get("GPSLongitudeRef", "E"))
            if lat is not None and lon is not None:
                gps_coords = {"latitude": lat, "longitude": lon}

        # Parse exposure time
        exp_time = raw_tags.get("ExposureTime")
        exp_str = None
        if exp_time is not None:
            if isinstance(exp_time, float) and exp_time > 0 and exp_time < 1:
                exp_str = f"1/{round(1.0 / exp_time)}"
            else:
                exp_str = f"{exp_time}s"

        # Parse focal length
        focal = raw_tags.get("FocalLength")
        focal_str = f"{focal}mm" if focal is not None else None

        clean_str = lambda s: str(s).replace('\x00', '').strip() if s is not None else None

        return {
            "has_exif": has_exif or bool(png_info),
            "tag_count": len(raw_tags) + len(png_info),
            "camera_make": clean_str(raw_tags.get("Make")),
            "camera_model": clean_str(raw_tags.get("Model")),
            "software": clean_str(raw_tags.get("Software")),
            "datetime_original": raw_tags.get("DateTimeOriginal") or raw_tags.get("DateTime"),
            "exposure_time": exp_str,
            "f_number": raw_tags.get("FNumber"),
            "iso": raw_tags.get("ISOSpeedRatings") or raw_tags.get("PhotographicSensitivity"),
            "focal_length": focal_str,
            "gps_coords": gps_coords,
            "gps_raw": gps_info,
            "png_text": png_info,
            "raw_tags": raw_tags,
            "image_format": img.format if hasattr(img, "format") else None,
            "image_mode": img.mode if hasattr(img, "mode") else None,
            "image_size": img.size if hasattr(img, "size") else (0, 0),
        }
    except Exception as e:
        logger.warning(f"Error parsing EXIF metadata: {e}")
        return {"has_exif": False, "raw_tags": {}, "tag_count": 0}
