Éditer la correspondance de <br>Constance de Salm (1767-1845)
====

![accueil](./accueil.jpg)

Ce travail vise à la mise en place d'un flux de production pour l'édition électronique nativement numérique de la correspondance de Constance de Salm (1767-1845), dont [l'inventaire](https://constance-de-salm.de/) a été dressé par le département de l'Histoire numérique de l'[Institut historique allemand à Paris (DHIP/IHA)](http://www.dhi-paris.fr/fr/page-daccueil.html).

Le fichier [documentation.pdf](./documentation/documentation.pdf) donne une description complète de la méthodologie adoptée et du travail en cours.

Objectifs :
- Procéder à une reconnaissance automatique des écritures manuscrites (voir le [dossier dédié](./htr))
- Transformer les transcriptions en édition XML-TEI

# Installation
Afin de pouvoir consulter les Jupyter notebooks ou de tester les scripts contenus dans ce dépôt, il est nécessaire de télécharger l'archive zip, disponible sur cette page via le bouton **Code**, puis de la dézipper localement.

Pour l'évaluation et l'entraînement des modèles HTR, nous avons utilisé l'application *open-source* [Kraken](https://github.com/mittagessen/kraken), disponible pour Linux et Mac OSX, non pour Windows.

## Sous Linux (Ubuntu/Debian)
Face aux difficultés rencontrées pour l'utilisation de Kraken avec Python 3.10, nous proposons une méthode d'installation avec Python 3.9

- Pour installer Python 3, ouvrez un terminal et saisissez la commande :
    ```shell
    sudo apt-get install python3 libfreetype6-dev python3-pip python3-venv python3-virtualenv
    ```
- Pour créer un environnement virtuel Python 3.9, effectuez successivement les commandes suivantes :
    ```shell
    python3 -m venv env
    ```

- Déplacez-vous dans le dossier de l'application dézippé.
- Créez un environnement virtuel à l'aide de la commande :
    ```shell
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.9
    sudo apt-get install python3.9-venv
    python3.9 -m venv ~/python/foo-3.9 venv
    ```
- Activez cet environnement virtuel à l'aide de la commande (opération à **réitérer** à chaque lancement de l'application) :
    ```shell
    source env/bin/activate
    ```
- Installer les modules requis grâce à la commande :
    ```shell
    pip install -r requirements.txt
    ```

## Sous Windows
L'installation de Python 3 est nécessaire pour faire tourner les scripts. Nous recommandons la distribution [Anaconda](https://www.anaconda.com/products/individual).

Une fois la distribution Anaconda installée :
- Lancez, depuis le menu Démarrer, l'**Anaconda Powershell Prompt** ;
- Déplacez-vous dans le dossier de l'application dézippée ;
- Créez un environnement virtuel à l'aide de la commande :
    ```shell
    conda create -n cdsenv
    ```
- Activez cet environnement virtuel à l'aide de la commande (opération à **réitérer** à chaque lancement de l'application) :
    ```shell
    conda activate cdsenv
    ```
- Installez le module pip :
    ```shell
    conda install pip
    ```
- Installez les modules requis par l'application grâce à la commande :
    ```shell
    pip install -r requirements.txt
    ```
