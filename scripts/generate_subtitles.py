"""Build one SRT file from per-scene word timestamps.

Usage: python generate_subtitles.py --timestamps-dir timestamps/ --output video.srt [--pause 0.5] [--max-chars 42] [--max-gap 0.6]
Scenes are laid end to end in id order, separated by --pause seconds (matching the audio concat).
"""
import argparse, json, re
from pathlib import Path


def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timestamps-dir", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--pause", type=float, default=0.5)
    ap.add_argument("--max-chars", type=int, default=42)
    ap.add_argument("--max-gap", type=float, default=0.6)
    args = ap.parse_args()

    files = sorted(p for p in Path(args.timestamps_dir).iterdir() if re.fullmatch(r"scene-\d{2,3}\.json", p.name))
    cues, offset = [], 0.0
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        line = []
        for w in data["words"]:
            start, end = w["start"] + offset, w["end"] + offset
            text = " ".join(x["word"] for x in line + [w])
            if line and (len(text) > args.max_chars or start - line[-1]["_end"] > args.max_gap
                         or re.search(r"[.?!]$", line[-1]["word"])):
                cues.append(line); line = []
            line.append({"word": w["word"], "_start": start, "_end": end})
        if line:
            cues.append(line)
        offset += data["duration"] + args.pause

    out = []
    for i, c in enumerate(cues, 1):
        out.append(f"{i}\n{ts(c[0]['_start'])} --> {ts(c[-1]['_end'])}\n{' '.join(x['word'] for x in c)}\n")
    Path(args.output).write_text("\n".join(out), encoding="utf-8")
    print(f"{len(cues)} cues -> {args.output}")


if __name__ == "__main__":
    main()
