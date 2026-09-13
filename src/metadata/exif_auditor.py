"""
SignalScope — EXIF Forensic Auditor & Generative AI Footprint Detector
Audits metadata fields for AI software signatures, prompt leaks, and synthetic anomalies.
"""
from typing import Dict, Any, List, Tuple
import re

# Known AI generators, models, and UI frameworks
AI_SOFTWARE_SIGNATURES = [
    "midjourney",
    "stable diffusion",
    "stablediffusion",
    "automatic1111",
    "comfyui",
    "dall-e",
    "dalle",
    "novelai",
    "adobe firefly",
    "firefly",
    "photoshop generative fill",
    "bing image creator",
    "invokeai",
    "fooocus",
    "civitai",
    "leonardo.ai",
    "playground ai",
    "flux.1",
    "sdxl",
    "imagen",
]

# Common parameter keys stored in PNG text chunks by diffusion tools
DIFFUSION_PROMPT_KEYS = [
    "parameters",
    "prompt",
    "negative_prompt",
    "workflow",
    "prompt_json",
    "sd-metadata",
    "generation_data",
]

# Standard synthetic training / generation dimensions
SYNTHETIC_CANVAS_DIMENSIONS = [
    (512, 512),
    (768, 768),
    (1024, 1024),
    (1152, 896),
    (896, 1152),
    (1216, 832),
    (832, 1216),
    (1344, 768),
    (768, 1344),
    (1536, 640),
    (640, 1536),
]


def audit_metadata(exif_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Examines raw and parsed EXIF fields to detect AI signatures and suspicious anomalies.
    
    Args:
        exif_dict: Output dictionary from deep_exif.extract_deep_exif
        
    Returns:
        Dictionary with detected AI tools, anomalies list, and audit score.
    """
    anomalies: List[str] = []
    detected_ai_software: List[str] = []
    has_exif = exif_dict.get("has_exif", False)
    raw_tags = exif_dict.get("raw_tags", {})
    png_text = exif_dict.get("png_text", {})
    img_size = exif_dict.get("image_size", (0, 0))

    # 1. Search for known AI software signatures in standard tags
    text_corpus_fields = [
        raw_tags.get("Software", ""),
        raw_tags.get("ImageDescription", ""),
        raw_tags.get("UserComment", ""),
        raw_tags.get("Artist", ""),
        raw_tags.get("Copyright", ""),
        raw_tags.get("ProcessingSoftware", ""),
    ]
    
    for field in text_corpus_fields:
        if not field:
            continue
        field_lower = str(field).lower()
        for signature in AI_SOFTWARE_SIGNATURES:
            if signature in field_lower and signature not in detected_ai_software:
                detected_ai_software.append(signature)
                anomalies.append(f"AI software fingerprint detected in EXIF tags: '{signature}'")

    # 2. Check PNG metadata chunks (Automatic1111 / ComfyUI / NovelAI parameter dump)
    if png_text:
        for key, val in png_text.items():
            key_lower = key.lower()
            val_lower = str(val).lower()
            
            # Check keys
            if any(k in key_lower for k in DIFFUSION_PROMPT_KEYS):
                anomalies.append(f"Diffusion generation parameters found in PNG chunk '{key}'")
                if "parameters" not in detected_ai_software:
                    detected_ai_software.append("diffusion_parameters")
            
            # Check value contents for characteristic parameter patterns
            if "steps:" in val_lower and "sampler:" in val_lower:
                anomalies.append("Automatic1111/Forge generation log found in PNG metadata")
                if "automatic1111" not in detected_ai_software:
                    detected_ai_software.append("automatic1111")
            
            for signature in AI_SOFTWARE_SIGNATURES:
                if signature in val_lower and signature not in detected_ai_software:
                    detected_ai_software.append(signature)
                    anomalies.append(f"AI signature in PNG metadata '{key}': '{signature}'")

    # 3. Check for stripped metadata anomaly
    if not has_exif:
        anomalies.append("Stripped metadata: No EXIF tags found (typical for web synthetic images)")

    # 4. Check for suspicious camera tags without optical parameters
    camera_make = exif_dict.get("camera_make")
    camera_model = exif_dict.get("camera_model")
    has_camera = bool(camera_make or camera_model)
    has_exposure = bool(exif_dict.get("exposure_time") or exif_dict.get("iso"))
    
    if has_camera and not has_exposure:
        anomalies.append("Incomplete camera metadata: Camera make/model exists without shutter/ISO optical tags")

    # 5. Check canvas dimension fingerprints
    if img_size in SYNTHETIC_CANVAS_DIMENSIONS:
        if not has_camera:
            anomalies.append(f"Standard synthetic canvas dimension: {img_size[0]}x{img_size[1]}")

    is_ai_software_detected = len(detected_ai_software) > 0

    return {
        "is_ai_software_detected": is_ai_software_detected,
        "detected_ai_software": detected_ai_software,
        "anomalies": anomalies,
        "anomaly_count": len(anomalies),
        "has_authentic_camera_tags": has_camera and has_exposure,
    }
