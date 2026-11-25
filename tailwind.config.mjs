/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Charte graphique Yummy v2 — logo "sticker" + remorque vert émeraude.
        // Refonte 2026-11 : vert profond #083E23 dominant, fond crème chaud, accent citron.
        primary: {
          DEFAULT: '#0C7C5E', // Vert émeraude (remorque) — liens et boutons secondaires (contraste 4,9:1 sur crème)
          dark: '#083E23', // Vert profond (corps du logo) — header, footer, titres, boutons principaux
        },
        lime: '#BED70B', // Vert citron ("Street Food" du logo) — accent : CTA sur fond vert, surbrillances (jamais en texte sur fond clair)
        leaf: '#5FB98A', // Vert feuille moyen — décor
        mint: '#E4EFE2', // Vert menthe très pâle — fonds doux, texte secondaire sur fond vert
        cream: '#FAF5EA', // Crème chaud — fond principal
        paper: '#FFFDF8', // Blanc chaud — cartes
        anthracite: '#303030', // Texte courant
        muted: '#55554F', // Texte secondaire (contraste ≥ 7:1 sur crème)
      },
      fontFamily: {
        // Fredoka (titres, lettrage rond dans l'esprit du logo) + Lato (texte courant).
        heading: ['Fredoka', 'sans-serif'],
        body: ['Lato', 'Open Sans', 'sans-serif'],
      },
      maxWidth: {
        prose: '62ch',
      },
    },
  },
  plugins: [],
};
