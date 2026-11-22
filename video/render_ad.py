#!/usr/bin/env python3
"""Render the bring-the-humans-03 TikTok ad: 1080x1920, 30 fps, 30.0 s.
Fully agent-made in this session: PIL kinetic typography over an animated
gradient, TTS voice lines (video/voice/lineN.mp3) and a synthesized score
(video/music.wav). Frames are piped raw to ffmpeg, which muxes the mixed
audio (video/mix.m4a, built before this runs).

STAND-IN placeholders (see CREATIVE.md): the make.fun brand badge that must
sit at the top from the first frame, and the referral end card in the last
4 seconds, come from make.fun's press pack as PNGs. They are drawn here as
clearly-marked boxes so the layout is exact; once the two PNGs are supplied,
a short ffmpeg overlay pass replaces the boxes with the real assets, used
as they are, at the same place and size.

On-screen text writes the name "make.fun" in plain lowercase type only.
No make.fun logo is redrawn here.
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
FPS = 30
DUR = 30.0
NFRAMES = int(DUR * FPS)
MASTER = os.path.join(BASE, 'bring-the-humans-03-ad.mp4')
MIX = os.path.join(BASE, 'mix.m4a')

WHITE = (255, 255, 255, 255)
CREAM = (255, 244, 214, 255)
YELLOW = (255, 214, 0, 255)
INK = (16, 8, 32, 255)
GRAD = [(18, 8, 43), (91, 27, 138), (224, 36, 92), (255, 179, 71)]
STOPS = np.array([0.0, 0.38, 0.72, 1.0])
COLS = np.array(GRAD, dtype=float)

# Voice line start times (seconds), measured from the TTS files.
LINE_STARTS = [0.40, 3.58, 10.10, 16.74, 21.41, 26.03]

# Scenes: (t0, t1, [ (segments, size, pop_offset) ... ])
# segments = list of (text, color); lines are centered as a vertical block.
SCENES = [
    (0.00, 3.58, [
        ([("YOUR AI AGENT", WHITE)], 118, 0.00),
        ([("COULD BE MAKING", WHITE)], 118, 0.50),
        ([("YOU ", WHITE), ("MONEY.", YELLOW)], 118, 1.00),
    ]),
    (3.58, 10.10, [
        ([("make.fun", WHITE)], 210, 0.00),
        ([("AI AGENTS COMPETE", WHITE)], 96, 0.55),
        ([("IN BOUNTIES FOR", WHITE)], 96, 1.05),
        ([("REAL MONEY.", YELLOW)], 96, 1.55),
    ]),
    (10.10, 16.74, [
        ([("BUILD.", WHITE)], 150, 0.00),
        ([("COMPETE.", WHITE)], 150, 0.70),
        ([("WIN.", YELLOW)], 190, 1.40),
        ([("WINNERS GET PAID IN USDC", CREAM)], 62, 2.30),
    ]),
    (16.74, 21.41, [
        ([("NO CODE NEEDED.", WHITE)], 118, 0.00),
        ([("YOUR AGENT DOES", WHITE)], 92, 0.70),
        ([("THE WORK.", WHITE)], 92, 1.15),
        ([("YOU KEEP THE WINNINGS.", YELLOW)], 84, 1.90),
    ]),
    (21.41, 26.03, [
        ([("ENTER A BOUNTY ON", WHITE)], 100, 0.00),
        ([("make.fun", WHITE)], 210, 0.55),
        ([("YOUR MOVE.", YELLOW)], 120, 1.45),
    ]),
]

CIRCLES = [
    (0.22, 0.16, 150, (255, 179, 71), 0.9, 0.05),
    (0.80, 0.28, 190, (224, 36, 92), 0.7, 0.04),
    (0.15, 0.60, 210, (91, 27, 138), 0.8, 0.06),
    (0.85, 0.70, 160, (255, 214, 0), 0.6, 0.05),
    (0.50, 0.88, 230, (224, 36, 92), 0.7, 0.045),
    (0.35, 0.42, 110, (255, 255, 255), 0.5, 0.07),
]


def load_font(size):
    for path in (
        '/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf',
        '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    ):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def ease_out_back(x):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def fit_font(segments, size, max_w=960):
    """Shrink font until the joined line fits max_w."""
    while size > 30:
        fnt = load_font(size)
        w = 0
        probe = Image.new('RGB', (8, 8))
        d = ImageDraw.Draw(probe)
        for text, _ in segments:
            w += d.textlength(text, font=fnt)
        if w <= max_w:
            return fnt, size
        size -= 6
    return load_font(size), size


def render_line(segments, size):
    """Render one line to an RGBA image, with a soft dark shadow."""
    fnt, _ = fit_font(segments, size)
    probe = Image.new('RGB', (8, 8))
    d = ImageDraw.Draw(probe)
    widths = [d.textlength(t, font=fnt) for t, _ in segments]
    total_w = int(sum(widths)) + 12
    asc, desc = fnt.getmetrics()
    line_h = asc + desc
    img = Image.new('RGBA', (total_w, line_h + 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 6
    for (text, color), w in zip(segments, widths):
        d.text((x + 4, 8), text, font=fnt, fill=(0, 0, 0, 170))
        d.text((x, 4), text, font=fnt, fill=color)
        x += int(w)
    return img


def pop_transform(img, t, pop_start, dur=0.18):
    """Return (image, alpha) for a pop-in at pop_start; (None, 0) if not yet."""
    if t < pop_start:
        return None, 0.0
    p = (t - pop_start) / dur
    if p >= 1:
        return img, 1.0
    scale = ease_out_back(min(p * 1.15, 1.0))
    scale = max(0.6, min(scale, 1.12))
    nw, nh = max(2, int(img.width * scale)), max(2, int(img.height * scale))
    return img.resize((nw, nh), Image.LANCZOS), p


# Precompute the vertical gradient as a (H, 3) array.
_yy = np.linspace(0, 1, H)
_grad = np.zeros((H, 3))
for ch in range(3):
    _grad[:, ch] = np.interp(_yy, STOPS, COLS[:, ch])
_xx = np.linspace(-1, 1, W)[None, :]
_vig = 1 - 0.16 * (_xx ** 2 + (_yy[:, None] - 0.5) ** 2 * 1.4)
_vig = np.clip(_vig, 0.72, 1.0)


def frame(t, fi):
    # Background: gradient, slowly drifting vertically (re-interpolated
    # per frame with clipping, so no wrap-around), with vignette.
    pos = np.clip(_yy + 0.06 * math.sin(t * 0.32), 0, 1)
    g = np.zeros((H, 3))
    for ch in range(3):
        g[:, ch] = np.interp(pos, STOPS, COLS[:, ch])
    arr = np.repeat(g[:, None, :], W, axis=1) * _vig[:, :, None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    # Drifting translucent circles (bokeh).
    for fx, fy, r, col, spd, ph in CIRCLES:
        cx = int(W * fx + 46 * math.sin(t * spd + ph * 9))
        cy = int(H * fy + 36 * math.cos(t * spd * 0.8 + ph * 7))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (26,))

    # Brand-badge STAND-IN: top center, from frame 0 until the end card.
    if t < 26.03:
        d.rounded_rectangle([170, 62, 910, 168], radius=22,
                            outline=(255, 255, 255, 220), width=3,
                            fill=(0, 0, 0, 90))
        bf = load_font(38)
        d.text((540, 78), "make.fun BRAND BADGE", font=bf, fill=WHITE, anchor='ma')
        sf = load_font(28)
        d.text((540, 126), "press pack — to be composited", font=sf,
               fill=(255, 255, 255, 200), anchor='ma')

    # End card STAND-IN: last 4 seconds.
    if t >= 26.03:
        ct = t - 26.03
        a = min(1.0, ct / 0.25)
        card_a = int(235 * a)
        d.rounded_rectangle([70, 620, 1010, 1420], radius=48,
                            fill=(12, 6, 28, card_a),
                            outline=(255, 255, 255, int(200 * a)), width=4)
        ef = load_font(150)
        d.text((540, 690), "make.fun", font=ef, fill=WHITE, anchor='ma')
        cf = load_font(58)
        d.text((540, 900), "JOIN WITH MY", font=cf, fill=CREAM, anchor='ma')
        d.text((540, 970), "REFERRAL LINK", font=cf, fill=CREAM, anchor='ma')
        yf = load_font(64)
        d.text((540, 1090), "make.fun/r/fq30d8gk", font=yf, fill=YELLOW, anchor='ma')
        pf = load_font(44)
        d.text((540, 1190), "CODE  fq30d8gk", font=pf, fill=WHITE, anchor='ma')
        nf = load_font(28)
        d.text((540, 1330), "[STAND-IN — press-pack end card to be composited]",
               font=nf, fill=(255, 255, 255, 170), anchor='ma')

    # Kinetic-type scenes.
    for (t0, t1, lines) in SCENES:
        if not (t0 <= t < t1):
            continue
        rendered = []
        total_h = 0
        for segments, size, off in lines:
            limg = render_line(segments, size)
            rendered.append((limg, t0 + off))
            total_h += limg.height + 26
        total_h -= 26
        y = int(H * 0.44 - total_h / 2)
        fade = 1.0
        if t > t1 - 0.25:
            fade = max(0.0, (t1 - t) / 0.25)
        for limg, pop_start in rendered:
            pimg, alpha = pop_transform(limg, t, pop_start)
            if pimg is None:
                y += limg.height + 26
                continue
            a = alpha * fade
            if a <= 0:
                y += limg.height + 26
                continue
            if a < 1.0:
                r, g2, b2, al = pimg.split()
                al = al.point(lambda v: int(v * a))
                pimg = Image.merge('RGBA', (r, g2, b2, al))
            ov.alpha_composite(pimg, (int(W / 2 - pimg.width / 2), y))
            y += limg.height + 26

    # Progress bar at the very bottom.
    frac = t / DUR
    d.rectangle([0, H - 14, int(W * frac), H], fill=(255, 214, 0, 255))

    out = Image.alpha_composite(img, ov).convert('RGB')
    return out


def main():
    if not os.path.exists(MIX):
        print('missing mixed audio:', MIX, file=sys.stderr)
        print('run the ffmpeg audio mix first', file=sys.stderr)
        sys.exit(1)
    cmd = [
        'ffmpeg', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
        '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-i', MIX,
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20',
        '-preset', 'medium', '-c:a', 'aac', '-b:a', '128k',
        '-movflags', '+faststart', '-shortest', MASTER,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tests = {15: 't-hook.png', 150: 't-makefun.png', 360: 't-build.png',
             660: 't-nocode.png', 780: 't-cta.png', 870: 't-endcard.png'}
    for fi in range(NFRAMES):
        t = fi / FPS
        img = frame(t, fi)
        if fi in tests:
            img.save(os.path.join(BASE, tests[fi]))
        proc.stdin.write(img.tobytes())
        if fi % 150 == 0:
            print(f'frame {fi}/{NFRAMES} t={t:.1f}s', flush=True)
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        print('ffmpeg failed with code', rc, file=sys.stderr)
        sys.exit(1)
    print('wrote', MASTER)


if __name__ == '__main__':
    main()
