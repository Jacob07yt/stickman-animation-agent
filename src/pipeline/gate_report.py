"""Quality-gate evidence for a finished video (PLAYBOOK.md section 3).

Works on the rendered file, not the plan:
  - contact sheet with one frame from the middle of every scene      -> gate/frames.png
  - Whisper transcript of the final audio vs the script, word diffs  -> gate/transcript-diff.txt
  - integrated loudness / true peak                                   -> gate/report.json
  - format check (resolution, duration)

Usage: .venv/bin/python src/pipeline/gate_report.py projects/<slug> [--vertical]
"""
import argparse, difflib, json, os, re, subprocess, sys
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--vertical", action="store_true")
    a = ap.parse_args()
    proj = Path(a.project).resolve(); slug = proj.name
    video = proj / "output" / f"{slug}.mp4"; gate = proj / "gate"; gate.mkdir(exist_ok=True)
    report = {"video": str(video)}

    # Format
    p = sh(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration", "-of", "json", str(video)])
    info = json.loads(p.stdout)
    vs = [s for s in info["streams"] if "width" in s][0]
    want = (1080, 1920) if a.vertical else (1920, 1080)
    report["format"] = {"width": vs["width"], "height": vs["height"], "duration": float(info["format"]["duration"]),
                        "ok": (vs["width"], vs["height"]) == want}

    # Loudness
    p = sh(["ffmpeg", "-hide_banner", "-i", str(video), "-af", "ebur128=peak=true", "-f", "null", "-"])
    summ = p.stderr[p.stderr.rfind("Summary"):]
    I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summ).group(1))
    peak = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ).group(1))
    report["loudness"] = {"integrated_lufs": I, "true_peak_dbfs": peak, "ok": -15.5 <= I <= -12.5 and peak <= -1.0}

    # One frame from the middle of every scene
    starts, t = [], 0.0
    for f in sorted((proj / "timestamps").glob("scene-*.json")):
        d = json.loads(f.read_text())["duration"]; starts.append(t + (d + 0.5) / 2); t += d + 0.5
    frames = gate / "frames"; frames.mkdir(exist_ok=True)
    for i, s in enumerate(starts, 1):
        sh(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{s:.2f}", "-i", str(video), "-frames:v", "1",
            "-vf", "scale=480:-1", str(frames / f"f{i:02d}.png")])
    cols = 6 if not a.vertical else 8
    sh(["ffmpeg", "-loglevel", "error", "-y", "-pattern_type", "glob", "-i", str(frames / "f*.png"),
        "-vf", f"tile={cols}x{-(-len(starts)//cols)}", "-frames:v", "1", str(gate / "frames.png")])
    report["frames"] = {"count": len(starts), "sheet": str(gate / "frames.png")}

    # Transcript of the final audio vs script
    from faster_whisper import WhisperModel
    import numpy as np
    wav = gate / "final.wav"
    sh(["ffmpeg", "-loglevel", "error", "-y", "-i", str(video), "-ac", "1", "-ar", "16000", str(wav)])
    import soundfile as sf
    audio, _ = sf.read(str(wav), dtype="float32")
    segs, _ = WhisperModel("small.en", device="cpu", compute_type="int8").transcribe(audio, language="en")
    heard = " ".join(s.text for s in segs)
    script = json.loads((proj / "scripts" / "narration-script.json").read_text())
    said = " ".join(s["narration"] for s in script["scenes"])
    norm = lambda x: re.sub(r"[^a-z0-9 ]", " ", x.lower()).split()
    A, B = norm(said), norm(heard)
    diffs = [f"script: {' '.join(A[i1:i2])!r:40} heard: {' '.join(B[j1:j2])!r}"
             for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B).get_opcodes() if op != "equal"]
    (gate / "transcript-diff.txt").write_text("\n".join(diffs) + "\n", encoding="utf-8")
    report["transcript"] = {"script_words": len(A), "diff_count": len(diffs), "file": str(gate / "transcript-diff.txt")}
    wav.unlink(missing_ok=True)

    (gate / "report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
