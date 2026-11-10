---
name: daily-batch
description: Produce the daily Stick to History batch unattended - 2 long videos (5-7 min, 16:9) and 2 standalone Shorts (vertical, under 60 s), researched, built, quality-gated at 90/100 and delivered to the owner. Use when a scheduled run or the owner asks for the daily batch.
---

# Daily batch (Stick to History)

Runs unattended in a fresh cloud session. The owner is offline: do not ask questions, make sensible decisions and
write them down. Read `PLAYBOOK.md` first and follow it; where this file and the playbook differ, the playbook wins.

## Targets

| Item | Count | Format | Length |
|---|---|---|---|
| Long video | 2 | 1920x1080 | 5-7 min (about 850-1150 narration words) |
| Short | 2 | 1080x1920 | 35-58 s (about 100-150 words), **topics unrelated to the long videos and to each other** |

Order of work: long 1, Short 1, long 2, Short 2. Deliver each item as soon as it passes the gate, so a run that hits a
usage limit still delivers what finished. Never deliver anything that scored below 90.

## 0. Setup (every run)

```bash
cd <repo> && git fetch origin channel-video-ideas && git checkout channel-video-ideas && git pull --ff-only
test -x .venv/bin/python && test -f models/kokoro/voices.npz && test -d node_modules/gsap || bash src/pipeline/setup.sh
```
`src/pipeline/setup.sh` installs the Python venv (kokoro-onnx, faster-whisper), downloads the Kokoro model and runs
`npm install --ignore-scripts`. Chromium/Playwright and ffmpeg are preinstalled.

Read `channel/topics-log.md`. Never repeat a topic or angle listed there.

## 1. Research (role: researcher - one Agent)

Spawn one general-purpose agent with WebSearch. Ask it to return, as JSON plus notes:
- 8 long-video ideas and 6 Short ideas in the channel niche (history, "How It Really Happened", "What If...?",
  "History's Dumbest..."), excluding everything in `channel/topics-log.md`.
- For each: the playbook score out of 100 (hot right now / searchable name / story with stakes / is a big channel already
  doing this angle / can we make it well in the sketch style), with a one-line reason per factor.
- For the top ideas: top YouTube videos found in search (title, channel, views, date, length), and the angle nobody has used.
- For the chosen 2 long + 2 Short ideas: a fact sheet where **every fact has two independent sources (URLs)**; facts with
  one source are marked "single-source: cut or label as claimed/reportedly".

Pick the 2 highest-scoring long ideas and 2 highest-scoring Short ideas **at or above 90**. If fewer than needed reach 90,
make only those and say so in the delivery note.

## 2. Script (role: writer - one Agent per video)

Give the writer the fact sheet, `PLAYBOOK.md`, and `examples/cuban-missile-crisis/scripts/narration-script.json` as the
format reference. The script must:
- Start with voice and the promise on the first frame (no intro, no logo). State plainly what the video reveals.
- Use only two-source facts; anything else is cut or labelled ("reportedly", "according to accounts...").
- Plan 2-4 shot changes per sentence in each scene's `actions` (the picture changes whenever the idea changes).
- End long videos with a spoken subscribe line tied to what's next ("Subscribe - next we're ...") plus an answerable
  comment question ("Which ... would you pick?", "What did we miss?"). Shorts end with a one-line spoken hook to the channel.
- Write years and numbers as digits (the TTS normaliser handles them); avoid ALL CAPS except emphasis words.
- Save `scripts/narration-script.json` and `sources.md` (claim -> two URLs) in the project.

## 3. Build (role: editor - main session)

