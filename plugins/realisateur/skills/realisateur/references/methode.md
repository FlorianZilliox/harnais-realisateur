# La méthode : faire un film court écrit en code

Tirée de la fabrication de trois films de démonstration d'agents IA (60 à 100 s chacun, projetés devant un comité de direction), et de leurs nombreux allers-retours. Elle vaut pour toute vidéo ; les quelques règles propres aux films qui montrent un outil ou un agent le disent. Chaque règle vient d'une version refusée. Les nombres sont des points de départ, et on s'en écarte exprès, jamais par accident.

## 1. Le cadre de travail

- **Un film = un dossier projet** (`om new <dossier>`), qui contient ses fichiers de fond : `TREATMENT.md` (l'histoire), `timeline.json` (chaque moment en secondes), `TEXTES.md` (tous les textes à l'écran et leurs tenues), `FACTS.md` (chaque chiffre et chaque affirmation, avec sa source), `materials/` (les vraies captures et vidéos).
- **Une consigne permanente par projet**, lue par chaque agent qui travaille sur les films (modèle : `consigne-modele.md`). Elle porte ce qui est décidé, et on la met à jour à chaque retour : un agent neuf qui la lit doit pouvoir reprendre sans rien redemander.
- **Une chose à la fois, montrée dès qu'elle est montrable.** Une image clé validée avant le film entier, un film validé avant les deux autres. Jamais une série entière d'un coup.
- **Garder les versions validées, numérotées** (`out/film-v8.mp4`), et faire le ménage des rendus intermédiaires une fois la version validée.

## 2. Avant de construire : chercher, pas improviser

- Regarder ce que font les meilleurs sur ce genre de film (`references-motion.md`, puis deux ou trois références proches du sujet, regardées image par image). Juger le résultat face à eux, pas seulement « est-ce que ça marche ».
- Le film de référence est une **barre de qualité, jamais un style à copier** : en reprendre les effets (sphères, halos, dégradés) donne un pastiche.
- **Trois directions** qui diffèrent par le langage du mouvement ou la matière, pas seulement par la couleur, chacune en une vraie image clé. La personne choisit, puis on n'y revient plus.
- Le thème graphique de l'entreprise (ses couleurs, sa police, son gabarit) bloque la créativité d'un film : un film qui doit marquer a sa propre direction.

## 3. L'histoire

- **Du storytelling, pas un catalogue** : une tension, un tournant, une chute. Une seule idée par film, et rien à l'image ne doit lui voler l'attention.
- **Jamais d'ouverture sur une heure d'horloge** (« 9 h 30 », « chaque matin à… ») : c'est un tic, il se voit dès le deuxième film. Le déroulé se raconte en étapes et en durées.
- **Aucune date à l'écran** (ni jour, ni mois, ni trimestre) : le film vieillit mal et ouvre des débats. Ce qui est futur se dit « Prochaine étape : … » et se dessine en contour.
- **Le public d'abord.** Si les spectateurs ne font pas le métier montré (une direction devant un film de chefs de projet), chaque phrase doit se comprendre sans le connaître : des mots simples et complets, pas des ellipses de métier (« Tout avance. Sauf un. » ne dit rien à qui ne lit pas un tableau de tâches). Un mot du métier s'explique une fois (« le daily : le point d'équipe de chaque matin »), sinon on prend le mot courant (une tâche plutôt qu'un ticket).
- **Un film dans une présentation ne répète pas les slides** : les slides cadrent (la question, le contexte, la cible), les films montrent. Chaque film finit sur son propre message.
- **L'impact plutôt que l'inventaire** : faire comprendre ce que la chose montrée change (un produit, un outil, une méthode, un agent), pas énumérer ce qu'elle fait. Pour un outil ou un agent, un garde-fou n'a sa place à l'écran que s'il montre comment il travaille (il demande la donnée qui manque, il signale un biais, il repère sa propre erreur, il attend l'accord de la personne). Une propriété de sécurité (« rien ne quitte l'ordinateur ») n'en dit rien.
- **Mieux, pas forcément plus vite** (outil ou agent) : le moment fort est la qualité (la bonne question, rien d'oublié, la donnée demandée plutôt qu'inventée, le biais trouvé). Les gains de temps restent petits et au second plan.
- **Le temps est compté** : si le film passe dans une intervention de quelques minutes, chaque seconde doit servir le message. Raccourcir est presque toujours un progrès.

