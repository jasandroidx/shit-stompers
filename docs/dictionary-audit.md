# Dictionary audit — Shit Stompers

Date: 2026-11-18
Game audited: `files/shit-stompers.html` (built 1129 KB from `pack/v2-src.html`)
Tools: `pack/dict_audit.js`, plus throwaway replay scripts that re-implement the game's
rack and board logic and compare it against an independent implementation.
Nothing in this document is a guess: every number comes from a run.

## What was checked

Two different failures matter, and they are opposite:

1. **A word she types is rejected** even though it is a real word. Annoying, feels broken.
2. **A word on the board is not a real word to a normal person** (ESS, ARS, ATS). Worse —
   the round cannot be won.

## Integrity (400 racks, then 800)

| Check | Result |
|---|---|
| Dictionary size | 31,522 words, all unique |
| Characters | 100% plain a–z, no apostrophes, no capitals |
| Lengths | 3 letters: 1,087 · 4: 4,250 · 5: 9,478 · 6: 16,707 |
| Board-word pool (`COMMON`) | 6,439 words, every one present in the dictionary |
| Game's letter-mask lookup vs independent multiset enumeration | 0 mismatches over 800 racks |
| Board words that can't be spelled from the rack | 0 |
| Board words rejected on submit | 0 |
| Boards shorter than the skill-level target | 0 (exactly 12 / 16 / 22) |
| Boards whose longest word isn't six letters | 0 |
| Crude words merged into the dictionary for swear coverage | 150, every one spellable from a six-letter rack |

Rack pool size after the fix: min 24, median 34–35, max 74. Generation never fell through
to the emergency rack in 2,300 attempts.

## Profanity: nothing is filtered, and the vocabulary is complete

The base word list already accepted 137 of 156 rude words and phrases tested. The 19 it
missed were mostly plurals and derivatives of words it did have (`cunts` but not `cunts` was
missing while `cunt` was present; `queefs`, `minges`, `poofs`, `quims`, `cunty`, `cacks`,
`crapper`, `pooper`, `numpty`, `lesbo` and a few others). All 150 playable ones (3–6 letters)
are now merged into the dictionary in the game itself, before any lookup table is built, so
they are scored like any other word and can turn up as bonus words on any rack that spells
them. Seven-letter entries were dropped from the list because a six-letter rack can never
spell them.

Nothing was removed and nothing is blocked. The hook list and the accepted list now come from
one source: 118 genuinely rude words flash `onSwearWord`'s bonus, and 38 tame ones (`idiot`,
`dork`, `screw`, `suck`) are accepted silently so the joke doesn't wear out. Of the words that
can also be *required* board words, 42 are rude ones that are common enough to appear on a
board, and in 600 sampled racks the golden six-letter word was itself a swear word 7 times.

Slurs were deliberately left alone: 12 of 20 tested are not in the base dictionary and I did
not add them, since that is a different decision from "swear words are fine". Say the word and
it is a one-line change.

## Failure 1 — real words rejected: essentially clean

Against the top 25,000 English words by real-world frequency, 11,439 are 3–6 letters and
2,936 of those are not in the dictionary. Reading them, they are not gaps:

- contractions with the apostrophe stripped: `didn doesn isn wasn wouldn couldn`
- names and places: `jesus george david york london sarah kevin`
- abbreviations: `fbi dna cia mri gps bbc nypd`
- brand names: `wifi uber iphone pepsi skype`
- slang spellings: `goin nothin talkin fuckin wanna gonna`

A word game should reject all of those. Every modern word that *is* a word is accepted:
`email online okay app selfie vegan emoji meme covid corona zoom blog podcast` — checked
individually. British spellings that fit six letters are accepted too (`colour grey centre
metre litre cheque learnt whilst maths telly`). The long ones people suggested
(`favourite`, `neighbour`, `programme`, `biscuit`, `gardens`) are 7+ letters and can never be
spelled from a six-letter rack, so their absence is irrelevant.

Conclusion: no additions needed. The only genuinely missing items are brands and newly coined
words, which do not belong in a word game.

## Failure 2 — junk on the board: found and fixed

Before the fix, 8.8% of Skill 3 boards contained at least one word outside the frequency
list (mean 0.2 words, worst 4): `ers ars als cis hist cote ats ess cert bis moc alt eds eds
serif eco emo bas soma mis mips imp rove ack bal kart bos ors res tort tote lac gis mos peso
att kos eau`. Several of those are not words at all outside a Scrabble board, and a player
cannot win a round that requires them.

Fix, in two places in `pack/v2-src.html`:

- `boardWordsForLevel()` now draws the board only from words the frequency list knows; a rack
  with fewer familiar words asks for fewer words instead of asking for nonsense.
- `generateRack()` now requires 24 *familiar* laid-out words, so the 22-word Skill 3 board is
  still always full.

Everything that is no longer on the board is still accepted as a bonus word — junk included.
Nothing was removed from the dictionary.

After the fix, over 800 racks and 40,000 board words: **0 obscure words on any board**, sizes
still exactly 12 / 16 / 22, gold word six letters every time.

Board quality now: 0.72% of board words rank worse than 12,000th in English, and the worst of
them are still real words (`liners patios tonics barges lodges tweaks`). Sample boards:

```
RAWSNP   pan ran raw san saw war was snap warn wars wrap prawns
STICHE   his hit ice its set she sit the tie shit this ethics
WREOLS   low owe row lose role rose slow wore loser lower worse slower
AERDNG   age and are end ran red dare dear near read grand danger
AETMNH   eat man men met the mean name team than them then anthem
```

(`shit` on a board is intended — no filtering, ever.)

## Known limits

- Familiarity is measured by one frequency list (subtitle corpus). That is why the fixed
  teaching rack still offers `sen` and `sis`; both are real words in the list, neither is
  wrong, `sen` is just obscure. A second list would fix that if it ever matters.
- Gold words come from the same list, so an occasional surname can be gold (`marcel`).
- Skill 3 on the fixed first rack asks for 17 words, not 22, because that teaching rack only
  has 17 familiar words in it. Generated racks are always 22.

## Re-running

```
node pack/dict_audit.js 400      # integrity, coverage, swear-word reachability
node pack/balance_stats.js 1500  # pool and board sizes, gold familiarity
python3 pack/build_v2.py         # rebuild files/shit-stompers.html from v2-src.html
```
