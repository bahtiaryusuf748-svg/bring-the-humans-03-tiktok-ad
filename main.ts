// bring-the-humans-03 entry program (Node 22, standard library only).
//
// The entry is the video itself: an original short vertical ad for make.fun,
// made by the agent in this session and posted publicly on TikTok from a
// public account. This program hands VIDEO.json (the video's TikTok address)
// from the repository root to /output/VIDEO.json, where the gate reads it.
// Nothing this program writes about the video is scored.
//
// Before handing it over it checks that VIDEO.json parses and names a TikTok
// video address (tiktok.com/@<handle>/video/<id>, id digits only). A short
// share link, a photo post, or a placeholder is refused by the gate, so a bad
// address is reported here on stderr first; the file is still handed over so
// the gate can refuse it with its own message. A good address is canonicalised
// to the www host with no query or fragment.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// A TikTok video address, query string or fragment aside: the gate reads past
// those, but a canonical address is cleaner to hand in.
const TIKTOK_VIDEO_URL =
  /^https:\/\/(?:www\.|m\.)?tiktok\.com\/(@[^/?#]+)\/video\/(\d+)(?:[/?#].*)?$/;

const videoJsonPath = join(BOT_DIR, 'VIDEO.json');
let raw: string;
try {
  raw = readFileSync(videoJsonPath, 'utf8');
} catch (err) {
  console.error(`VIDEO.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

let videoUrl: unknown;
try {
  const parsed: unknown = JSON.parse(raw);
  if (typeof parsed !== 'object' || parsed === null || !('url' in parsed)) {
    throw new Error('VIDEO.json has no "url" field');
  }
  videoUrl = (parsed as { url: unknown }).url;
} catch (err) {
  console.error(`VIDEO.json could not be parsed: ${(err as Error).message}`);
  process.exit(1);
}

let outUrl: string;
if (typeof videoUrl === 'string') {
  const match = TIKTOK_VIDEO_URL.exec(videoUrl);
  if (match) {
    // Canonical form: www host, no query or fragment.
    outUrl = `https://www.tiktok.com/${match[1]}/video/${match[2]}`;
  } else {
    console.error(
      `WARNING: VIDEO.json "url" is not a TikTok video address (${videoUrl}); the gate will refuse it. ` +
        `Expected https://www.tiktok.com/@<handle>/video/<id>.`,
    );
    outUrl = videoUrl;
  }
} else {
  console.error('WARNING: VIDEO.json "url" is not a string; the gate will refuse it.');
  outUrl = String(videoUrl);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  writeFileSync(join(OUTPUT_DIR, 'VIDEO.json'), JSON.stringify({ url: outUrl }) + '\n');
  console.log(`VIDEO.json ready for ${outUrl}`);
} catch (err) {
  console.error(`VIDEO.json could not be written to ${OUTPUT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
