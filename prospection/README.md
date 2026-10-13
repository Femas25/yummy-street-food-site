# Prospection événements privés — Yummy Street Food

Outils pour trouver et contacter des clients d'événements privés (mariages, entreprises, anniversaires, associations) autour de Virton.
Ce dossier ne fait pas partie du site : Astro ne compile que `src/` et `public/`.

| Fichier | Rôle |
|---|---|
| `prospects.csv` | Liste source des prospects (coordonnées publiques vérifiées le 13/10/2026). |
| `generer_crm.py` | Génère le classeur de suivi (`Yummy_Prospection_Evenements.xlsx`) : prospects, tableau de bord, modèles d'e-mails, calendrier saisonnier, canaux, calculateur de devis. |
| `Yummy_Prospection_Evenements.xlsx` | Le classeur généré. À importer dans Google Sheets (Fichier → Importer → Remplacer la feuille de calcul). |
| `chercher_prospects.py` | Récupère e-mails et téléphones publics d'un site : `python3 prospection/chercher_prospects.py --site https://exemple.be` |

Côté site :
- `/evenements-prives` est la page de conversion, avec le formulaire de devis (Web3Forms). Ajouter `?src=nom-campagne` aux liens envoyés pour savoir d'où vient chaque demande (champ `source` dans l'e-mail reçu).
- `public/plaquette-evenements-yummy.pdf` est la plaquette A4 à joindre ou à lier dans les e-mails. Son QR code renvoie vers `/evenements-prives?src=plaquette`.

Règle : aucun e-mail n'est envoyé automatiquement. Les messages sont préparés en brouillons Gmail, puis relus et envoyés à la main.
