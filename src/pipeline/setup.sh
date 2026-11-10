#!/usr/bin/env bash
# One-time (per container) setup for the sketch pipeline on Linux/macOS.
set -euo pipefail
cd "$(dirname "$0")/../.."
PYBIN=$(command -v python3.12 || command -v python3)
[ -x .venv/bin/python ] || "$PYBIN" -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q kokoro-onnx soundfile faster-whisper huggingface_hub numpy
[ -f models/kokoro/voices.npz ] || .venv/bin/python scripts/download_models.py \
  --voices bm_fable,bm_george,bm_lewis,bm_daniel,am_michael,am_fenrir,am_puck,af_heart,bf_emma
npm install --ignore-scripts --no-audit --no-fund >/dev/null
echo "setup ok"
