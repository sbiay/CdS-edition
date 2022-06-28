Documents anciens et reconnaissance automatique des écritures manuscrites, colloque sur l'HTR qui se tiendra les 23 et 24 juin 2022 à l'École nationale des chartes, Paris
====
***
# Organisateurs
Comité d’organisation : Ariane Pinche et Floriane Chiffoleau

Comité scientifique : Jean-Baptiste Camps, Alix Chagué, Thibault Clérice, Frédéric Duval, Vincent Jolivet, Benjamin Kiessling, Nicolas Perreaux, Ariane Pinche, Laurent Romary, Peter Stokes.

# Archive vidéo
- Le 23 juin : https://www.youtube.com/watch?v=dE1XUXiuitU

- Le 24 juin : https://www.youtube.com/watch?v=YORfV0yIsQg

# Argument
Nombre de projets incluent aujourd’hui une étape d’acquisition automatique du texte dans leur chaîne de production ou d’exploitation des données. Plusieurs plateformes de transcription et différents moteurs HTR sont maintenant disponibles. L’intégration de cette technologie dans des chaînes de traitement de plus en plus efficaces a entraîné une automatisation des tâches qui remet en question la place du chercheur dans le processus d’établissement du texte. Cette nouvelle pratique, gourmande en données, rend pressant le besoin de rassembler, et donc d’harmoniser les corpus nécessaires à la constitution de corpus d’entraînement, mais aussi leur mise à disposition pour améliorer la qualité des résultats de l’HTR. 

