#!/usr/bin/env python3
"""Recherche semi-automatique de prospects pour Yummy Street Food.

Usage :
  python3 prospection/chercher_prospects.py "salle mariage Virton" "séminaire Arlon"
  python3 prospection/chercher_prospects.py --site https://www.exemple.be

Pour chaque requête, récupère les sites trouvés via DuckDuckGo, puis visite
la page d'accueil et les pages « contact » pour en extraire e-mails et
téléphones publics. Sortie : CSV sur stdout (à coller dans le Google Sheet).
Aucun e-mail n'est envoyé : ce script ne fait que lire des pages publiques.
"""
import csv
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) YummyProspection/1.0"
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:be|lu|fr|com|net|eu|org)\b")
PHONE_RE = re.compile(r"(?:\+32|0032|\+352|\+33|\b0)[\s./-]?\(?\d{1,3}\)?(?:[\s./-]?\d{2,3}){2,4}")
# Annuaires et réseaux : on garde leurs pages comme source mais on ne les « scrape » pas comme prospects.
SKIP = ("duckduckgo", "facebook.", "instagram.", "youtube.", "wikipedia.", "booking.", "tripadvisor",
        "google.", "linkedin.", "expedia", "hotels.com", "kayak", "airbnb")
IGNORE_EMAILS = ("example", "sentry", "wixpress", "domain.", "email.com", "@2x", ".png", ".jpg")


def get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr-BE,fr"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(800_000).decode(r.headers.get_content_charset() or "utf-8", "replace")


def search(query, limit=10):
    html = get("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query))
    if "anomaly" in html:
        print(f"[!] DuckDuckGo limite les requêtes ({query!r}) : réessayez plus tard ou utilisez --site.", file=sys.stderr)
        return []
    seen, out = set(), []
    for m in re.finditer(r'uddg=([^"&]+)', html):
        url = urllib.parse.unquote(m.group(1))
        host = urllib.parse.urlparse(url).netloc
        if host in seen or any(s in host for s in SKIP):
            continue
        seen.add(host)
        out.append(url)
        if len(out) >= limit:
            break
    return out


def contacts(url):
    pages = [url]
    try:
        html = get(url)
    except Exception as e:  # site down, 403, etc.
        return {"url": url, "titre": "", "emails": "", "telephones": "", "erreur": str(e)[:80]}
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    base = urllib.parse.urljoin(url, "/")
    for href in re.findall(r'href="([^"#]+)"', html):
        if re.search(r"contact|coordonn|reserv|devis", href, re.I):
            pages.append(urllib.parse.urljoin(url, href))
    text = html
    for p in list(dict.fromkeys(pages))[1:4]:
        try:
            text += get(p)
        except Exception:
            pass
    text = urllib.parse.unquote(text).replace("[at]", "@").replace("(at)", "@").replace("&#64;", "@")
    emails = sorted({e.lower() for e in EMAIL_RE.findall(text) if not any(i in e.lower() for i in IGNORE_EMAILS)})
    phones = [p for p in dict.fromkeys(p.strip() for p in PHONE_RE.findall(re.sub(r"<[^>]+>", " ", text)))
              if len(re.sub(r"\D", "", p)) >= 9][:3]
    return {
        "url": base,
        "titre": re.sub(r"\s+", " ", title.group(1)).strip()[:90] if title else "",
        "emails": " ; ".join(emails[:4]),
        "telephones": " ; ".join(phones),
        "erreur": "",
    }


def main(argv):
    w = csv.DictWriter(sys.stdout, fieldnames=["requete", "url", "titre", "emails", "telephones", "erreur"])
    w.writeheader()
    if argv[:1] == ["--site"]:
        for url in argv[1:]:
            w.writerow({"requete": "site", **contacts(url)})
        return
    for q in argv:
        for url in search(q):
            w.writerow({"requete": q, **contacts(url)})
            time.sleep(0.5)


if __name__ == "__main__":
    main(sys.argv[1:])
