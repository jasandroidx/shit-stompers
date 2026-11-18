# Word Whomp HD on Pogo — clean-room study + ranked improvement list

Date: 2026-11-18
Played: https://www.pogo.com/games/word-whomp (Word Whomp HD, free, guest, no account)
Method: clean-room, player-visible behaviour only. No `--deep`. No attempt to extract
Pogo's word list or scoring formula — where I write "bonus" or "about 30 points" it is
what the screen showed a player, not a formula I recovered.

## What I actually did

Two full rounds plus a third, both skill levels reachable in the session:

- Round 1, Skill Level 1, rack `D E N D E A`. Found ADD, DEAN, and the six-letter DEADEN.
  Let the clock run out to see the end state.
- Round 2, Skill Level 1, rack `R E D Y M E`. Found RYE, DRY, DYE, RED, DEER, EYE. Also
  tested an invalid word, a duplicate, Mixup and the settings panel.
- Switched to Skill Level 2 mid-round (which ends the round), saw the same rack re-scored
  against a bigger word list, then started a fresh level-2 round with rack `K S I C S T`.

I did **not** reach Skill Level 3. No audio was evaluated — I can see a mute button and a
sound slider, but I cannot hear the game, so I make no claims about its sounds.

## What the real game does, in order

### 1. Shell
The game loads inside Pogo's own chrome: a right-hand toolbar (home, fullscreen, rank,
mute, chat) and a "Play Game" brick. The game itself is a Cocos canvas, **480×1000
portrait**, letterboxed hard on a desktop screen — big black bars top and bottom.

### 2. How-to-play card, once
Before the first round: a parchment card with three panels (To Play / To Win / To Score),
a "Do not show again" checkbox, and START. It teaches clicking vs typing, Enter to submit
and space to mix up.

### 3. The round screen
- Top bar: `?` help, `◀ Skill Level 1 ▶`, `TIME 2:30`, `SCORE`, `RANK`, and a small
  settings signpost on the fence at the right.
- **Word board, upper left:** the words you can find sit there as *blank tile strips*,
  four rows to a column, sorted by length and flowing into a new column as needed. Skill
  Level 1 = 3 columns (12 words); Skill Level 2 = 4 columns (16 words). You can see how
  much is left without being told any word.
- **Six letter tiles** across the middle, each held by its own carrot character. Picking a
  letter physically lifts that character and its tile into a row of six dirt patches above
  the tray, so the word you are building reads left to right in the dirt.
- Buttons: `MIX UP` (tree stump), `ENTER` (log), `CLEAR LETTER` (stone).
- **Bonus track** along the bottom: a row of carrots with a carrot-character marker, a
  `20 BONUS` flag partway along and a `50 LAST WORD` flag at the far end. Skill Level 2
  raises these to `30 BONUS` and `75 LAST WORD`.
