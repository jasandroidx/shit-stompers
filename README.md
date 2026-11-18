# Shit Stompers

A word game for Laura. Tap the letters to spell a word, stomp it, clear the
board before the clock runs out. Built to feel like PopCap's *Word Whomp*, with
its own dictionary, its own scoring, a swear jar, and a talking turd called
Crappy.

**The game is one file.** `index.html` — no server, no install, no internet
needed, no dependencies. Double-click it, or host it anywhere static
(GitHub Pages works out of the box).

## Play it right now

Open `index.html` in a browser. That's the whole game.

## Working on it

`index.html` is generated. Edit the source, then build:

```bash
python3 -m pip install pillow     # once
python3 build/build.py            # writes index.html
```

Check the build before committing — the game's JavaScript has to parse:

```bash
node -e 'const fs=require("fs");const h=fs.readFileSync("index.html","utf8");new Function(h.match(/<script>([\s\S]*)<\/script>/)[1].replace(/<\/script>/g,""));console.log("js parses")'
```

## What's in here

| Path | What it is |
|---|---|
| `index.html` | The game. Generated — do not edit by hand. |
| `src/game.html` | The source you actually edit: markup, CSS, all game logic. |
| `build/build.py` | Packs the source, word lists, art and audio into `index.html`. |
| `build/score_words.py` | Regenerates `data/word-levels.txt` from wordfreq (rarely needed). |
| `build/make_voice.py` | Optional: renders a synthetic voice with Kokoro. The shipped voice is Jason's own clips. |
| `data/dictionary.txt` | The word list. 31,522 words, one per line. |
| `data/common.txt` | The everyday words that get first pick of the board. |
| `data/freq-50k.txt` | Word frequency ranking, used to order the board. |
| `data/google20k.txt` | Common-word ordering, used the same way. |
| `data/word-levels.txt` | How obvious each word is, 0–15, baked in as one character per word. |
| `assets/porch-bg.png` | The porch behind everything. |
| `assets/sprites/` | Crappy's poses (plain, excited, sleepy), the gold crown, the pile, and the superhero fly-in strip for the title. |
| `fonts/` | Luckiest Guy (wordmark) and Fredoka (menu UI), both OFL — inlined by the build as base64 WOFF2. |
| `audio/` | Jason's voice clips plus `lines.txt` (what each one says). |
| `docs/` | Design notes: the Pogo study, the dictionary audit, parked ideas. |

## Rules the game actually plays by

- Three to six letters. Every word formed from the rack counts, not just the
  ones on the board — the off-board ones are "secret stinkers" and pay points.
- Skill level sets the clock and the board size: 2:30 / 12 words, 2:15 / 16,
  2:00 / 22.
- 20 points a letter at skill 1, 30 at 2, 40 at 3. The golden six-letter word
  pays +100. The 4th word and the last word each pay a pile bonus.
- **No word filtering.** Swear words are real words, they score, and they drop
  25¢ in the swear jar. `onSwearWord(word)` is the hook.

## Credits

- Word frequency: [wordfreq](https://github.com/rspeer/wordfreq) (Apache-2.0).
- Optional synthetic voice: [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache-2.0).
- The voice in `audio/` is Jason's own recordings.
- Character art, music and wording are original to this project. *Word Whomp*
  belongs to PopCap/EA; this is an homage, not a copy of their assets.
