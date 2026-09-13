"""
SignalScope — Simple Clean Verdict Card
"""
import streamlit as st
from app.schemas.contracts import VerdictResult, VerdictTier
from .confidence_gauge import render_confidence_gauge


def render_verdict_card(verdict: VerdictResult, generator_family: str, latency_ms: float):
    """
    Renders a clear, human-friendly verdict card.
    """
    if verdict.tier == VerdictTier.CONFIDENT_AI:
        badge_class = "badge-ai"
        verdict_title = "AI GENERATED"
        short_summary = "Our analysis detected synthetic patterns consistent with AI generation."
    elif verdict.tier == VerdictTier.CONFIDENT_REAL:
        badge_class = "badge-real"
        verdict_title = "AUTHENTIC PHOTO"
        short_summary = "Physical camera sensor noise and natural lighting patterns were detected."
    else:
        badge_class = "badge-uncertain"
        verdict_title = "UNCERTAIN"
        short_summary = "The image has mixed characteristics. We recommend manual review."

    st.markdown(
        f"""
        <div class="clean-card">
          <div class="clean-card-header">
            <span>Scan Result</span>
            <span style="font-size: 0.85rem; color: #777;">Checked in {latency_ms:.0f} ms</span>
          </div>

          <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 12px;">
            <span class="status-badge {badge_class}">{verdict_title}</span>
            <span class="status-badge badge-sub">{generator_family}</span>
          </div>

          <p style="font-size: 0.95rem; margin-bottom: 14px; color: #333333; line-height: 1.4;">
            {verdict.action_recommendation or short_summary}
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Simple Confidence Gauge
    render_confidence_gauge(verdict.confidence, verdict.tier)