Project folder: `projects/<slug>/` (gitignored). For each video:
1. `video-project.json`, `characters/*.json` (reuse `examples/cuban-missile-crisis/characters` style).
2. Voice: `.venv/bin/python scripts/kokoro_tts.py --script scripts/narration-script.json --output audio --voice bm_fable`
3. Timestamps: `.venv/bin/python scripts/whisper_transcribe.py --audio-dir audio --output timestamps`
4. Compare the transcript with the script (names, numbers); fix wording that is misread and regenerate that scene.
5. Write `scenes.py` with the sketch kit (`src/sketch/kit.py`), modelled on `examples/cuban-missile-crisis/scenes.py`:
   every cue keyed to a word time via `Words`; constant brand (parchment, ink, Caveat, faction colours);
   change the picture every 1.5-4 s; big text readable on a phone (min 44 px on 1080 wide, 56 px on Shorts).
   Shorts: `page(..., width=1080, height=1920)` and layouts designed for vertical.
6. **Sample check first**: build scene 01, render it with `node src/render/capture.cjs`, inspect frames, fix, then build all.
7. Snapshot every scene at 6 points (seek the timeline in Playwright) and fix layout problems before the full render.
8. Render: `bash src/pipeline/render_project.sh projects/<slug>` (frame-accurate, narration, -14 LUFS, subtitles).
9. Long videos: thumbnail (one clear idea, 1280x720, see `examples/cuban-missile-crisis/thumbnail.py`, then
   `node src/render/screenshot.cjs output/thumbnail.html output/thumbnail.jpg`) and `output/metadata.txt`
   (3 title options, description with chapters, tags, category Education, sources note). Shorts: title + description.
No background music unless the owner adds it later.

## 4. Quality gate (role: quality checker - one Agent per video, on the finished file)

Run `.venv/bin/python src/pipeline/gate_report.py projects/<slug>` (add `--vertical` for Shorts), then spawn the checker
agent with: the report, `gate/frames.png`, `gate/transcript-diff.txt`, the script, `sources.md` and the playbook
checklist. It must view the frame sheet, verify each item and return a score out of 100 with evidence and a fix list.
- 90 or more: pass.
- Below 90: apply the fixes and re-gate (at most 2 rounds). Still below 90: do not deliver; record why.
The researcher, writer and editor roles also each give a score with evidence in the delivery note.

## 5. Publish and deliver (role: publisher)

For each passed item:
1. Write `projects/<slug>/upload.json` (format in `src/publish/youtube_upload.py`; example `examples/cuban-missile-crisis/upload.json`):
   key `<date>-<slug>`, `"expect_channel": "Stick to History"`, title, description (with chapters for long videos),
   tags, category 27, `made_for_kids: false`, thumbnail and captions paths, **`"privacy": "private"` and no `publish_at`**.
   The owner reviews each private upload and approves it by scheduling or publishing it in YouTube Studio.
   Shorts: title ends with " #Shorts", vertical file, no thumbnail.
2. Upload: `python3 src/publish/youtube_upload.py projects/<slug>/upload.json`. It refuses a wrong channel or a repeat key.
   Uploads are always private: never set public or unlisted. If the upload fails (missing credentials, quota, auth),
   do not retry in a loop: record the error and fall back to delivery only.
3. Deliver with SendUserFile (status "proactive") as a backup copy: the MP4, `.srt`, metadata and thumbnail.

Then send a short delivery note: what was made, the private YouTube links, the **suggested release time for each**
(Europe/Dublin: long videos 17:00 and 20:00, Shorts 12:00 and 15:00 the next day, until analytics say otherwise),
the four role scores, anything cut or labelled, and which earlier video each new one should link to in end screens/playlists.
To approve a video the owner opens it in YouTube Studio -> Visibility -> Schedule (or Public).

## 6. Record (end of every run)

- Append each made topic (date, title, format, score, delivered or not) to `channel/topics-log.md`.
- Commit `channel/upload-log.md` (written by the uploader).
- Copy each project's text files (script, `sources.md`, `scenes.py`, `metadata.txt`, `gate/report.json`) to
  `batches/<YYYY-MM-DD>/<slug>/` - never audio or video.
- Add any new lesson to the "Lessons learned" section of `PLAYBOOK.md`.
- Commit and push to `channel-video-ideas`.
