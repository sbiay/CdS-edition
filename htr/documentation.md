HTR
====
Plan :
1. Analyse du corpus
	1. Paléographie
	2. Organisation des sources
2. Problématique
3. Expériences comparables
	1. Lectaurep
4. Mettre en oeuvre des entraînements de modèles HTR
	1. Constituer des sous-corpus paléographiquement homogènes
		1. Main1
	2. Corriger les prédictions
		1. Correction manuelle
		2. Correction automatisée grâce aux scripts du projet DAHN
			1. Marche à suivre
			2. Développements et remarques
	3. Tester les performances du modèle entraîné par H. Souvay
	4. Réitérer les opérations pour d'autres sous-corpus
	5. Confronter les résultats avec ceux d'un autre modèle générique
5. Test de transcription de l'écriture CDS
6. Segmentation et typage des zones

***

# <span style="color : rgb(015, 005, 230, 0.8)">Analyse du corpus</span>
## <span style="color : rgb(020, 080, 170, 0.8)">Paléographie</span>
- Ecriture de l'A. difficile à lire et reconnaître ;
- 4-5 mains : donc 4-5 algorithmes.
- Une partie de manuscrit à la BNF qui pourrait être de sa main.

## <span style="color : rgb(020, 080, 170, 0.8)">Organisation des sources</span>
- Peut-on trouver une cohérence de main en prenant un **filtre chronologique** ?
	- Par exemple l'année 1800, les lettres ayant pour auteur CDS : 29, soit 28 copies et 1 item sans type.

