import commande from '../data/commande.json';

// Date du jour en heure belge (AAAA-MM-JJ), indépendante du fuseau du visiteur.
export const todayInBelgium = () =>
  new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Brussels' }).format(new Date());

// Les commandes ne sont ouvertes que les jours listés dans src/data/commande.json.
// `?commande=test` force l'ouverture pour vérifier le module un jour fermé.
export const ordersOpen = () =>
  commande.jours.includes(todayInBelgium()) || new URLSearchParams(location.search).get('commande') === 'test';
