#!/usr/bin/env python3
"""Génère le classeur de prospection Yummy (à importer dans Google Sheets).

  python3 prospection/generer_crm.py sortie.xlsx
Source des prospects : prospection/prospects.csv
"""
import csv
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

HERE = Path(__file__).parent
VERT, FORET, CITRON, MENTHE = "0C7C5E", "083E23", "BED70B", "E4EFE2"
H = Font(bold=True, color="FFFFFF")
HFILL = PatternFill("solid", fgColor=FORET)
WRAP = Alignment(wrap_text=True, vertical="top")
STATUTS = ["À contacter", "Brouillon prêt", "Contacté", "Relancé", "Intéressé", "RDV / dégustation",
           "Devis envoyé", "Gagné", "Perdu", "Pas maintenant"]
SIGNATURE = "Christelle Muller\nYummy Street Food — food truck local, végétal et gourmand\n+32 474 60 64 51 · yummy-streetfood.be"
PAGE = "https://yummy-streetfood.be/evenements-prives"
PLAQUETTE = "https://yummy-streetfood.be/plaquette-evenements-yummy.pdf"


def header(ws, cols, widths):
    ws.append(cols)
    for c, w in zip(ws[1], widths):
        c.font, c.fill, c.alignment = H, HFILL, Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[c.column_letter].width = w
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 30


def mode_emploi(wb):
    ws = wb.active
    ws.title = "Mode d'emploi"
    ws.column_dimensions["A"].width = 120
    lignes = [
        ("YUMMY STREET FOOD — Outil de prospection des événements privés", Font(bold=True, size=16, color=FORET)),
        ("", None),
        ("LA ROUTINE (30 minutes par semaine, le lundi)", Font(bold=True, size=12, color=VERT)),
        ("1. Onglet « Prospects » : filtrer Statut = « Brouillon prêt ». Les brouillons sont déjà dans Gmail (dossier Brouillons) : relire, personnaliser une phrase, envoyer.", None),
        ("2. Après l'envoi : passer le statut à « Contacté » et noter la date dans « Date 1er contact ». La colonne « Prochaine relance » se calcule toute seule (J+7, puis J+14).", None),
        ("3. Les lignes en ROUGE sont à relancer aujourd'hui : utiliser le modèle « Relance » de l'onglet « Modèles », ou mieux, un appel de 2 minutes (script dans « Modèles »).", None),
        ("4. Chaque réponse positive : statut « Intéressé », puis proposer une dégustation des starters (c'est ce qui convertit le mieux).", None),
        ("5. Onglet « Devis » : calculer le prix en 1 minute, puis passer le statut à « Devis envoyé » avec le montant.", None),
        ("6. Après chaque événement : envoyer le modèle « Après l'événement » (avis Google + parrainage). Un client content = 2 prospects.", None),
        ("", None),
        ("LES 3 RÈGLES QUI FONT SIGNER", Font(bold=True, size=12, color=VERT)),
        ("• Les prescripteurs d'abord : un lieu de réception ou un wedding planner qui vous recommande vaut 10 mails à des particuliers.", None),
        ("• Faire goûter : un plateau de starters déposé à un lieu de réception ou à une RH ouvre plus de portes qu'un PDF.", None),
        ("• Relancer : la plupart des réponses arrivent après une relance. Deux relances maximum, puis « Pas maintenant » (on recontacte dans 6 mois).", None),
        ("", None),
        ("LES OUTILS", Font(bold=True, size=12, color=VERT)),
        (f"• Page de devis du site : {PAGE} (ajouter ?src=nom-campagne au lien pour savoir d'où viennent les demandes).", None),
        ("• Plaquette PDF à joindre aux mails : https://yummy-streetfood.be/plaquette-evenements-yummy.pdf", None),
        ("• Trouver les coordonnées d'un nouveau prospect : python3 prospection/chercher_prospects.py --site https://site-du-prospect.be", None),
        ("• Claude peut refaire toute la boucle chaque semaine (trouver de nouveaux prospects, les ajouter ici, préparer les brouillons Gmail). Rien n'est jamais envoyé sans vous.", None),
        ("", None),
        ("À COMPLÉTER PAR VOUS", Font(bold=True, size=12, color="C0392B")),
        ("• Onglet « Devis » : vos prix (plat, dessert, boissons, déplacement, minimum de prestation). Seul le prix des starters (3 €) est connu à ce jour.", None),
    ]
    for texte, font in lignes:
        ws.append([texte])
        c = ws.cell(ws.max_row, 1)
        c.alignment = WRAP
        if font:
            c.font = font


