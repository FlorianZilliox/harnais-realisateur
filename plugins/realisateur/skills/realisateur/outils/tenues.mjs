// Mesure des tenues de lecture (« lu deux fois ») sur la vraie composition, image par image.
//
// Chaque texte à lire porte l'attribut data-lire dans index.html (sa valeur sert de nom court, sinon le texte) :
//   <div class="narr" data-lire="accroche"><div class="ln"><span>Une phrase à lire.</span></div></div>
// Pour chacun, l'outil cherche l'intervalle où il est entièrement en place (visible, opacité pleine sur toute la
// chaîne des parents, lignes masquées .ln > span remontées à yPercent 0) et le compare au minimum :
//   2 s + 0,3 s par mot (réglable : --base 2 --par-mot 0.3). La montée du texte n'est pas comptée dans la tenue.
//
// Usage : sh lancer.sh node tenues.mjs <dossier du film ou index.html> [--pas 0.0333] [--base 2] [--par-mot 0.3]
// Le moteur est cherché dans OM_MOTEUR (posé par lancer.sh), sinon à côté du skill (../../huashu-motion/moteur).
import { existsSync, statSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ici = dirname(fileURLToPath(import.meta.url));
const moteur = process.env.OM_MOTEUR || join(ici, '..', '..', 'huashu-motion', 'moteur');
const lib = join(moteur, 'cli', 'lib', 'capture.js');
if (!existsSync(lib)) {
  console.error(`Moteur huashu-motion introuvable (${lib}). Lancer l'outil par « sh lancer.sh node tenues.mjs … », ou indiquer le dossier moteur dans OM_MOTEUR.`);
  process.exit(1);
}
const { openFilm } = await import(pathToFileURL(lib).href);

const args = process.argv.slice(2);
const opt = (nom, defaut) => { const i = args.indexOf(nom); return i >= 0 ? Number(args[i + 1]) : defaut; };
const cible = args.find((a) => !a.startsWith('--') && !/^[\d.]+$/.test(a));
if (!cible) { console.error('Usage : sh lancer.sh node tenues.mjs <dossier du film ou index.html> [--pas 0.0333] [--base 2] [--par-mot 0.3]'); process.exit(2); }
let page = resolve(cible);
if (existsSync(page) && statSync(page).isDirectory()) page = join(page, 'index.html');
if (!existsSync(page)) { console.error(`Page introuvable : ${page}`); process.exit(1); }
const pas = opt('--pas', 1 / 30), base = opt('--base', 2), parMot = opt('--par-mot', 0.3);
const mots = (s) => s.replace(/[«»:?,.;!→…]/g, ' ').split(/\s+/).filter((w) => /[\p{L}\d]/u.test(w)).length;
const f = (x) => x.toFixed(2).replace('.', ',');

const film = await openFilm(page, { video: 'seek' });
try {
  const fin = Number(await film.evaluate('window.__omEngine.duration()'));
  const items = await film.evaluate(`[...document.querySelectorAll('[data-lire]')].map((el, k) => {
    el.setAttribute('data-lire-k', k);
    const texte = el.textContent.replace(/\\s+/g, ' ').trim();
    return [el.getAttribute('data-lire') || texte.slice(0, 40), texte];
  })`);
  if (!items.length) {
    console.error('Aucun texte marqué : ajouter data-lire sur chaque élément de narration à lire (voir l\'en-tête de tenues.mjs).');
    process.exit(1);
  }
  await film.evaluate(`window.__tenue = (n) => Array.from({ length: n }, (_, k) => {
    const el = document.querySelector('[data-lire-k="' + k + '"]'); if (!el) return null;
    if (el.checkVisibility && !el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) return false;
    let op = 1; for (let e = el; e && e !== document.documentElement; e = e.parentElement) op *= Number(getComputedStyle(e).opacity);
    if (op < 0.98) return false;
    const sp = el.matches('.ln') ? [el.firstElementChild] : [...el.querySelectorAll('.ln > span')];
    if (sp.length && window.gsap) return sp.every((s) => !s || Math.abs(Number(gsap.getProperty(s, 'yPercent'))) < 0.05);
    return true;
  })`);
  const etat = items.map(() => ({ runs: [], on: null }));
  const n = Math.ceil(fin / pas);
  for (let i = 0; i <= n; i++) {
    const t = Math.min(fin - 1e-3, i * pas);
    await film.seek(t);
    const r = await film.evaluate(`window.__tenue(${items.length})`);
    r.forEach((v, k) => {
      const s = etat[k];
      if (v && s.on == null) s.on = t;
      if (!v && s.on != null) { s.runs.push([s.on, t]); s.on = null; }
    });
  }
  etat.forEach((s) => { if (s.on != null) s.runs.push([s.on, fin]); });
  console.log(`page : ${page}\ndurée : ${f(fin)} s, pas : ${f(pas)} s, règle : ${f(base)} s + ${f(parMot)} s par mot\n`);
  console.log('| Texte | Mots | En place (s) | Tenue | Requis | Verdict |\n|---|---|---|---|---|---|');
  let courts = 0;
  items.forEach(([nom, texte], k) => {
    const s = etat[k], m = mots(texte), req = base + parMot * m;
    if (!s.runs.length) { courts++; console.log(`| ${nom} | ${m} | jamais en place | 0 | ${f(req)} | à vérifier |`); return; }
    const best = s.runs.reduce((a, b) => (b[1] - b[0] > a[1] - a[0] ? b : a));
    const ten = best[1] - best[0];
    const bon = ten + 1e-6 >= req; if (!bon) courts++;
    console.log(`| ${nom} | ${m} | ${s.runs.map(([a, b]) => `${f(a)} → ${f(b)}`).join(' ; ')} | ${f(ten)} | ${f(req)} | ${bon ? 'ok' : `court de ${f(req - ten)}`} |`);
  });
  console.log(courts ? `\n${courts} texte(s) à rallonger ou à vérifier.` : '\nTous les textes se lisent deux fois.');
  process.exitCode = courts ? 1 : 0;
} finally { await film.close(); }
