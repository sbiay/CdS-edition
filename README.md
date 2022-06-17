Éditer la correspondance de <br>Constance de Salm (1767-1845)
====

![accueil](./accueil.jpg)

Ce travail vise à la mise en place d'un flux de production pour l'édition électronique nativement numérique de la correspondance de Constance de Salm (1767-1845), dont [l'inventaire](https://constance-de-salm.de/) a été dressé par le département de l'Histoire numérique de l'[Institut historique allemand à Paris (DHIP/IHA)](http://www.dhi-paris.fr/fr/page-daccueil.html).

Le fichier [documentation.pdf](./documentation/documentation.pdf) donne une description complète de la méthodologie adoptée et du travail en cours.

Objectifs :
- Procéder à une reconnaissance automatique des écritures manuscrites (voir le [dossier dédié](./htr))
- Transformer les transcriptions en édition XML-TEI

# Installation (sous Linux Ubuntu/Debian)
Afin de pouvoir consulter les Jupyter notebooks ou de tester les scripts contenus dans ce dépôt, il est nécessaire de télécharger l'archive zip, disponible sur cette page via le bouton **Code**, puis de la dézipper localement.

Pour l'évaluation et l'entraînement des modèles HTR, nous avons utilisé l'application *open-source* [Kraken](https://github.com/mittagessen/kraken), disponible pour Linux et Mac OSX, non pour Windows.

Pour la consultation des notebooks et la prise en main du projet sous Windows, il est possible d'utiliser le programme Bash ([un peu d'aide ici](https://blog.ineat-group.com/2020/02/utiliser-le-terminal-bash-natif-dans-windows-10/)), qui permet de travailler dans une machine virtuelle Linux tout en restant sous Windows. Mais **il est recommandé** de faire appel à une distribution native d'Ubuntu, qui peut être facilement installée en parallèle du système Windows en suivant les instructions de [cette page](https://lecrabeinfo.net/installer-ubuntu-20-04-lts-dual-boot-windows-10.html).

Face aux difficultés rencontrées pour l'utilisation de Kraken avec Python 3.10, nous proposons une méthode d'installation avec Python 3.9.

- Pour installer Python 3, ouvrez un terminal et saisissez la commande :
    ```shell
    sudo apt-get install python3 libfreetype6-dev python3-pip python3-venv python3-virtualenv
    ```
    
- Pour créer un environnement virtuel Python 3.9, effectuez successivement les commandes suivantes :
    - Récupérez le dépôt des anciennes versions de Python
        ```shell
        sudo add-apt-repository ppa:deadsnakes/ppa
        ```
    - Recherchez les mises à jour :
        ```shell
        sudo apt-get update
        ```
    - Installez Python 3.9 :
        ```shell
        sudo apt-get install python3.9
        ```
    - Installez le gestionnaire d'environnement virtuel de Python 3.9 :
        ```shell
        sudo apt-get install python3.9-venv
        ```

- Puis déplacez-vous dans le dossier de l'application dézippé.

- Créez un environnement virtuel à l'aide de la commande :
    ```shell
    python3.9 -m venv ~/python/foo-3.9 venv
    ```

- Activez cet environnement virtuel à l'aide de la commande (opération à **réitérer** à chaque lancement de l'application) :
    ```shell
    source venv/bin/activate
    ```
- Installer les modules requis grâce à la commande :
    ```shell
    pip install -r requirements.txt
    ```
