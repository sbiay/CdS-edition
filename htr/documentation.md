HTR
====
Plan :
1. Expériences d'HTR comparables
	1. Lectaurep
2. Comment s'y retrouver dans le corpus ?
3. Choisir un corpus d'entraînement
	1. Analyse paléographique du corpus
	2. Problématique
	3. Pistes méthodologiques
	4. Test de transcription de l'écriture CDS
4. Choisir des modèles HTR à entraîner
	1. Choix d'application

***

# <span style="color : rgb(015, 005, 230, 0.8)">Expériences d'HTR comparables</span>
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


# <span style="color : rgb(020, 080, 170, 0.8)">Analyse du corpus</span>
## Paléographie
- Ecriture de l'A. difficile à lire et reconnaître ;
- 4-5 mains : donc 4-5 algorithmes.
- Une partie de manuscrit à la BNF qui pourrait être de sa main.

## <span style="color : rgb(015, 005, 230, 0.8)">Organisation des sources</span>
- Peut-on trouver une cohérence de main en prenant un **filtre chronologique** ?
	- Par exemple l'année 1800, les lettres ayant pour auteur CDS : 29, soit 28 copies et 1 item sans type.

- On peut accéder aux **recueils complets** des lettres en format pdf sous le *Dokumenttyp* *band* :
	1. [1er volume](../recueils/2e-copie-01-CdS-b2-007z-0.pdf)
	2. [2e volume](../recueils/2e-copie-02-CdS-b2-0080-0.pdf) : La distribution des mains me paraît plus claire dans le 2e volume que dans le premier ;
	6. [6e vol.](https://constance-de-salm.de/wp-content/themes/pukeko-child/app/assets/vimg/CdS-b2-0084-0.pdf) me paraît plutôt homogène

Le **volume des recensions** est assez homogène sur le plan de l'écriture, mais ne concerne pas la correspondance [ici](https://constance-de-salm.de/archiv/#/document/11221).

# <span style="color : rgb(020, 080, 170, 0.8)">Problématique</span>
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

# Constituer des sous-corpus paléographiquement homogènes
## Main1
Les fichiers images sont issus de la même source que celle testée par HS : `CdS02_Konv002-02` ([Corres. générale, 2e vol., 2e t.](../recueils/2e-copie-02-CdS-b2-0080-0.pdf))
- 64-73
- 76-83
- 92-120

On ne s'est pas attaché à prendre des pièces entières mais à ne sélectionner que des doubles pages ne comportant qu'une seule main principale.

# <span style="color : rgb(020, 080, 170, 0.8)">Test de transcription de l'écriture CDS</span>
Je passe en revue les lettres de l'auteur de façon chronologique en commençant par les plus anciennes.

Les lettres sont de trois types : 
1. Original
2. Copie : *Abschrift*
3. Brouillon : *Entwurf*

Aucun *original* de CdS, mais **52 brouillons** (passage en revue depuis les plus récents). Le dépouillement des notices se trouve dans le fichier.

Voir le dépouillement dans le fichier `../brouillonsCDS.md`

# Segmentation et typage des zones
Les tests effectés dans le projet eScriptorium "CDS-correspGale-copie2-vol2" sur la main1 font apparaître une bonne segmentation des doubles pages.

Difficultés dans la reconnaissance des lignes :
- Les références placées en haut à gauche (avec la date et le nom de l'expéditeur), écrites en diagonale, ne sont pas toujours bien lues (lignes sectionnées en plusieurs morceaux) ; et **quel type leur donner ?** (voir l'ontologie de DAHN)
- **Corrections**  :CDS corrige certains mots de sa main
- Des mots soulignés
- Des rubriques : "autographe"

# Corrections
## Test sur main1
### Correction manuelle
Temps de correction manuel d'une double page : environ 25 min (c'est le cas de la p. 1).

### Correction automatisée
D'après la démarche expliquée dans {chiffoleauDAHNProject}, plus particulièrement [ici](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Documentation/Post-OCR%20correction%20for%20TEXT%20files.md#how-to-do-a-post-ocr-correction-for-text-files).

1. Exporter les prédiction HTR au format XML-Page (le format texte ne peut pas être réimporté dans eScriptorium) dans un [dossier dédié](./xmlPage/) ;
2. Créer un dossier destiné à héberger les dictionnaires Python qui seront générés par le premier script poru chaque fichier

Reprendre la correction du dictionnaire `DictCdS02_Konv002-02_0065.py` à la ligne 35