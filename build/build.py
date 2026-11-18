import base64, io, json, os, re
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # project root
SPRITES = os.path.join(ROOT, "assets", "sprites")
SRC = os.path.join(ROOT, "src", "game.html")
OUT = os.path.join(ROOT, "index.html")

def cutout(path, size):
    im = Image.open(path).convert("RGBA")
    # knock out the flat white studio background, keeping white inside the art
    for xy in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)]:
        ImageDraw.floodfill(im, xy, (0, 0, 0, 0), thresh=40)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    im.thumbnail((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def sprite(prefix, size):
    hits = [f for f in os.listdir(SPRITES) if f.startswith(prefix)]
    return cutout(os.path.join(SPRITES, hits[0]), size)

def jpeg_uri(path, width=1024, quality=78):
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def webp_uri(path):
    with open(path, "rb") as fh:
        return "data:image/webp;base64," + base64.b64encode(fh.read()).decode()

def word_line(name, path):
    """Rebuild one of the game's big const strings from a plain word list."""
    words = open(path, encoding="utf-8").read().split()
    return 'const %s = "' % name + " ".join(words) + '".split(" ");'

dict_line = word_line("DICT", os.path.join(ROOT, "data", "dictionary.txt"))
common_line = word_line("COMMON", os.path.join(ROOT, "data", "common.txt"))

# Word order by real-world frequency, used only to rank which words go on the
# board first and which six-letter word is the golden one.
freq_path = os.path.join(ROOT, "data", "freq-50k.txt")
if os.path.exists(freq_path):
    dict_words = set(re.search(r'"([^"]*)"', dict_line).group(1).split(" "))
    ordered = []
    with open(freq_path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= 50000:
                break
            w = line.split(" ")[0].strip()
            if w in dict_words:
                ordered.append(w)
    freq_line = 'const FREQ_ORDER = "' + " ".join(ordered) + '";'
    print("freq words:", len(ordered), round(len(freq_line) / 1024), "KB")
else:
    freq_line = 'const FREQ_ORDER = "";'
    print("WARNING: freq-50k.txt missing, board order falls back to length")

# Google's 20k common words, used to order the board the way a person would
# think of the words. Only entries that are in the dictionary are kept.
g_dict_words = set(re.search(r'"([^"]*)"', dict_line).group(1).split(" "))
google_path = os.path.join(ROOT, "data", "google20k.txt")
if os.path.exists(google_path):
    gorder = []
    with open(google_path, encoding="utf-8") as f:
        for line in f:
            w = line.strip().lower()
            if w in g_dict_words and w not in gorder:
                gorder.append(w)
    google_line = 'const GOOGLE_ORDER = "' + " ".join(gorder) + '";'
    print("google words:", len(gorder), round(len(google_line) / 1024), "KB")
else:
    google_line = 'const GOOGLE_ORDER = "";'

# How obvious each word is, 0-15, one character per DICT entry (chr(33 + level)).
# Produced by pack/score_words.py from wordfreq; omitted harmlessly if missing.
levels_path = os.path.join(ROOT, "data", "word-levels.txt")
levels = {}
if os.path.exists(levels_path):
    for line in open(levels_path, encoding="utf-8"):
        bits = line.split()
        if len(bits) == 2:
            levels[bits[0]] = int(bits[1])
if levels:
    words = re.search(r'"([^"]*)"', dict_line).group(1).split(" ")
    packed = "".join(chr(33 + levels.get(w, 0)) for w in words)
    levels_line = 'const WORD_LEVELS = "' + packed + '";'
    print("word levels:", len(words), round(len(levels_line) / 1024), "KB")
else:
    levels_line = 'const WORD_LEVELS = "";'
    print("WARNING: word-levels.txt missing, board order falls back to word lists")

def voice_uris():
    """Jason's own voice clips, baked in so the game stays one file."""
    d = os.path.join(ROOT, "audio")
    out = {}
    if not os.path.isdir(d):
        print("WARNING: audio/ missing, voice disabled")
        return out
    for f in sorted(os.listdir(d)):
        if f.lower().endswith(".mp3"):
            name = f.lower()
            if name.startswith("poop-"):
                name = name[5:]
            name = name[:-4]
            with open(os.path.join(d, f), "rb") as fh:
                out[name] = "data:audio/mpeg;base64," + base64.b64encode(fh.read()).decode()
    return out

def font_css():
    """Title/menu type from fonts/, base64'd so the game stays one file.

    Luckiest Guy is the wordmark, Fredoka is the menu UI. Both OFL, so embedding
    is fine. Missing files just warn — the CSS falls back to Arial Black.
    """
    faces = [
        ("Luckiest Guy", "luckiest-guy-latin.woff2", "400"),
        ("Fredoka", "fredoka-latin.woff2", "300 700"),
    ]
    out = []
    for family, fn, weight in faces:
        path = os.path.join(ROOT, "fonts", fn)
        if not os.path.exists(path):
            print("WARNING: fonts/%s missing, using fallback" % fn)
            continue
        with open(path, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        out.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%s;"
            "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}"
            % (family, weight, b64)
        )
    print("fonts:", len(out), "faces,", round(sum(len(f) for f in out) / 1024), "KB")
    return "".join(out)

tpl = open(SRC, encoding="utf-8").read()

art = {
    "__ART_PLAIN__": sprite("media-generation-crappy-tile-plain-0-", 200),
    "__ART_EXCITED__": sprite("media-generation-crappy-tile-excited-0-", 200),
    "__ART_SLEEPY__": sprite("media-generation-crappy-tile-sleepy-0-", 200),
    "__ART_CROWN__": sprite("media-generation-crappy-gold-crown-0-", 240),
    "__ART_PILE__": cutout(os.path.join(SPRITES, "poop-pile.png"), 170),
    "__ART_BG__": jpeg_uri(os.path.join(ROOT, "assets", "porch-bg.png")),
    "__ART_HERO__": webp_uri(os.path.join(SPRITES, "crappy-superhero-strip.webp")),
}

out = tpl.replace("/*__DICT_DATA__*/", common_line + "\n" + dict_line + "\n" + freq_line + "\n" + google_line + "\n" + levels_line)
for k, v in art.items():
    out = out.replace(k, v)

voice = voice_uris()
assert "__VOICE__" in out, "voice placeholder missing"
out = out.replace("__VOICE__", json.dumps(voice))
assert "__FONT_CSS__" in out, "font placeholder missing"
out = out.replace("/*__FONT_CSS__*/", font_css())

leftover = re.findall(r"__ART_[A-Z]+__", out)
assert not leftover, leftover
assert "const COMMON = " in out and "const DICT = " in out and ".split(\" \");" in out

open(OUT, "w").write(out)
print("wrote", OUT, round(len(out) / 1024), "KB")
for k, v in art.items():
    print(k, round(len(v) / 1024), "KB")
print("voice", len(voice), "clips,", round(sum(len(v) for v in voice.values()) / 1024), "KB")
