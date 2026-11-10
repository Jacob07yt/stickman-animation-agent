# Video Quality Playbook

Read this before any video work. Quality comes from a process followed on every video, not from one good prompt.
These rules apply to every Stick to History video and Short.

Each job has its own role: **researcher, writer, editor, quality checker, publisher**.
One rule is absolute: **nothing gets posted until the quality checker passes it.**
Add a rule here every time something goes wrong, so the same mistake never happens twice.

## 1. Before you make anything

1. Score the idea out of 100: how hot it is right now, is there a name people search for, is there a story with stakes,
   has a bigger channel already done this angle, can we make it well. Only build ideas above the bar.
2. Search YouTube for the topic and list the top videos with views and dates. If big channels own it, find the angle nobody has used.
3. Study the best video on the topic: count cuts (median shot length, cuts in the first 60 seconds), note the first 10 seconds
   word by word, the on-screen text, the music, the length. Copy the craft, never the content. Numbers beat adjectives:
   "their shots last 1.6 s, ours 6.5 s" tells you what to fix.
4. If you can't make a click-worthy title and a thumbnail with one clear idea, the video won't get watched however good it is.
5. Anything you can't confirm twice comes out, or is clearly labelled as opinion or rumour.

## 2. While you build

- Voice or action on the very first frame; the promise of the video stated plainly; no slow intro or logo.
- A sentence spans 2 to 4 shots; change the picture whenever the idea changes.
- Style each video to suit its title (colour, fonts, music), not one fixed template for everything.
- On-screen text big and readable on a phone.
- "Subscribe for part 2 next week" beats "like and subscribe" (say it out loud, not just on screen). Ask a comment question
  people can actually answer ("pick one", "what did we miss?"), never a bare yes/no.
- Render a sample and check it before rendering the whole thing.

## 3. The quality gate (on the finished file, every time)

Check the rendered video, not the script or the plan. Most mistakes only show up in the final file:
a wrong shot under a caption, a mispronounced name, a missing end card.

- [ ] One frame from every shot on a single image. Check each: right person, right moment, nothing blurry, no stray logos or text cut off.
- [ ] Transcribe the audio (Whisper) and compare it word for word with the script; every name and number must be right.
- [ ] Captions, title card, end card, credits all present.
- [ ] Loudness around -14 LUFS, voice clearly above the music, no clipping.
- [ ] Format right for where it's going (vertical 1080x1920 for Shorts).
- [ ] Each claim on screen ties back to two sources.
- [ ] Each role scores it out of 100 with evidence and lists fixes. Anything below the bar goes back, not out.

## 4. After posting

- Post when the audience is online (YouTube Studio: "when your viewers are on YouTube"); decide the time per video, not by habit.
- Link videos together: end screens, playlists and Shorts' "related video" link, kept within the same topic so YouTube learns who the channel is for.
- Track click-through rate, average % viewed, and subscribers gained per 1,000 views. Write down what worked and add it to this playbook.

## Lessons learned (add one each time something goes wrong)

- HyperFrames' screenshot fallback (no chrome-headless-shell) produced ghosted/duplicated frames. Render with `src/render/capture.cjs` and always inspect frames from the final file.
- Kokoro read "1962" as "nineteen hundred and sixty-two". Years, decades and clock times are normalised in `scripts/kokoro_tts.py`; still verify with Whisper.
- First Cuban Missile Crisis render measured -23.3 LUFS; normalise final mixes to about -14 LUFS.