def prospects(wb):
    ws = wb.create_sheet("Prospects")
    cols = ["ID", "Priorité", "Segment", "Organisation", "Commune", "Contact", "Email", "Téléphone", "Site / source",
            "Pourquoi eux (angle d'approche)", "Canal conseillé", "Statut", "Date 1er contact", "Prochaine relance",
            "Date événement", "Montant devis (€)", "Notes / historique"]
    header(ws, cols, [6, 8, 17, 30, 20, 18, 30, 17, 28, 60, 18, 16, 13, 13, 13, 12, 40])
    with open(HERE / "prospects.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            statut = "Brouillon prêt" if r["email"] else "À contacter"
            ws.append([r["id"], r["priorite"], r["segment"], r["organisation"], r["commune"], r["contact"], r["email"],
                       r["telephone"], r["site"], r["angle"], r["canal"], statut, None, None, None, None, ""])
    last = 150
    # Une seule formule pour toute la colonne : J+7 après le 1er contact, J+14 après une relance.
    ws["N2"] = ('=ARRAYFORMULA(IF(M2:M="","",IF(REGEXMATCH(L2:L,"Gagné|Perdu|Pas maintenant"),"",'
                'IF(L2:L="Relancé",M2:M+14,M2:M+7))))')
    for row in range(2, ws.max_row + 31):
        for col in (13, 14, 15):
            ws.cell(row, col).number_format = "DD/MM/YYYY"
        for col in (10, 17):
            ws.cell(row, col).alignment = WRAP
    dv = DataValidation(type="list", formula1='"' + ",".join(STATUTS) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"L2:L{last}")
    dvp = DataValidation(type="list", formula1='"A,B,C"', allow_blank=True)
    ws.add_data_validation(dvp)
    dvp.add(f"B2:B{last}")
    rng = f"A2:Q{last}"
    ws.conditional_formatting.add(rng, FormulaRule(formula=['AND($N2<>"",$N2<=TODAY())'], fill=PatternFill("solid", fgColor="F5B7B1")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=['$L2="Gagné"'], fill=PatternFill("solid", fgColor="C8E6A0")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=['OR($L2="Intéressé",$L2="RDV / dégustation",$L2="Devis envoyé")'], fill=PatternFill("solid", fgColor="FFF3B0")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=['OR($L2="Perdu",$L2="Pas maintenant")'], font=Font(color="999999")))
    ws.auto_filter.ref = f"A1:Q{last}"


MODELES = [
    ("Lieu de réception — partenariat", "Prestation food truck sur mesure pour vos mariages et réceptions",
     "Bonjour,\n\nNous sommes Yummy Street Food, le food truck vert de Virton : une street-food végétale préparée avec les légumes que nous cultivons nous-mêmes.\n\n"
     "Nous aimerions faire partie des prestataires que vous recommandez à vos clients. Pour un vin d'honneur ou un cocktail, nous proposons une formule de 3 ou 5 starters végétaux, puis un plat street food (burger ou pita) et un dessert si vous le souhaitez. Nous pouvons aussi assurer un service en fin de soirée, et même le brunch du lendemain.\n\n"
     f"Notre plaquette : {PLAQUETTE}\n\nLe plus simple est encore de goûter : nous pouvons passer vous déposer un plateau de starters, à vous de nous dire quand.\n\n"
     f"Toutes nos formules : {PAGE}?src=lieux\n\nBelle journée,\n{SIGNATURE}"),
    ("Wedding planner — partenariat", "Une prestation food truck sur mesure pour vos mariés",
     "Bonjour {prénom},\n\nJ'ai découvert votre travail et votre approche des mariages, et je pense que nous pourrions faire de beaux mariages ensemble.\n\n"
     "Yummy Street Food, c'est une remorque vert émeraude et une cuisine végétale, locale et colorée : starters en ouverture, puis burgers et pitas, avec les légumes de notre potager en Gaume, et même le brunch du lendemain. Le résultat est aussi joli que bon, ce qui compte pour vos couples.\n\n"
     "Seriez-vous partant(e) pour un café et une dégustation ? Et bien sûr, nous recommandons volontiers vos services à nos clients en retour.\n\n"
     f"Notre offre mariage : {PAGE}?src=planners\n\nAu plaisir,\n{SIGNATURE}"),
    ("Entreprise — RH / comité du personnel", "Prestation food truck sur mesure pour vos événements d'entreprise",
     "Bonjour {prénom},\n\nVous préparez peut-être déjà la fête du personnel, un repas de cohésion, un family day ou un séminaire pour 2027 ?\n\n"
     "Yummy Street Food est un food truck basé à Virton. Nous cuisinons une street-food végétale et gourmande avec les légumes de notre propre potager. Concrètement, la remorque s'installe sur votre site et sert vos équipes rapidement, sans qu'il y ait rien à organiser de votre côté.\n\n"
     "Nous proposons par exemple :\n- un repas de cohésion ou un lunch d'équipe, servi sur votre site ;\n- un apéro avec une formule de 3 ou 5 starters végétaux ;\n- un repas complet pour une fête du personnel ou un family day.\n\n"
     f"Notre plaquette : {PLAQUETTE}\nEt pour un devis en deux minutes : {PAGE}?src=entreprises\n\nBonne journée,\n{SIGNATURE}"),
    ("Commune / salles communales", "Proposition pour les locataires de vos salles",
     "Bonjour,\n\nNous sommes Yummy Street Food, food truck de street-food végétale installé à Virton (vous nous avez peut-être vus au marché du vendredi).\n\n"
     "Les personnes qui louent vos salles pour un anniversaire ou une fête de famille cherchent souvent une solution repas simple. Serait-il possible de joindre notre plaquette au dossier de location, ou de nous citer parmi les prestataires locaux ?\n\n"
     "Nous serions aussi ravis de participer aux événements organisés par la commune.\n\n"
     f"Nos formules : {PAGE}?src=communes\n\nMerci d'avance et belle journée,\n{SIGNATURE}"),
    ("Gîte de groupe", "Une soirée food truck sur mesure pour vos groupes",
     "Bonjour,\n\nVos gîtes accueillent des groupes pour des anniversaires, des cousinades, des week-ends entre amis ou des réunions de famille. Pour eux, la question du repas du samedi soir revient souvent.\n\n"
     "Nous sommes Yummy Street Food, un food truck végétal et local basé à Virton, à quelques minutes de chez vous. Nous pouvons venir cuisiner sur place pour vos hôtes (starters à l'apéro, puis burger ou pita, et un dessert).\n\n"
     f"Seriez-vous d'accord de mentionner cette option à vos clients ? Notre plaquette : {PLAQUETTE}\n\n"
     f"Lien direct pour vos clients : {PAGE}?src=gites\n\nBelle journée,\n{SIGNATURE}"),
    ("Réseau d'affaires / association", "Yummy Street Food pour vos événements",
     "Bonjour,\n\nNous sommes Yummy Street Food, food truck de street-food végétale basé à Virton. Nous cuisinons les légumes que nous cultivons nous-mêmes.\n\n"
     "Nous aimerions participer à vos prochains événements (afterworks, salons, assemblées, fêtes), comme traiteur ou comme exposant. Pourriez-vous nous indiquer la marche à suivre ou la bonne personne à contacter ?\n\n"
     f"Notre plaquette : {PLAQUETTE}\nNos formules : {PAGE}?src=reseaux\n\nAu plaisir d'échanger,\n{SIGNATURE}"),
    ("Relance J+7", "Re: {sujet initial}",
     "Bonjour,\n\nJe me permets de revenir vers vous au sujet de mon message de la semaine dernière. Notre proposition de passer vous faire goûter nos starters tient toujours, cela prend dix minutes.\n\n"
     f"Bonne journée,\n{SIGNATURE}"),
    ("Relance J+21 (dernière)", "Re: {sujet initial}",
     "Bonjour,\n\nDernier petit message de ma part, promis ! Si ce n'est pas le bon moment, aucun souci : je garde vos coordonnées et vous recontacterai au printemps. Et si un événement se présente d'ici là, vous savez où nous trouver.\n\n"
     f"Belle continuation,\n{SIGNATURE}"),
    ("Après l'événement — avis + parrainage", "Merci pour votre confiance !",
     "Bonjour {prénom},\n\nMerci encore de nous avoir accueillis pour {événement} ! Nous avons adoré.\n\n"
     "Deux petites choses qui nous aideraient énormément :\n1. Laisser un avis Google (deux minutes) : {lien avis Google}\n"
     "2. Penser à nous si quelqu'un autour de vous prépare un mariage, un anniversaire ou une fête d'entreprise. Pour chaque événement réservé grâce à vous, {cadeau parrainage}.\n\n"
     f"À bientôt sur les marchés,\n{SIGNATURE}"),
    ("Réponse à une demande de devis", "Votre événement du {date} — proposition Yummy",
     "Bonjour {prénom},\n\nMerci pour votre demande ! Pour {nombre} invités le {date} à {lieu}, voici ce que nous vous proposons :\n\n{détail du devis — onglet Devis}\n\n"
     "Ce prix comprend la venue de la remorque, la préparation sur place et le service. Pour bloquer la date, il suffit de nous confirmer par retour de mail.\n\n"
     "Si vous voulez goûter avant de décider, venez nous voir au marché (Virton le vendredi, Arlon le jeudi, de 8 h à 13 h).\n\n"
     f"Belle journée,\n{SIGNATURE}"),
    ("Script téléphone (2 minutes)", "—",
     "« Bonjour, Christelle Muller de Yummy Street Food, le food truck végétal de Virton. Je vous ai envoyé un petit mail la semaine dernière. Je vous appelle juste pour savoir à qui je dois m'adresser pour les [fêtes du personnel / mariages chez vous]. »\n"
     "→ Si intéressé : « Le plus simple, c'est que je passe vous faire goûter nos starters. Plutôt mardi ou jeudi ? »\n"
     "→ Si pas le moment : « Aucun souci. Je peux vous rappeler quand ? En janvier pour les événements de printemps ? » (noter la date dans « Prochaine relance »)"),
    ("Message LinkedIn (RH)", "—",
     "Bonjour {prénom}, je suis Christelle de Yummy Street Food, un food truck végétal et local basé à Virton. Nous préparons notre saison 2027 d'événements d'entreprise (fêtes du personnel, family days, lunchs d'équipe) dans la région. Est-ce que ce type de prestation pourrait vous intéresser ? Je vous envoie notre plaquette si c'est le cas. Belle journée !"),
]


def modeles(wb):
    ws = wb.create_sheet("Modèles")
    header(ws, ["Modèle", "Objet", "Texte (remplacer les {…})"], [30, 45, 120])
    for m in MODELES:
        ws.append(list(m))
        for c in ws[ws.max_row]:
            c.alignment = WRAP


CALENDRIER = [
    ("Octobre 2026", "Lieux de réception, wedding planners, gîtes, communes", "Lancement : envoyer les brouillons prêts. S'inscrire comme exposant au Salon du mariage d'Arlon (ACIA). Créer la fiche Google Business Profile et les fiches sur mariages.net et eventigo."),
    ("Novembre 2026", "Futurs mariés 2027, wedding planners", "Les couples réservent leurs prestataires 9 à 15 mois avant le mariage : c'est le moment des salons du mariage. Dégustations chez les lieux partenaires."),
    ("Décembre 2026", "Entreprises", "Proposer un « drink des vœux » en janvier (les fêtes de fin d'année sont déjà réservées). Message LinkedIn aux RH."),
    ("Janvier 2027", "Entreprises, écoles, comités", "Les budgets 2027 se votent : family days et fêtes du personnel (juin à septembre). Contacter les associations de parents pour les fancy-fairs de mai-juin. Soirée des vœux de la CCILB."),
    ("Février 2027", "Communions, anniversaires d'été", "Publicité Facebook/Instagram ciblée sur 25 km autour de Virton : communions (avril-mai) et anniversaires. Relancer les « Pas maintenant »."),
    ("Mars 2027", "Garages, commerces, clubs", "Portes ouvertes des concessions auto, inaugurations, saison des clubs sportifs. Relancer les lieux de réception avant la saison."),
    ("Avril 2027", "EVJF/EVG, groupes en gîte", "Pousser l'offre « soirée food truck en gîte ». Publier des photos des premiers événements."),
    ("Mai-Juin 2027", "Exécution", "Saison des mariages et des fancy-fairs : après chaque événement, demander un avis Google et lancer le parrainage. Photos et vidéos pour les réseaux."),
    ("Juillet-Août 2027", "Rentrée et fin d'année", "Préparer les fêtes du personnel de septembre et prospecter les fêtes de fin d'année 2027 (les entreprises réservent dès septembre)."),
    ("Septembre 2027", "Entreprises (fin d'année), mariages 2028", "Envoyer la campagne fêtes de fin d'année et relancer les wedding planners pour 2028. Bilan : quel canal a apporté quel chiffre d'affaires ?"),
]

CANAUX = [
    ("Google Business Profile", "Gratuit", "Catégorie « Traiteur » + « Food truck », photos, lien vers /evenements-prives. Demander un avis après chaque événement.", "À faire"),
    ("mariages.net", "Fiche gratuite (options payantes)", "Rubrique Food truck, Belgique : les couples y comparent les prestataires.", "À faire"),
    ("eventigo.eu", "Commission", "Plateforme de réservation de food trucks qui couvre la province de Luxembourg.", "À faire"),
    ("mariage.be", "Annuaire", "Rubrique traiteur / food truck, province de Luxembourg.", "À faire"),
    ("Salon du mariage d'Arlon (ACIA)", "Stand", "Château du Bois d'Arlon, en novembre : stand avec dégustation des starters et collecte des contacts.", "À demander"),
    ("Groupes Facebook locaux", "Gratuit", "Groupes de Virton, Gaume et Arlon : publier les photos des événements (sans démarchage agressif).", "En continu"),
    ("Publicité Meta (Facebook/Instagram)", "Environ 5 €/jour", "Rayon de 25 km autour de Virton, audiences « fiancé(e)s » et parents. Lien avec ?src=meta.", "Février et septembre"),
    ("Marchés de Virton et Arlon", "Déjà en place", "Mettre la plaquette au truck et un chevalet « Vos événements privés » avec le QR code.", "Maintenant"),
    ("Parrainage", "Remise ou cadeau", "Pour chaque événement réservé grâce à un client : récompense à définir (ex. starters offerts).", "À définir"),
]


def calendrier(wb):
    ws = wb.create_sheet("Calendrier")
    header(ws, ["Mois", "Cibles prioritaires", "Actions"], [18, 40, 110])
    for r in CALENDRIER:
        ws.append(list(r))
        for c in ws[ws.max_row]:
            c.alignment = WRAP
    ws2 = wb.create_sheet("Canaux")
    header(ws2, ["Canal", "Coût", "Comment l'utiliser", "Statut"], [32, 22, 90, 18])
    for r in CANAUX:
        ws2.append(list(r))
        for c in ws2[ws2.max_row]:
            c.alignment = WRAP


def devis(wb):
    ws = wb.create_sheet("Devis")
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 60
    rows = [
        ("CALCULATEUR DE DEVIS", None, "Cases jaunes = à remplir"),
        ("Nombre d'invités", 80, ""),
        ("Starters par invité (0, 3 ou 5)", 5, "La Complète = 5 · La Gourmande = 3 · L'Essentielle = 0"),
        ("Prix d'un starter (€)", 3, ""),
        ("Plat street food ? (1 = oui, 0 = non)", 1, "Burger ou pita"),
        ("Prix du plat par invité (€)", None, "À FIXER par vous"),
        ("Dessert ? (1 = oui, 0 = non)", 0, "En option sur La Complète et La Gourmande, inclus dans L'Essentielle"),
        ("Prix du dessert par invité (€)", None, "À FIXER par vous"),
        ("Boissons par invité (€)", None, "À FIXER (0 si pas de boissons)"),
        ("Forfait déplacement (€)", None, "À FIXER (ex. selon la distance depuis Virton)"),
        ("Minimum de prestation (€)", None, "À FIXER (repère du marché : 250 à 800 €)"),
        ("", None, ""),
        ("Sous-total starters", "=B2*B3*B4", ""),
        ("Sous-total plats", "=B2*B5*B6", ""),
        ("Sous-total desserts", "=B2*B7*B8", ""),
        ("Sous-total boissons", "=B2*B9", ""),
        ("TOTAL PROPOSÉ (€)", "=MAX(B11,B13+B14+B15+B16+B10)", "Le minimum de prestation s'applique si le total est inférieur"),
        ("Prix par invité (€)", "=IF(B2>0,B17/B2,0)", ""),
    ]
    for r in rows:
        ws.append(list(r))
    ws["A1"].font = Font(bold=True, size=14, color=FORET)
    for r in range(2, 12):
        ws.cell(r, 2).fill = PatternFill("solid", fgColor="FFF3B0")
    for r in (17, 18):
        ws.cell(r, 1).font = Font(bold=True, color=VERT, size=12)
        ws.cell(r, 2).font = Font(bold=True, size=12)
        ws.cell(r, 2).number_format = '#,##0.00 "€"'


def tableau_de_bord(wb):
    ws = wb.create_sheet("Tableau de bord", 1)
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 14
    ws.append(["TABLEAU DE BORD"])
    ws["A1"].font = Font(bold=True, size=14, color=FORET)
    ws.append(["Statut", "Nombre"])
    for c in ws[2]:
        c.font, c.fill = H, HFILL
    for s in STATUTS:
        ws.append([s, f"=COUNTIF(Prospects!L:L,\"{s}\")"])
    n = ws.max_row
    ws.append([])
    ws.append(["Relances à faire aujourd'hui", '=COUNTIFS(Prospects!N:N,"<="&TODAY(),Prospects!N:N,"<>")'])
    ws.append(["Taux de signature (gagnés / contactés)",
               f'=IFERROR(B{n-2}/(COUNTA(Prospects!M2:M150)),0)'])
    ws.cell(ws.max_row, 2).number_format = "0%"
    ws.append(["CA signé (€)", '=SUMIF(Prospects!L:L,"Gagné",Prospects!P:P)'])
    ws.append(["CA en devis (€)", '=SUMIF(Prospects!L:L,"Devis envoyé",Prospects!P:P)'])
    for r in range(n + 2, ws.max_row + 1):
        ws.cell(r, 1).font = Font(bold=True, color=VERT)


def main(out):
    wb = Workbook()
    mode_emploi(wb)
    prospects(wb)
    tableau_de_bord(wb)
    modeles(wb)
    calendrier(wb)
    devis(wb)
    wb.save(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Yummy_Prospection_Evenements.xlsx")
