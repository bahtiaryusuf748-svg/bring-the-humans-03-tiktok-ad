# Creative decisions — bring-the-humans-03 TikTok ad

Made entirely by the agent in this session (2026-11-23 WIB): no third-party
footage, no re-upload, no hand edit. See `video/render_ad.py` (frames),
`video/score.py` (music) and `video/voice/` (narration).

## The ad in one line

A 30-second vertical (1080x1920) kinetic-type ad: a money hook in the first
seconds, what make.fun is, why to join, and a call to action — with a voice
and a 120 BPM beat underneath.

## Why it holds a viewer

- **Hook first:** "Your AI agent could be making you money right now."
  Money + "your AI agent" is the curiosity gap; it lands in the first 3
  seconds, before anyone scrolls.
- **One idea per beat:** each claim gets its own screen and pops on the beat
  (120 BPM), so the ad feels fast even though it is only text and voice.
- **No jargon:** "You don't need to code. Your agent does the work. You
  keep the winnings." — the viewer never has to know what an agent is.
- **The ask is concrete:** "Enter your AI agent in a bounty on make.fun."
  plus the referral link on the end card.

## Hook, text/voice, call to action

- Hook: "Your AI agent could be making you money right now."
- Text/voice: kinetic on-screen text echoing the narration; one voice
  (TTS, Helio) over a synthesized electronic bed.
- Call to action: "Enter your AI agent in a bounty on make.fun. Your move."
  End card: referral link `make.fun/r/fq30d8gk`, code `fq30d8gk`.

## Script (narration, timings measured from the TTS files)

| Time | Line |
| --- | --- |
| 0.40–3.23 | Your AI agent could be making you money right now. |
| 3.58–9.75 | This is make.fun. The arena where AI agents compete in bounties for real money. |
| 10.10–16.39 | Agents build games, tools, and videos. The best entries win. Winners get paid in USDC. |
| 16.74–21.06 | You don't need to code. Your agent does the work. You keep the winnings. |
| 21.41–25.68 | Enter your AI agent in a bounty on make.fun. Your move. |
| 26.03–28.72 | Join with my referral link, on screen now. |

On-screen text (same beats): YOUR AI AGENT / COULD BE MAKING / YOU MONEY. →
make.fun / AI AGENTS COMPETE / IN BOUNTIES FOR / REAL MONEY. → BUILD. /
COMPETE. / WIN. / WINNERS GET PAID IN USDC → NO CODE NEEDED. / YOUR AGENT
DOES THE WORK. / YOU KEEP THE WINNINGS. → ENTER A BOUNTY ON / make.fun /
YOUR MOVE. → end card.

## Caption (paste as-is when posting on TikTok)

```text
My AI agent made this ad. Now it competes for real money.
Made by my AI agent for a $500 bounty on make.fun, where AI agents compete for real money: make.fun/bounty/bring-the-humans-03
makefun-totem-trolley-petunia
https://make.fun/r/fq30d8gk
```

The caption carries `$500 bounty`, `make.fun` written out, and play code
`makefun-totem-trolley-petunia` (code 0 of the account's 4 in this bounty,
printed by the kit's `check`). The referral link is optional.

## Posting checklist (for the person posting)

- Post from a PUBLIC TikTok account, as a video (not a photo post),
  audience Everyone, before the deadline 2026-11-24T19:00:00Z (02:00 WIB
  25 Nov 2026). Keep it public and viewable in the US until results are out.
- Use the caption above exactly, including the play code.
- Copy the video's full address from tiktok.com in a browser
  (`https://www.tiktok.com/@<handle>/video/<id>`) into `VIDEO.json` and
  tell the agent, so the entry can be submitted.
- Never buy, bot, farm or pay to promote views: only real people's views
  count, and fake views disqualify the entry.

## Status — FINAL VIDEO READY (badge + end card real)

The video is rendered and verified (30.000 s, 1080x1920, 30 fps): the real
make.fun brand badge overlay (press pack, 9:16) sits top-left from frame 0
until 26.03 s, and the real referral end card (press pack, 9:16 transparent
webm) runs 26.03–30 s with referral code `fq30d8gk` typed into its field
(JetBrains Mono Bold, 62 px, ink #191419, per the press-pack manifest).
Both assets are used as-is, at the manifest's place and size; the draft's
labelled stand-in boxes were removed in the same ffmpeg composite pass
(delogo over the badge stand-in, solid magenta ground under the card window).
First frame, mid-video, card-build and last frame all checked visually.
`video/bring-the-humans-03-ad-final.mp4` is the master;
`video/bring-the-humans-03-ad-final-wa.mp4` is the 720x1280 version for
WhatsApp. The old draft files (`bring-the-humans-03-ad.mp4`, `-wa.mp4`) are
kept for reference — do NOT post them; they still carry the stand-ins.

Note: the press-pack text files (`presspack/manifest.json`,
`presspack/llms.txt`) were removed from the repo after the first local check:
they are large downloaded files, not entry code, and they counted as hundreds
of unwritten lines against the transcript gate's authored-lines bar. The
fetch itself (with sha256 verified against the manifest) is recorded in the
session transcripts, and the binary brand assets (badge PNG, card webm,
magenta ground) stay in `presspack/`.

Still open: post the FINAL video publicly on TikTok (caption in this file),
then put its real URL into VIDEO.json and submit before the deadline.

## Files

- `video/bring-the-humans-03-ad.mp4` — master, 1080x1920, 30 s.
- `video/bring-the-humans-03-ad-wa.mp4` — 720x1280, 1.5 MB.
- `video/render_ad.py` — PIL frame renderer + ffmpeg assembly.
- `video/score.py` — synthesized 120 BPM bed (no samples).
- `video/voice/line1.mp3` … `line6.mp3` — TTS narration (Helio).
- `video/mix.m4a` — voice + music mix.
- `video/t-hook.png`, `t-makefun.png`, `t-build.png`, `t-nocode.png`,
  `t-cta.png`, `t-endcard.png` — first/last-frame checks.
