"""
SignalScope — Simple Frequency & Compression Plots
"""
import streamlit as st
import plotly.graph_objects as go
from app.schemas.contracts import SpectralData


def render_spectrum_plots(spectral: SpectralData):
    """Renders clean, readable charts for frequency and compression analysis."""
    st.markdown("#### Deep Signal Analysis")

    tab1, tab2, tab3 = st.tabs(["Frequency Spectrum", "Compression Check", "Camera Sensor Trace"])

    with tab1:
        if spectral.azimuthal_freqs:
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(spectral.azimuthal_freqs))),
                    y=spectral.azimuthal_freqs,
                    mode="lines",
                    line=dict(color="#080808", width=2.5),
                    fill="tozeroy",
                    fillcolor="rgba(0, 215, 34, 0.25)",
                )
            )
            fig.update_layout(
                title=dict(text="Frequency Distribution (Center to Edge)", font=dict(family="Plus Jakarta Sans", size=13)),
                xaxis_title="Low Frequencies  →  High Frequencies",
                yaxis_title="Energy Level",
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font=dict(family="Plus Jakarta Sans", color="#080808"),
                margin=dict(l=30, r=20, t=35, b=35),
                height=240,
                xaxis=dict(showgrid=True, gridcolor="#EEEEEE"),
                yaxis=dict(showgrid=True, gridcolor="#EEEEEE"),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Real photos have a smooth, natural dropoff. AI generators often leave unnatural spikes or sharp cutoffs in the higher frequencies.")
        else:
            st.info("No frequency data available.")

    with tab2:
        if spectral.jpeg_ghost_diffs:
            fig_g = go.Figure()
            fig_g.add_trace(
                go.Scatter(
                    x=spectral.jpeg_ghost_levels,
                    y=spectral.jpeg_ghost_diffs,
                    mode="lines+markers",
                    line=dict(color="#080808", width=2.0),
                    marker=dict(size=7, color="#00D722", line=dict(color="#080808", width=1.5)),
                )
            )
            fig_g.update_layout(
                title=dict(text="Recompression Error Across Quality Levels", font=dict(family="Plus Jakarta Sans", size=13)),
                xaxis_title="Quality (50% to 95%)",
                yaxis_title="Pixel Difference",
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font=dict(family="Plus Jakarta Sans", color="#080808"),
                margin=dict(l=30, r=20, t=35, b=35),
                height=240,
                xaxis=dict(showgrid=True, gridcolor="#EEEEEE"),
                yaxis=dict(showgrid=True, gridcolor="#EEEEEE"),
            )
            st.plotly_chart(fig_g, use_container_width=True)
            st.caption("Real JPEGs show a clear dip at their original save quality. Synthetic images are often uncompressed and show flatter lines.")
        else:
            st.info("No compression profile data available.")

    with tab3:
        bayer_text = "Detected (Matches real camera sensor)" if spectral.has_bayer_trace else "Not Detected (Consistent with AI generation)"
        bayer_badge = "badge-real" if spectral.has_bayer_trace else "badge-ai"

        st.markdown(
            f"""
            <div style="padding: 16px; background: #F9F9F9; border: 2px solid #080808; border-radius: 10px; margin-top: 10px;">
              <div style="font-weight: 700; margin-bottom: 6px;">Camera Sensor Grid (Bayer Pattern)</div>
              <span class="status-badge {bayer_badge}">{bayer_text}</span>
              <div style="margin-top: 10px; font-size: 0.88rem; color: #555555; line-height: 1.4;">
                Physical camera sensors have a colored grid over their sensor chips that leaves a tiny microscopic pattern in real photos. AI-generated images synthesize pixels directly and do not have this camera sensor fingerprint.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
