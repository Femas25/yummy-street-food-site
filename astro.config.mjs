import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://yummy-streetfood.example', // [À compléter] remplacer par le nom de domaine définitif une fois l'hébergement choisi
  integrations: [tailwind()],
});
