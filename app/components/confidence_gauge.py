"""
SignalScope — Simple Clean Confidence Meter
"""
import streamlit as st
from app.schemas.contracts import VerdictTier


def render_confidence_gauge(confidence: float, tier: VerdictTier):
    """
    Renders a clean, easy-to-understand progress bar showing certainty.
    """
    pct = int(round(confidence * 100))

    if tier == VerdictTier.CONFIDENT_AI:
        fill_class = "fill-ai"
        label_text = "AI Probability"
    elif tier == VerdictTier.CONFIDENT_REAL:
        fill_class = "fill-real"
        label_text = "Authenticity Confidence"
    else:
        fill_class = "fill-uncertain"
        label_text = "Confidence Level"

    html = f"""
    <div class="simple-progress-container">
      <div class="simple-progress-label">
        <span>{label_text}</span>
        <span>{pct}%</span>
      </div>
      <div class="simple-progress-track">
        <div class="simple-progress-fill {fill_class}" style="width: {pct}%;"></div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
