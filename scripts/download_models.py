"""Download the Kokoro-82M ONNX model and voices into models/kokoro/.

Usage: python download_models.py [--voices am_michael,bm_george,...]
"""
import argparse, os
from pathlib import Path

import numpy as np

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
from huggingface_hub import hf_hub_download

REPO = "onnx-community/Kokoro-82M-v1.0-ONNX"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voices", default="am_michael,am_adam,am_onyx,am_fenrir,bm_george,bm_lewis,bm_daniel")
    args = ap.parse_args()
    dest = Path(__file__).resolve().parent.parent / "models" / "kokoro"
    hf_hub_download(REPO, "onnx/model.onnx", local_dir=dest)
    voices = {}
    for v in [x.strip() for x in args.voices.split(",") if x.strip()]:
        p = hf_hub_download(REPO, f"voices/{v}.bin", local_dir=dest)
        voices[v] = np.fromfile(p, dtype=np.float32).reshape(-1, 1, 256)
    np.savez(dest / "voices.npz", **voices)
    print(f"Saved model and {len(voices)} voices to {dest}")


if __name__ == "__main__":
    main()
