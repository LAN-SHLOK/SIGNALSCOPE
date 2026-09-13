"""
SignalScope — Predict Re-export
Provides backward-compatibility for src.model.predict imports.
"""
from predict import predict_single, main

__all__ = ["predict_single", "main"]

if __name__ == "__main__":
    main()
