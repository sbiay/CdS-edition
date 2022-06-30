Atelier HTR 9 mai 2022
===

# Présentation de Transkribus
Günter Mühlberger (Université d’Innsbruck) et Maxime Gohier (Université du Québec à Rimouski)

## L'écosystème
- Traitement d'images
- Edition collecte de données, annotation, entraînement d'IA
- Reconnaissance IA
- Publication

Les applications :
- **T. ai** : utilisation gratuire, cliquer-glisser en interface web pure, conversion image-texte, 14 langues, sortie texte brut ()
- **T. Lite** : 
    - appli en ligne
    - interface intuitive
    - *majorité* des fonctionnalités les plus utilisées (HTR, segmentation, correction, gestion de collections, export) ; interface en 7 langues dont le français
    - Très utile pour la transcription participative
- **T. expert client** : pour les utilisateurs avancés, installation locale, Win Mac, Linux, toutes les fonctionnalités de T.
- **Metagrapho api** à installer sur serveur, pour gérer un flux de travail dans une institution travaillant sur des masses de données

- **Citizen-science** : participatif, en dév.

- **Scantent** : fonctionnant avec la tente à éclairage contrôlé

- **Read & Search** :
    - Recherche plein texte
    - Par *keyword spotting* (fouille dans les données non retenues dans la version finale de la transcription)
    - Affichage texte et image
    - Téléchargement à la page (pas trouvé pour la source complète)

## Les modèles publics
120 modèles p., toutes langues et époques confondues
- Incunables latins et grecs
- ms. néérlandais 17e-19e
- ms. néérlandais 17e-18e
- Modèle français + Schlegel : 17e-20e
- Techno NewsEye : segmentation d'imprimés de presse (Université de La Rochelle)

## Fonctionnement institutionnel
Read-Coop SCE
- 2016 consortium financé par l'UE
- 2019 fin du financement

Modèle coopératif privé, tous gains sont réinvestis dans la plateforme.

## Projet Nouvelle-France numérique
Rassembler et transcrire toutes les archives de la NF, 16e-18e s.
- Deux modèles publics (17e-18e) (ils sont réutilisables avec leurs données d'entraînement dans Transkribus mais les données ne sont pas ouverters) :
    - New France … : multi-mains (secrétaires et administrateurs), écr. rondes, bâtardes, coulées
    - Notaires des 17e-18e (grand volume de texte pour une seule main d'écriture) : performance optimale
- Ouverture des données : étant donné l'imperfection des données transcrites, on diffuse les données pour permettre un enrichissement au fil du temps (avec 5 niveaux de finalisation).

Usage collaboratif de Transkribus :
- Bonne gestion des coll. partagées dans l'interface T.
- Suivi exhaustif des versions sauvegardées
- Aucun risque de sauvegarde conflictuelle

**Balisage facile de métadonnées**, intuitif en *front* (XML en back)
On peut directement associer un passage balisé avec une URI (pour la récupération de métadonnées depuis des référentiels). Très intéressant pour baliser les entités nommées déjà enrichies dans les notices d'inventaire.

Outils de recherche et de fouille de texte :
- Plein texte : **Solr**, avec ou sans le mode fuzzy (contourne 2 à 3% d'erreur des prédictions)

## Crédits
La segmentation, l'entraînement sont gratuits.

Seul lancer un modèle sur un lot d'images est payant (système de crédits).

# Présentation d’eScriptorium
Peter Stokes (AOROC CNRS/ENS/EPHE)

Titre : *Introduction à la plateforme eScriptorium et la diversité des écritures : Source ouverte, données ouvertes, modèles ouverts*

## Kraken
Optimisé pour les écritures historiques rares et non latines

Avenir proche :
- Détection de l'ordre de lecture

Plus tard : 
- datation
- classification de styles

## eScriptorium
Conçu pour les chercheurs en SHS. 
Début en 2019, projet Scripta-PSL ; 

Bientôt :
- entraînement de la machine pour la séquence des lignes, réentraîner le modèle
- Balisage de texte
- Annotation graphique : annoter les images directement, sans nécessairement de lien au texte (données paléo, description d'élément non écrits)
- Recherche de texte
- Interface multilingue
- Alignement automatique des textes : une transcription préexistante et une image non segmentée

Défis d'écritures rares et diverses :
- Types d'écriture
- Directions d'écriture :
    - Sens
    - Diagonale
    - Circulaire
    - En spirale
- Ecriture sur la ligne de base

## Infrastructure
- Usage personnel : pas d'entraînement, un ordinateur suffit, ou GPU externe. Le problème va apparaître quand on voudra **entraîner un modèle sur des centaines de pages**. Il faudrait se rapprocher d'une institution pour bénéficier d'un serveur : le DHI devrait se rapprocher de Scripta PSL.
- Un seul projet : un serveur + GPU modeste pour une dizaine d'utilisateurs
- Un consortium de classe moyenne : utilise un cluster institutionnel

## Standards
- Le partage des modèles se fait sur Zenodo
- HTR-United, indépendant d'eScriptorium, pour partager les VT
- Segmonto

**Il faut proposer au DHI de s'associer au CREMMA pour bénéficier des capacités de calcul d'Inria (2 cartes graphiques et serveurs)**

# Débats
eScriptorium est dans une phase collaborative dont les bornes ne sont pas encore très bien posées. C'est un point critique de tous les projets Open-source :
- ajouter des fonctionnalités pour la publication ?
- veut-on des interfaces simplifiées pour téléphone portable ?
- comment prendre les décisions ?

Transkribus n'a pas non plus de feuille de route définie :
- Il y a deux mois a été lancé la **transcription de la musique** pour les documents médiévaux


# Tobias Hodel
Le défi de l'entraînement est de pouvoir généraliser pour des mains inconnues du set d'entraînement : de multiples mains issues d'un panel large du même type d'écriture.

Le taux d'erreur objectif est de **-5%**.

Comment gérer efficacement les abréviations :
- La techno est capable de faire une expansion des abréviations
- Mais le principe est contraire au principe de l'apprentissage des réseaux neuronaux

La meilleure qualité de reconnaissance est quand on reflète les caractères abrégés. Il est possible d'entraîner l'apprentissage de la résolution, mais si le développement prend +de 3 lettres, cela devient trsè compliqué, et la qualité de l'HTR perd en qualité.

On peut prendre une solution hybride : résoudre auto. les abré courte, ne pas résoudre les longues.

Comment ont-été traitées les abrév. dans les VT du 19e. pour HTR-United.

# Manuscrits hébreux : Daniel Stoeckl
Pour structurer le document en livre, chapitre etc., Stoeckl a utilisé l'insertion d'ajouts marginaux comme marqeurs de début de partie (annotation des zone des manchettes).