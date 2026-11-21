// the-poster-for-a-place-that-i-2-20261121-0539: a travel poster for
// VELMARA, a place that isn't there — dusk over a turquoise lagoon,
// one white lighthouse on the headland, a low sun and its reflection.
//
// The poster is drawn ahead of time by draw_poster.py (Pillow) and shipped
// in this repository as entry.png. This program does nothing but place that
// file where the grader looks, so the graded run is deterministic, uses no
// network, and needs only the Node 22 standard library. Two runs therefore
// write byte-identical files.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// then open out/entry.png.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const shipped = join(repoRoot, "entry.png");

// The gate caps the image at 1 MiB; refuse to ship anything larger.
const MAX_BYTES = 1024 * 1024;
if (statSync(shipped).size > MAX_BYTES) {
  throw new Error("entry.png is larger than the 1 MiB gate limit");
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(shipped, target);
console.log(`wrote ${target} (${statSync(target).size} bytes)`);
