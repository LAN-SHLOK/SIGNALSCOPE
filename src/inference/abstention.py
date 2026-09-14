"""
Smart three-tier verdict system with responsible framing.
Never over-claims — uses 'Likely' language and abstains when uncertain.
"""
from typing import Dict

from src.config import CONFIDENT_AI_THRESHOLD, CONFIDENT_REAL_THRESHOLD


def responsible_verdict(confidence: float, threshold: float = 0.5) -> Dict[str, str]:
    """
    Three-tier verdict system:
    - confident_ai (> 0.75):  "Likely AI-generated"
    - confident_real (< 0.25): "Likely authentic"
    - uncertain (0.25–0.75):   "Uncertain — human review recommended"

    Args:
        confidence: float in [0, 1], probability of being AI-generated
        threshold: decision boundary (unused for tier, used for binary label)

    Returns:
        dict with keys: verdict, tier, color, icon, action, confidence
    """
    confidence = float(confidence)
    confidence = max(0.0, min(1.0, confidence))  # Clamp to [0, 1]

    if confidence > CONFIDENT_AI_THRESHOLD:
        return {
            'verdict': 'Likely AI-generated',
            'tier': 'confident_ai',
            'color': '#FF4444',
            'icon': '🔴',
            'action': 'Review the forensic cues below for details.',
            'confidence': round(confidence, 4),
        }
    elif confidence < CONFIDENT_REAL_THRESHOLD:
        return {
            'verdict': 'Likely authentic',
            'tier': 'confident_real',
            'color': '#44BB44',
            'icon': '🟢',
            'action': 'No significant AI artifacts detected.',
            'confidence': round(confidence, 4),
        }
    else:
        return {
            'verdict': 'Uncertain — human review recommended',
            'tier': 'uncertain',
            'color': '#FFAA00',
            'icon': '🟡',
            'action': (
                'The model cannot confidently classify this image. '
                'Consider source context, metadata, and expert review.'
            ),
            'confidence': round(confidence, 4),
        }
