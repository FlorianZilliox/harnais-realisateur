# Modèle : consigne permanente des agents vidéo d'un projet

> Copier ce fichier dans le dossier des films du projet sous le nom `CONSIGNE-FILM.md`, remplir les crochets, et le tenir à jour à chaque retour. Chaque agent qui fabrique ou corrige un film le lit en premier ; ce qu'il contient prime sur tout storyboard antérieur. Les décisions s'y écrivent avec leur date et, si possible, les mots exacts de la personne.

## Où les films se placent
- [Le contexte : qui présente, à qui, combien de temps, dans quelle présentation.]
- [Le récit qui fait foi, et le fichier qui le porte.]
- [La liste des films, leur ordre, et l'idée unique de chacun.]

## Le public
- [Qui regarde, et ce qu'il connaît ou ignore du sujet. Par défaut : chaque phrase se comprend sans faire le métier montré.]

## Règles communes, non négociables
- Pas de voix off : [oui / non, et pourquoi].
- Du storytelling : une tension, un tournant, une chute ; une seule idée par film.
- Aucune heure d'horloge en ouverture, aucune date à l'écran ; le futur se dit « Prochaine étape : … » en contour.
- Rien de nominatif : [« une PO », « une PM »… ; ce qui peut être nommé].
- Aucune interface inventée pour ce qui existe ; l'imaginé porte « Exemple ».
- Le waouh par la forme, jamais par la promesse.
- [Les chiffres autorisés à l'écran, et seulement eux.]
- [Les boîtes aux lettres de la personne : en lecture seule.]

## La direction visuelle retenue
- [Son nom, ses références (voir `references-motion.md`), la date du choix.]
- [Constantes de tous les films : matières, palette commune, le héros (le produit, l'outil ou l'agent montré), les personnes (abstraites, jamais de personnage animé en code), les typographies et leurs rôles, la taille minimale du texte.]
- [Palettes et musiques propres à chaque film, pour qu'on ne les confonde pas.]
- [Ce qui est rejeté, avec les mots de la personne.]

## Film par film
### Film 1 : [titre] (≈ [durée] s), projet `[dossier]/`
- [La trame en 4 à 6 temps : accroche, tournant, chute.]
- [Ce qui est validé et à ne plus toucher.]
- [Ce qui est à retirer.]

## La vérité à l'écran
| Affirmation | Source |
|---|---|
| [chaque chiffre ou fait montré] | [fichier, transcription, capture] |

## Matière
- [Les vraies captures, vidéos et documents à reconstruire, avec leurs chemins.]

## Outils
- Le harnais `realisateur` : méthode (`references/methode.md`), docteur, outils (`outils/`).
- huashu-motion (`om new`, `om check`, `om still`, `om sound`, `om render`, `om qa --sheet`) par `sh <outils>/lancer.sh om …`.
- video-director : la méthode en étapes et ses contrôles (`check_timeline.py`, `qa_video.py`).
- Format : 1920 × 1080, 30 i/s pour les rendus de travail ; master 3840 × 2160 après validation.

## Comment prouver
- Avant de construire : `TREATMENT.md`, puis trois images clés regardées.
- Après chaque rendu : `om qa --sheet` regardée (et à 360 px de large), `tenues.mjs`, `qa_video.py` sur le mixage final.
- Les trois notes d'un directeur exigeant (forme, rythme, vérité), corrigées, puis un seul nouveau rendu.
- Ne rien affirmer qui n'a pas été vu ou mesuré.

## Format du rapport de l'agent
1. Ce qui est fait, chemins complets (MP4 et planche).
2. Ce qui a été vérifié et comment.
3. L'histoire en une phrase, les décisions prises et le plan le plus faible.
4. Ce qui reste incertain.

## Leçons des agents
- [À compléter après chaque film : ce qui a raté, comment on l'a vu, la règle qui l'évite.]
