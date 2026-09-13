"""
SignalScope — EXIF Parser Re-export
Provides backward-compatibility for src.data.exif_parser imports.
"""
from src.metadata.exif_parser import extract_exif_signals, parse_exif
from src.metadata.deep_exif import extract_deep_exif

__all__ = ["extract_exif_signals", "parse_exif", "extract_deep_exif"]
