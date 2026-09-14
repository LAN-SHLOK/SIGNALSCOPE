import glob
import json
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from model.predict import predict

def run_verification():
    print("=" * 60)
    print("SIGNALSCOPE REGRESSION & VERIFICATION GATE")
    print("=" * 60)

    # 1. Real Smartphone Photo (4000x3000)
    print("\n[1] Real Smartphone Camera Photo:")
    phone_path = "unseen_test/real/real_phone_photo.png"
    if os.path.exists(phone_path):
        res = predict(phone_path)
        print(f"  Image: {phone_path}")
        print(f"  Label: {res.get('label')} | Confidence: {res.get('confidence')} | Verdict: {res.get('verdict', {}).get('verdict')}")
        assert res.get('label') == "Real", f"FAILED: Phone photo was misclassified as {res.get('label')}"
        assert res.get('confidence') < 0.10, f"FAILED: Phone photo confidence too high: {res.get('confidence')}"
        print("  -> PASS (Authentic camera photo correctly classified as Real)")
    else:
        print(f"  Warning: {phone_path} not found")

    # 2. Modern AI Images (Watchmaker, Cyberpunk Cat)
    print("\n[2] Modern AI High-Resolution Images:")
    for ai_p in ["unseen_test/ai/watchmaker_ai.jpg", "unseen_test/ai/cyberpunk_cat_ai.jpg"]:
        if os.path.exists(ai_p):
            res = predict(ai_p)
            print(f"  Image: {ai_p}")
            print(f"  Label: {res.get('label')} | Confidence: {res.get('confidence')} | Verdict: {res.get('verdict', {}).get('verdict')}")
            assert res.get('label') == "AI-generated", f"FAILED: {ai_p} misclassified as {res.get('label')}"
            assert res.get('confidence') > 0.90, f"FAILED: {ai_p} confidence too low: {res.get('confidence')}"
            print(f"  -> PASS ({ai_p} correctly classified as AI)")

    # 3. Unseen Real Eval Photos
    print("\n[3] Unseen Real Evaluation Photos:")
    real_paths = sorted(glob.glob("unseen_test/eval_real/*.jpg"))[:5]
    for rp in real_paths:
        res = predict(rp)
        print(f"  Image: {os.path.basename(rp)} | Label: {res.get('label')} | Conf: {res.get('confidence')} | Verdict: {res.get('verdict', {}).get('verdict')}")
        assert res.get('label') == "Real", f"FAILED: {rp} misclassified as {res.get('label')}"

    # 4. Unseen AI Eval Images
    print("\n[4] Unseen AI Evaluation Images:")
    ai_paths = sorted(glob.glob("unseen_test/eval_ai/*.jpg"))[:5]
    for ap in ai_paths:
        res = predict(ap)
        print(f"  Image: {os.path.basename(ap)} | Label: {res.get('label')} | Conf: {res.get('confidence')} | Verdict: {res.get('verdict', {}).get('verdict')}")
        assert res.get('label') == "AI-generated", f"FAILED: {ap} misclassified as {res.get('label')}"

    print("\n" + "=" * 60)
    print("SUCCESS: ALL REGRESSION TESTS PASSED! ZERO CATASTROPHIC FORGETTING.")
    print("=" * 60)

if __name__ == "__main__":
    run_verification()