- On peut accéder aux **recueils complets** des lettres en format pdf sous le *Dokumenttyp* *band* :
	1. [1er volume](../recueils/2e-copie-01-CdS-b2-007z-0.pdf)
	2. [2e volume](../recueils/2e-copie-02-CdS-b2-0080-0.pdf) : La distribution des mains me paraît plus claire dans le 2e volume que dans le premier ;
	6. [6e vol.](https://constance-de-salm.de/wp-content/themes/pukeko-child/app/assets/vimg/CdS-b2-0084-0.pdf) me paraît plutôt homogène

Le **volume des recensions** est assez homogène sur le plan de l'écriture, mais ne concerne pas la correspondance [ici](https://constance-de-salm.de/archiv/#/document/11221).

# <span style="color : rgb(015, 005, 230, 0.8)">Problématique</span>
- Le problème des recueils est l'hétérogénéité des mains sur la même page ?
- Peut-on regrouper des copies cohérentes de lettres ?
- Faut-il trouver une méthode de **segmentation particulière** ? Il n'est pas possible d'éditer plusieurs textes dans le même export XML : on veut pouvoir associer un texte unique avec ses métadonnées.
	- Comme on a déjà le début de la lettre, peut-être pourrait-on faire reconnaître la fin automatiquement ? car une lettre se termine toujours par une signature.
- Y aurait-il des idées à prendre dans le projet DAHN ? (non, purement en OCR).

Deux pistes méthodologiques se dessinent :
1. Rassembler dans un premier temps des lettres qui sont de **la même main**, pour voir quels sont les résultats. Hyppolite a fait plein d'essais : 
    - Comment les sources ont été sélectionnées et les 31 modèles entraînés ?
    - Quels ont été les résultats ? 
    - Quels sont après les expériences que l'on peut faire ?

2. Reprendre un modèle déjà entraîné à travailler sur plusieurs mains (l'option privilégiée par Lectaurep, cf. {chagueCreationModelesTranscriptiona}).

# <span style="color : rgb(015, 005, 230, 0.8)">Expériences comparables</span>
## <span style="color : rgb(020, 080, 170, 0.8)">Lectaurep</span>
> Quand on se lance dans une campagne de transcription reposant sur la reconnaissance d’écritures manuscrites, on passe généralement par une série de questions qui sont les mêmes d’un projet à l’autre. Parmi ces questions, il y a celle des modèles de transcription et de leur rapport à la variation des écritures. Doit-on entraîner un modèle pour chaque type d’écriture présent dans un corpus de documents ? Au contraire, peut-on se contenter d’entraîner un seul modèle tout terrain (qu’on appellera mixte ou générique) ? {chagueCreationModelesTranscription}

Différentes méthodes employés :
1. "ne traiter que quelques notaires lisibles et dont les scribes sont restés constants"
    - Constat sur le corpus d'entraînement : "Nous nous sommes aperçus, sans surprise, que la densité du texte a un impact sur la quantité de pages qu’il faut transcrire pour obtenir de bons résultats".
    - Chiffre à prévoir pour l'amélioration des performances : "il semblait nécessaire de prévoir de transcrire manuellement 200 pages (ou plus) pour certains notaires avant de parvenir à un modèle à peu près efficace".

2. Acquisition d'un modèle mixte, puis utilisation des vérités terrain créées pour en augmenter les performances ;
    > Au-delà du score de précision fourni par Kraken à la fin des cycles d’entraînement, **nous nous interrogions sur la capacité du modèle à généraliser son apprentissage à d’autres écritures**. La question était alors de savoir si un modèle mixte est plus robuste qu’un modèle unique face à des données légèrement différentes. Derrière la notion de **robustesse**, nous entendons la capacité d’un modèle à maintenir une transcription correcte malgré l’apparition d’écritures qui n’étaient pas présentes dans le set d’entraînement. Ce sont ces éléments inconnus du modèle que l’on appelle les données hors-domaine {chagueCreationModelesTranscription}.

3. Entraînement d'un modèle mixte {chagueCreationModelesTranscriptiona} :
    - Corpus d'entrîanement :
        - Quantité : "480 fichiers XML, correspondant chacun à une page de répertoire" ;
        - Limite de la qualité des données : "aucune de ces transcriptions n’avait été relue en totalité. Cette vérité de terrain comportait donc non seulement des erreurs de transcription, mais également des omissions non résolues, généralement marquées par une suite de “X” ou de “?”"{chagueCreationModelesTranscriptiona}.
    - Optimisation du temps de calcul : "les modalités de chargement des images par Kraken ont été revues dans le code source, de manière à effectuer plusieurs chargements en parallèle" {chagueCreationModelesTranscriptiona} ;
    - Résultats mauvais : 67% de précision dans un premier temps ;
    - Pour obtenir de meilleurs résultats, modification du *learning rate* (ou vitesse d’apprentissage) et de l’architecture des réseaux de neurones employée (exprimée en spécifications VGSL).
    - Temps de calcul nécessaire : "Comme on a plus d’images et que le learning rate est plus petit, le modèle a besoin de plus de époques d’entraînement, ce qui ralentit l’ensemble du processus . Pour obtenir notre modèle à 91%, il nous a ainsi fallu compter 16h pour l’apprentissage" {chagueCreationModelesTranscriptiona}.
    - Résultat : le modèle `generic_lectau26`. Serait intéressant de l'obtenir (**il est volontiers partagé**).

# <span style="color : rgb(015, 005, 230, 0.8)">Mettre en oeuvre des entraînements de modèles HTR</span>
Il s'agit dans un premier temps d'augmenter le volume des vérités de terrain pour améliorer les performances du modèle entraînés par H. Souvay.

## <span style="color : rgb(020, 080, 170, 0.8)">Constituer des sous-corpus paléographiquement homogènes</span>
### <span style="color : rgb(000, 200, 100, 0.7)">Main1</span>
Les fichiers images sont issus de la même source que celle testée par H. Souvay : `CdS02_Konv002-02` (Corres. générale, 2e vol., 2e t. - [ici en local](../recueils/2e-copie-02-CdS-b2-0080-0.pdf)). La liste des images est contenue dans le fichier [main1-liste-images.txt](./main1-liste-images.txt).

On ne s'est pas attaché à prendre des pièces entières mais à ne sélectionner que des doubles pages ne comportant qu'une seule main principale (quelques corrections de la main de CDS apparaissent ponctuellement).

## <span style="color : rgb(020, 080, 170, 0.8)">Corriger les prédictions</span>
### <span style="color : rgb(000, 200, 100, 0.7)">Correction manuelle</span>
Temps de correction manuel d'une double page : environ 25 min (c'est le cas de la p. 1).

### <span style="color : rgb(000, 200, 100, 0.7)">Correction automatisée grâce aux scripts du projet DAHN</span>
#### <span style="color : rgb(050, 100, 060, 0.7)">Marche à suivre</span>
D'après la démarche expliquée dans {chiffoleauDAHNProject}, plus particulièrement [ici](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Documentation/Post-OCR%20correction%20for%20TEXT%20files.md#how-to-do-a-post-ocr-correction-for-text-files), on procède ainsi :

1. Exporter les prédictions HTR au format XML-Page dans un [dossier dédié](./xmlPage-aCorriger/) ;

2. Créer un [dossier](./dictPages/) destiné à héberger les dictionnaires Python qui seront générés par le premier script pour chaque fichier représentant une double page ;

3. Appliquer le [script](./py/spellcheck_texts_PAGEXML.py) d'analyse des mots dans le fichier XML :
	```shell
	python3 py/spellcheck_texts_PAGEXML.py ./xmlPage-aCorriger/ ./dictPages/
	```

4. Corriger à la main les entrées du dictionnaire de chacun des fichiers générés dans le dossier `./dictPages/` ;

5. Regrouper les dictionnaires produits dans un seul fichier (**pas de script pour cela**) ;

6. Appliquer le dictionnaire de correction aux fichiers XML grâce à ce [script](./py/text_correction_XML.py) :
	```shell
	python3 py/text_correction_XML.py ./xmlPage-aCorriger/ ./xmlPage-corrigees/
	```
7. Réimporter les fichiers corrigés dans eScriptorium :

8. Corriger manuellement les résultats

#### <span style="color : rgb(050, 100, 060, 0.7)">Développements et remarques</span>
##### <span style="color : rgb(080, 080, 050, 0.7)">Exporter les prédictions HTR au format XML-Page</span>
On a écarté le format texte, qui ne peut pas être réimporté dans eScriptorium.

##### <span style="color : rgb(080, 080, 050, 0.7)">Appliquer le script d'analyse de mots spellcheck_texts_PAGEXML.py</span>
Les corrections sont plus nombreuses sur des prédictions HTR que sur des prédictions OCR, surtout en l'état actuel du modèle encore peu entraîné. La correction est donc un travail conséquent.

Développement réalisés :
1. On a donc développé le script pour afficher le contexte du mot et en conserver la mémoire, ce qui limite les allers-retours entre le dictionnaire à corriger et l'image ou la prédiction d'origine ; le contexte est en effet déterminant pour valider ou modifier une correction proposée automatiquement.

2. On mobilise désormais les ressources du dictionnaire des corrections déjà validées (dictCDS) avant de parser le dictionnaire gloabl de la langue française (dictionnaireComplet). Cela permet de :
	- Réduire le temps de calcul ;
	- Ne pas travailler sur des corrections déjà identifiées comme ambiguës (*id est* ayant deux contextes différents en compétition).

A faire :
- Mobiliser les vérités de terrain afin de ne pas rechercher dans tout le **dictionnaireComplet** les formes déjà validées. 

##### <span style="color : rgb(080, 080, 050, 0.7)">Corriger à la main les entrées des dictionnaires pour chaque fichier</span>
- Temps de correction initial : 35 min pour une double page.
- Il faut veiller à ne produire que des corrections dépourvues d'ambiguïtés et applicable en toutes circonstances. Si le modèle lit "celle" pour "cette", seule une correction manuelle peut y remédier ; le risque du dictionnaire est de remplacer automatiquement ailleurs des prédictions justes par le terme trouvé. Il ne faut pas oublier que le remplacement des mots par le dictionnaire est indépendant du contexte du mot.
- La présentation du contexte du mot développée au point précédent facilite cette tache de validation des corrections proposées par le script **spellcheck_texts**. 

##### <span style="color : rgb(080, 080, 050, 0.7)">Regrouper les dictionnaires produits dans un seul fichier</span>
Cette opération se fait pour l'instant à la main, elle est facilement automatisable mais suppose de **faire attention** à ne pas effacer d'anciennes corrections par de nouvelles corrections : certaines formes mal reconnues seront ambiguës, car pouvant se résoudre dans des mots différents selon les contextes. Il faudra donc les neutraliser et conserver la mémoire de cette neutralisation.

Lui consacrer un script permet de contrôler les nouvelles entrées du dictionnaire :
- Si la clé existe (la forme est déjà référencée par le dicttionnaire) :
	- Si le lemme est différent : c'est un conflit, on propose en sortie, pour l'utilisateur, une comparaison des lemmes et des contextes ; on lui indique ensuite la marche à suivre :
		1. Ouvrir dictCDS ;
		2. Changer le lemme en `None` ;
		3. Ajouter le contexte présent à la liste des contextes ;
		4. Supprimer la clé du dictionnaire en cours d'intégration ;
		5. Relancer le script.
	- Si le lemme est identique : on intègre l'entrée au dictionnaire en remplaçant le contexte par le plus récent ;

##### <span style="color : rgb(080, 080, 050, 0.7)">Appliquer le dictionnaire de correction aux fichiers XML (text_correction_XML.py)</span>
Développements effectués :
- Les modifications étant nombreuses, il a fallu adapter le script afin de *tokéniser* les mots à remplacer.

##### <span style="color : rgb(080, 080, 050, 0.7)">Réimporter les fichiers corrigés dans eScriptorium</span>
- Attention, il faudrait transformer les **esperluettes** pour éviter des problèmes de lecture du XML.

##### <span style="color : rgb(080, 080, 050, 0.7)">Corriger manuellement les résultats</span>
- **J'en suis ici** : reprendre la correction du fichier [texte](./correctionManuelle/CdS02_Konv002-02_0066-corr-auto.txt), l. 40.

## <span style="color : rgb(020, 080, 170, 0.8)">Tester les performances du modèle entraîné par H. Souvay</span>

## <span style="color : rgb(020, 080, 170, 0.8)">Réitérer les opérations pour d'autres sous-corpus</span>

## <span style="color : rgb(020, 080, 170, 0.8)">Confronter les résultats avec ceux d'un autre modèle générique</span>
On testera le modèle entraîné par le projet Lectaurep.

# <span style="color : rgb(015, 005, 230, 0.8)">Test de transcription de l'écriture CDS</span>
Je passe en revue les lettres de l'auteur de façon chronologique en commençant par les plus anciennes.

Les lettres sont de trois types : 
1. Original
2. Copie : *Abschrift*
3. Brouillon : *Entwurf*

Aucun *original* de CdS, mais **52 brouillons** (passage en revue depuis les plus récents). Le dépouillement des notices se trouve dans le fichier.

Voir le dépouillement dans le fichier `../brouillonsCDS.md`

# <span style="color : rgb(015, 005, 230, 0.8)">Segmentation et typage des zones</span>
Les tests effectés dans le projet eScriptorium "CDS-correspGale-copie2-vol2" sur la main1 font apparaître une bonne segmentation des doubles pages.

Difficultés dans la reconnaissance des lignes :
- Les références placées en haut à gauche (avec la date et le nom de l'expéditeur), écrites en diagonale, ne sont pas toujours bien lues (lignes sectionnées en plusieurs morceaux) ; et **quel type leur donner ?** (voir l'ontologie de DAHN)
- **Corrections** : CDS corrige certains mots de sa main. Il faut pouvoir poser une balise qui s'exporte avec la transcription afin de permettre de savoir à la lecture du fichier TEI, qu'il y a une correction à ajouter (Floriane Chiff. le faisait et ajoutant un symbole `££`) ;
- Des mots soulignés
- Des rubriques : "autographe"
- Des notes de bas de page (CdS02_Konv002-02_0066)