Dans le cadre du projet CREMMALab soutenu par le DIM MAP, l’École nationale des chartes (centre Jean Mabillon) en partenariat avec le LAMOP et le LabEX Hastec organise les 23 et 24 juin 2022 un colloque mêlant questions philologiques et techniques pour faire un état des lieux scientifique de l’HTR pour les documents anciens. Nous ferons le point à cette occasion sur l’HTR et ses outils, ses résultats, ses apports et les nouvelles pratiques qu’induit son utilisation dans les projets d’édition et d’exploitation des documents. Cet événement permettra de rassembler une communauté internationale de chercheurs, aujourd’hui grandissante, pour échanger autour de l’usage de l’HTR dans leurs projets scientifiques. Enfin, ce colloque repose sur la volonté de traiter la thématique de l’HTR tout en l’articulant à des problématiques scientifiques de constitution et/ou d’exploitation des corpus. Nous souhaitons également questionner les aspects pratiques de l’utilisation de cette technologie (développement de moteur HTR, d’interface de transcription, d'interface utilisateurs pour utiliser et entrainer des modèles, etc.), tout en soulevant ses enjeux méthodologiques et son impact sur les données de la Recherche.

# Programme détaillé
## Jour 1 : 23 juin

### Discours d'ouverture et présentation des projets CREMMA et CREMMALAB
Elsa Marguin-Hamon, directrice de la recherche et des relations internationales, École nationale des chartes

#### Mes notes
L'infrastructure CREMMA est prête à être ouverte au public (sur inscription par voie institutionnelle)

CREMMA est un lieu de réflexion pour l'hamonisation des pratiques de segmentation et de transcription. 

Adoption d'ontologie et de schémas de données communs
Rédaction d'un guide de transcription pour les documents médiévaux (différent du CR du séminaire ?), jusqu'aux incunables et imprimés anciens
Communauté européenne : Portugal, Italie, Suisse, France ; ainsi que partenaires nord-américains

### CremmaLab projects: Transcription guidelines and HTR models for French medieval manuscripts
Jean-Baptiste Camps, maître de conférence, École nationale des chartes, CJM
Ariane Pinche, post-doctorante, École nationale des chartes, CJM

#### Résumé
L’étape d’acquisition du texte est première dans la plupart de nos entreprises de recherche, qu’il s’agisse d’édition de texte, d’études linguistiques, philologiques et historiques, ou de traitement massif de corpus. Pour produire des corpus textuels de qualité, il est crucial de pouvoir partager librement, en en garantissant l’interopérabilité, les données que nous produisons, et, in fine, de proposer à la communauté scientifique des modèles réutilisables. Pour répondre à ces besoins, et plus spécifiquement aux besoins des médiévistes, le projet CREMMALAB propose des réflexions méthodologiques sur les protocoles de transcriptions des corpus afin d’optimiser des modèles d’HTR à travers la rédaction d’un guide de transcription et la mise à disposition de modèles d’HTR. Nous présenterons les premiers résultats de ces travaux à travers le traitement de deux corpus massifs : un corpus de romans de chevalerie et un corpus de textes hagiographiques, pris en diachronie (xiiie‑xve siècle).

#### Mes notes
Plusieurs initatives financées par le DIMMAP et l'INRIA
- CREMMA : offrir un serice d'accès à eScriptorium, en part. avec Sripta

- CREMMA LAB : projet d'APinche
	- Réflexion sur la meilleure façon de produire des données
	- Irriguer une communauté de chercheur de plus en plus grande
	- Proposer des solutions aux institutions patr. de + en + intéressées par ces technologies 
	
	- Mise à disposition de vérités de terrain : 21000 lignes de transcription
	- Outil de validation de conformité HTRUC
	- ChocoMufi : validation des caractères unicode utilisés pour les carac. spéciaux
	- Catalogue HTR-United et publication sur Zenodo
	- Mettre en place des Guidelines pour tenter des modèles génériques, robustes sur de grands nb de documents, pour réduire le temps de création des données pour chaque projet nouv. (INSISTER sur le fait que la généricité repose sur des règles communes et PERMET une meilleure réutilisation (efficacité de la généricité))
	- Proposer une succession d'étapes pour le traitement des textes (pour bien sauvegarder chaque étape, améliorer chacun des outils indépendamment)
	
	- Des préconisations simples :
		- Ne pas imiter les formes de lettres pour les docs médiévaux
		- Conserver les abrév. (le développement dépend du contexte, de la scripta) : meilleure généricité (la prédiction est distinguée du déve. des abrév.) : proposition d'une table de caractères unicode recommandés
		- Pas  de distinction du IJ UV (ATTENTION on l'illustre toujours avec un exemple où il n'y a pas de u initial en forme de v...)
	- Modèles :
		- Arabica (corpus de thèse d'A Pinche
		- Bicerin
		- Cortado : en cours de développpement : inètgre des incunables Gallicorpora

Il faut faire attention aux scores : si le corpus d'entraînement est fondé sur des documents  similaires : hors-domaine, c'est moins bon.
Bicerin a été amélioré (avec une accuracy plus faible) en ajoutant des choses très différentes.
Plus les données d'entraînement sont variées et non même rien à voir, plus le meilleur est souple
Le modèle de langue peut avoir une influence sur la prédiciton : il faut varier les thèmes des sources pour une meilleure ROBUSTESSE (attention, robustesse et souplesse , plasticité, sont utilisés un peu synonymes)

POUR avoir des bons scores, il n'est pas la peine de spécialiser les données d'entraîenemnt (on peut mélanger les langues romanes sans problèmes).

CAMPS :
Création d'un corpus de fictions littéraires fr. du XIe s. à nos jours : "From Roland to Conan", DH Tokyo 2022
cf. PC Langlais, article publié
- Coeur du corpus XVIe-XVIIe romans numérisés sur Gallica (cote Y2 du cata. Nic. Clément)
- Ajout par Google books des romans du même corpus (la médiocrité de la qualité de reprod. n'est pas trop problém. pour les imprimés)
- Ms. méd. en  gothique (variété d'écriture) + incunables

#### Discussion
Est-ce qu'un modèle générique n'est pas bon à rien ?
Il y a déjà beaucoup de variété ; Prochaine étape : avoir un très vaste jeu de données de validation, pour savoir où ajouter des données
L'équilibre n'est pas encore trouvé entre généricité et acuité particulière.

Des carac. pour les lettrines ?
Pose de gros problèmes de reconnaissance
On séloigne de l'HTR pour se rapproche de la segmentation : faut-il traiter la lettrine différemment ? Segmonto tente de poser des règles

Des calculs d'acuité au niveau du mot ? 
Pour l'instant, la sortie HTR est totalement détachée du post-traitement. Il y aura un autre modèle de deep learning pour la lemmatisation des mots, leur normalisation.
Ne se sont pas lancés dans une étape de correction : trop de variété graphique et linguistique, ça n'aurait pas de sens.
Les scores de Kraken sont au niveau du caractère.
Le taux d'erreur par mot ou la distribution des erreurs sur la page pourrait être intéressant.

L'influence de la qualité des images sur le taux de reconnaissance (bruit dans les images, etc.)
Ont tenté de dégrader artificiellement des images pour voir si le modèle s'entraînait mieux : pas flagrant du tout

Erreur caractère => erreur mot
Le taux d'erreur va bcp monter. Mais veut-on tout corriger ? les erreurs ont une signification. Est-ce que certaines erreurs sont corrigées par le modèle
IL Y A UN MODELE DE LANGUE dans la reconnaissance des caractères
La post-correction ne pose pas de problème si ou conserve les documents intermédiaires.

### Modélisation et affinage HTR pour les ms méd. : stratégies et évaluation
Sergio Torres Aguilar, post-doctorant, École nationale des chartes, CJM
Vincent Jolivet, responsable de la mission projets numériques, École nationale des chartes

#### Résumé
In this presentation we intend to explore different practical questions about HTR modeling in order to determine at what point a model reaches the necessary robustness and a sufficiently broad-level of generalization to serve as a pre-trained base to raise a new specialized model. For this end, we use several HTR ground-truth documents from medieval cartularies and registers ranging from 12th to 15th centuries and we will evaluate two aspects: (1) the creation of robust models by trying to calculate the learning break‑point and the minimum amount of ground truth necessary to achieve good generalization performances from a limited collection of documents and (2) the process of fine‑tuning in the aim to quickly specialize a robust model, used here as a pre-trained base, on a type of source other than those used during training.

#### Mes notes
Sources à 90% en latin, pas de modèle HTR pour la cursiva, textualis, prégothique, semihybride ; mise en page particulière, des listes en marge, dates, titres, etc.

Normalisation de la VT : multi langue fr. et lat.

Corpus HOME-ALCAR publié sur Zenodo

Tests toujours sur les cartulaires que les modèles ne connaissent pas

Le modèle est capable de distinguer, dans chaque source, les types d'écriture, au niveau de la ligne, le TYPE d'ECRITURE, avec un seul modèle : classification aut. des types d'écriture
Des techniques importées de l'imagerie médicale
Modèle nommé Xception lancé en 2017

Comme indiqué dans le résumé : méthodologie en deux temps : 
1. entraînement d'un modèle robuste par production de VT et test toujours hors domaine ; la courbe d'apprentissage se tasse à l'approche de 90%, qui est le seuil de lisibilité ; 
2. puis observation du fait que le fine-tuning fait gagner tout à coup 8 points

Vincent Jolivet : l'époque est révolue de la production de VT à chaque nouveau projet
- On repère un modèle existnant : transfer learning : le partage est essentiel (contribution de Stutz, Cremma, HTR-United avec le catalogue)
- On adapte : fine-tuning par la production de VT
	- Quelle quantité ? Quelle est la méthode pour optimiser cette étape ? La réponse n'est pas trouvée : la décision est empirique : dépend des ressources disponinbles (les paléographes sont rares), évaluer le gain attentdu (seuil de 90%), quelle est la précision que l'on veut ?
	- Avec 90% d'acuité, l'effort de production de VT ne vaut plus la peine, après il vaut mieux investir dans le post-traitement : c'est là dessus qu'il faut porter l'effort, et envisager des solutions de partage et mutualisation
	- Comment traiter des sources hétérogènes ?  Ont proposé une méthode de classification auto d'écriture. Identifier automatiquement l'écriture pour déclencher automatiquement le bon modèle d'HTR (on arrive à 85% d'acuité de bonne reconnaissance). La classif. des écritures se fait zone par zone, mais eScriptorium ne permet d'appliquer qu'un modèle page par page ; on voudrait pouvoir appliquer des modèles zone par zone. Mais à la fin, il faut des modèles efficaces pour chaque type d'écriture, ce n'est pas encore le cas. GENERICITE des modèles : sur les 12 types d'écritures proposés par les paléographes (mais cela dépend de l'étendue du corpus - dixit Smith - mais l'échelle serait encore différente si l'on prenait tous les ms. de Gallica), sont-ils tous utiles pour l'HTR ? Des modèles sont portables d'un type d'écriture à l'autre.
	
#### Discussion
Jolivet : En réalité, il est compliqué de définir ce qui est dans le domaine et ce qui est hors domaine : cela mobiliserait vraiment les appréciations des paléographes. IL FAUT QUE JE DISE QUE MON TEST HORS DOMAINE N'EST PAS VRAIMENT HORS DOMAINE MAIS SUR DES CHOSES TRÈS PROCHES

### Une cursive du 17e siècle
Élodie Paupe, assistante-doctorante, université de Neuchâtel et chargée de projet pour les AAEB

#### Résumé
Le projet « Crimes et châtiments » (2022-2025) a pour objectif la numérisation et la transcription des procédures criminelles de l’ancien Évêché de Bâle (1461-1797). Dans le cadre de la phase pilote en cours de réalisation du projet, un modèle HTR est développé sur une série de procès de sorcellerie dont la majorité des documents sont écrits en cursive française par le prévôt Henri Farine, actif entre 1580 et 1618. Après avoir présenté les particularités de cette main et le corpus, un retour d’expérience sera donné autour des deux infrastructures utilisées (Transkribus et eScriptorium) et du recours aux méthodes de binarisation sur des documents manuscrits. Pour conclure, l’efficience du modèle « Farine » sur des documents contemporains d’autres mains sera présentée, ainsi que les pistes de développement poursuivies.

#### Mes notes
env. 110 000 pages ; faire l'inventaire détaillé, à la pièce, numérisation coul. HD, dévelp. modèle HTR, mise en ligne des num. et transcriptions
Corpus de départ de 57 pages d'une seule main, prévôt Farine, main facile à lire et attestée dans 3500 docs en tout (1580-1618)
Pas encore de modèle pour la segmentation
Main très cursive : cursive fr. assez régulière, quelques traits communs avec une écriture germ., quelques diacritiques, allographes rendus par un seul carac. (S) ; Variété des jambages des m et n 
Viser la lecture par un public qui n'est pas forc. acad. : permettre la lecture des sources
- Maj. rendues
- Appréciation du transcripteur pour les maj. min. 
- Restitution de la valeur moderne IJ UV
- Développement des abréviations
- Césures et apostrophes fidèles à la source

Retours d'expérience des applications Transkribus et Fondue, l'instance genevoise d'eScriptorium
- Transkribus : facilité d'utilisation pour les chercheurs (transfert ensuite vers Fondue et Kraken) ; utilisation de la VT pour faire un modèle de 0
	- de 0 CER de 11% avec 57 p de VT : seuil de lecture non atteint
	- Test d'un modèle récupéré, dév. sur des chartes (avec dév. d'abrév.) : lisait très bien certains termes mal lus : affinage de ce modèle => CER de 5.69% LECTURE POSSIBLE, mais pas encore satisf.
	- Réentraîné avec le dév. de toutes les abrév. => CER 4.68%  BEAUCOUP MOINS DE PROBLEMES HORS ABRÉVIATIONS tout le modèle a été amélioré
	- Test sur d'autres mains de la même époque : CER de 29% sur une main plus archaïque ; de 44% sur encore une autre main

- Kraken : même jeu de documents
	- de 0 avec accuracy de 75%
	- Tentative de binarisation : altère bcp de documents (fait diminuer l'acuité)
	- Modification de l'architecture d'apprentissage de Kraken => acuité de 85%
	- Modification du param. -r (vitesse d'apprentissage) : grosse influence
	- Pas de modèle disponible sur Kraken pour cette cursive 16e-17e

### Un modèle ouvert pour la reconnaissance automatique des manuscrits du théâtre espagnol du Siècle d’Or
Cuéllar Álvaro, PhD Student, University of Kentucky

#### Résumé
Le projet ETSO, Estilometría aplicada al Teatro del Siglo de Oro (Cuéllar et Vega García-Luengos 2017-2022) (https://etso.es/), se propose de collecter et d’analyser à travers des techniques stylométriques le plus grand nombre de pièces de théâtre espagnol du Siècle d’Or. Un nombre important de ces textes ne se retrouvent que dans des témoignages manuscrits, pour lesquels il a fallu entreprendre un processus de transcription automatique à l’aide de Transkribus. L’entraînement du modèle « Spanish Golden Age Manuscripts (Spelling Modernization) 1.0 » a nécessité 3 250 116 mots et il est capable de moderniser automatiquement le texte, en obtenant un Character Error Rate (CER) de 10,54 % dans le validation set. Grâce à ce modèle, nous avons pu transcrire quelque 400 manuscrits de pièces du Siècle d’Or. Parmi tous les textes, un a retenu l’attention : La francesa Laura. Cette pièce de théâtre anonyme a été alignée stylométriquement avec l’ensemble du corpus du dramaturge Lope de Vega (1562-1635).

#### Mes notes
Des milliers de textes, de nbx problms d'attribution
Dév. d'un projet de stylométrie : ETSO

1300 pièces collectées avec une orthographe modernisée
Des centaines de textes non numérisés existaient encore ; l'OCR donnait de très mauvais résultats
Transkribus : jugé formidable pour le projet  ; modèle déve. avec 99% d'acuité
Besoin de la modernisation ortho. : création de règles automatiques de transformation
Tentative d'entraînement du modèle avec cette modernisation : utilisation de la fonction Text2IMage : associe une transcription existante avec une image => 96 % d'acuité
Capacité de détecter les ITALIQUES => Il faut que je dise que pour les parties soulignées , J'AI TROP PEU DE DONNÉES D'ENTRAÎNEMENT

Pour la stylométrie, les textes fonctionnaient aussi bien que des textes édités.

Il n'est pas possible d'indiquer quels sont les mots propres à un auteur ; ce sont des calculs statistiques capables de mettre en rapport des mots fréquents combinés et des petites différences entre des combinaisons.

### New Developments in Kraken and eScriptorium
Benjamin Kiessling, ingénieur de recherche, PSL
Peter Stokes, directeur d’étude, EPHE

#### Summary
Recent releases of Kraken (v4) and eScriptorium introduce a number of new features that improve user experience and performance. The presentation will introduce the most important ones such as the new training library, binary datasets, and new layer types for Kraken, and annotation and text search for eScriptorium, as well as integration of both into Biblissima+. We will elaborate how these impact the use of the software in a variety of contexts, such as institutional and individual use, differences in dataset and target corpus size, etc. In addition, we will look briefly at subsystems in development such as a new algorithm for trainable reading order.

- A venir pour la segmentation : intégration de l'ordre des lignes dans l'entraînement du modèle
- Recherche de termes
- Balisage TEI basique
- annotation graphique
- Alignement automatique d'un texte existant

Dév. à plus long terme
- Bibliossima + nouvelle infrastructure

Version 4 (stable)
- Nouvelle bib. d'entraînement, meilleure accssibilité de l'API
- Amélioration des performances des modèles de reconn.
- Nouvelle layout analysis basée sur Transformers, CurT : archi. très nouvelle ; 
	- il est possible de segmenter des lignes qui se croisent
	- La détection de l'orientation des lignes est plus ROBUSTE (**intéressant pour moi**)
	- inférence plus rapide, et peut être accélérée avec des GPU (infrastructure très exigeante cependant)
	- d'autre tâches peuvent être ajoutées : détection de l'ordre de lecture, etc.
- Reconstruction de lacunes
- Apprentissage non-supervisé 

### De Transkribus à eScriptorium : retour(s) d’expérience sur l’usage d’outils d’HTR appliqués à un corpus d’imprimés espagnols du XIXe siècle
Élina Leblanc, post-doctorante, unité d’espagnol, faculté des lettres, université de Genève
Pauline Jacsont, collaboratrice scientifique, unité d’espagnol, Faculté des lettres, université de Genève 

#### Résumé
Dans cette communication, nous présenterons la chaîne éditoriale mise au point pour le projet *Démêler le cordel*, en vue d’élaborer une bibliothèque numérique dédiée à la collection d’imprimés éphémères espagnols du xixe siècle de la Bibliothèque universitaire de Genève (1000 in-quarto). Notre chaîne éditoriale a pour particularité d’avoir eu recours à deux outils d’HTR, Transkribus et eScriptorium, dont nous proposerons une analyse en termes d’usages à différentes étapes d’un projet.

Dans un premier temps, nous décrirons la collection d’imprimés, en insistant sur ses spécificités et ses enjeux dans un contexte de transcription automatique. Puis, nous reviendrons sur notre expérience avec chacun des outils d’HTR employés, sur les raisons qui nous ont conduites à passer de l’un à l’autre et sur les difficultés rencontrées. Pour conclure, nous présenterons l’exploitation des prédictions HTR sur notre site web, développé avec TEI‑Publisher.

- Importance de l'image gravée
- Difficultés particulières
	- Numérisation des images en BD
	- Impression déjà de basse qualité (encre, transparence, coquilles, bavures)
	- Multitude de fontes
	- Mise en page très variée
- Choix du corpus d'un seul imprimeur : objectif de publier ce corpus en 18 mois

Utilisation de Transkribus pour la facilité d'installation

Rejoint les tests de la plateforme Fondue 

### Lettres en lumières
Florian Fizaine, doctorant, archives départementales de la Côte-d’Or
Édouard Bouyé, directeur des archives départementales de la Côte-d’Or

#### Résumé
Dans le cadre du projet « Lettres en lumières » mené par les Archives départementales de la Côte-d’Or en partenariat avec le Laboratoire d’étude de l’apprentissage et du développement (LEAD, Université de Bourgogne), nous développons un outil de HTR en utilisant Mask RCNN, un algorithme de segmentation d’instance utilisé notamment dans le médical, pour la segmentation des lignes et les réseaux transformer qui ont largement montré leur efficacité dans la compréhension du langage naturel, pour la transcription. Nous avons commencé ce travail sur les registres des états de bourgogne du xviiie siècle, ces données d’entraînements sont obtenues grâce à la participation de transcripteurs bénévoles.

#### Mes notes
- Approche contributive (associée à des cours de paléographie)
- Fonctionnement habituel de l'HTR : 1 couche LSTL intégrant un modèle de langue et une lecture séquentielle
- *Vision transformer encoder* (méthode élaborée par Google) : encoder/decoder
- Segmentation fonctionnant sur le principe du Mask-RCNN (une boîte pour chaque forme ou chaque ligne de l'image), pas spécifique de la segmentation des lignes ; ne fonctionne pas sur les *baselines* ; c'est un masque non orienté

### Les archives inquisitoriales (Portugal) sous HTR : le projet TraPrInq (Transcribing the court records of the Portuguese Inquisition, 1536-1821)
Hervé Baudry, chercheur au CHAM-Centro de Humanidades (Universidade Nova de Lisboa). Responsable du projet TraPrInq.

#### Résumé
Le projet TraPrInq a pour objectif de créer un modèle d’HTR. Une partie des archives inquisitoriales portugaises (Arquivo Nacional da Torre do Tombo, Tribunal do Santo Ofício, 1536‑1821) est constituée de procès, au nombre de plus de 40 000. Près de la moitié de ce sous-fonds a été numérisée. Le modèle générique en cours d’élaboration sur la plateforme Transkribus par une équipe d’une dizaine de paléographes permettra la transcription à grande échelle des documents. La présente communication établit en premier lieu un état d’avancement des travaux à l’issue des cinq premiers mois d’activité : particularité du corpus, mode de travail, obstacles rencontrés et solutions adoptées, premiers résultats (données d’entraînement). En outre, comme il semble prématuré de dresser un bilan général, elle s’attache à décrire la démarche adoptée, ses évolutions, ainsi qu’à réfléchir sur les aspects techniques et humains des moyens mis en œuvre et des objectifs à atteindre.

#### Mes notes
- Consituer 5000 p. de VT et création d'un modèle robuste
- Obj. édition TEI
- Grande variété paléographique ; mains récurrentes des notaires
- Des pièces nombreuses et brèves insérées dans les dossiers de procès
- Variété également des supports (tissu)
- Mélange de langues (y compris des inclusions de caractères arabes ou hébreux)
- Mise en page avec d'importantes notes marginales
- Pas de développement des abréviations (en raison de la pratique propre au portugais)
- **Il n'est pas possible d'exporter un modèle entraîné sur Transkribus**

### Segmentation Mode for Archival Documents with Highly Complex Layout
Daniel Stökl Ben Ezra, directeur d’étude, EPHE
Marina Rustow, professor, Princeton University
Devorah Witty, software developper, The Research software compagny

#### Summary
Using eScriptorium together with kraken as an infrastructure, we developed a simple but highly efficient procedure for reducing the amount of human labor necessary for creating large amounts of segmentation ground truth for documents with highly complex layouts, i.e documents comprising regions with lines at eight different angles. Our specific project deals with medieval documents in Hebrew script in Judeo‑Arabic, Aramaic and Hebrew from the Cairo Genizah, including letters, legal documents, lists, notes and accounts. There are about 40,000 documentary texts from the Genizah, of which only about 5,000 have been transcribed. Therefore, our current aim is to create enough data to be able to train a global segmentation model with a very large number of classes, so that it can segment complex layouts in a single step.

#### Mes notes
- Geniza Lab
- Très vaste typologie de documents
- Mises en page simples :
	- lignes horizontales, mais avec des lacunes potentiellement nombreuses
	- Des ajouts interlinéaires
	- Signatures avec ornements
	- Lignes intersectionnelles
	- Donner des statistiques n'a pas de sens tant que l'on ne constate pas le résultat appliqué à un corpus de validation particulier.
- Mises en page complexes :
	- Marges avec l'écriture orientée tête en bas et disposition giratoire : ce sont à la fois des types de région et de lignes différents
	- Des lignes simplement tête en bas 

Deux méthodes :
1. 8 modèles avec rotation de 45° pour chacun : pas besoin de VT d'entraînement
2. 1 modèle sans rotation, avec correction à la main et application d'une ontologie pour chaque orientation (cf infra)

- Méthode avec entraînement :
	- Classification des types de layout
	- Appliquer un modèle spécifique à chaque type
	=> Mais des schémas récurrents ont été repérés ; un type de région pouvait, indépendammant de la conception SEMANTIQUE du texte, être appliqué à une région selon sa position et orientation (ontologie dont les types de région sont des disposition et orientation de texte, en somme des configurations du texte ; identique pour les types de lignes) **CELA CONFIRME L'INTERET D'AVOIR UN TYPE DE REGION ET DE LIGNE PARTICULIER POUR LE HEADER DES LETTRES**

### SegmOnto – A Controlled Vocabulary to Describe Historical Textual Sources
Simon Gabay, maître-assistant, université de Genève
Ariane Pinche, post-doctorante, École nationale des chartes, CJM
Kelly Christensen, docteure, INRIA

#### Summary
Our initiative aims to design a controlled vocabulary for the description of the layout of textual sources: SegmOnto. Following a codicological approach rather than a semantic one, it is designed as a generic typology, coping with a maximised number of cases rather than answering specific needs. Systematise the layout description has a double objective: on the one hand it facilitates the exchange of annotated data and therefore the training of better models for image segmentation (a crucial preliminary step for text recognition), on the other hand, it allows the development of a shared post-processing workflow and pipeline for the transformation of ALTO or PAGE files into DH standard formats such as RDF or TEI.

## Jour 2 : 24 juin

### FoNDUE - A Lightweight HTR Infrastructure for Geneva
Simon Gabay, maître-assistant, université de Genève
Pierre Künzli, Jean-Luc Falcone, (Christophe Charpilloz) (SciCoz)

#### Summary
Recognising text on an image is becoming increasingly important for scholars working with textual sources. Because institutions have to address the needs of their members, the University of Geneva has decided to offer a free of charge and user-friendly solution based on eScriptorium. The specificity of our instance is that it relies only on local infrastructures to minimise its cost and offer additional services, such as training models directly with command lines. Therefore, it promotes a double empowerment: the one of the institution, that does not depend on external private solutions, but also the one of scholars, who gain new digital skills. On top of a theoretical reflexion on this empowerment, we propose a first feedback on how to deploy an efficient HPC-based instance of eScriptorium.

#### Mes notes
- Données sensibles, accès aux données, anonymisation : comment protéger les données quand on fait de l'HTR ? Il est problématique de travailler sur des softwares hebergés dans un pays étranger.
- Coût par page : très élevé étant donné l'infrastructure
- Les résultats doivent être parfaitement reproductibles : maîtriser l'intégralité du résultat **En termes scientifiques, on doit pouvoir livrer toutes les données du processus**
- Que coûte le changement d'outil si nécessaire ? Comment enseigner ces outils (et donc les mettre à disposition) ; comment les déployer localement pour donner de la flexibilité aux équipes

- Infrastructure CREMMA : 3 GPUs (plus de 10 000 euros pièce), puis il faut les renouveler fréquemment
- Geneve : cluster de l'université ("HPC", 150 GPU) => donne accès à une autre interface que CREMMA : les infrastructures permettent notamment de sortir de l'infrastructure eScriptorium

- Qu'est-ce qu'un cluster de calcul ? Interconnexion d'ordinateurs avec CPU, avec un réseau très rapide ; tous accès aux mêmes données ; système de gestion des ordinateurs pour le fonctionnement en synergie (on se connecte seulement à un frontend, qui gère les calculs selon les machines disponibles : "Slurm")
- Applications concernées : météo, mécanique des fluides (simulation de la circulation sanguine), rendu d'un film en 3D
- Limitations : plateformes simples (ligne de commande), pas fait pour communiquer avec d'autres serveurs (comme eScriptorium) ; difficultés d'administration
- eScriptorium est développé en Python-Django
- Multi-processing : outil Celery (garder l'application active quand un processus gourmand est lancé)
- Le temps d'exécution des entraînements n'est pas proportionnel au nb d'images : il n'est pas en l'état calculable de manière simple.
- La performance est optimisée par la rechrche d'un équilibre entre temps de calcul par image et nombre de tâches lancées en parallèle

### From HTR to Critical Edition: A Semi-Automatic Pipeline
Daniel Stoekl Ben Ezra, directeur d’étude, EPHE
Hayim Lapin, professor, University of Maryland, College Park
Bronson Brown-Devost, post-doctoral researcher, Scripta Qumranica Electronica
Pawel Jablonski, PhD student, EPHE

#### Summary
This paper describes a pipeline for the creation of critical editions of literary texts from manually corrected HTR results of distinct manuscripts as prepared in the Sofer Mahir project. 
The Sofer Mahir project produces manually corrected transcriptions of 16 large medieval Hebrew codexes of all six main works of Tannaitic Rabbinic literature, redacted in the third or perhaps fourth century CE in Galilee. 
These works comprise Mishnah (~200k tokens), Tosefta (~300k tokens), Mekhilta deRabbi Yishmael (~80k tokens), Sifra (~120k tokens), Sifre Numbers (~60k tokens) and Sifre Deuteronomy (~60k tokens). 
Each work is extant in between 3 (Mishnah and Tosefta) to 5 witnesses (all others). 

- Très nbses agglutinations : 1 token peut comprendre + de 6 mots !
- Intertextualité riche
- **Patrick Sahle Text wheel** : schéma pour les finalités de numérisation de textes
- COMMENT ALLER DE LA HIERARCHIE DU DOCUMENT SOURCE A CELLE DU TEXTE ? Les différents témoins du texte n'ont pas la même mise en page, apparat, en somme hiérarchie de document
- Comment gérer les élts interlinéaires ? Ils sont distingués entre deux qui doivent s'insérer dans le texte (correction) et les autres (**méthode pas expliquée**)
- Utilisation de Dicta's Synopsis pour la comparaison synoptique des textes longs : canonical versification, résolution des abrév., correction automatique des témoins les uns par les autres, annotation linguistique (lemmatisation)
- Publication avec exist-DB

### Analyse, Reconnaissance et Indexation des manuscrits cham
Anne-Valérie Schweyer, chercheuse CNRS, Centre Asie du Sud-Est (CASE-EHESS-INALCO),
Jean-Christophe Burie, professeur des universités, Université de La Rochelle
Tien Nam Nguyen, doctorant, Université de La Rochelle

#### Résumé
Le cham ancien a été la langue véhiculaire utilisée dans des inscriptions gravées dans tout le centre du Vietnam du vie au xviie siècle. Le cham ancien a ensuite été remplacé par le cham moyen, la langue d’une riche collection de manuscrits écrits entre les xviie et xixe siècles dans le Centre-Sud du Vietnam et au Cambodge. Afin d’éviter la disparition de ces écritures alpha syllabiques, le projet CHAMDOC, projet pluridisciplinaire, regroupant des chercheurs en SHS et en informatique, vise à concevoir des méthodes et des outils innovants basés sur l’intelligence artificielle pour extraire, reconnaitre, translittérer et indexer les caractères Cham. Nous présenterons les travaux en cours et les premiers résultats.

#### Mes notes
- Langue en voie de disparition ; système alphasyllabique
- Conditions de conservation difficiles (papier brun, tâches) : des possibilités de restition automatique
- Des évolutions paléographiques entre le Ve et le XVe siècle ainsi que des évolutions du système vocalique
- Des langues et des vocabulaires différents (pas d'intercompréhension)
- Nécessité d'un débruitage des images : si trop de diacritiques, ne fonctionne pas
- Fonction de *coût adapté* pour la segmentation des lignes : à partir du milieu de la ligne, il pose un masque sur les signes qui se déploient au-dessus et en-dessous

	

### Expérimentations pour l’analyse automatique de sources chinoises anciennes
Marie Bizais-Lillig, maître de conférences, université de Strasbourg, 
Chahan Vidal-Gorène, doctorant, École nationale des Chartes et EPHE

#### Résumé
Dans cette présentation, nous nous proposons de rendre compte d’une expérience de transcription automatisée de textes xylographiés de la Chine impériale, à partir d’un très petit jeu de données (50 images). Bien que particulièrement lisibles, ces documents très denses présentent un double défi pour les HTR tant au niveau du sens de lecture du contenu que du très grand nombre de caractères différents à reconnaître, variété impossible à représenter en apprentissage. Le propos questionnera tout d’abord les choix de transcription réalisés et leur impact sur la capacité des modèles à apprendre efficacement en situation de one-shot learning, puis nous aborderons la question du sens de lecture du résultat produit et des différentes approches mises en place avec et sans apprentissage machine.

#### Mes notes
- Le chinois ancien représente 54 000 caractères (4000-5000 dans le jeu de données) ; tous ne sont pas dans Unicode (l'ajout est problématique : on ne sait pas toujorus ce qu'il y a derrière un code; plusieurs projets d'enrichissement sont concurrents… mieux vaut normaliser)
- 7000 glyphes de départ : il peut exister plusieurs glyphes pour un caractère (styles diff.), avec des décisions impériales qui établissent des modes pour un règne : **normalisation indispensable**
- Des caractères tabous (on n'écrit pas le nom de l'empereur de son vivant)
- Des versions cursives des carac. officiels
- Des textes à glose, des caractères servant de rubrique

- La reconnaissance des caractères se passe en fait bien

- La segmentation, les sens de lecture posent plus de problème
	- Approche par *baseline* dans un premier temps (par conformité aux autres jeux de données)
	- Problème des colonnes verticales avec possibilité de doubles colonnes
	- Gros problème de gestion du rapport entre texte et glose (déséquilibre du centroïde, ligne baselin tracée au centre)
	- Autre démarche : *bounding-box* et non de *baseline* pour identifier les doubles colonnes, puis distinction des types de contenus pour travailler par régions cohérentes

- Seulement 50 images : comment spécialiser une architecture
	- Il n'y a pas les mêmes glyhes dans les corpus de train et de validation
	- La majorité des caractères sont des hapax, certains ne sont pas vus à l'apprentissage
	- Mise en place d'une méthode dév. pour l'arabe : entraînement d'un modèle classique (extraction de caractéristiques sommaires des glyphes)
	- A partir des carac. extraites, on génère des faux glyphes à partir d'un vaste corpus de texte ramassé sur le web, pour générer les glyphes qui manquaient
	- Affinage d'un second recognizer à partir des faux caract. ou plutôt pour reconnaître des séquences de caractères (modèle de langue)
	- Aboutissement à une acuité de 93% ; seulement 14% d'erreur pour les glyphes inconnus

- Choix de la **normalisation linguistique**
	- La finalité est de suivre l'utilisation de portions de texte à travers les siècles

### Sharing HTR datasets with standardized metadata: the HTR‑United initiative
Alix Chagué, doctorante, EPHE, Université de Montréal, Inria
Thibault Clérice, responsable pédagogique du master TNAH, École nationale des chartes, CJM

#### Summary
Since some scholars adopted Ocropy in the mid-2010s, production of HTR or OCR ground truth has seen an impressive and steady growth. However, few projects share their gold dataset, and when they do, they are scattered across many different hosting options (Github, zenodo, gitlab, institutional repository, etc.) making them very hard to find. For reuse, when they are "discovered", their description is often lacking crucial details. The HTR-United initiative is an answer to this problem: with a standardized metadata schema, a curated catalogue and tools focusing on helping them through every step, owners can now easily publish and make their dataset findable.

- Le catalogue existe en version machine et en interface utilisateur
- Il n'existait pas de méthode de description des VT
- Format : **YAML**, même potentiel (et conversibilité) que Json, mais plus grande souplesse de la syntaxe d'écriture
- Export automatique vers Zenodo
- Les métadonnées
	- titre, lien, description
	- license et format de fichier
	- Software utilisé
	- … **revoir la diapo**
	- Statistiques : nb de mots, de lignes, etc.

- Les gens veulent souvent exploiter des jeux de données différents, qui soient compatibles
- HTRUC
- HTRVX : conformité XML et Segmonto
- HUMG(enerator) : computing metrics : un outil en ligne de commande pour créer des badges avec les valeurs statistiques.
- ChocoMufi : pour les usages des Unicode, qui contrôle et corrige (il liste tous les caractères existants, puis établit ceux qui correspondent au même caractère, et ceux validés par CREMMA)
	- Permet de conserver une diversité d'usage mais de conserver les choses compatibles

- Avenir : 
	- Construire plus de filtres pour améliorer le référencement des caractéristiques
	- Mise en oeuvre de *guidelines* pour la transcription
	- Construire un écosystème au-delà du catalogue : Elargir à la bibliographie relative aux projets HTR
	
#### Discussion
- Visualiser les images : pose problème de la limite technique pour la récupération et la gestion de la taille des images (supposerait de faire porter un poids aux utilisateurs)
- Des dépôts d'échantillons ? (temporalité de construction des corpus) : les jeux de données déjà petits sont très utiles ; la démarche de dépôt peut même être incrémentale ; la plupart des jeux de données sont en cours d'enrichissement
- Recenser des données non distribuées (car les droits ne sont pas ouverts) ? Il est possible de publier des donnée sous requête de consultation sur Zenodo.

### EpiSearch. Recognising Ancient Inscriptions in Epigraphic Manuscripts
Federico Boschetti, researcher; Institute for Computational Linguistics “A. Zampolli” – CNR, Pisa / VeDPH, Ca’ Foscari University of Venice
Tatiana Tommasi, MA student; Ca’ Foscari University of Venice

#### Summary
The project focuses on epigraphic codices as a proof of concept for putting digital tools at the test, thus defining new ways for the integration of large epigraphic collections. As a sample, we use the epigraphic manuscript composed by the learned ecclesiastical antiquarian Giovanni Antonio Astori (Venice, 1672-1743) and preserved in the Marciana National Library in Venice: Marc. lat. XIV, 200 (4336). In the first part of our talk, we analyse the life of the author and the characteristics of his manuscript. In the second part, we focus on the following tasks:
a) evaluating the accuracy of eScriptorium on epigraphic manuscripts with training sets of different size, in order to estimate the best trade-off between the human effort to prepare the training sets and the human effort to correct the results;
b) mapping legacy manual transcriptions on the manuscript facsimile
c) improving the layout analysis for epigraphic manuscripts.

- Seulement 11 feuillets ; enrichissement de la VT par des ms. complémentaires de l'auteur pour la reconnaissance de la cursive. Jeu enrichi par les dépôts HTR-United.
- Segmentation au niveau de la granularité du mot pour les inscriptions dessinées, et même au niveau du glyphe (par un entraînement over-fitted du modèle de seg.)

### HTR of Handwritten Paleographic Greek Text as a Function of Chronology
Platanou Paraskevi, postgraduate student, Athens University of Economics and Business

#### Summary
Today classicists are provided with a large number of digital tools which, in turn, offer possibilities for further study and new research goals. In this paper, we explore the idea that old Greek handwriting can be machine-readable and consequently, researchers can study the target material fast and efficiently. The overall aim of this paper is to assess HTR for old Greek manuscripts. To address this statement, we study and use images of the Oxford University Bodleian Library Greek manuscripts. By manually transcribing images, we have created and present here a new dataset for Handwritten Paleographic Greek Text Recognition. The dataset instances have been organized by establishing as a leading factor the century to which the manuscript and hence the image belongs. In this way, the HTR performance can reveal century-specific challenges when it comes to Handwritten Paleographic Greek Text Recognition.

#### Mes notes
- Minuscule et cursive
- Pas d'espace entre les caractères
- Des ligatures

Analyse du type d'erreur selon les siècles pour dégager des caractéristiques d'évolution de l'écriture (?) jusqu'au XVe-XVIe s. ; le classement des fautes permet d'objectiver ces évolutions : 
- imbrication de caractères

#### Discussion
- Méthode de gestion des abréviations ?

### Reconnaissance et extraction d’informations dans des tableaux manuscrits historiques : vers une compréhension des recensements de Paris de l’entre‑deux guerre
Thomas Constum, doctorant, LITIS EA4108, université Rouen Normandie

#### Résumé
Le projet POPP, Projet d’Océrisation des Recensements de la Population Parisienne (S. Brée et al, 2022) vise à constituer une vaste base de données à partir des recensements nominatifs de Paris de l’entre‑deux guerres, composés chacun d’environ 100 000 pages simples manuscrites sous forme de tableaux. Nous avons à ce jour traité les recensements de 1926, 1931, et 1936, ce qui représente un total d’environ 9 millions d’individus. Ce corpus est une source d’information primordiale pour les historiens, les démographes, les économistes ou les sociologues. L’objectif de notre communication est de décrire un système complet pour l’extraction d’informations de recensements historiques de la population. POPP est un projet qui a réuni des chercheurs en vision par ordinateur, en reconnaissance de formes et en démographie historique.

### Retour d’expériences sur l’utilisation comparée de plusieurs dispositifs de transcription numérique d’archives de fouilles archéologiques
Christophe Tufféry, ingénieur de recherche à l’Institut national de recherches archéologiques préventives, doctorant à CY Cergy Paris Université, en partenariat avec l’Institut national du patrimoine.

#### Résumé
Dans le cadre d’une thèse de doctorat engagée depuis 2019, nous proposons une étude historiographique et épistémologique des effets du numérique sur l’archéologie et sur les archéologues sur les cinquante dernières années, une période pendant laquelle l’archéologie a vu ses méthodes modifiées par l’introduction progressive de la micro-informatique dès le terrain. Cette recherche s’appuie sur notre expérience comme archéologue depuis la fin des années 1970 et sur notre activité à l’Inrap depuis 2010. Nous avons exploité plusieurs archives de chantiers de fouilles dont celles d’un chantier sur lequel nous avons été fouilleur bénévole entre 1980 et 1988. Nous avons procédé à la numérisation de deux cahiers de fouille. Nous avons ensuite procédé à leur transcription numérique avec trois solutions techniques différentes et complémentaires, dont eScriptorium, qui présentent des avantages et des limites techniques et méthodologiques. Nous avons pu ensuite exploiter les résultats de la transcription avec diverses méthodes et outils numériques.

# Ma synthèse
Dans le cadre du projet CREMMALab soutenu par le DIM MAP, le centre Jean-Mabillon (École nationale des chartes), en partenariat avec le LAMOP et le LabEX Hastec, a organisé les 23 et 24 juin 2022 un colloque intitulé *Documents anciens et reconnaissance automatique des écritures manuscrites*[^1].

[^1]: Comité d’organisation : Ariane Pinche et Floriane Chiffoleau. Comité scientifique : Jean-Baptiste Camps, Alix Chagué, Thibault Clérice, Frédéric Duval, Vincent Jolivet, Benjamin Kiessling, Nicolas Perreaux, Ariane Pinche, Laurent Romary, Peter Stokes.

Ce colloque a été l'occasion de rassembler une communauté scientifique représentant internationalement les pays du sud de l'Europe (France, Italie, Grêce, Portugal, Suisse) et quelques partenaires nords-américains autour des enjeux, des finalités, des problèmes et des solutions d'avenir de la reconnaissance automatique des écritures manuscrites ou HTR [@marguin-hamonDiscoursOuverturePresentation2022]. Il a ainsi illustré les différentes facettes du projet CREMMA-Lab : favoriser une réflexion sur la meilleure façon de produire des données ; irriguer de ses réflexions une communauté de chercheurs qui ne fait que croître autour des enjeux de l'HTR ; proposer des solutions aux institutions patrimoniales qui sont de plus en plus intéressées par ces technologies [@campsCremmaLabProjectsTranscription2022].

### Des finalités et des publics multiples
Les finalités de l'HTR sont multiples. Elle concerne aussi bien les scientifiques qu'un public élargi aux savants et aux curieux. Les projets *Crimes et châtiments* et *Lettres en lumières* [@paupeCursive17eSiecle2022] et  [@fizaineLettresLumieres2022] ont illustré l'intérêt de l'HTR pour donner accès à la lecture des textes en dehors du monde académique ou pour le développement de projets de transcription contributive.

Pour le public scientifique, l'HTR est en mesure de rendre accessibles des données selon plusieurs modalités. 
Le projet POPP (Projet d’Océrisation des Recensements de la Population Parisienne) a montré comment elle permet de construire de vastes bases de données par l'extraction d’informations de recensements historiques de la population dans les textes analysés [@constumReconnaissanceExtractionInformations2022].
Le projet Sofer Mahir a proposé une méthode pour l'établissement d'éditions critiques impliquant une quinzaine de témoins [@stoklbenezraHTRCriticalEdition2022], ce qui impose de passer par une étape de structuration de la hiérarchie du documents à partir de témoins n'ayant pas tous la même mise en page.
Les travaux de thèse de doctorat de Christophe Tufféry [@tufferyRetourExperiencesUtilisation2022] ont montré quant à eux un exemple de développement d'application visant, à partir de la transcription des carnets de fouilles archéologiques, à proposer des visualisation des ces données permettant de comprendre l'histoire d'une fouille programmée.

Outre la mise à disposition des sources textuelles ou des données qu'elles contiennent, l'HTR offre des possibilités de traitement massif de ces données en ouvrant plusieurs finalités. Les *Expérimentations pour l’analyse automatique de sources chinoises anciennes* [@bizais-lilligExperimentationsPourAnalyse2022] ont montré l'intérêt de l'HTR pour suivre l'utilisation de textes à travers les siècles. Dans les domaines épigraphique et paléographique également, les algorithmes HTR servent d'outil à l'analyse des mots et des glyphes par [@boschettiEpiSearchRecognisingAncient2022] ; l'analyse des erreurs de reconnaissance des caractères est également exploitée afin dégager des caractéristiques d'évolution des écritures [@paraskeviHTRHandwrittenPaleographic2022].

Enfin le projet CHAMDOC a montré que l'HTR peut intervenir dans la préservation des langues écrites en péril, comme c'est le cas du cham ancien, langue véhiculaire utilisée dans des inscriptions gravées dans tout le centre du Vietnam du VIe au XVIIe siècle [@schweyerAnalyseReconnaissanceIndexation2022].

### Transkribus et eScriptorium
Le paysage des applications dédiées à l'HTR se partage depuis 2019 entre Transkribus (2016) et eScriptorium. Certains projets de recherche ont eu l'occasion de tester les deux applications [@leblancTranskribusEScriptoriumRetour2022] [@paupeCursive17eSiecle2022] et ainsi fait part de leurs expériences.
L'HTR, en particulier l'entraînement de modèles, est un processus exigeant de très grandes capacités de calcul, et donc des infrastructures coûteuses. L'infrastructure CREMMA ouvrira bientôt au public des institutions académiques partenaires une instance d'eScriptorium [@marguin-hamonDiscoursOuverturePresentation2022] dotée de trois GPU (*Graphics Processing Unit* ou unité de traitement graphique), chacune représentant en moyenne un coût d'une dizaine de milliers d'euros. L'infrastructure Fondue de l'université de Genève bénéficie quant à elle de la puissance du superordinateur (HPC) de l'université, doté de 150 GPU. La recherche des meilleures performances des entraînements de modèles consiste à trouver le bon équilibre entre temps de calcul par image et nombre de tâches lancées en parallèle [@gabayFoNDUELightweightHTR2022].

Les développements en cours de l'interface eScriptorium donneront lieu dans un avenir proche à une fonctionnalité de recherche des termes transcrits, à du balisage TEI basique, à la possibilité d'annotation graphique des pages, à l'alignement automatique d'un texte existant sur une image et à l'intégration de l'ordre des lignes dans l'entraînement des modèles de segmentation [@kiesslingNewDevelopmentsKraken2022].



## Produire des modèles
### Les domaines explorés
- Création d'un corpus de fictions littéraires fr. du XIe s. à nos jours : "From Roland to Conan", DH Tokyo 2022 ; Coeur du corpus XVIe-XVIIe romans numérisés sur Gallica (cote Y2 du cata. Nic. Clément) [@campsCremmaLabProjectsTranscription2022].

- Ecritures gothiques, avec e-NDP : Sources à 90% en latin, pas de modèle HTR pour la cursiva, textualis, prégothique, semihybride [@torresaguilarModelisationAffinageHTR2022].

- Une cursive du 17e siècle [@paupeCursive17eSiecle2022].

- Des projets abordent des sources variées à tous les niveaux :
	- [@baudryArchivesInquisitorialesPortugal2022]
		- Grande variété paléographique ; mains récurrentes des notaires
		- Des pièces nombreuses et brèves insérées dans les dossiers de procès
		- Variété également des supports (tissu)
		- Mélange de langues (y compris des inclusions de caractères arabes ou hébreux)

- Ecritures non latines
	- Cham [@schweyerAnalyseReconnaissanceIndexation2022]

- Cursives contemporaines :
	- carnets de fouilles archéologiques [@tufferyRetourExperiencesUtilisation2022]

### Affiner des modèles plutôt que repartir de 0
- Vincent Jolivet : l'époque est révolue de la production de VT à chaque nouveau projet [@torresaguilarModelisationAffinageHTR2022].
	- On repère un modèle existnant : transfer learning : le partage est essentiel (contribution de Stutz, Cremma, HTR-United avec le catalogue)
	- On adapte : fine-tuning par la production de VT
		- Quelle quantité ? Quelle est la méthode pour optimiser cette étape ? La réponse n'est pas trouvée : la décision est empirique : dépend des ressources disponinbles (les paléographes sont rares), évaluer le gain attentdu (seuil de 90%), quelle est la précision que l'on veut ?

### Convertir des textes
- Le projet Le projet ETSO, Estilometría aplicada al Teatro del Siglo de Oro : MODERNISATION de la graphie avec récupération d'éditions de textes ; tentative d'entraînement du modèle avec cette modernisation : utilisation de la fonction Text2IMage de Transkribus : associe une transcription existante avec une image => 96 % d'acuité

### Problématique des sources
#### Classification automatique des types d'écriture
- [@torresaguilarModelisationAffinageHTR2022] **Compléter avec les notes**

#### L'influence de la qualité des images
- [@leblancTranskribusEScriptoriumRetour2022] pointe des difficultés particulières
	- Numérisation des images en BD
	- Impression déjà de basse qualité (encre, transparence, coquilles, bavures)

- CREMMA LAB : ont tenté de dégrader artificiellement des images pour voir si le modèle s'entraînait mieux : pas flagrant du tout [@campsCremmaLabProjectsTranscription2022].

#### Avec des données lacunaires
- [@bizais-lilligExperimentationsPourAnalyse2022]

### Le défi technique de la segmentation
- [@stoklbenezraSegmentationModeArchival2022]

### Ingénierie avancée
- Personnaliser Les techniques d'apprentissage : A joué un rôle important pour Le projet « Crimes et châtiments » (2022-2025) :
	- Modification de l'architecture d'apprentissage de Kraken => acuité de 85%
	- Modification du param. -r (vitesse d'apprentissage) : grosse influence [@paupeCursive17eSiecle2022]

- Nouveautés
	- [@kiesslingNewDevelopmentsKraken2022]
	- [@fizaineLettresLumieres2022]

## Partager les données
### Partager des vérités de terrain
- Mise à disposition de vérités de terrain : 21000 lignes de transcription [@campsCremmaLabProjectsTranscription2022].
- Mise à disposition de modèles d’HTR 
	- Arabica (corpus de thèse d'A Pinche
	- Bicerin
	- Cortado : en cours de développpement : inètgre des incunables Gallicorpora [@campsCremmaLabProjectsTranscription2022].

- HTR-United [@chagueSharingHTRDatasets2022]

### Pour des données génériques
- POUR avoir des bons scores, il n'est pas la peine de spécialiser les données d'entraîenemnt (on peut mélanger les langues romanes sans problèmes)
[@campsCremmaLabProjectsTranscription2022].

- Il faut faire attention aux scores : si le corpus d'entraînement est fondé sur des documents similaires : hors-domaine, c'est moins bon ; Bicerin a été amélioré (avec une accuracy plus faible) en ajoutant des choses très différentes. Plus les données d'entraînement sont variées et non même rien à voir, plus le meilleur est souple [@campsCremmaLabProjectsTranscription2022].

- Le **modèle de langue** peut avoir une influence sur la prédiciton : il faut varier les thèmes des sources pour une meilleure ROBUSTESSE (attention, robustesse et souplesse , plasticité, sont utilisés un peu synonymes) [@campsCremmaLabProjectsTranscription2022].

- L'équilibre n'est pas encore trouvé entre généricité et acuité particulière [@campsCremmaLabProjectsTranscription2022].

- Jolivet : En réalité, il est compliqué de définir ce qui est dans le domaine et ce qui est hors domaine : cela mobiliserait vraiment les appréciations des paléographes. IL FAUT QUE JE DISE QUE MON TEST HORS DOMAINE N'EST PAS VRAIMENT HORS DOMAINE MAIS SUR DES CHOSES TRÈS PROCHES [@torresaguilarModelisationAffinageHTR2022].

### Suggérer l'harmonisation
- Le projet CREMMALAB propose des réflexions méthodologiques sur les protocoles de transcriptions des corpus 
	- rédaction d’un guide de transcription ; mettre en place des Guidelines pour tenter des modèles génériques, robustes sur de grands nb de documents, pour réduire le temps de création des données pour chaque projet nouv. (INSISTER sur le fait que la généricité repose sur des règles communes et PERMET une meilleure réutilisation (efficacité de la généricité))
		- Ne pas imiter les formes de lettres pour les docs médiévaux
		- Conserver les abrév. (le développement dépend du contexte, de la scripta) : meilleure généricité (la prédiction est distinguée du déve. des abrév.) : proposition d'une table de caractères unicode recommandés
		- Pas  de distinction du IJ UV (ATTENTION on l'illustre toujours avec un exemple où il n'y a pas de u initial en forme de v...)
	- Outil de validation de conformité HTRUC
	- ChocoMufi : validation des caractères unicode utilisés pour les carac. spéciaux
	- Catalogue HTR-United et publication sur Zenodo [@campsCremmaLabProjectsTranscription2022].

- Segmonto : [@gabaySegmOntoControlledVocabulary2022]

### Post-traiter, exploiter les données : pour des briques open-source
- Etablir des éditions critiques : 
	- [@stoklbenezraHTRCriticalEdition2022]

- Avec 90% d'acuité, l'effort de production de VT ne vaut plus la peine, après il vaut mieux investir dans le post-traitement : c'est là dessus qu'il faut porter l'effort, et envisager des solutions de partage et mutualisation [@torresaguilarModelisationAffinageHTR2022].

- Proposer une succession d'étapes pour le traitement des textes (pour bien sauvegarder chaque étape, améliorer chacun des outils indépendamment) [@campsCremmaLabProjectsTranscription2022].

- Pour l'instant, la sortie HTR est totalement détachée du post-traitement. Il y aura un autre modèle de *deep learning* pour la lemmatisation des mots, leur normalisation. Ne se sont pas lancés dans une étape de correction : trop de variété graphique et linguistique, ça n'aurait pas de sens. Les scores de Kraken sont au niveau du caractère  [@campsCremmaLabProjectsTranscription2022].

- La post-correction ne pose pas de problème si ou conserve les documents intermédiaires [@campsCremmaLabProjectsTranscription2022].

### Modèles de publication
- Gallicorpora : [@gabaySegmOntoControlledVocabulary2022]