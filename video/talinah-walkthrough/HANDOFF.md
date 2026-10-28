# Talinah walkthrough video: pipeline and handoff

This folder rebuilds the Talinah sales walkthrough from the raw screen recordings and the voice-over. It covers fake demo data instead of real people, the editorial motion style, the music and a privacy audit. Everything here is code; the private inputs are **not** in git, because this repo is public.

## 1. Resume in a new session

1. Upload these files to the session and tell Claude where they landed:
   - `talinah_raw_part1.webm`, `talinah_raw_part2.webm`: the raw screen recordings, each under 30 MB.
   - The voice-over MP3.
   - `talinah_private_subs.json`: the real → fake name map. It was sent in chat, never commit it.
2. Put them in place. This folder's `.gitignore` covers both locations.
   ```
   mkdir -p inputs private
   cp <raw1> inputs/raw_part1.webm; cp <raw2> inputs/raw_part2.webm; cp <vo> inputs/voiceover.mp3
   cp <subs json> private/subs.json
   ```
3. `./setup.sh` installs the Python dependencies and fonts.
4. `./prepare.sh` builds the reference frames, OCR keyframes, fake-data templates and music. It takes about 5 minutes.
5. Check a few frames: `python3 showcase.py --stills check.jpg 12.3 21.5 28.6 35`.
6. Do the full render and audit: `./render_showcase.sh`. It takes about 20 minutes; any hit in `audit_*.json` is a real name that slipped through.

## 2. Approved decisions

- **Logo**: "Talinah" in Poppins SemiBold (600), with no dot.
- **Style**: editorial, copied from the Kinai reference the client liked:
  - **Headlines**: Inter Display Medium, with an Instrument Serif italic accent in muted sage, for example "Better *hires.*" and "powered by *AI.*".
  - **Colours**: soft green-grey ink, a cool grey-white background with mint and pale-blue glows, and a faint dot grid.
  - **Reveals**: mask wipes, where each line slides up from an invisible edge.
  - **Frame**: in split layouts, the logo sits top-left, the step pills (01 Overview, 02 Rank, 03 Decide) top-right, and a thin progress line runs along the bottom.
- **Chapters**: each opens as a split, with "STEP 0X · NAME", a 2-line headline and a body line on the left and the product on the right. It then expands into the zoomed product.
- **Spotlights**: dim the rest of the screen, put a green ring around the element and show a white callout chip. They are anchor-tracked, so they follow the page as it scrolls.
- **Captions**: light, as a white card with ink text.
- **Fake demo data, never blur**: names, emails, phone numbers, org ID and avatar are typeset in the app's own font (DM Sans, with weight and size fitted per line). The HR user is *Nour Hassan (NH)* and the hero candidate is *Mariam Adel*.
- **Background**: the Higgsfield-generated gradient `hfbg/gradient.webp`. The client rejected icon badges and the solid green background.
- **QR code** to https://talinah.com, large, with the end card held long enough to scan. Use it only in the 16:9 master, not in social cuts.
- **Music**: an original score from `music.py` (96 BPM, D major), ducked under the voice-over and mastered to -14 LUFS. **The client is still judging the draft.**

## 3. Status

| Deliverable | State |
|---|---|
| Showcase (intro, then dashboard, AI ranking and AI Insights, then closing card), ~39 s | Rendered; voice-only and music versions sent in chat |
| Full video with all 8 chapters | **To do** (see 5) |
| 9:16 vertical cut, 15–20 s cut-down | To do |

## 4. File map

| File | Role |
|---|---|
| `render.py` | Base engine: timeline `SEGS` (VO time → source time), camera keys `CAM`, captions `CAPS`, `Reader` (decodes source at 60 fps), `main()` for chunked renders |
| `intro6.py` | The approved intro: hook with strike-through, logo reveal and dock, "Hiring, powered by *AI.*" with the live AI Insights card, then the push-in |
| `showcase.py` | The showcase: chapter splits, spotlights and callouts (`ANCH`, `SPOTS`), ripples, light captions, closing card, fake data plus edge fade in `Reader.at` |
| `fakedata.py` | Builds templates from OCR keyframes (`build()`) and replaces real text per frame (`Faker.apply`): global matching, a lower threshold for long strings (cursor cover), partial matches at the viewport edges, overlap suppression |
| `v4.py`, `backgrounds.py` | Shared helpers: window compositing, perspective cards, QR, button, background functions (`gradient_plate` is the approved one) |
| `music.py`, `mixmusic.sh` | Score synthesis; duck under the VO and master to -14 LUFS |
| `audit.py` | OCRs every frame of a render and lists any real name or email (the watch-list comes from `private/subs.json`) |
| `ocr_kf.py`, `fontfit.py`, `sheet.py`, `pii.py` | Keyframe OCR, font fitting, contact sheets, and the legacy blur (still used by `v4` helpers) |

**Timing convention:** everything is on the voice-over clock (t = 0 when the VO starts). The video adds `OFF = 0.35` s of lead-in, so output time = VO time + 0.35.

## 5. Next steps (the rest of the video)

All times are on the voice-over clock. `render.py` already has the matching `SEGS` from the v3 edit.

| Chapter | VO | Plan |
|---|---|---|
| 04 Scheduling | 36.8–45.4 | Split headline, then a spotlight on each field as it is named (date 39.4, duration 40.9, type 41.4, location 42.5), then the success toast on "handles the rest" |
| 05 Scorecard | 46.8–60.5 | Spotlights on recommendation, then skill ratings, then strengths, then areas to improve; then the submitted feedback on "consistent evidence" |
| 06 Automation | 61.1–70.8 | Status dropdown, then an **animated flow graphic**: Status changed → Recruiter assigned → Next round scheduled |
| 07 Notes | 71.8–75.9 | Typing, then the "Saved automatically" toast |
| 08 Offer | 77.0–81.0 | Offer Sent, then the upload dialog. **Fake file name**; the file-picker and Gmail segments stay cut |
| Outro | 81.1–end | Reference style: fanned product cards ("all in one place"), then the end card with CTA and QR |

Part 2 of the recording has new real people: the interviewer dropdown with colleague emails, a notification dialog and file names. Add them to `private/subs.json`, OCR part-2 keyframes (extend `ocr_kf.py` to take the part), rebuild and audit.

## 6. Lessons on cost

- The fake-data pass costs about 1.5 s per frame and drives most of the render time. Each leak the audit finds means another full render, about 10 minutes for 39 s.
- **The biggest saving is to re-record on a demo account with fake candidates.** That removes the fake-data step, the audits and the re-renders.
- Review with `--stills` contact sheets, and render the full video once at the end.
- Leaks found and fixed so far:
  - Cursor hover over an email: long-string threshold of 0.66.
  - Names cut by the viewport edge while scrolling: edge matching plus a 34 px bottom fade.
