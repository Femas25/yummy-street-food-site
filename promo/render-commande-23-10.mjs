// Génère la vidéo promo du vendredi 23/10 (« On vous livre ! », à emporter ou à livrer,
// commandes par message privé Messenger ou par téléphone) : 1080x1920, 30 i/s.
// Prérequis : ffmpeg et Playwright (Chromium). Pas besoin du serveur Astro (page autonome).
// Usage : node promo/render-commande-23-10.mjs [sortie.mp4]
import { chromium } from 'playwright';
import { cpSync, mkdirSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const out = path.join(root, 'dist', 'promo-23-10');
mkdirSync(path.join(out, 'img'), { recursive: true });
cpSync(path.join(here, 'commande-23-10.html'), path.join(out, 'index.html'));
cpSync(path.join(root, 'src/assets/brand/logo.png'), path.join(out, 'img/logo.png'));
cpSync(path.join(root, 'src/assets/menu/pita-garni-sauce-blanche.jpg'), path.join(out, 'img/pita.jpg'));
cpSync(path.join(root, 'src/assets/menu/burger-betterave.jpg'), path.join(out, 'img/burger.jpg'));
cpSync(path.join(here, 'img/bowl.jpg'), path.join(out, 'img/bowl.jpg'));
cpSync(path.join(here, 'img/potage-cerfeuil.jpg'), path.join(out, 'img/potage-cerfeuil.jpg'));

const FPS = 30;
const frames = path.join(here, '.frames-23-10');
rmSync(frames, { recursive: true, force: true });
mkdirSync(frames);

const browser = await chromium.launch({ args: ['--lang=fr-BE'], env: { ...process.env, LANG: 'fr_BE.UTF-8' } });
const page = await browser.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2, locale: 'fr-BE' });
await page.goto(pathToFileURL(path.join(out, 'index.html')).href);
await page.waitForFunction(() => window.DURATION);
const dur = await page.evaluate(() => window.DURATION);
const n = Math.round(dur * FPS);
for (let i = 0; i < n; i++) {
  await page.evaluate((t) => window.render(t), i / FPS);
  await page.screenshot({ path: path.join(frames, `f${String(i).padStart(4, '0')}.png`) });
}
await browser.close();

const mp4 = process.argv[2] || path.join(here, 'yummy-commande-23-10.mp4');
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(frames, 'f%04d.png'),
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'slow', '-movflags', '+faststart', mp4]);
rmSync(frames, { recursive: true, force: true });
console.log('Vidéo :', mp4, `(${n} images)`);
