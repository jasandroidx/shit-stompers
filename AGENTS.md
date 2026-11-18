# Notes for whoever works on this next

Read this before touching anything. It is the difference between a five-minute
change and an afternoon of guessing.

## The shape of the thing

One self-contained HTML file is the product: `index.html`. No server, no
dependencies, no network calls, no build step for the player. It opens from a
file path and works offline. Keep it that way.

`index.html` is **generated**. Never edit it directly — your change will be
wiped by the next build. Edit `src/game.html` and rebuild.

```bash
python3 -m pip install pillow     # once, for the art packing
python3 build/build.py            # src + data + assets + audio -> index.html
```

Always check the JS parses after a build:

```bash
node -e 'const fs=require("fs");const h=fs.readFileSync("index.html","utf8");new Function(h.match(/<script>([\s\S]*)<\/script>/)[1].replace(/<\/script>/g,""));console.log("js parses")'
```

## Non-negotiables

- **One file.** Anything added to the game has to be inlined by the build.
  No CDN, no external font, no `fetch`.
- **No profanity filtering, ever.** Swear words are real words, they score, and
  `onSwearWord(word)` fires so the swear jar can charge 25¢. Do not add a filter,
  a toggle, or a "family friendly" mode. That is the entire point of the game.
- **The player is not a gamer.** Laura plays this. Big targets, plain words,
  forgiving timers, no reflex tests, no penalty for exploring.
- **No new dependencies** without a real reason. The whole game is stdlib HTML,
  CSS and JS.

## How the build works

`build/build.py` takes `src/game.html` and substitutes four placeholder families:

| Placeholder in the source | Replaced with |
|---|---|
| `/*__DICT_DATA__*/` | `const DICT`, `COMMON`, `FREQ_ORDER`, `GOOGLE_ORDER`, `WORD_LEVELS` |
| `__ART_PLAIN__`, `__ART_EXCITED__`, `__ART_SLEEPY__`, `__ART_CROWN__`, `__ART_PILE__`, `__ART_BG__` | base64 data URIs from `assets/` |
| `__ART_HERO__` | the title's superhero fly-in: `assets/sprites/crappy-superhero-strip.webp`, a 40-frame transparent WebP strip (16fps) |
| `__VOICE__` | a JSON object of `"name": "data:audio/mpeg;base64,…"` from `audio/` |
| `__SFX__` | the same, for short recorded effects in `audio/sfx/` (mono 96k mp3) |
| `/*__FONT_CSS__*/` | `@font-face` blocks from `fonts/*.woff2` — Luckiest Guy (wordmark) and Fredoka (menu UI), base64'd |

If a placeholder is left unsubstituted the build asserts and fails. That is
deliberate.

Word lists live in `data/` as one word per line and are joined with spaces into
the const strings. `DICT` and `COMMON` **must** be followed by `.split(" ")` so
the runtime gets arrays — `build.py` appends it, so if you change that function,
keep it.

## Where things live in `src/game.html`

CSS is in labelled blocks in this order: HUD, staging, tiles, buttons, word
board, bonus, pile track, overlays, title screen life, keyframes, responsive.

JS is in labelled blocks too:

| Block | What's in it |
|---|---|
| `profanity, unfiltered` | `CRUDE_WORDS`, `TAME_WORDS`, `SWEAR_SET`, `onSwearWord()` (the swear jar hook), `JAR_RATE` |
| `sound` | tiny WebAudio synth: `tone()`, `noise()`, `sfx.*`, the mute toggle |
| `Crappy's voice` | `speak(name)`, `stopVoice()`, one-line-at-a-time policy |
| `dictionary helpers` | `formableWords()`, `splitKey()`, `generateRack()` |
| `round setup` | `setupRound()`, `boardWordsForLevel()`, `pointsFor()`, `LEVEL_FLAGS` |
| `play` | `stageTile()`, `submitWord()`, `mixUp()`, `bad()`, scoring, `endRound()` |
| `timer` | countdown, the 30-second warning, the idle nudge |
| `end` | summary screen, totals, high score |
| `wire up` | button listeners, title slam sequence, `ss-slam` events |
| `skill levels` | `applyLevel()`, `requestLevel()`, level change confirmation |

