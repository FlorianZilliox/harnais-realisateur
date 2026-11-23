---
name: realisateur
description: "Point d'entrée du harnais « réalisateur » : fabriquer des films courts écrits en code et rendus image par image (HTML et GSAP → MP4), en particulier des films de démonstration d'agents IA, de produits ou de méthodes à projeter dans une présentation : la méthode tirée de vrais films (histoire, vérité à l'écran, forme, langue française, temps de lecture, son), le docteur qui installe seul tout ce qu'il faut, le moteur huashu-motion figé, la méthode video-director et des outils de contrôle (tenues de lecture mesurées, mixage final, planches). À charger dès qu'on veut « faire une vidéo », « un film », « une démo animée », « un motion design », « une vidéo pour ma présentation », « animer notre agent », « réalisateur », ou corriger un film déjà fait (« trop rapide », « on n'a pas le temps de lire », « c'est froid », « ça fait cheap »)."
---

# Réalisateur

Un film de démonstration est un film, pas une démo technique : une histoire, une idée, une forme qui donne envie, et rien d'affirmé qui ne soit vrai. Ce harnais réunit trois skills frères, installés côte à côte :
- **realisateur** (ce skill) : la méthode tirée de vrais films, le docteur, les outils de contrôle, un modèle de consigne.
- **huashu-motion** : le moteur, figé (`om` : créer, prévisualiser, composer la musique, rendre, contrôler). Lire sa section « Réglages locaux » avant tout film.
- **video-director** : la méthode générale en étapes (traitement, timeline, images clés, construction, son, rendu, revue) et ses scripts de contrôle.

## En arrivant

1. Lancer le docteur : `python3 -I "${CLAUDE_SKILL_DIR}/scripts/docteur.py"`. S'il manque quelque chose : `--installer` (Node.js, ffmpeg, Python des contrôles et instruments s'installent dans `~/.cache/realisateur`, versions figées, empreintes vérifiées ; rien ailleurs). La première fois, finir par `--essai` : un film de quelques secondes rendu de bout en bout. Si `python3` manque sur un Mac, `xcode-select --install` l'apporte (une fenêtre Apple, un clic). Si Chrome manque, le docteur le dit : il faut Google Chrome installé.
2. Lire le contexte du projet courant (CLAUDE.md, mémoire, charte, dossier de livraison) : il prime sur les défauts de ce harnais. Ne rien redemander de ce qui est déjà décidé.
3. Lire `references/methode.md` en entier avant de proposer quoi que ce soit, puis la consigne des films du projet si elle existe (sinon la créer depuis `references/consigne-modele.md`).

## Le chemin d'un film

| Étape | Ce qu'on fait | La porte |
|---|---|---|
| 1. Matière | Rassembler les vraies captures, vidéos, documents dans `<film>/materials/` ; écrire `FACTS.md` (chaque affirmation et sa source) | rien d'inventé pour ce qui existe |
| 2. Références | Relire `references/references-motion.md`, regarder deux ou trois films proches du sujet | une grammaire choisie, pas une œuvre copiée |
| 3. Directions | Trois directions, une vraie image clé chacune (`om still`) | la personne choisit |
| 4. Traitement | `TREATMENT.md` : l'histoire en une phrase, accroche, tournant, chute, ce qu'on lit à chaque moment ; `timeline.json` | `check_timeline.py` sans erreur |
| 5. Construction | `index.html` (gabarit `blank`, polices par `om fonts add`), textes marqués `data-lire` | `om check` à 0 erreur |
| 6. Son | Partition ABC écrite pour le film (`exemples/partition-jazz.py`), `om sound` | les temps forts tombent sur les marques |
| 7. Rendu et contrôles | `om render`, `om qa --sheet`, `tenues.mjs`, notes de directeur, un nouveau rendu | planche regardée, tenues ok |
| 8. Final | `om render --blur`, `mixage_final.sh`, `qa_video.py` | −14 LUFS ± 1, crête ≤ −1 dBTP |

Montrer à chaque porte dès que c'est montrable ; une chose à la fois.

## Les outils

Toujours passer par `lancer.sh`, qui met en place Node, ffmpeg et le Python des contrôles installés par le docteur :

```sh
L="${CLAUDE_SKILL_DIR}/outils/lancer.sh"
sh "$L" om new <film>                                   # un projet de film (puis om check, om still, om sound, om render, om qa --sheet)
sh "$L" om studio <film> --no-open &                     # aperçu en direct, la personne commente le plan à corriger
sh "${CLAUDE_SKILL_DIR}/outils/stills.sh" <film> <lot> 1.0,4.5,9.2   # images clés + planche dans <film>/stills/<lot>/
sh "$L" node "${CLAUDE_SKILL_DIR}/outils/tenues.mjs" <film>          # « lu deux fois », mesuré image par image (textes data-lire)
sh "$L" python "${CLAUDE_SKILL_DIR}/exemples/partition-jazz.py" <film>   # exemple : la partition écrite dans index.html
sh "${CLAUDE_SKILL_DIR}/outils/mixage_final.sh" <brut.mp4> <final.mp4> [<début> <fin> du silence avant le temps fort]
sh "$L" python "${CLAUDE_SKILL_DIR}/../video-director/scripts/qa_video.py" <final.mp4> --out <film>/qa --beats <film>/timeline.json
sh "$L" python "${CLAUDE_SKILL_DIR}/../video-director/scripts/check_timeline.py" <film>/timeline.json
sh "$L" python "${CLAUDE_SKILL_DIR}/outils/planche.py" <dossier d'images>
```

La liste complète des commandes `om` est dans le skill huashu-motion (section « The tool »).

## Ce qu'on ne fait jamais

- Publier ou partager quoi que ce soit (`om share`, mise en ligne) sans demande explicite.
- Animer des personnages en code : les personnes sont abstraites (voir la méthode, section 5).
- Montrer un film sans avoir regardé sa planche, ni affirmer un contrôle qui n'a pas été fait.
- Télécharger du code ou un modèle hors du docteur, ou changer la version du moteur sans l'accord de la personne.

## Faire grandir le harnais

Une leçon nouvelle (un refus, un piège, une mesure qui a manqué) s'ajoute à `references/methode.md` à l'endroit qui lui correspond, et dans la consigne du projet. Un outil né sur un film et utile au suivant s'écrit en générique dans `outils/` (chemins relatifs, message clair s'il manque quelque chose).
