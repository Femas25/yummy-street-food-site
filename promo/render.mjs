// Génère la vidéo promo « commande à emporter » (1080x1920, 30 i/s) à partir du vrai site.
// Prérequis : `npm run build` puis `npx astro preview --port 4321` dans un autre terminal,
// ffmpeg et Playwright (Chromium) installés. Usage : node promo/render.mjs
import { chromium } from 'playwright';
import { cpSync, mkdirSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const out = path.join(root, 'dist', 'promo');
mkdirSync(path.join(out, 'img'), { recursive: true });
cpSync(path.join(here, 'commande-a-emporter.html'), path.join(out, 'index.html'));
cpSync(path.join(root, 'src/assets/brand/logo.png'), path.join(out, 'img/logo.png'));
cpSync(path.join(root, 'src/assets/menu/pita-garni-sauce-blanche.jpg'), path.join(out, 'img/pita.jpg'));
cpSync(path.join(root, 'src/assets/menu/burger-betterave.jpg'), path.join(out, 'img/burger.jpg'));
cpSync(path.join(root, 'src/assets/gallery/potimarrons-herbe.jpg'), path.join(out, 'img/potage.jpg'));

const FPS = 30;
const frames = path.join(here, '.frames');
rmSync(frames, { recursive: true, force: true });
mkdirSync(frames);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
await page.goto('http://localhost:4321/promo/index.html');
await page.waitForFunction(() => window.DURATION);
const dur = await page.evaluate(() => window.DURATION);
const n = Math.round(dur * FPS);
for (let i = 0; i < n; i++) {
  await page.evaluate((t) => window.render(t), i / FPS);
  await page.screenshot({ path: path.join(frames, `f${String(i).padStart(4, '0')}.png`) });
}
await browser.close();

const mp4 = process.argv[2] || path.join(here, 'yummy-commande-a-emporter.mp4');
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(frames, 'f%04d.png'),
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'slow', '-movflags', '+faststart', mp4]);
rmSync(frames, { recursive: true, force: true });
console.log('Vidéo :', mp4, `(${n} images)`);
