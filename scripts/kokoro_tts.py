"""Generate per-scene narration WAVs with Kokoro-82M (ONNX runtime, no PyTorch needed).

Usage: python kokoro_tts.py --script narration-script.json --output audio/ [--voice am_michael] [--speed 1.0] [--scenes 01,02]
Writes audio/scene-NN.wav (24 kHz mono) for each scene in the script.
"""
import argparse, json, re, sys
from pathlib import Path

import numpy as np
import soundfile as sf

SAMPLE_RATE = 24000
# All-caps words kept as-is (spoken as letters/acronyms); other ALL CAPS words are emphasis markers
ACRONYMS = {"US", "USA", "CIA", "TV", "UK", "USSR", "NATO", "UN", "FBI", "KGB"}


ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def two_digits(n: int) -> str:
    if n < 20:
        return ONES[n]
    t, o = divmod(n, 10)
    return TENS[t] + ("" if o == 0 else "-" + ONES[o])


def say_year(y: int) -> str:
    """1962 -> nineteen sixty-two, 1900 -> nineteen hundred, 1905 -> nineteen oh five, 2001 -> two thousand one."""
    hi, lo = divmod(y, 100)
    if 2000 <= y <= 2009:
        return "two thousand" + ("" if lo == 0 else " " + ONES[lo])
    if lo == 0:
        return two_digits(hi) + " hundred"
    if lo < 10:
        return two_digits(hi) + " oh " + ONES[lo]
    return two_digits(hi) + " " + two_digits(lo)


def plural(word: str) -> str:
    return word[:-1] + "ies" if word.endswith("y") else word + "s"


def say_time(h: int, m: int, ampm: str) -> str:
    hour = two_digits(h)
    mins = " o'clock" if m == 0 and not ampm else "" if m == 0 else " oh " + ONES[m] if m < 10 else " " + two_digits(m)
    suffix = {"am": " a.m.", "pm": " p.m."}.get(ampm.lower().replace(".", ""), "") if ampm else ""
    return hour + mins + suffix


def normalize_numbers(text: str) -> str:
    # Clock times: 6:30, 6:30 AM, 11:05pm
    text = re.sub(r"\b(\d{1,2}):(\d{2})\s*([AaPp]\.?[Mm]\.?)?",
                  lambda m: say_time(int(m.group(1)), int(m.group(2)), m.group(3) or ""), text)
    # Decades: 1960s -> nineteen sixties, '60s -> sixties
    text = re.sub(r"\b(1[1-9]|20)(\d)0s\b",
                  lambda m: two_digits(int(m.group(1))) + " " + (plural(two_digits(int(m.group(2)) * 10)) if m.group(2) != "0" else "hundreds"), text)
    text = re.sub(r"[\u2019']([2-9])0s\b", lambda m: plural(TENS[int(m.group(1))]), text)
    # Years: four-digit numbers 1100-2099 not part of a larger number or comma-grouped figure
    text = re.sub(r"(?<![\d,.$])\b(1[1-9]\d\d|20\d\d)\b(?![,.]\d)", lambda m: say_year(int(m.group(1))), text)
    return text


def prepare(text: str) -> str:
    text = normalize_numbers(text)

    def fix(m):
        w = m.group(0)
        return w if w in ACRONYMS else w.capitalize() if m.start() == 0 else w.lower()
    text = re.sub(r"\b[A-Z]{2,}\b", fix, text)
    text = text.replace("—", ", ").replace("–", ", ")
    return re.sub(r"\s+", " ", text).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--voice", default="", help="Kokoro voice id (default: config.voiceId in video-project.json, else am_michael)")
    ap.add_argument("--speed", type=float, default=0, help="default: config.voiceSpeed in video-project.json, else 1.0")
    ap.add_argument("--scenes", default="", help="comma-separated scene ids (default: all)")
    ap.add_argument("--model", default="", help="path to Kokoro ONNX model")
    ap.add_argument("--voices", default="", help="path to voices .npz")
    ap.add_argument("--tail", type=float, default=0.25, help="seconds of silence appended to each scene")
    args = ap.parse_args()

    project_file = Path(args.script).resolve().parent.parent / "video-project.json"
    cfg = json.loads(project_file.read_text(encoding="utf-8")).get("config", {}) if project_file.exists() else {}
    args.voice = args.voice or cfg.get("voiceId") or "am_michael"
    args.speed = args.speed or float(cfg.get("voiceSpeed") or 1.0)
    print(f"voice={args.voice} speed={args.speed}")

    from kokoro_onnx import Kokoro
    root = Path(__file__).resolve().parent.parent / "models" / "kokoro"
    model = Path(args.model or root / "onnx" / "model.onnx")
    voices = Path(args.voices or root / "voices.npz")
    if not model.exists() or not voices.exists():
        sys.exit(f"Kokoro model not found ({model}, {voices}) - run scripts/download_models.py first")
    tts = Kokoro(str(model), str(voices))
    lang = "en-gb" if args.voice.startswith("b") else "en-us"

    script = json.loads(Path(args.script).read_text(encoding="utf-8"))
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    only = {s.strip() for s in args.scenes.split(",") if s.strip()}

    for scene in script["scenes"]:
        sid = str(scene["id"]).zfill(2)
        if only and sid not in only:
            continue
        text = prepare(scene["narration"])
        audio, sr = tts.create(text, voice=args.voice, speed=args.speed, lang=lang, sentence_pause=0.35, clause_pause=0.15)
        if sr != SAMPLE_RATE or len(audio) == 0:
            print(f"scene-{sid}: unexpected output (sr={sr}, len={len(audio)})", file=sys.stderr); sys.exit(1)
        audio = np.concatenate([np.asarray(audio, dtype=np.float32), np.zeros(int(args.tail * SAMPLE_RATE), dtype=np.float32)])
        path = out / f"scene-{sid}.wav"
        sf.write(path, audio, SAMPLE_RATE)
        print(f"scene-{sid}.wav  {len(audio) / SAMPLE_RATE:.2f}s")


if __name__ == "__main__":
    main()
