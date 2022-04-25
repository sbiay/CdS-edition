import json

import click
import os

from htr.py.toutesDonnees import donneesFud, donneesZenodo


def noticeImage(image):
    """
    Cette fonction prend comme argument un nom de fichier image et retourne une liste de dictionnaires renseignant :
    - Leur identifiant FuD ;
    - Leur numéro de digitalisation ;
    - L'URL de sa publication sur le site http://constance-de-salm.de/
    :param image: nom de fichier
    :type image: str
    :return: liste de dictionnaires de métadonnées sur l'image
    :return type: list
    """
    # On charge les données exportées de FuD et de Zenodo
    fud = donneesFud()
    zenodo = donneesZenodo()
    notices = []
    for item in fud:
        # On pose comme condition que l'item ait une liste d'images
        if item.get("Images"):
            # et que cette liste ne soit pas vide
            if item["Images"]:
                # On pose enfin comme condition que l'image recherchée soit dans la liste
                for cliche in item["Images"]:
                    if image == cliche:
                        notices.append(item)
    
    # On boucle sur les notices recueillies
    for item in notices:
        # On récupère les URL des notices publiées dans le jeu de données Zenodo
        item["URL"] = zenodo[item["idno"]]["URL"]
    
    return notices

@click.command()
@click.argument("SOURCE")
@click.argument("SORTIE")
def donneesImages(source, sortie):
    """
    Cette fonction prend comme argument un chemin de dossier source contenant des images
    et retourne dans un fichier Json la liste des identifiants et des URL du site http://constance-de-salm.de
    :param source: chemin du dossier où se trouvent les images
    :param sortie: chemin du dossier où placer le fichier de résultat
    :return: None
    """
    listeImages = []
    # On analyse l'arborescence du chemin de dossier passée en argument
    for racine, dirs, fichiers in os.walk(source):
        for fichier in fichiers:
            # On ne sélectionne dans le dossier que les fichiers portant l'extension jpg
            if fichier[-3:] == "jpg":
                listeImages.append(fichier)
    
    # On initie la liste des résultats
    avecNotice = {}
    sansNotice = []
    for image in listeImages:
        # On récupère les données relatives à l'image grâce à la fonction noticeImage()
        if noticeImage(image):
            # On boucle sur les notices renvoyées par la fonction
            for notice in noticeImage(image):
                avecNotice[notice["Nr. der Digitalisate"]] = {
                        "URL": notice["URL"],
                        "Images": notice["Images"]
                    }
                
        else:
            sansNotice.append(image)
    
    # On écrit l'objet final
    resultats = {
        "results": {
            "records": avecNotice,
            "no-record": sansNotice
        }
    }
    
    with open(f"{sortie}/donnees.json", mode="w") as jsonf:
        json.dump(resultats, jsonf)
    
donneesImages()