// news-image-20261125 entry (Node 22, standard library only).
// The infographic is rendered ahead of time by render.py and shipped as
// entry.png beside this file; the program copies it to /output/entry.png.
// It runs offline: no network, no dependencies.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
const dest = join(outDir, 'entry.png');

// The grader hands us a fresh writable /output, but creating the directory
// when it is missing also makes the local check work without a mkdir step.
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
if (!existsSync(dest)) {
  throw new Error(`failed to write ${dest}`);
}
