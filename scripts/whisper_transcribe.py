"""Extract word-level timestamps from scene WAVs with faster-whisper.

Usage: python whisper_transcribe.py --audio-dir audio/ --output timestamps/ [--model small.en]
Writes timestamps/scene-NN.json: {sceneId, duration, text, words:[{word,start,end}]}
"""
import argparse, json, os, re
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
from pathlib import Path

import numpy as np
import soundfile as sf


def load_16k_mono(path):
    """Read a WAV with soundfile and resample to 16 kHz mono (avoids PyAV version issues)."""
    audio, sr = sf.read(str(path), dtype="float32", always_2d=True)
    audio = audio.mean(axis=1)
    if sr != 16000:
        n = int(round(len(audio) * 16000 / sr))
        audio = np.interp(np.linspace(0, len(audio) - 1, n), np.arange(len(audio)), audio).astype(np.float32)
    return audio


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio-dir", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--device", default="auto")
    args = ap.parse_args()

    from faster_whisper import WhisperModel
    device = args.device
    if device == "auto":
        try:
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            device = "cpu"
    model = WhisperModel(args.model, device=device, compute_type="float16" if device == "cuda" else "int8")

    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    wavs = sorted(p for p in Path(args.audio_dir).iterdir() if re.fullmatch(r"scene-\d{2,3}\.wav", p.name))
    for wav in wavs:
        sid = wav.stem.split("-", 1)[1]
        duration = sf.info(str(wav)).duration
        segments, _ = model.transcribe(load_16k_mono(wav), language="en", word_timestamps=True, vad_filter=False)
        words = []
        for seg in segments:
            for w in seg.words or []:
                words.append({"word": w.word.strip(), "start": round(w.start, 3), "end": round(min(w.end, duration), 3)})
        data = {"sceneId": sid, "duration": round(duration, 3), "text": " ".join(w["word"] for w in words), "words": words}
        (out / f"scene-{sid}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"scene-{sid}.json  {len(words)} words  {duration:.2f}s")


if __name__ == "__main__":
    main()
