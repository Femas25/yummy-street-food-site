/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Charte graphique Yummy v2 — logo "sticker" + remorque vert émeraude
        primary: {
          DEFAULT: '#0C7C5E', // Vert émeraude (remorque), légèrement foncé pour rester lisible en petit texte / boutons — à affiner sur photo lumière du jour
          dark: '#083E23', // Vert forêt (corps du logo) — header, footer, titres
        },
        lime: '#BED70B', // Vert citron ("Street Food" du logo) — accent pop, CTA, surbrillances
        leaf: '#5FB98A', // Vert feuille moyen — décor, feuilles flottantes
        mint: '#E4EFE2', // Vert menthe très pâle — fonds et teintes douces
        cream: '#F8F6F2', // Blanc cassé
        anthracite: '#303030', // Texte courant
      },
      fontFamily: {
        // Police ronde et chaleureuse, dans l'esprit du lettrage "bulle" du logo Yummy,
        // tout en restant lisible et premium pour l'UI (inspirée d'Airbnb/Notion).
        heading: ['Fredoka', 'sans-serif'],
        body: ['Lato', 'Open Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
