import click
import csv
import os

from toutesDonnees import donneesFud, donneesZenodo


def noticeImage(image):
    """
    Cette fonction prend comme argument un nom de fichier image et retourne un dictionnaire renseignant :
    - Son numéro de digitalisation ;
    - L'URL de sa publication sur le site http://constance-de-salm.de/
    :param image: nom de fichier
    :type image: str
    :return: dictionnaire de métadonnées sur l'image
    :return type: dict
    """
    # On charge les données exportées de FuD et de Zenodo
    fud = donneesFud()
    zenodo = donneesZenodo()
    for item in fud:
        # On pose comme condition que l'item est une liste d'images
        if item.get("Images"):
            # et que cette liste ne soit pas vide
            if item["Images"]:
                # On pose enfin comme condition que l'image recherchée soit dans la liste
                if image in item["Images"]:
                    zenodo[item["idno"]]["nom_image"] = image
                    return zenodo[item["idno"]]

@click.command()
@click.argument("DOSSIER")
def donneesImages(dossier):
    """
    Cette fonction prend comme argument une liste de fichiers images
    et retourne dans un fichier CSV la liste des identifiants et des URL du site http://constance-de-salm.de
    :param dossier: chemin du dossier où se trouvent les images et où est exporté le CSV de sortie
    :return: None
    """
    listeImages = []
    # On analyse l'arborescence du chemin de dossier passée en argument
    for racine, dirs, fichiers in os.walk(dossier):
        for fichier in fichiers:
            # On ne sélectionne dans le dossier que les fichiers portant l'extension jpg
            if fichier[-3:] == "jpg":
                listeImages.append(fichier)
    
    # On initie la liste des résultats
    resultats = []
    for image in listeImages:
        if noticeImage(image):
            resultats.append(noticeImage(image))
        else:
            resultats.append(
                {
                    'nom_image': image,
                    'Nr. der Digitalisate': None,
                    'URL': None
                }
            )
    print(resultats)
    # On écrit les résultats dans un fichier CSV
    with open(f"{dossier}/donnees.csv", 'w', newline='') as csvfile:
        fieldnames = ['nom_image', 'Nr. der Digitalisate', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for resultat in resultats:
            writer.writerow(
                {
                    'nom_image': resultat['nom_image'],
                    'Nr. der Digitalisate': resultat['Nr. der Digitalisate'],
                    'URL': resultat['URL']
                }
            )

donneesImages()