## 4. La vérité à l'écran

- **Le waouh par la forme, jamais par la promesse** : lumière, mouvement, rythme, vrai écran mis en scène ; aucun superlatif.
- Chaque chiffre vient de `FACTS.md`, avec des mots pas plus forts que la source (« estimation de la PO » si c'en est une).
- **Aucune interface inventée pour ce qui existe** : on reconstruit d'après les vraies captures. Ce qui est imaginé porte la mention « Exemple » ou se dessine en contour. Un extrait accéléré affiche son facteur.
- **Raconter ce qui se passe sous le capot** (outil ou agent) : les vraies lignes qu'il lit et écrit, ce qu'il attend, refuse ou rate. C'est ce qui rend une démonstration crédible.
- **Rien de nominatif** sauf accord : « une PO », « une PM ». Retirer des écrans reconstruits les noms, prénoms, chemins (`/Users/...`), adresses, noms de fichiers sensibles. Aucun nom d'outil ou de licence mis en avant sans l'accord de celui qui présente.

## 5. La forme

- **Pas de bruit** : ni libellés décoratifs, ni logo répété, ni particules, ni grain gratuit, ni halo. Peu d'éléments, un seul accent de couleur par plan, réservé à ce qui compte dans le plan (dans un film d'agent : ce qu'il trouve).
- **Pas de voix off** quand le film doit tourner seul dans une présentation : tout se comprend à l'image et au texte, la musique et les effets portent le rythme. (Si une voix est voulue : `om voice`, voir les réglages de huashu-motion.)
- **Aucun personnage animé en code** : des silhouettes déplacées en papier découpé « ne bougent pas » et ruinent le film. Les personnes sont abstraites (un poteau, une ligne, une étiquette suspendue « une PO », un objet qui leur appartient), leurs décisions s'écrivent dans une typographie à elles (un italique à empattements). Dans un film d'agent, l'agent est une forme simple et claire (une sphère) et son cône de lumière à bord franc : c'est le seul acteur qui se déplace. Une silhouette plate ne se montre que de face ou de profil, jamais en plongée.
- **De l'espace, pas des aplats** : chaque scène construite en 3D (CSS `perspective`, plans à des profondeurs différentes), une caméra qui se déplace (plongée, travelling rasant, passage à travers un plan, du très large au très gros plan), des objets avec une épaisseur et une ombre nette.
- **Rendre visible ce que l'histoire dit** : une idée visuelle par acte, qui montre au lieu d'écrire (la tâche immobile n'a pas de trace de chemin ; elle s'enfonce sous les autres).
- **Un geste signature récurrent** (par exemple « soulever le capot » : une surface pivote sur sa charnière, dessous la couche machine, puis elle se rabat avec le résultat) et des **raccords par les objets** (la forme d'un plan devient l'élément du suivant).
- **Plusieurs films d'une même famille** : même grammaire, même mouvement, mêmes polices, même motif récurrent ; mais pour chacun une palette dominante, un monde et un dispositif d'espace, une musique et un objet d'ouverture et de fermeture propres, pour qu'on ne les confonde pas.
- **Montage** : 12 à 18 plans pour une minute, coupés sur les temps de la musique ; une dominante de couleur par acte, deux ou trois couleurs par plan.

## 6. La langue (français)

- **Accents partout**, majuscules comprises (À, É, Ê, Ç), vérifiés sur une image rendue : les polices de certains gabarits n'ont pas les accents.
- **Typographie française** : espace insécable avant « : », fine insécable avant « ; ? ! », guillemets « » avec espaces insécables, la même apostrophe partout. Jamais de tiret cadratin dans les textes à l'écran.
- **Du français écrit par un francophone**, pas un calque de l'anglais : articles présents, ordre des mots français, verbes français (« remettre en cause » plutôt que « challenger »). Les termes du métier restent tels que l'équipe les dit (daily, sprint, discovery).
- **L'anglais seulement s'il est réel** : une ligne de terminal ou un nom de fichier du vrai déroulé. Tout titre ou phrase de narration est en français.
- **Avant chaque rendu final**, tous les textes à l'écran dans `TEXTES.md`, relus un par un avec ces règles.

## 7. Le temps de lecture

- **« Lu deux fois »** : un texte reste en place au moins 2 s + 0,3 s par mot après la fin de son arrivée, sans qu'une autre phrase arrive pendant qu'il se lit. Le mesurer avec `outils/tenues.mjs` (image par image) plutôt qu'à l'œil : à la main, un film validé avait encore sept textes trop courts.
- Dans un segment ralenti, une montée prévue en 0,6 s dure 1,5 à 2,5 s : y raccourcir les montées.
- La règle vaut pour un film court et dense devant un public non initié. Sur un film long, une lecture plus lente que nécessaire lasse vite : caler sur le public, montrer, ajuster.
- Tout texte à lire fait au moins 40 px à 1920 px de large, mesuré sur l'image rendue (après zoom et perspective), et reste lisible sur la planche réduite à 360 px.

## 8. Le son

- **Une musique écrite pour le film** : une partition ABC dans `index.html`, jouée par `om sound` avec des instruments réels (exemple complet : `exemples/partition-jazz.py`). Un jazz élégant (contrebasse, piano, cordes, balais) a porté les films d'origine ; le genre se choisit selon le film, avec une couleur propre à chaque film d'une même famille.
- **La musique suit le récit** : presque silence sur le doute, vrai silence juste avant le temps fort, tutti sur le temps fort. Les `!mark:nom!` de la partition tombent sur les étiquettes `scene:nom` de la timeline.
- **Tout effet sonore fort reste sous le temps fort** : à revérifier après chaque recoupe de la partition.
- **Mixage final** : jamais `loudnorm` en mode dynamique (il écrase la dynamique et laisse passer la crête). Gain fixe vers −14 LUFS, puis limiteur : `outils/mixage_final.sh`, contrôlé ensuite par `qa_video.py` de video-director (−14 LUFS ± 1, crête vraie ≤ −1 dBTP).

## 9. Les pièges techniques

- **GSAP** : poser les états initiaux par `gsap.set` au chargement **et** par `tl.set(…, 0)` ; `fromTo` avec `immediateRender: false`, sinon des éléments apparaissent à 0 s.
- **Polices** : partir du gabarit `blank` et déclarer les polices par `om fonts add` (les gabarits « grammaire » ont des polices sans accents).
- `data-om-signature="off"` sur la racine pour tout film commandé ; jamais `om share` sans demande.
- Une ligne du décor 3D qui passe derrière une narration la fait paraître barrée : vérifier chaque phrase sur une image.
- La mesure d'immobilité de `om qa` ne voit pas une dérive lente sur des aplats sombres : juger aussi sur les images.
- Rendus de travail en 1920 × 1080 à 30 i/s, sans flou de mouvement ; le rendu final avec `om render --blur` ; un master 3840 × 2160 seulement après validation.
- Les MP4 lourds pour une présentation : réencoder en H.264 CRF 23 garde l'image (SSIM 0,99) pour une fraction du poids.

## 10. Prouver avant de montrer

- Avant de construire : `TREATMENT.md` (l'histoire en une phrase, l'accroche, le tournant, la chute, ce qu'on doit lire à chaque moment), puis trois images clés des plans les plus différents, faites avec le vrai code (`om still`) et regardées.
- `om check` à 0 erreur avant chaque rendu.
- Après chaque rendu : `om qa --sheet`, regarder la planche, et une image réduite à 360 px ; `tenues.mjs` ; `qa_video.py` sur le mixage final.
- Écrire les trois notes qu'un directeur exigeant donnerait (forme, rythme, vérité), les corriger, rerendre une fois.
- **Ne rien affirmer qui n'a pas été vu ou mesuré.** Dire ce qui n'a pas été vérifié.
