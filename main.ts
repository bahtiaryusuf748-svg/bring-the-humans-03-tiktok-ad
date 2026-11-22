// bring-the-humans-03 entry program (Node 22, standard library only).
//
// The entry is the video itself: an original short vertical ad for make.fun,
// made by the agent in this session and posted publicly on TikTok from a
// public account. This program only copies VIDEO.json (the video's TikTok
// address) from the repository root to /output/VIDEO.json, where the gate
// reads it. Nothing this program writes about the video is scored.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, 'VIDEO.json'), join(OUTPUT_DIR, 'VIDEO.json'));
} catch (err) {
  console.error(`VIDEO.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
