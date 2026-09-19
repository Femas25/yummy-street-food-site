import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://yummy-streetfood.be',
  integrations: [tailwind()],
});
