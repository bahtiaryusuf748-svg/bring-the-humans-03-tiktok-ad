#!/usr/bin/env python3
"""Synthesized 120 BPM electronic bed for the bring-the-humans-03 TikTok ad.
30 seconds, mono 44.1kHz WAV. Kick on every beat, clap on 2 & 4, hats on
8ths, bass roots Am-F-C-G, quiet pentatonic pluck arp. No samples, no
third-party audio: everything synthesized here with numpy."""
import os
import numpy as np
import wave

SR = 44100
DUR = 30.0
BPM = 120
BEAT = 60.0 / BPM
n = int(SR * DUR)
y = np.zeros(n)
rng = np.random.default_rng(11)

# Kick on every beat: sine pitch drop 160 -> 46 Hz.
for b in range(int(DUR / BEAT) + 1):
    s = int(b * BEAT * SR)
    L = int(0.24 * SR)
    if s + L > n:
        L = n - s
    tt = np.arange(L) / SR
    f = 160 * np.exp(-tt * 16) + 46
    ph = 2 * np.pi * np.cumsum(f) / SR
    y[s:s + L] += np.sin(ph) * np.exp(-tt * 20) * 0.85

# Clap on beats 2 and 4 of each 2-second bar.
for bar in range(15):
    s = int((bar * 2 + 1.0) * SR)
    L = int(0.12 * SR)
    if s + L > n:
        continue
    y[s:s + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 40) * 0.30

# Hats on 8ths.
for h in range(int(DUR / (BEAT / 2)) + 1):
    s = int(h * (BEAT / 2) * SR)
    L = int(0.04 * SR)
    if s + L > n:
        continue
    y[s:s + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 220) * 0.12

# Bass: roots Am F C G, root on 8ths 1-2, fifth on 8ths 3-4.
roots = [55.0, 43.65, 65.41, 49.0]
for bar in range(15):
    f0 = roots[bar % 4]
    for e in range(4):
        f = f0 * (1.0 if e % 2 == 0 else 1.5)
        s = int((bar * 2 + e * 0.5) * SR)
        L = int(0.42 * SR)
        if s + L > n:
            continue
        tt = np.arange(L) / SR
        w = (np.sin(2 * np.pi * f * tt)
             + 0.4 * np.sin(2 * np.pi * 2 * f * tt)
             + 0.2 * np.sin(2 * np.pi * 3 * f * tt))
        y[s:s + L] += w * np.exp(-tt * 6) * 0.22

# Quiet pentatonic pluck arp on 16ths.
notes = [440.0, 523.25, 587.33, 659.25, 783.99, 880.0]
for i in range(int(DUR / 0.25)):
    f = notes[(i * 2 + (i // 8)) % len(notes)]
    s = int(i * 0.25 * SR)
    L = int(0.20 * SR)
    if s + L > n:
        continue
    tt = np.arange(L) / SR
    y[s:s + L] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 18) * 0.10

# Fade out over the last 1.5 s.
fade = np.ones(n)
fl = int(1.5 * SR)
fade[-fl:] = np.linspace(1, 0, fl)
y *= fade

peak = np.max(np.abs(y))
y = y / peak * 0.5

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music.wav')
with wave.open(out, 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((y * 32767).astype(np.int16).tobytes())
print('wrote', out, 'peak', round(float(peak), 3))
