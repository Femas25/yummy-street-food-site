// Agenda des passages de Yummy Street Food : UNE seule source (src/data/evenements.json) pour
// la carte « Prochain passage » de l'accueil, la page « Où nous trouver » et les données schema.org.
// Le même code tourne au build (HTML de base) et dans le navigateur (mise à jour à l'heure réelle),
// toujours en heure belge (Europe/Brussels), quel que soit le fuseau du visiteur.
import data from '../data/evenements.json';

export const TZ = 'Europe/Brussels';
const isoDateRe = /^\d{4}-\d{2}-\d{2}$/;

export interface EvenementBrut {
  date: string;
  titre: string;
  lieu: string;
  adresse?: string;
  horaires?: string;
  couleur?: string;
  commune?: string;
  statut?: string;
}

export interface Passage {
  id: string;
  date: string; // AAAA-MM-JJ (jour de début)
  titre: string;
  lieu: string;
  adresse?: string;
  commune?: string;
  horaires: string; // texte affiché, ex. « 16h – minuit »
  couleur: string;
  prive: boolean;
  annule: boolean;
  finApresMinuit: boolean;
  heureDebut?: string; // HH:MM, absent si horaires non précisés
  heureFin?: string;
  debut: number; // instant (ms) de début
  fin: number; // instant (ms) de fin (lendemain si la fin passe minuit)
}

const pad = (n: number) => String(n).padStart(2, '0');

/** Décalage de Bruxelles (en minutes) à un instant donné : 60 en hiver, 120 en été. */
const offsetMinutes = (instant: number) => {
  const name =
    new Intl.DateTimeFormat('en-US', { timeZone: TZ, timeZoneName: 'shortOffset' })
      .formatToParts(new Date(instant))
      .find((p) => p.type === 'timeZoneName')?.value ?? 'GMT+1';
  const m = name.match(/GMT([+-]\d+)(?::(\d+))?/);
  return m ? Number(m[1]) * 60 + Math.sign(Number(m[1])) * Number(m[2] ?? 0) : 60;
};

/** Instant (ms) correspondant à « date à HH:MM » heure de Bruxelles. */
export const instantBruxelles = (date: string, hhmm: string) => {
  const [y, mo, d] = date.split('-').map(Number);
  const [h, mi] = hhmm.split(':').map(Number);
  const naif = Date.UTC(y, mo - 1, d, h, mi);
  return naif - offsetMinutes(naif - 60 * 60 * 1000) * 60 * 1000;
};

/** Décalage ISO (+01:00 / +02:00) d'un instant, pour schema.org. */
export const isoOffset = (instant: number) => {
  const o = offsetMinutes(instant);
  return `${o >= 0 ? '+' : '-'}${pad(Math.floor(Math.abs(o) / 60))}:${pad(Math.abs(o) % 60)}`;
};

