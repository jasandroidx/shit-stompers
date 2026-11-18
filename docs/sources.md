# Word Whomp — outside sources, and what they actually settle

Date: 2026-11-18
Purpose: see whether public documentation or a cousin game can pin down the rules that live
play could not (points per word, bonus values, level differences), and whether anything in
those rules is worth taking into Shit Stompers.

Rule for this doc: a source is only cited for what it actually says. Where two sources
disagree I say so instead of picking one and calling it fact.

---

## 1. What is now confirmed by a source, not just by watching the game

| Thing | Value | Source |
|---|---|---|
| Clock per skill level | L1 2:30, L2 2:15, L3 2:00 | BadgeHungry comment thread on the 2018 HD launch (reader "Brenda M." states all three) |
| Original Flash clock | 2:30 | MobyGames entry for Word Whomp (2001) |
| Level changes the payout | "You earn more points as the difficulty increases" | Pogo's own game page |
| Carrot payouts, original | 10 tokens, or 10 / 50 / 100 by difficulty at the "Spin" carrot | MobyGames (2001); BadgeHungry Word Whomp ranks page |
| Last-word payout, original | +200 tokens | MobyGames; BadgeHungry |
| Golden/highlighted word, original | either 20 tokens **or** +15 seconds on the clock | MobyGames (2001) |
| Six-letter word always exists | "At least one word can be made with all six letters" | MobyGames |
| Word slots are alphabetical within length | stated as a playing aid | wordfinder.yourdictionary guide; treocentral TextTwist review describes the same convention |
| Points are not in tokens | HD dropped tokens entirely in 2018 | BadgeHungry launch post |

The one conflict: wordfinder's guide says the clock is 2:20. MobyGames says 2:30, BadgeHungry
says 2:30/2:15/2:00, and the live game read 2:30. So 2:20 is an error in that guide, which is
what we already assumed.

## 2. The thing we most wanted — points per word — is still not published

No source gives a points-per-letter or points-per-length table for Pogo's game. The closest
evidence stays what the screen showed: roughly 30 for a three-letter word at Level 1, and a
flat 100 gold-word bonus. Pogo has never documented the formula and the client does not
expose it. Our 20/30/40 per letter by level is therefore a stand-in, and will stay one.
Nothing found today justifies changing it.

## 3. An open-source Word Whomp clone that published its own rules

`https://github.com/slayyyyer/word-chomp` — "Word Chomp", vanilla JS, no build step, playable
at `https://slayyyyer.github.io/word-chomp/`. It is an original game in the Word Whomp shape,
not a copy of Pogo's code, and its README documents its rules in full:

- 6 letters in round one, 7 afterwards; 2:20 per round.
- Scores by word **length**, not per letter: 3 = 30, 4 = 40, 5 = 50, 6 = 60, 7 = 70.
- "Garden words" (their laid-out set) must be cleared; every other valid word is a **bonus
  word** that scores but does not block the clear. Exactly our split.
- Uses every tile in the rack: **+100 Chomp bonus**. Independently confirms 100 as the
  natural gold-word number.
- Clearing the round early pays **5 points per leftover second**.
- Hint costs 50 points and reveals one missing garden word without paying its points.
- Rack generator guarantees at least one full-length word, rejects racks with fewer than two
  vowels, triple letters, or Q without U, and keeps 14–36 garden words per rack.
- Garden targets are limited to common English (top-20k frequency); every other dictionary
  word is still accepted as a bonus word.

That last pair is the useful part for us: an independent implementation arrived at our exact
architecture — small familiar must-find set, wide bonus acceptance, gold always real, pool
size banded. It is a second opinion, not a new mechanic. Two of its rules we deliberately do
not want: hints that cost score, and length-based scoring (flat 30–70 makes a six-letter word
barely better than three short ones, which is the opposite of the tension Word Whomp has).

## 4. The other close cousin: TextTwist

`https://www.wordplays.com/wordgames/text-twist`, plus MobyGames for TextTwist 2.

- Six letters, 2 minutes, find every word, 3 letters minimum.
- To advance you must find the **bingo word** — one word using all the letters. Everything
  else is score padding. That is a stricter version of our gold word: ours pays, theirs gates
  progress.
- Word slots are laid out alphabetically by length, so the blank board doubles as a hint.
- A "Last Word" button re-inserts your previous word, which makes plurals two clicks.
- TextTwist 2 adds a mode where only bingo words count and each find buys more time — the
  same shape as the original Word Whomp's "+15 seconds for the gold word".

Nothing here beats what we have, but "Last Word re-insert" is a genuinely kind touch for a
slow typist and costs almost nothing to add if wanted.

