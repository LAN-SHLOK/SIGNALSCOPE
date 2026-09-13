"""
SignalScope — Simple Metadata & Camera Info Panel
"""
import streamlit as st
from app.schemas.contracts import MetadataReport


def render_metadata_panel(report: MetadataReport):
    """Renders simple, readable camera EXIF and digital signature verification."""
    st.markdown("#### Metadata & Provenance Details")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Camera & File Info**")
        exif_items = [
            ("Camera Make", report.camera_make or "None"),
            ("Camera Model", report.camera_model or "None"),
            ("Software", report.software or "None"),
            ("Shutter Speed", report.exposure_time or "None"),
            ("Aperture", f"f/{report.f_number}" if report.f_number else "None"),
            ("ISO Speed", str(report.iso) if report.iso else "None"),
            ("Date Taken", report.datetime_original or "None"),
        ]
        rows = "".join([f"<tr><td style='font-weight: 600; width: 45%;'>{k}</td><td>{v}</td></tr>" for k, v in exif_items])
        st.markdown(f'<table class="simple-table">{rows}</table>', unsafe_allow_html=True)

    with col2:
        st.markdown("**Digital Authenticity (C2PA)**")
        c2pa_items = [
            ("Digital Credentials Found", "Yes" if report.c2pa_present else "No"),
            ("Verification Status", report.c2pa_status.replace("_", " ")),
            ("Claimed Creator/Tool", report.c2pa_claim_generator or "None"),
            ("Signing Authority", report.c2pa_issuer or "None"),
        ]
        c2pa_rows = "".join([f"<tr><td style='font-weight: 600; width: 45%;'>{k}</td><td>{v}</td></tr>" for k, v in c2pa_items])
        st.markdown(f'<table class="simple-table">{c2pa_rows}</table>', unsafe_allow_html=True)

        if report.anomalies:
            st.markdown("<div style='margin-top: 12px;'><b>Detected Flags</b></div>", unsafe_allow_html=True)
            for a in report.anomalies:
                st.markdown(f"<div style='font-size: 0.88rem; color: #D32F2F; margin-bottom: 2px;'>• {a}</div>", unsafe_allow_html=True)