/** Date et heure de Bruxelles d'un instant, ex. « 2026-11-28T00:00:00+01:00 ». */
export const isoBruxelles = (instant: number) => {
  const parts = Object.fromEntries(
    new Intl.DateTimeFormat('en-GB', {
      timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
    })
      .formatToParts(new Date(instant))
      .map((p) => [p.type, p.value])
  );
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:00${isoOffset(instant)}`;
};

/** Jour (AAAA-MM-JJ) à Bruxelles pour un instant. */
export const jourBruxelles = (instant: number) => new Intl.DateTimeFormat('en-CA', { timeZone: TZ }).format(new Date(instant));

const lendemain = (date: string) => {
  const [y, m, d] = date.split('-').map(Number);
  const t = new Date(Date.UTC(y, m - 1, d + 1));
  return `${t.getUTCFullYear()}-${pad(t.getUTCMonth() + 1)}-${pad(t.getUTCDate())}`;
};

/** « 8h - 13h », « 16h30 – 0h » → { debut: '08:00', fin: '13:00' } ; null si non précisé (ex. « Privé »). */
export const lireHoraires = (horaires = '') => {
  const m = horaires.match(/(\d{1,2})\s*h\s*(\d{2})?\s*[-–à]+\s*(\d{1,2})\s*h\s*(\d{2})?/i);
  if (!m) return null;
  return { debut: `${pad(Number(m[1]))}:${m[2] ?? '00'}`, fin: `${pad(Number(m[3]) % 24)}:${m[4] ?? '00'}` };
};

const fmtHeure = (hhmm: string) => {
  if (hhmm === '00:00') return 'minuit';
  const [h, m] = hhmm.split(':');
  return `${Number(h)}h${m === '00' ? '' : m}`;
};

/** Commune lue dans l'adresse (« Place Léopold, 6700 Arlon, Belgique » → « Arlon »), sauf si précisée. */
const communeDe = (e: EvenementBrut) => {
  if (e.commune) return e.commune;
  const m = e.adresse?.match(/\b\d{4}\s+([^,]+)/);
  return m ? m[1].trim() : undefined;
};

export const normaliser = (e: EvenementBrut, index: number): Passage | null => {
  if (!isoDateRe.test(e.date)) return null;
  const h = lireHoraires(e.horaires);
  const finApresMinuit = !!h && h.fin <= h.debut;
  const debut = instantBruxelles(e.date, h?.debut ?? '00:00');
  const fin = h ? instantBruxelles(finApresMinuit ? lendemain(e.date) : e.date, h.fin) : instantBruxelles(lendemain(e.date), '00:00');
  const prive = !e.adresse || /priv/i.test(e.horaires ?? '') || /priv/i.test(e.titre);
  return {
    id: `${e.date}-${index}`,
    date: e.date,
    titre: e.titre,
    lieu: e.lieu,
    adresse: e.adresse,
    commune: communeDe(e),
    horaires: h ? `${fmtHeure(h.debut)} – ${fmtHeure(h.fin)}` : e.horaires || 'Horaires à confirmer',
    couleur: e.couleur ?? 'primary',
    prive,
    annule: /annul/i.test(e.statut ?? ''),
    finApresMinuit: finApresMinuit && h!.fin !== '00:00',
    heureDebut: h?.debut,
    heureFin: h?.fin,
    debut,
    fin,
  };
};

/** Tous les passages datés, triés par heure de début. */
export const tousLesPassages = (brut: EvenementBrut[] = data.evenements as EvenementBrut[]): Passage[] =>
  brut
    .map(normaliser)
    .filter((p): p is Passage => p !== null)
    .sort((a, b) => a.debut - b.debut || a.titre.localeCompare(b.titre));

/** Passages pas encore terminés (une sortie en cours reste visible jusqu'à sa fin, même après minuit). */
export const passagesAVenir = (maintenant: number, liste = tousLesPassages()) => liste.filter((p) => p.fin > maintenant);

export const estEnCours = (p: Passage, maintenant: number) => p.debut <= maintenant && maintenant < p.fin;

/** Prochain passage public (en cours ou à venir), hors événements privés et annulés. */
export const prochainPassage = (maintenant: number, liste = tousLesPassages()) =>
  passagesAVenir(maintenant, liste).find((p) => !p.prive && !p.annule) ?? null;

export const itineraire = (adresse: string) => `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(adresse)}`;
export const lienPlans = (adresse: string) => `https://maps.apple.com/?daddr=${encodeURIComponent(adresse)}`;
export const lienWaze = (adresse: string) => `https://www.waze.com/ul?q=${encodeURIComponent(adresse)}&navigate=yes`;

/** « vendredi 27 novembre » (année ajoutée si différente de l'année en cours). */
export const dateLongue = (date: string, maintenant = Date.now()) => {
  const [y, m, d] = date.split('-').map(Number);
  const opts: Intl.DateTimeFormatOptions = { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'UTC' };
  if (String(y) !== jourBruxelles(maintenant).slice(0, 4)) opts.year = 'numeric';
  return new Date(Date.UTC(y, m - 1, d, 12)).toLocaleDateString('fr-BE', opts);
};

export const moisAnnee = (date: string) => {
  const [y, m] = date.split('-').map(Number);
  return new Date(Date.UTC(y, m - 1, 15)).toLocaleDateString('fr-BE', { month: 'long', year: 'numeric', timeZone: 'UTC' });
};

/** Libellé relatif : « Aujourd'hui », « Demain », ou rien. */
export const jourRelatif = (p: Passage, maintenant: number) => {
  if (estEnCours(p, maintenant)) return 'En ce moment';
  const auj = jourBruxelles(maintenant);
  if (p.date === auj) return "Aujourd'hui";
  if (p.date === lendemain(auj)) return 'Demain';
  return '';
};

/** Données schema.org d'un passage public (l'entreprise est décrite à part, dans le Layout). */
export const schemaEvenement = (p: Passage, site: string) => ({
  '@context': 'https://schema.org',
  '@type': 'Event',
  name: `${p.titre.replace(/^\p{Extended_Pictographic}\s*/u, '')} — Yummy Street Food`,
  description: `Le food truck Yummy Street Food sera présent : ${p.lieu}, ${p.horaires}.`,
  startDate: isoBruxelles(p.debut),
  endDate: isoBruxelles(p.fin),
  eventAttendanceMode: 'https://schema.org/OfflineEventAttendanceMode',
  eventStatus: p.annule ? 'https://schema.org/EventCancelled' : 'https://schema.org/EventScheduled',
  location: {
    '@type': 'Place',
    name: p.lieu,
    address: {
      '@type': 'PostalAddress',
      streetAddress: p.adresse?.split(',')[0]?.trim(),
      postalCode: p.adresse?.match(/\b(\d{4})\s/)?.[1],
      addressLocality: p.commune,
      addressCountry: 'BE',
    },
  },
  organizer: { '@id': `${site}#entreprise` },
});