## 5. What this changes for Shit Stompers

Nothing has to change. Two optional, small, source-backed tweaks:

1. **Gold word as +15 seconds instead of (or as well as) +100 points.** This is a documented
   original Word Whomp behaviour, not an invention, and it suits a 60-something player more
   than points do — the reward is more time to use the word you just found. One-line change
   at the point the gold word is scored, plus a line in the round summary.
2. **"Last word" button** next to Clear. Re-stages your previous submission so plural hunting
   is two clicks. Borrowed from TextTwist, tiny, and it removes the single most common
   hand-typing chore for someone who is not a fast typist.

Explicitly rejected after reading the sources: hinting that costs score (wrong for Mom),
length-based flat scoring (flattens the incentive), required-bingo-to-advance (turns a miss
into a wall), and the original's end-of-round spinner (pure token-era chrome).

## 6. What this kind of game is called, and its family tree

The umbrella term is a **word game**; the useful term is **anagram game** (or **word
scramble / word jumble**). The specific format we built — a fixed rack of letters, a list of
hidden words to find, a clock — is described in the trade as a **timed anagram word list** or
**word discovery** game, and informally as a **TextTwist-style** game, after the 2001
GameHouse title that defined it. Wikipedia's broader heading is **letter arrangement games**
(Scrabble, Upwords, Bananagrams, Countdown). Word Game Wiki's anagram category defines the
family as "letter-rearranging games where players build words from a limited set of letters",
and lists Text Twist under the alias "six-letter anagram game".

So if Jason wants to search for more of them, the words that work are: *anagram word game*,
*word scramble*, *TextTwist-style*, *six-letter anagram*. "Word Whomp-like" also works in
casual-games circles.

Five distinct mechanics get lumped together as "word games", and only the first is ours:

1. **Fixed rack, list of words** (ours): Word Whomp, TextTwist, Word Chomp, Wordshake,
   Pop-a-Word, Anagram Magic. All letters available at once, any subset spells a word.
2. **Grid trace**: Boggle, Wordament, Word Streak, Word Blitz, Word Grid. Letters must
   connect on a board, so words are constrained by adjacency, not just by the rack.
3. **Letter wheel into crossword slots**: Wordscapes, Word Cookies, Word Connect, Word
   Collect, Word Yard, Zen Word. Same anagram skill, but the crossword shape tells you word
   lengths and starting letters — much easier, and usually untimed.
4. **Falling / chaining tiles**: Bookworm, Bookworm Adventures, WordBrain, SpellTower,
   Letter Run. The board changes as you play, so order matters.
5. **Daily constraint puzzles**: Spelling Bee, Blossom, Strands, Letter Boxed, Jumble.
   One puzzle per day, one right answer, no clock.

The one worth noting for Mom: category 3 is where the enormous casual audience actually is
(Wordscapes alone is over 100 million installs, Word Connect and Word Cookies 50 million
plus each), and those are untimed, ad-supported and phone-first. If she already plays one of
those, the thing our game adds is the clock and the hunt for *every* word rather than the
easy crossword fit.

## 7. Sources

- Pogo game page — https://www.pogo.com/games/word-whomp
- BadgeHungry, original Word Whomp ranks/rules — https://www.badgehungry.com/game-ranks/word-whomp-ranks
- BadgeHungry, HD launch + clock-per-level comments — https://www.badgehungry.com/2018/09/13/now-available-word-whomp-hd
- BadgeHungry, HD ranks/tips — https://www.badgehungry.com/game-ranks/word-whomp-hd-ranks
- MobyGames, Word Whomp (2001) — https://www.mobygames.com/game/40113/word-whomp
- MobyGames, Word Whomp To Go (2004) — https://www.mobygames.com/game/40289/word-whomp-to-go
- pogofans how-to — https://pogofans.com/games/word-whomp-hd
- wordfinder guide (2:20 claim, otherwise accurate) — https://wordfinder.yourdictionary.com/blog/how-to-play-word-whomp-for-a-smashing-good-time/
- Word Chomp (open-source clone, full rules) — https://github.com/slayyyyer/word-chomp
- TextTwist rules — https://www.wordplays.com/wordgames/text-twist
- MobyGames, TextTwist 2 — https://www.mobygames.com/game/106845/texttwist-2
- Word Game Wiki, anagram category (taxonomy + cousins) — https://www.wordgamewiki.com/categories/anagram
- Word Game Wiki, Text Twist rules — https://www.wordgamewiki.com/games/text-twist/rules
- Wikipedia, word game (letter arrangement games) — https://en.wikipedia.org/wiki/Word_game
