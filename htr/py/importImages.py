import click
import os


@click.command()
@click.argument("SOURCE")
def importImages(source):
    """
    :param source: chemin du dossier où se trouvent les images
    :return: None
    """
    
    # On initie un booléen pour le contrôle des fichiers du dossier source
    aucunJpg = True
    aucunJson = True
    # On analyse l'arborescence du chemin de dossier passée en argument
    for racine, dirs, fichiers in os.walk(source):
        for fichier in fichiers:
            # On ne sélectionne dans le dossier que les fichiers portant l'extension jpg
            if fichier[-3:] == "jpg":
                aucunJpg = False
            if fichier[-4:] == "json":
                aucunJson = False
    if aucunJpg:
        print("Le dossier source ne semble pas contenir de fichier .jpg")
    if aucunJson:
        print("Le dossier source ne semble pas contenir de fichier .json")


if __name__ == "__main__":
    importImages()
