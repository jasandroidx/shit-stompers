"""Renders Crappy's voice clips with Kokoro-82M (Apache-2.0) and pitches them up.

Setup (once):
    python3 -m pip install --target /tmp/ko kokoro-onnx soundfile
    curl -L -o /tmp/ko/kokoro-v1.0.onnx <model-files-v1.0 release>/kokoro-v1.0.onnx
    curl -L -o /tmp/ko/voices-v1.0.bin <model-files-v1.0 release>/voices-v1.0.bin

Run:
    PYTHONPATH=/tmp/ko python3 build/make_voice.py

Pitch: resampling by r raises pitch by 12*log2(r) semitones AND speeds the clip
up by r, so the model is rendered at 1/r to land back at natural speed.
"""
import os

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

MODEL = "/tmp/ko/kokoro-v1.0.onnx"
VOICES = "/tmp/ko/voices-v1.0.bin"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "voice-kokoro")   # scratch output; Jason's own clips live in audio/

# Measured from Jason's own Crappy clips (22 lines, 24 kHz): median fundamental
# 295 Hz, spectral centroid 1855 Hz. Kokoro at +3 gave 257 Hz and 2806 Hz — too
# low and far too bright — so the target here is his pitch with a softer top end.
SEMITONES = 5.4
R = 2 ** (SEMITONES / 12)
SPEED = 1.0 / R
TILT_CUTOFF = 2100.0                # Hz, above this the top end rolls off
TILT_STRENGTH = 0.88                # how much of the top to keep away

LINES = [
    ("greeting", "Well, hey there, Laura."),
    ("golden", "Ooh. Golden word."),
    ("rejected", "That is not a word, and you know it."),
    ("timeup", "Time's up, sweetheart."),
    ("theone", "Laura... I think you're the shit."),
    ("jar", "Another quarter in the swear jar."),
]

CAST = ["bf_emma", "af_heart"]


def tilt_down(x, sr):
    """Smooth high-shelf cut: takes the glassy edge off a pitched-up voice."""
    spec = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(len(x), 1.0 / sr)
    span = np.clip((freqs - TILT_CUTOFF) / max(sr / 2 - TILT_CUTOFF, 1.0), 0, 1)
    gain = 1.0 - TILT_STRENGTH * span ** 0.6
    return np.fft.irfft(spec * gain, len(x)).astype(np.float32)


def pitch_up(samples, factor, sr):
    x = np.asarray(samples, dtype=np.float32)
    x = tilt_down(x, sr)
    n = int(len(x) / factor)
    pos = np.linspace(0, len(x) - 1, n)
    y = np.interp(pos, np.arange(len(x)), x).astype(np.float32)
    peak = float(np.max(np.abs(y))) or 1.0
    return np.clip(y / peak * 0.92, -1.0, 1.0)


os.makedirs(OUT, exist_ok=True)
k = Kokoro(MODEL, VOICES)

for voice in CAST:
    for name, text in LINES:
        samples, sr = k.create(text, voice=voice, speed=SPEED, lang="en-us")
        out = pitch_up(samples, R, sr)
        path = os.path.join(OUT, f"{name}-{voice}.wav")
        sf.write(path, out, sr, subtype="PCM_16")
        print("%-26s %5.2fs  %4d KB" % (os.path.basename(path), len(out) / sr,
                                        os.path.getsize(path) / 1024))
print("done: %d files at +%.0f semitones" % (len(CAST) * len(LINES), SEMITONES))
