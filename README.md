# Harnais « réalisateur »

Les outils et la méthode qui ont servi à fabriquer des films de démonstration d'agents IA : des films courts, écrits en code (HTML et GSAP) et rendus image par image en MP4, avec leur musique, sans logiciel de montage. À charger dans Claude Code, pour l'ajouter à ton Personal OS.

Ce qu'il contient (un plugin, `realisateur`, avec trois skills) :
- **realisateur** : le point d'entrée. La méthode tirée de vrais films (histoire, vérité à l'écran, forme, français, temps de lecture, son, contrôles), un docteur qui vérifie la machine et installe seul ce qui manque, des outils de contrôle (tenues de lecture mesurées image par image, mixage final, planches d'images), un exemple de partition jazz, un modèle de consigne pour les agents vidéo, et une recherche sur 33 films et keynotes de référence.
- **huashu-motion** : le moteur des films (`om`), copie figée du projet open source du même nom.
- **video-director** : la méthode générale de réalisation en étapes, et ses scripts de contrôle.

## L'installer

Il suffit de demander à Claude Code (dans n'importe quel dossier) :

> Installe le plugin « realisateur » depuis le repo GitHub privé FlorianZilliox/harnais-realisateur, puis lance son docteur avec --installer et --essai.

Ce que Claude fera, pour information :

```sh
claude plugin marketplace add FlorianZilliox/harnais-realisateur
claude plugin install realisateur@harnais-realisateur
python3 -I <dossier du skill realisateur>/scripts/docteur.py --installer --essai
```

Le repo est privé : il faut d'abord accepter l'invitation GitHub reçue par mail, et que l'ordinateur soit connecté à ton compte GitHub (si Claude te le signale : `gh auth login`, puis `gh auth setup-git`). Une fois le plugin installé, redémarrer Claude Code (ou taper `/reload-plugins`).

Le docteur installe ce qui manque dans `~/.cache/realisateur`, sans rien toucher d'autre : Node.js 22, ffmpeg, un environnement Python pour les contrôles et les instruments réels de la musique (environ 200 Mo en tout). Il faut seulement que Google Chrome soit installé. L'essai fabrique un film de quelques secondes de bout en bout : s'il passe, tout est prêt.

**Sans plugin**, l'installation marche aussi en copiant les trois dossiers de `plugins/realisateur/skills/` (realisateur, huashu-motion, video-director) dans `~/.claude/skills/`, côte à côte, puis en lançant le docteur.

## S'en servir

Demander simplement un film : « Fais-moi un film de 60 secondes qui montre comment fonctionne mon agent X, pour ma présentation de jeudi. » Le skill `realisateur` se charge, lit sa méthode et suit ses étapes : la matière (tes vraies captures), trois directions visuelles au choix, l'histoire, la construction, la musique, le rendu et les contrôles. Il montre à chaque étape. On peut aussi l'appeler par `/realisateur:realisateur`.

Pour corriger un film pendant qu'il se fabrique : `om studio` ouvre un aperçu en direct où l'on peut commenter un plan précis.

## Mettre à jour

> Mets à jour le plugin realisateur.

(Claude fera `claude plugin marketplace update harnais-realisateur`, puis `claude plugin update realisateur@harnais-realisateur`.)

## Licences

- huashu-motion : MIT (`plugins/realisateur/skills/huashu-motion/moteur/LICENSE`), avec ses composants tiers (GSAP, three.js, polices OFL) décrits dans `moteur/THIRD_PARTY.md`.
- video-director : MIT (`plugins/realisateur/skills/video-director/LICENSE`).
- Les instruments de la musique sont téléchargés par le docteur (CC0 et CC-BY, crédits dans `~/.cache/huashu-motion/samples/NOTICE.txt`) ; ils ne sont pas dans ce repo.
