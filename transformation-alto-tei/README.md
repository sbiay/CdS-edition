Transformation ALTO vers TEI
====

Ce dossier contient les fichiers et scripts nécessaires à la réalisation du processus de transformation des fichiers ALTO contenant les transcriptions en encodage TEI.

Cette chaîne de traitement est fondée sur l'application [alto2tei](https://github.com/kat-kel/alto2tei), conçue dans le cadre du projet Gallicorpora, qui se lance avec le fichier [run.py](./run.py) (cf. documentation fonctionnelle).

# Documentation fonctionnelle (*notebooks*)
La mise en oeuvre concrète est expliquée dans les *notebooks* de ce dossier :
1. [Transformer un lot de fichiers ALTO en encodage TEI](./Transformer_lot_ALTO_vers_TEI.ipynb)
2. [Finaliser l'encodage TEI](./Finaliser_encodage.ipynb)

# Contenu des dossiers :
- [collection-test](./collection-test/) contient une série d'encodages réalisés de manière automatique à partir de différents dossiers
- [demo/](./demo) contient les images qui illustrent les *notebooks*.
- [final/](./final) contient une série d'encodages finalisés manuellement
- **import-\*/** contiennent des fichiers ALTO et leurs images, ainsi que les fichiers **donnees.json** indispensables à la transformation
- [py/](./py) contient les scripts nécessaires à la transformation