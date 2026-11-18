# Shit Stompers — saved ideas and open decisions

Running list so nothing decided in conversation gets lost. Newest at the top.

## Audit, 2026-11-18

Full read, play-throughs and board sampling: `docs/analysis-2026-11-18.md`.
Six bugs fixed there (idle nudge, clock while hidden, oversized boards, swear
message, thin-rack pile labels, title past the fold), plus the genre research
that backs the board sizes and clocks, and a ranked list of what to build next.

## Saved for later

**A porch that changes as you progress.** The background should not be one fixed
picture forever: as you clear levels or pass score thresholds, the scene shifts —
later evening, deeper night, fireflies, decorations, the yard filling up, seasons.
Tied to the game total (or rounds cleared) rather than to a single round, so it
reads as the game world moving on. Jason's idea, 2026-11-18; deliberately parked
until the art and voice pass is done, not built.

## Craft pack (installed 2026-11-18)

Jason dropped two packs in; both are extracted into `.agents/skills/` (46 skills
in total). The second one is the Craft set: AniCraft, DesignCraft, VectorCraft,
EffectCraft, PhotoCraft, MaterialCraft, CADCraft, FigCraft, Craft Anything, plus
the router and 8 more whose binaries are not installed.

**AniCraft is the right tool for animating Crappy's PNGs** — it imports the
bitmap, tweens it, and exports a sprite sheet + JSON frame map, GIF, Lottie or
HTML. Ready-to-run handoff script: `pack/anicraft-crappy.sh` (untested here; the
Craft binaries live on Jason's laptop, not in this sandbox).

Two gotchas from the skill: CLI frames are 1-based while command/MCP frames are
0-based, and AniCraft bakes its tweens into exported frames — so it is for
one-off assets, not the live in-game animation, which stays CSS/JS.

## Open decisions, waiting on Jason

- **Board size.** Settled for now: 12/16/22 stays, and SINE now makes the
  starter board anyway (the plural rule and the shift-list freed the slots).
- **Crappy's voice.** Leaning to Kokoro-82M (Apache 2.0, CPU, 54 voices, no
  account) rendered at build time, pitched up 3 semitones. Samples in
  `files/voice/`, audition page `files/voice-test.html`, script
  `pack/make_voice.py`. Open question: British `bf_emma` or American `af_heart`,
  and whether 3 semitones is enough cartoon.
- **Music.** Banjo porch loop, synthesized (Karplus-Strong), G–Em–C–D at 88 with
  crickets — see `files/audio-test.html`.
- **Sprite faces.** Six still missing: blink, shocked, annoyed, dizzy,
  raspberry, laugh. Sheet and loose PNGs delivered in `files/crappy-sprites/`.
- **GitHub repo.** One repo per game, private, include template + build script +
  word lists; leave out the 22MB art zip. README and ignore file offered.
- **Slurs.** Still deliberately absent from the dictionary; awaiting Jason's word.

## Already settled

- No word filtering of any kind; swear words score normally.
- Swear jar: 25c a word, never resets, costs no points.
- Words removed at Jason's request: cacks, numpty, helluva, cunty.
- Word engine: every dictionary word now carries a wordfreq Zipf score (baked
  in at build time, 31KB, no runtime dependency), and boards are ordered by it.
  Two curation rules on top: plurals are held back (ask for SIN and NOISE, not
  SIN, SINS, NOISE, NOISES) and a short shift-list keeps corpus artefacts like
  NESS, SEN, ONS, NOS, ESS off the board while leaving them valid to type.
  Starter rack now reads: ins, ion, one, sin, sis, son, eons, nose, ones, sine,
  sons, noise.
  Rebuild: `PYTHONPATH=/tmp/wf python3 pack/score_words.py` (needs wordfreq),
  then `python3 pack/build_v2.py`.
- Shake repaints the plaques (fixed).