## Board generation (the bit that's easy to break)

Board sizes are 16 / 20 / 24 with clocks of 2:30 / 2:30 / 2:45 (relaxed
mode drops the clock entirely — see below). Pogo publishes
12 / 16 / 22, but a rack here offers a median of 27 good words, so a 12-word
board hid obvious answers as "secret stinkers". A picked word drags its plural
(or singular) onto the board, the golden word drags its stem (POISED -> POISE),
and a thin rack asks for fewer words rather than for nonsense.

The rack is a six-letter word, shuffled. Every formable 3–6 letter word is found,
then split into board words and "secret stinkers":

1. A word is board-eligible if it's in `COMMON` or frequent enough in
   `data/freq-50k.txt`.
2. Plurals are held back so the board isn't four spellings of the same word.
3. `BOARD_SKIP` removes corpus artefacts that are technically valid but that no
   person would list (`ness`, `sen`, `ons`, `ess`, `sos`…). They stay valid
   words if typed — they just never occupy a slot.
4. `data/word-levels.txt` (obviousness 0–15, one character per `DICT` entry)
   orders the board so the easy words land first.

`WORD_LEVELS` is one character per entry of `data/dictionary.txt` — it covers
that **prefix** of `DICT`, because the crude words are appended at runtime. The
build compares lengths naively, so the runtime check is `ra <= DICT.length` and
maps the first `WORD_LEVELS.length` entries; an equality check silently disabled
the whole ranking once and every board fell back to Google rank. If you edit the
dictionary, regenerate it:
`PYTHONPATH=/tmp/wf python3 build/score_words.py` (needs `wordfreq`).

## Relaxed mode

Persisted as `ss_relaxed`. The title card has a checkbox, and the Time chip in the
HUD toggles it too — that second control is what keeps it reachable after "don't
show this again" hides the title. Relaxed means no clock at all: `startTimer()`
returns early, the HUD shows `∞`, `endRound()` pays no time bonus, and the summary
hides the time row. `timeLeft` is untouched while relaxed, so switching back to
timed mid-round starts the clock at the full level time.

## Sound effects (recorded)

Jason's short effects live in `audio/sfx/` as mono 96k mp3 and are packed into
`__SFX__`, decoded into WebAudio buffers on the first sound (`warmSfx`), and
played with no per-play latency. The synth in the `sound` block is the fallback
for the moment before a buffer is ready, or if a file is missing.

| file | fires on |
|---|---|
| `tap.mp3` | a letter tile is clicked |
| `right.mp3` | a correct word is stomped |
| `wrong.mp3` | a rejected word ("Not a word here.") |
| `shuffle.mp3` | Shake / Space |
| `allletters.mp3` | a six-letter word (uses the whole rack) |
| `powerup.mp3` | the golden word |
| `idle.mp3` | the "anybody there?" nudge |

## Music

