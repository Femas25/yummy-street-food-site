# CLAUDE.md — Site vitrine Yummy (Food Truck)

Ce fichier donne à Claude Code le contexte nécessaire pour travailler efficacement sur ce projet. Il doit être tenu à jour au fur et à mesure des décisions prises.

## 1. Présentation du projet

**Yummy** est un food truck (entreprise en création). Ce dépôt contient le site vitrine de l'entreprise, destiné à présenter le concept, le menu, les emplacements/horaires du truck, et à permettre le contact et/ou la commande en ligne.

- **Public cible :** clients locaux, potentiels organisateurs d'événements (mariages, entreprises, festivals)
- **Langue du site :** français uniquement
- **Ton :** convivial, gourmand, chaleureux — cohérent avec l'univers street food

## 2. Stack technique

- **Framework :** [Astro](https://docs.astro.build/) (dernière version stable)
- **Styling :** Tailwind CSS — **confirmé** le 2026-08-07, via `@astrojs/tailwind`
- **Contenu :** données structurées en JSON dans `src/data/` (`planning.json`, `evenements.json`, `contact.json`) plutôt que des Content Collections — suffisant pour le volume de contenu d'un site vitrine de food truck, plus simple à maintenir pour l'utilisateur. Pas de `menu.json` : la page "Nos créations" est une galerie photo, pas une carte à prix fixes.
- **Déploiement :** non décidé — Netlify ou Vercel sont les options les plus simples pour un site Astro statique de ce type ; à trancher avant la mise en prod
- **Gestion de version :** Git *(dépôt pas encore initialisé)*
- **Commande en ligne / réservation :** **confirmé** le 2026-08-07 — formulaire de contact basique unique (pas de distinction commande à emporter / événement), sans backend. Prêt pour un service tiers type [Web3Forms](https://web3forms.com) ; clé d'accès à renseigner dans `src/components/ContactForm.astro` (`WEB3FORMS_ACCESS_KEY`)

> Claude Code : si une décision ci-dessus doit être prise pendant le développement (ex. choix définitif du styling ou de l'hébergeur), demande confirmation à l'utilisateur avant de t'engager dans une direction structurante.

## 3. Identité visuelle

Le logo et la charte graphique ont été **fournis par l'utilisateur** le 2026-08-07 (fichier `Charte_graphique_Yummy_v1.docx` + `logo final.png` + `projet final.png`), puis **remis à jour le 2026-08-31 (charte v2)** : nouveau logo « sticker » dessiné (`Yummy_Logo.pdf`) + photo de la remorque réelle peinte en vert émeraude. Les assets sont dans `src/assets/brand/` (`logo.png` = nouveau badge détouré transparent avec cerne blanche, fonctionne sur fond clair comme sur fond vert foncé ; `truck-hero.png` conservé mais plus utilisé, en attente d'une vraie photo de la remorque finie). Traduction en tokens Tailwind dans `tailwind.config.mjs`.

### Charte graphique — v2 (2026-08-31)

**ADN de la marque**
- Mission : proposer une street-food végétale locale élaborée à partir de légumes cultivés par la maraîchère.
- Valeurs : Local • Végétal • Circuit court • Gourmand • Authentique.
- Promesse : « La street-food cultivée par la maraîchère ». Le local et la fraîcheur sont les messages principaux.
- Slogan : « La street-food cultivée par la maraîchère. Végétal • Local • Gourmand. » (mis à jour le 2026-09-15 — remplace "Healthy", jugé moins pertinent qu'un mot français pour ce concept végétal)

**Couleurs** (tokens Tailwind correspondants entre parenthèses)
- Vert émeraude : `#0C7C5E` (`primary`) — couleur de la remorque, légèrement foncée vs la photo pour rester lisible en petit texte ; à réajuster sur une photo en lumière du jour
- Vert forêt : `#083E23` (`primary-dark`) — corps du logo ; header, footer, titres, texte sur fond clair
- Vert citron : `#BED70B` (`lime`) — accent pop : CTA « Commander », onglet actif, surbrillances
- Vert feuille : `#5FB98A` (`leaf`) — feuilles décoratives (`src/components/icons/Leaf.astro`)
- Vert menthe pâle : `#E4EFE2` (`mint`) — fonds et teintes douces (remplace l'ancien `beige`)
- Blanc cassé : `#F8F6F2` (`cream`)
- Anthracite : `#303030` (`anthracite`) — texte courant
- (l'ancien token `beige` a été supprimé)

**Typographies**
- Titres : Fredoka (`font-heading`) — lettrage rond « bulle », dans l'esprit du logo
- Texte courant : Lato (`font-body`)

**Style visuel :** Nature, inox, légumes frais, feuilles ; design moderne, coloré, avec du relief (ombres portées) et des animations douces (scroll-reveal, feuilles flottantes `.leaf-deco`).

**Supports :** Remorque, menus, cartes de visite, flyers, réseaux sociaux, vêtements.

**Logo :** `src/assets/brand/logo.png` — badge « sticker » : corps vert forêt, « Yummy » blanc, « Street Food » vert citron, feuille bicolore, cerne blanche de découpe. Utilisé tel quel sur fond clair et sur fond vert foncé.
- Conserver les proportions, ne pas déformer le logo
- Respecter une zone de protection autour du logo
- Ne plus faire figurer « Par la maraîchère » dans le logo (reste dans les textes/slogan)

## 4. Structure du site (pages principales)

**Mise à jour 2026-09-15** — nav simplifiée à 3 liens + 1 CTA : Accueil, Nos créations, Où nous trouver, et un bouton « Contact » mis en avant (remplace l'ancien CTA « Commander »). Calendrier a été fusionné dans Où nous trouver ; Commander a été supprimé et absorbé par Contact.

- **Accueil** — présentation du concept Yummy, mosaïque photo, appel à l'action (voir nos créations / localiser le truck / nous contacter), coordonnées en pied de page d'accueil
- **Nos créations** (route `/menu`) — galerie photo des recettes/créations du truck (pas de carte à prix fixes pour l'instant)
- **Galerie photos** (`/galerie`) — photos du potager/récoltes/truck, plus accessible depuis la nav principale, reliée depuis la section photo de l'accueil
- **Où nous trouver** — emplacements du truck selon les jours de la semaine (tableau + carte à venir) **et** calendrier des prochains événements publics déjà confirmés (fusionné le 2026-09-15, ex-page `/calendrier`)
- **Contact** — coordonnées, réseaux sociaux, présentation "sur mesure" pour l'événementiel privé, et formulaire de contact unique (commande à emporter et demandes d'événement confondues, avec un champ "type d'événement")

> Chaque page doit rester simple à maintenir : privilégier des données structurées (JSON/Markdown) plutôt que du contenu codé en dur, pour que l'utilisateur puisse mettre à jour le menu et le planning sans toucher au code.

## 5. Conventions de code

- Composants Astro dans `src/components/`, un composant = une responsabilité claire
- Layouts partagés dans `src/layouts/`
- Pages dans `src/pages/`
- Données de contenu (menu, emplacements, etc.) dans `src/content/` (Content Collections) ou `src/data/`
- Nommage des fichiers en `kebab-case`
- Privilégier les composants `.astro` statiques ; n'introduire du JS côté client (`client:*`) que si une interactivité réelle est nécessaire (ex. filtrage du menu, carte interactive)
- Images optimisées via `astro:assets`

## 6. Commandes utiles

```bash
npm install         # installer les dépendances
npm run dev          # lancer le serveur de dev
npm run build         # build de production
npm run preview        # prévisualiser le build de production
```

*(à ajuster si un gestionnaire de paquets différent est utilisé, ex. pnpm/yarn)*

## 7. Accessibilité & SEO

- Respecter la sémantique HTML (titres hiérarchisés, `alt` sur les images, contrastes suffisants)
- Renseigner les balises meta (titre, description, Open Graph) pour chaque page, utile pour le référencement local du food truck
- Site pensé mobile-first (le public consulte majoritairement le planning/menu depuis un téléphone)

## 8. Ce que Claude Code doit éviter

- Ne pas inventer de logo, de nom de plats, de prix ou de coordonnées définitives — utiliser des placeholders explicites (`[À compléter]`) tant que l'information n'a pas été fournie par l'utilisateur
- Ne pas figer un choix d'hébergeur ou de styling sans validation, ces points sont encore ouverts
- Ne pas ajouter de dépendances lourdes non nécessaires pour un site vitrine

## 9. Historique des décisions

*(à compléter au fil du projet)*

- `2026-08-07` — Choix du framework Astro confirmé. Langue du site : français. Pages prévues : Accueil, Menu, Galerie photos, Localisation & planning, Commande en ligne/réservation, Contact. Styling et hébergement restent à trancher.
- `2026-08-07` — Charte graphique et logo définitifs fournis (voir section 3). Tailwind CSS confirmé. Mécanisme de commande/réservation confirmé : formulaire de contact basique unique, sans backend (Web3Forms). Site initial généré : config Astro + Tailwind, layout/header/footer, 6 pages, données JSON structurées (menu, planning, contact) avec placeholders `[À compléter]` pour tout ce qui n'a pas été fourni (plats, prix, emplacements, coordonnées, photos manquantes). Hébergement toujours à trancher. Node.js n'est pas installé sur la machine de développement — `npm install` / `npm run dev` n'ont pas pu être exécutés ni vérifiés en local.
