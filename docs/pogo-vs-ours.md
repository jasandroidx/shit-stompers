# Word Whomp — Pogo vs. ours (2026-11-18)

Part 1 (Pogo, live, clean room) is in `pogo-whomp-study-2026-11-18.md`.
This is part 2: the same observations put next to the actual `word-whomp-custom.html`
from the pack, so the ranking is about what we still lack — not about ideas in general.

Method: read `README.md`, both analysis docs, the mechanics research, the console log,
`word-whomp-custom.html` (all 661 lines, CSS + JS), and ran the game in a browser at
phone width to see the real screens. Pogo was played live earlier today: 3 racks,
rejections, Mixup, settings, skill arrows, two round-end states.

No craft-anything / Playwright MCP exists in this chat, so this is a hand comparison,
not that pipeline. Pogo's scoring formula and word list remain proprietary and were not
recovered — nothing below claims otherwise.

---

## What Pogo does that we don't (ranked by player impact)

### 1. The end-of-round reveal
Pogo freezes the board and fills it in place: every word you found lit, every word you
missed dim, held for a beat before the summary. You learn the rack.
Ours jumps straight from 0:00 to a modal. The fence is still behind it, but covered —
and the missed words never appear at all. This is the single biggest missing moment.

### 2. A skill level that exists
Our HUD says "SKILL LEVEL 1" — in our own `<div class="label">`, with no logic behind it
and no way to change it. That's the most "off" thing on the screen: it advertises a
feature we don't have.
Pogo's levels are real and change the ask: same rack, 12 words at level 1 vs 16 at
level 2; bonus markers move from 20 / 50 to 30 / 75; switching mid-round prompts
"This will end your current game. Are you sure?"
Two honest options: build 2–3 levels, or delete the label. Half-built is worse than either.

### 3. It fits on a phone / small tablet
At 432 px wide the page is 527 px wide: the 6th letter tile is cut off, the carrot row
runs off both edges, and "50 LAST WORD" is clipped. There are no media queries at all.
On a laptop (860 px game) everything fits. So this only matters if Mom plays on a
tablet or phone — worth knowing before spending time on it.

### 4. Picking up a letter feels like nothing
Clicking a tile re-renders the whole row: gopher goes to "z z z", a plain box appears in
the staging strip. No travel, no lift, no sound, no score pop. Pogo's letters physically
move up, the gopher reacts, the gold word flies to the trophy card, the score ticks.
Ours is correct but static — this is most of the "charm" gap.

### 5. The carrot row promises something it doesn't do
12 mounds, but racks have ~18 laid-out words. The marker under mound 12 says
"50 LAST WORD" and pays on your **12th** word, not your last. Either one mound per word
in the rack (row length follows the word count) or relabel it "50 BONUS".

### 6. No round continuity
After a round it's "NEW GAME" and the score returns to 0. Nothing on screen says round 2,
3, 4, and the score never accumulates. Pogo always shows what round you're in; ours
forgets the previous round the moment you continue. A running total + "NEXT ROUND"
would make a session feel like a session.

### 7. The gold word is telegraphed before you find it
`.word-box.gold` gives the unfound box a dashed gold border, so the fence points at the
answer. Gold styling should appear at the moment it's found (Pogo's does).

### 8. The how-to is a wall of text, and it comes back every time
Four paragraphs, a dictionary ad, and no way to dismiss it for good. Pogo's card is three
short columns — To Play / To Win / To Score — plus "Do not show again" and one START.

### 9. Rejections land away from the word
"Not a word!" / "Already found!" print in a line *below* the staging strip, which nudges
the board down. Pogo floats the message right at the word you built. We already shake the
staging strip — the text should live there too.

### 10. Flat round-end copy
"TIME'S UP!" + "You found 7 out of 18 words this round." Pogo: "You didn't reach the
carrot." + "You found 4 out of 22 words this round," with the rabbit reacting. Pure
flavor, nearly free.

---

## What we already match (don't rebuild)

- 2:30 clock, starting on the first letter click (Pogo's clock reads 2:30 even though its
  own page says 2:20).
- Blanks on the fence until found, green when found.
- Gold word bonus that does **not** end the round (verified against live Pogo; the old
  research doc was wrong about the instant clear).
- Inline invalid / duplicate rejections with no score penalty.
- Free Mixup, Space to jumble, Enter to submit, Backspace to clear.
- Carrot bonuses at 20 and 50, and a named end-of-round breakdown — ours already has
  Word / Bonus / Gold / Carrot / Time rows; Pogo has three of those.
- A 12-mound carrot row with markers under the right mounds.

## What we do better (keep)

- **The win is reachable.** 18 common words on the fence instead of Pogo's 22 including
  ENOSIS, EOSIN, OSSEIN. No obscure Scrabble word can block the win.
- **Bonus words pay and are separable.** They score, they're listed, they never gate the
  round. Pogo just makes you find them or lose.
- **We tell you the goal up front:** "0 / 18" words found. Pogo only shows boxes.
- **Keyboard typing works.** Typing into Pogo's canvas didn't register in my session —
  only mouse clicks did.
- **No ads, no account nag, no interstitial between rounds.** Pogo's CONTINUE leads
  straight to a "Register Free" challenge card.
- **No 99% loader, obviously.**

## Deliberately not copying

- The 480×1000 portrait letterboxed canvas.
- The per-round "Register Free" interstitial.
- The mid-round confirm dialog — only needed *if* we add skill arrows.
- Pogo's exact point values (proprietary; ours is 20/letter, Pogo showed ~30 for a
  3-letter word — not comparable and doesn't need to be).

---

## Pick list (ranked, with rough size)

| # | Change | Size | Note |
|---|---|---|---|
| 1 | Reveal board on time-up (found lit, missed dim), then summary | a sitting | best single upgrade |
| 2 | Real skill levels **or** drop the fake label | a sitting / 2 min | Jason's call which |
| 3 | Responsive pass for narrow screens | half hour | only if she uses a tablet/phone |
| 4 | Letter travel + gopher react + score pop + gold fly-away | a sitting | the charm gap |
| 5 | Carrot row length follows the rack / fix "LAST WORD" | 15 min | honesty fix |
| 6 | Round number + running total + "Next Round" | half hour | makes a session |
| 7 | Hide gold border until found | 2 min | spoiler fix |
| 8 | Three-column how-to + "Don't show again" | half hour | first impression |
| 9 | Move rejection text onto the staging strip | 10 min | small feel fix |
| 10 | Warmer round-end copy | 5 min | flavor |

Suggested minimum if he wants one build: 1 + 5 + 7 + 9 + 10 (all small), with 2 as the
one real decision and 3 as the one question (what does Mom play on?).

Build rules that don't move: new `word-whomp-v2.html`; never overwrite
`word-whomp-custom.html` or `word-whomp-clone.html`; NWL2023 + swear words, no
profanity filtering; laid-out/bonus split; `onSwearWord` hook; single self-contained file.

## Evidence

- Pogo: `pogo-10-end-of-round.png` (reveal), `pogo-grid-zoom2.png` (lit vs dim),
  `pogo-29-skill3-parchment.png` (level 2 rack, 16 words, 30/75 flags),
  `pogo-02-level-select.png` (three-column how-to), `pogo-14-invalid.png`,
  `pogo-16-duplicate.png`, `pogo-12-next-round.png` (summary rows).
- Ours: `ours-title.png`, `ours-play.png` (phone width, 6th tile + carrot row clipped),
  `ours-end.png` (summary already has the named rows).
