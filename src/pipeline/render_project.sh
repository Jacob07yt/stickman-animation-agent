#!/usr/bin/env bash
# Render a sketch-kit project end to end:
#   compositions/scene-NN.html  ->  output/scenes/scene-NN.mp4 (with narration, +0.5 s pad)
#   -> output/<slug>.mp4 (joined, loudness-normalised to -14 LUFS)
#   -> output/<slug>.srt (subtitles from word timestamps)
# Usage: src/pipeline/render_project.sh projects/<slug> [parallel=3]
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
PROJ=$(cd "$1" && pwd); PAR=${2:-3}
SLUG=$(basename "$PROJ"); OUT="$PROJ/output"; SC="$OUT/scenes"
PY="$ROOT/.venv/bin/python"; [ -x "$PY" ] || PY="$ROOT/.venv/Scripts/python.exe"
mkdir -p "$SC"
render_one() {
  local html=$1 n; n=$(basename "$html" .html)
  if [ -f "$SC/$n.mp4" ] && [ "$SC/$n.mp4" -nt "$html" ]; then echo "skip $n"; return; fi
  node "$ROOT/src/render/capture.cjs" "$html" "$SC/$n.video.mp4" 30 >/dev/null
  ffmpeg -loglevel error -y -i "$SC/$n.video.mp4" -i "$PROJ/audio/$n.wav" \
    -filter_complex "[1:a]aresample=48000,apad=pad_dur=0.5[a]" -map 0:v -map "[a]" \
    -c:v copy -c:a aac -b:a 192k -shortest "$SC/$n.mp4"
  rm -f "$SC/$n.video.mp4"; echo "rendered $n"
}
export -f render_one; export ROOT PROJ SC
ls "$PROJ"/compositions/scene-*.html | sort | xargs -P "$PAR" -I{} bash -c 'render_one {}'
ls "$SC"/scene-??.mp4 | sort | sed "s|^|file '|; s|$|'|" > "$SC/list.txt"
ffmpeg -loglevel error -y -f concat -safe 0 -i "$SC/list.txt" -c copy "$OUT/$SLUG.joined.mp4"
# Two-pass loudness normalisation to -14 LUFS (playbook quality gate)
STATS=$(ffmpeg -hide_banner -i "$OUT/$SLUG.joined.mp4" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$STATS" | sed -n "s/.*\"$1\" : \"\([^\"]*\)\".*/\1/p"; }
ffmpeg -loglevel error -y -i "$OUT/$SLUG.joined.mp4" -c:v copy -c:a aac -b:a 192k -ar 48000 \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true" \
  "$OUT/$SLUG.mp4"
rm -f "$OUT/$SLUG.joined.mp4"
"$PY" "$ROOT/scripts/generate_subtitles.py" --timestamps-dir "$PROJ/timestamps" --output "$OUT/$SLUG.srt" --pause 0.5
echo "FINAL $OUT/$SLUG.mp4 $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$SLUG.mp4")s"