Two pieces of music. The title fly-in plays `audio/music/flyin.mp3` (the fly-in
video's own track, inlined by the build as `__MUSIC__`); it stops on START. The
porch tune under play is synthesized (see `/* ---------------- music ---------------- */`):
a 104 BPM C-major eighth-note loop of triangle bass plus square melody on the same
AudioContext as the effects, scheduled with a 0.3s lookahead so it never stutters.
It starts on START or the first tile click, stops with the mute toggle, and drops to
30% while Crappy speaks (`duckMusic`, called from `speak` and the announcer).
`window.ssMusic` exposes `.on` and `.step` for tests. To use a recorded porch track,
drop it in `audio/music/`, inline it like `flyin.mp3`, and play it in `startMusic`.

`window.ssSfx` is the live buffer map — `ssSfx.tap.buffer` means it decoded.

## Voice

Clips live in `audio/` as `poop-<key>.mp3`; the build strips `poop-` and `.mp3`,
so the key is what you pass to `speak("<key>")`. `audio/lines.txt` records what
each one says. Adding a line is: drop the file in, rebuild, call `speak("key")`
where it belongs.

Policy: one line at a time. A new clip cuts the old one, and anything that fires
while a line is still talking is dropped unless it passes `{ force: true }`.
Reserve `force` for moments that deserve to interrupt (golden word, round over).

Current wiring: `letsstomp` (title + start), `again` (new rack), `bigword` (6+
letters), `onaroll` (8th word), `golden`, `sneaky` (off-board word), `pilebonus`
(4th/last word), `notaword` (wrong word, 65% of the time), `rudejar` (swear jar),
`hurry` (30s left), `anybody` (idle), `wedidit` (board cleared), `almosthadit`
(time up), `nicestomp` (level change ends a round), `shaky` (skill change),
`laurabest` (new high score).

## The title sequence

SHIT slams in first, STOMPERS lands under it (both `slamDown`), then Crappy
flies in and stands on the wordmark, then he says his line, and only then do
the tag and the rules card come up with START. JS fires an `ss-slam` CustomEvent
at each impact with `detail.n` of 1 or 2; the thuds are synthesized in the
`ss-slam` listener — bind sound to that event, do not retime the CSS to match a
sound. `.ready` on the overlay (which reveals the card) is set when his line
ends, with a timer fallback.

The wordmark and menu type are Luckiest Guy and Fredoka, inlined as base64 WOFF2
from `fonts/` by the build (both OFL, so embedding is fine). Without those files
the build warns and the CSS falls back to Arial Black / Trebuchet.

The whole intro is chained, clip to clip — `audio/poop-announcer-shit.mp3`
(1.10s) and `poop-announcer-stompers.mp3` (2.30s). SHIT lands at 420ms with
`announcer-shit`; STOMPERS lands when that line ends with `announcer-stompers`;
when that second line ends the hero's `.fly` class starts the 2.2s sprite strip
(`assets/sprites/crappy-superhero-strip.webp`, `steps(39)` over 40 frames — the
end value is `-97.5%` so the held last frame sits inside the window); on
`animationend` he bobs and `speak("letsstomp")` fires, and its `onEnd` reveals
the card. There is no speech bubble any more — the clip is the line.

## Gotchas learned the hard way

- **`background` shorthand kills gradient text.** `.logo b` clips a gradient to
  the glyph with `background-clip:text`. A later rule using `background:` resets
  `background-clip` to `border-box` and the letters become solid blocks. Use
  `background-image:` when overriding.
- CSS custom-property-free codebase: colours are literal, repeated per block.
  Match the surrounding style instead of introducing a token system.
- The word board restyles are keyed off `.wbox.found`, `.wbox.missed`,
  `.wbox.gold` and `.board.reveal`; renaming those breaks the reveal at the end
  of a round.
- `lastWordAt` / `idleSaid` drive the idle nudge. `idleSaid` is reset in
  `setupRound` — it used to live for the whole page load, so the nudge fired once
  and never again.
- The countdown holds while `document.hidden` is true (locked phone, switched
  tab) and resets `lastWordAt` on each held tick, so a player does not lose a
  round to a phone call or get scolded the moment they come back.
- `boardWordsForLevel` must never exceed `LEVEL_WORDS[lvl]`. The golden word and
  its stem used to be appended after the cap and skill 3 dealt 25-word boards;
  it now evicts the least obvious chosen words to make room.
- Title media queries are order-sensitive: `@media (max-width:640px)` comes after
  `@media (max-height:720px)`, so a short-screen rule that sets `.hero-wrap`,
  `.logo` or `.tag` has to be repeated in the combined
  `(max-width:640px) and (max-height:720px)` block at the very end of the sheet,
  or the width query wins and the card runs past the fold on a 360x640 phone.
- The timer is a plain `setInterval`; anything that pauses the game must clear
  `timerId` or the clock keeps running behind an overlay.

## Testing

There is no test suite. The checks that matter:

1. The build runs and the JS parses (commands above).
2. Open `index.html`, start a round, spell a word, stomp it, let the clock run
   out, start a new round. No console errors.
3. Try a rude word — it should score and charge the jar, not be refused.
4. Resize to a phone: the board, the title and the summary all have to fit.

## Open work

See `docs/ideas-and-decisions.md` for parked ideas (the pile growing, the porch
changing with progress, a real animated character). Do not start those without
asking; several are deliberately deferred.
