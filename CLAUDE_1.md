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
- Mission : proposer une street-food végétale locale élaborée à partir des légumes de saison de notre potager, avec des produits bio et locaux autant que possible.
- Valeurs : Local • Végétal • Circuit court • Gourmand • Authentique.
- Promesse : food truck local, végétal, gourmand. Le local, les légumes de saison du potager et la fraîcheur sont les messages principaux.
- Slogan : « Food truck — Local • Végétal • Gourmand. » (mis à jour le 2026-10-13 : l'ancienne promesse « La street-food cultivée par la maraîchère » est abandonnée et ne doit plus apparaître nulle part ; parler plutôt des légumes de saison de notre potager et de produits bio autant que possible.)

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
- Ne plus faire figurer « Par la maraîchère » dans le logo ni dans les textes

## 4. Structure du site (pages principales)

**Mise à jour 2026-09-15** — nav simplifiée à 3 liens + 1 CTA : Accueil, Nos créations, Où nous trouver, et un bouton « Contact » mis en avant (remplace l'ancien CTA « Commander »). Calendrier a été fusionné dans Où nous trouver ; Commander a été supprimé et absorbé par Contact.

- **Accueil** — présentation du concept Yummy, mosaïque photo, appel à l'action (voir nos créations / localiser le truck / nous contacter), coordonnées en pied de page d'accueil
- **Nos créations** (route `/menu`) — galerie photo des recettes/créations du truck (pas de carte à prix fixes pour l'instant)
- **Galerie photos** (`/galerie`) — photos du potager/récoltes/truck, plus accessible depuis la nav principale, reliée depuis la section photo de l'accueil
- **Où nous trouver** — emplacements du truck selon les jours de la semaine (tableau + carte à venir) **et** calendrier des prochains événements publics déjà confirmés (fusionné le 2026-09-15, ex-page `/calendrier`)
- **Événements privés** (`/evenements-prives`, ajouté le 2026-10-13) — page de conversion pour l'événementiel privé : occasions, formules (seul prix connu : 5 starters à 3 € pièce, le reste « sur devis »), formulaire de devis détaillé (`EventQuoteForm.astro`, avec suivi de la source `?src=`). Liée dans la nav, le footer et la page Contact. Plaquette PDF associée : `public/plaquette-evenements-yummy.pdf`.
- **Contact** — coordonnées, réseaux sociaux, présentation "sur mesure" pour l'événementiel privé, et formulaire de contact unique (avec un champ "type d'événement")
- **Commande à livrer** (ajouté le 2026-10-18) — module intégré au formulaire de contact : choix « Commande à livrer » → quantités (Pita, Burger, Potage, Loumonade cola, Loumonade pomme-cerise), adresse, heure ; message « Demande bien prise en compte ! Nous vous recontacterons pour valider la commande. ». Bandeau vert citron sous le header (`OrderBanner.astro`). **N'apparaît QUE les jours listés dans `src/data/commande.json` → `jours`** (heure belge, s'éteint seul le lendemain) ; n'ajouter un jour que sur demande explicite de l'utilisateur. `?commande=test` force l'affichage pour tester. Vidéo promo associée dans `promo/` (`node promo/render.mjs`). Depuis le 2026-10-22 : choix obligatoire « À emporter (retrait) » / « À livrer » (adresse obligatoire seulement pour la livraison), heure souhaitée limitée aux `creneaux` de `commande.json`, `lieuRetrait` vide = « lieu de retrait confirmé lors de notre appel », mention « Aussi par téléphone, Messenger et Instagram ».

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
- `2026-10-13` — Outil de prospection événements privés : page `/evenements-prives` + 4e lien de nav, plaquette PDF, dossier `prospection/` (liste de prospects réels, générateur du classeur CRM, script d'extraction de contacts publics). Google Sheet « Yummy — Prospection événements privés » créé sur le Drive. Brouillons Gmail préparés pour les prospects avec e-mail (jamais d'envoi automatique). Prix des plats, boissons, déplacement et minimum de prestation encore à fixer par l'utilisateur.
- `2026-10-18` — Statistiques anonymes du site (`src/components/Statistiques.astro`, chargé dans `Layout.astro`) : pages vues, clics sur les liens, formulaires envoyés (contact/commande/devis), source `?src=` / `utm_source` (QR code de la plaquette = `?src=plaquette`), site d'origine, type d'appareil. Stockées dans le projet Supabase **yummy-statistiques** (Paris), table `evenements_site` : la clé publique ne peut qu'ajouter des lignes. Pas de cookie, d'IP, d'identifiant ni de stockage sur l'appareil (nouvelle visite déduite du référent) ; base légale : intérêt légitime, opposition via le lien `/?stats=off` de la politique de confidentialité ; purge automatique après 25 mois (pg_cron). Actif uniquement sur `yummy-streetfood.be` ; `?stats=off` exclut les visites du propriétaire sur son appareil (`?stats=on` pour réactiver). Politique de confidentialité mise à jour. Pour chaque nouveau QR code ou lien de campagne, utiliser un `?src=` distinct.
- `2026-10-18` — Page « Où nous trouver » : la liste « Nos prochains événements » et les données schema.org ne montrent plus que les dates à venir (heure belge, au build) ; un script masque aussi dans le navigateur les dates passées depuis la dernière mise en ligne. Le calendrier garde tout l'historique.
- `2026-10-19` — Page `/evenements-prives` : plus aucune limite de zone (décision du patron) : « la remorque Yummy vient jusqu'à vous, où que soit votre événement », au lieu de « Gaume, autour de Virton et d'Arlon ». Ne plus jamais restreindre la zone des événements privés. La plaquette PDF porte encore l'ancienne mention (source HTML non conservée : à refaire).
- `2026-10-22` — Commandes du vendredi 23/10 préparées (branche de travail, en attente de l'accord de publication) : `commande.json` (`jours` = 2026-10-23, libellé « Commande à emporter ou à livrer », nouveaux champs `bandeau`, `creneaux` [11:30–14:00, 18:00–21:00], `lieuRetrait`), `ContactForm.astro` (choix à emporter / à livrer, validation des créneaux, résumé Web3Forms « mode — quantités — heure (livraison : adresse | retrait) », sujet « NOUVELLE COMMANDE À LIVRER/À EMPORTER — HH:MM »), `OrderBanner.astro` (« Commandes ouvertes aujourd'hui : à emporter ou à livrer » + « Aussi par téléphone, Messenger et Instagram »). Vidéo `promo/yummy-commande-23-10.mp4` (36 s, ralentie à la demande du patron : timeline ×1,3 + pauses de lecture, chaque texte lisible ≥ 2,5 s ; `promo/commande-23-10.html`, `node promo/render-commande-23-10.mjs`), même style que la vidéo « Commande à livrer », adresse fictive « Rue des Radis 7, Virton ».
- `2026-10-22` (soir) — Décision du patron : **pas de commande sur le site** pour le 23/10 (commandes uniquement par message privé Messenger ou au +32 474 60 64 51). `jours` remis à vide dans `commande.json` (le module reste en place mais inactif), créneaux mis à 11:30–14:00 / 18:00–20:00. Vidéo `promo/yummy-commande-23-10.mp4` refaite sans démo du site : accroche « pas de marché à cause de la météo… C'est nous qui venons à vous ! », Pita · Bowl · Burger · Potage au cerfeuil (photos `promo/img/`), créneaux, Messenger + téléphone, « Comment commander ? », site seulement en info dans l'outro. Puis correction du patron : **livraison uniquement** (pas d'« à emporter »), étape 2 « Dis ce que tu veux, ton adresse et ton heure de livraison ». Puis : menu final Pita · Burger · Bowl (potage retiré).