- Clock counts down from **2:30** (Pogo's own blurb says 2:20; the live game says 2:30).

### 4. Finding a word
The word fills its strip on the board and stays there. A short gold/green highlight marks
it. The score counter rolls up rather than snapping.

Finding the **six-letter word** is the set piece: it flies out of the tray to a card in the
top right with a carrot head on it and stays there for the rest of the round, and the score
jumps hard. That is the "gold word".

### 5. Getting it wrong
Both rejections are small text under the tray, and the tiles come back:
- `Not a valid word`
- `Word already found`

No modal, no penalty, no lost time beyond the typing. The clock keeps running.

### 6. Time up
Nothing pops up. The board simply flips to a **full reveal**: every word that was available
is shown, the ones you found stay lit, the ones you missed dim. `ENTER` becomes `CONTINUE`.
This is the single best thing in the game — you get to see exactly what you walked past.

### 7. After CONTINUE
A guest upsell interstitial (weekly challenge, "Register Free", BACK TO GAME), then a
parchment scroll over the board:

```
You didn't reach the carrot
You found 5 out of 16 words this round
Word Score            160
Gold Word Bonus         0
Time Remaining Bonus    0
TOTAL SCORE           160
[ New Game ]
```

Three named score categories, a found/total count, and a verdict line about the carrot
goal. Note "Time Remaining Bonus" — leaving time on the clock is worth points, and I
scored 0 because I let it run out.

### 8. Changing skill level
Clicking ◀ ▶ mid-round asks first: *"This will end your current game. Are you sure?"*
Skill changes what the board asks of you: same rack, 12 words at level 1, 16 at level 2,
with the bonus flags going 20/50 → 30/75.

### 9. Settings
A small parchment panel with a sound slider and a New Game button. That's the whole thing.

## What I could not observe, and will not claim

- The scoring formula. 3-letter words read about 30, the six-letter gold word paid a
  separate 100 gold-word bonus on one round; that is what the screens showed, not a rule
  set I recovered.
- The exact dictionary. I saw NEE and ERE accepted, and EDDY was not on a board that
  couldn't spell it anyway. No word list was extracted.
- Audio entirely.
- Skill Level 3.

## Ranked improvements — what is worth taking

Ranked by how much they'd matter to a player, not by how easy they are. Whether we already
have each one is **unverified**: the pack (`word-whomp-custom.html`, README, gap analysis,
steal sheet) is not in this chat, so this ranks the ideas, not the diff.

1. **Time-up reveal board.** At 0:00, keep the board and reveal every word, found ones lit
   and missed ones dimmed, instead of a plain results modal. This is the moment that makes
   you press play again. Highest impact of anything I saw.
2. **Named score breakdown at the end.** Word Score / Gold Word Bonus / Time Remaining
   Bonus / Total, plus "you found N of M words". Tells the player what they were rewarded
   for and gives them a number to beat.
3. **Laid-out words shown as a filling tile board.** Blanks on the board, four to a column,
   sorted by length, filled as you find them. Turns "how am I doing" into something you read
   at a glance, and makes the laid-out/bonus split legible without a word count popup.
4. **Gold-word fly-away.** When the six-letter word lands, send it to a card in the corner
   and pay a separate, loudly announced bonus. It makes the six-letter hunt the point.
5. **Skill levels that change the ask, not just the letters.** More words on the board
   (12 → 16) and bigger bonus flags (20/50 → 30/75). Difficulty you can see.
6. **Inline rejection messages.** "Not a valid word" / "Word already found" under the tray,
   tiles returned, nothing modal, no penalty. With our unfiltered dictionary this matters
   more than it does for Pogo.
7. **Time-remaining bonus.** Points for finishing with clock left, so speed is rewarded and
   the round has a second objective.
8. **Tactile letter picking.** Picked letters visibly lift out of the rack into a word tray;
   each tile carries its own character. Pure feel, cheap to do, very noticeable.
9. **Confirm before ending a round.** "This will end your current game. Are you sure?"
   Protects two and a half minutes of work from a misclick.
10. **Mixup taught, not just present.** Space bar mixes the rack in place, and the how-to
    card says so. Small, but it's the get-unstuck move.
11. **A how-to card you can dismiss for good,** and a settings panel with one slider.

## Where Pogo is worse — don't copy this

- A guest upsell interstitial between every round. It breaks the rhythm badly.
- The portrait 480×1000 canvas with letterboxing on desktop.
- Total opacity about scoring until the parchment appears; during play you just watch a
  number roll.

## Rules that don't move (unchanged by any of the above)

- Dictionary stays NWL2023 + swear words. No profanity filtering, ever.
- The laid-out / bonus split stays.
- The `onSwearWord` hook stays.
- Still one self-contained HTML file, no dependencies.

## Evidence

Screenshots in this folder: `pogo-02-level-select` (how-to card), `pogo-03-after-howto`
(round screen), `pogo-06-submitted` (board filling), `pogo-08-deaden` (gold word), 
`pogo-10-end-of-round` and `pogo-grid-zoom2` (full reveal), `pogo-12-next-round` (parchment
score breakdown), `pogo-14-invalid` / `pogo-16-duplicate` (rejections), `pogo-17-mixup`,
`pogo-19-settings`, `pogo-grid3-zoom` (board grouping by length), `pogo-29-skill3-parchment`
(skill level 2: 4 columns, 30/75 bonus flags).
