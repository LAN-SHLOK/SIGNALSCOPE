"""
Module D: C2PA & Content Credentials Validator for SignalScope.
Detects whether an image carries authentic C2PA manifests / Coalition for Content
Provenance and Authenticity metadata boxes (e.g. from Truepic, Leica, Adobe Content Authenticity).
"""

import os
from typing import Dict, Any


def check_c2pa_credentials(image_path: str) -> Dict[str, Any]:
    """
    Checks for presence of C2PA manifest boxes or JUMBF containers.
    """
    result = {
        "has_c2pa": False,
        "is_ai_declared": False,
        "is_camera_declared": False,
        "claim_generator": None,
        "details": "No C2PA metadata detected."
    }

    if not os.path.exists(image_path):
        return result

    try:
        with open(image_path, "rb") as f:
            data = f.read(131072)  # Check first 128KB
            
            # Look for C2PA box signatures
            if b"c2pa" in data or b"c2ma" in data or b"c2as" in data:
                result["has_c2pa"] = True
                result["details"] = "C2PA manifest box found."
                
                # Check for digital creation / AI assertions
                if b"c2pa.trainedAlgorithmicMedia" in data or b"digitalSourceType" in data:
                    result["is_ai_declared"] = True
                    result["details"] = "C2PA manifest explicitly declares AI-generated media."
                elif b"c2pa.capture" in data:
                    result["is_camera_declared"] = True
                    result["details"] = "C2PA manifest explicitly declares camera capture."
                    
            elif b"JUMBF" in data or b"jumb" in data:
                result["has_c2pa"] = True
                result["details"] = "JUMBF container detected."

    except Exception:
        pass

    return result
