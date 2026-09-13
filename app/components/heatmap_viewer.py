"""
SignalScope — Simple Heatmap Viewer Component
"""
import streamlit as st
import numpy as np
import cv2
from PIL import Image


def blend_heatmap_overlay(original_rgb: np.ndarray, heatmap_norm: np.ndarray, alpha: float) -> Image.Image:
    """Blends normalized heatmap onto original image with Jet colormap."""
    h, w = original_rgb.shape[:2]
    resized_heat = cv2.resize(heatmap_norm, (w, h), interpolation=cv2.INTER_CUBIC)
    resized_heat = np.clip(resized_heat, 0.0, 1.0)
    
    heat_uint8 = np.uint8(255 * resized_heat)
    colored_heat_bgr = cv2.applyColorMap(heat_uint8, cv2.COLORMAP_JET)
    colored_heat_rgb = cv2.cvtColor(colored_heat_bgr, cv2.COLOR_BGR2RGB)

    blended = cv2.addWeighted(colored_heat_rgb, alpha, original_rgb, 1.0 - alpha, 0)
    return Image.fromarray(blended)


def render_heatmap_viewer(original_img: Image.Image, heatmap_norm: np.ndarray):
    """Renders clean heatmap controls and image."""
    st.markdown("#### Heatmap Inspection")
    st.write("Warmer colors (red and yellow) show regions where our models flagged synthetic patterns.")

    col1, col2 = st.columns([2, 1])
    with col1:
        opacity = st.slider("Heatmap Intensity", min_value=0.0, max_value=1.0, value=0.60, step=0.05)
    with col2:
        side_by_side = st.checkbox("Show Side-by-Side", value=False)

    orig_rgb = np.array(original_img.convert("RGB"))

    if side_by_side:
        c1, c2 = st.columns(2)
        with c1:
            st.image(original_img, caption="Original Image", use_container_width=True)
        with c2:
            heat_only = blend_heatmap_overlay(orig_rgb, heatmap_norm, 1.0)
            st.image(heat_only, caption="Detected Hotspots", use_container_width=True)
    else:
        blended = blend_heatmap_overlay(orig_rgb, heatmap_norm, opacity)
        st.image(blended, caption=f"Overlay ({int(opacity * 100)}% strength)", use_container_width=True)
