HTR
====

Ce dossier contient les fichiers et scripts nécessaires à la réalisation du processus de reconnaissance automatique d'écriture et à la correction des prédictions.

Cette chaîne de traitement a été conçue pour être mise en oeuvre avec les logiciels [eScriptorium](https://escriptorium.fr/) et [Kraken](https://kraken.re/master/index.html). Ces deux applications bénéficient de leur propre documentation. Par conséquent, les *notebooks* suivants ne contiennent pas d'aide à la prise en main de ces logiciels. On pourra se reporter à [cet article pour prendre en main eScriptorium](https://lectaurep.hypotheses.org/documentation/prendre-en-main-escriptorium) ainsi qu'à la [documentation de Kraken](https://kraken.re/master/training.html), que le *notebook* n<sup>o</sup> 3 permet d'utiliser sans requérir une connaissance de son fonctionnemment.

# Documentation fonctionnelle (*notebooks*)
La mise en oeuvre concrète est expliquée dans les notebooks de ce dossier :
1. [Préparer le traitement d'un dossier](./Preparer_le_traitement_dun_dossier.ipynb)
2. [Importer un dossier dans eScriptorium](./Importer_dossier_dans_eScriptorium.ipynb)
3. [Segmenter et annoter une page](./Segmenter_et_annoter_une_page.ipynb)
4. [Tester et entraîner un modèle de reconnaissance d'écriture](./Tester_et_entrainer_un_modele_HTR_avec_Kraken.ipynb)
5. [Tutoriel Kami pour tester un modèle de reconnaissance d'écriture avec des statistiques riches](./Tutoriel_Kami.ipynb)
6. [Corriger une prédiction](./Corriger_une_prediction.ipynb)

# Contenu des dossiers :
- [demo/](./demo/) contient les illustrations de démonstration des *notebooks*
- [entrainements/](./entrainements/) est le dossier dédié à la méthodologie de test et d'entraînement des modèles de segmentation et de reconnaissance d'écriture
- [mainAuteur/](./mainAuteur/) contient des données permettant de tester des modèles de reconnaissance d'écriture sur l'écriture personnelle de Constance de Salm
- [mains/](./mains/) contient de brèves descriptions illustrées des écritures sur lesquelles des tests ou des entraînements ont été pratiqués
- [modeles-rec/](./modeles-rec/) contient les différents modèles de reconnaissance d'écriture entraînés ; les données chiffrées rendant compte des tests et des résultats des entraînements sont consultables dans le fichier [journal-rec.json](./entrainements/journal-rec.json)
- [predic-a-corriger/](./predic-a-corriger/) est destiné à recevoir les fichiers XML-Alto exporté d'eScriptorium et contenant les transcriptions
- [predic-corrigees/](./predic-corrigees/) est le dossier de destination des fichiers XML-Alto à la sortie du traitement semi-automatisé des corrections
- [py/](./py/) : contient les scripts Python exploités dans les *notebooks*
- [verite-terrain](./verite-terrain/) contient les images et les transcriptions consitutées en vérités de terrain pour le test et l'entraînement des modèles de reconnaissance d'écriture. Le fichier [mains.json](./mains/mains.json) donne la liste de ces fichiers par main et précise quels fichiers ont été utilisés pour les tests et quels fichiers ont été utilisés pour les entraînements

# Aide
La consultation de ces *notebooks* suppose d'avoir suivi les consignes d'[installation](https://github.com/sbiay/CdS-edition#installation).

Pour une documentation plus détaillée, on consultera le fichier [documentation.pdf](../documentation/documentation.pdf).

En cas de doute sur l'**avancement du traitement d'une source**, on peut comparer la liste des fichiers de deux dossiers à l'aide de la commande :
```shell
diff -r <directory1> <directory2> > diff.txt
```

Et pour obtenir la liste des fichiers exclusivement présents dans le dossier courant :
```shell
grep "Seulement dans ./" diff.txt > exclu.txt
```