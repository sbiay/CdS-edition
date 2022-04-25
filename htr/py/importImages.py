import click
import json
import os


@click.command()
@click.argument("SOURCE")
@click.argument("DESTINATION")
def importImages(source, destination):
    """
    Cette fonction prend comme argument un chemin de dossier SOURCE contenant des images au format .jpg
    et un chemin de dossier DESTINATION contenant un fichier de données au format .json
    elle analyse le contenu de ce fichier de données
    et écrit dans un fichier .txt la liste des fichiers du dossier SOURCE
    qui doivent être copiés dans le dossier DESTINATION
    :param source: chemin du dossier où se trouvent les images
    :param destination: chemin du dossier où se trouve le fichier de données .json
    :return: None
    """
    
    # On initie un booléen pour le contrôle des fichiers du dossier source
    aucunJpg = True
    aucunJson = True
    # On initie une liste d'erreurs
    erreurs = []
    
    # On initie la liste des images du dossier source
    contenuSource = []
    # On analyse l'arborescence du chemin de dossier source content les images
    for racineSource, dirs, fichiers in os.walk(source):
        # On boucle sur chaque fichier
        for fichier in fichiers:
            # On ne sélectionne dans le dossier que les fichiers portant l'extension jpg
            if fichier[-3:] == "jpg":
                aucunJpg = False
                contenuSource.append(fichier)
    
    # On analyse l'arborescence du chemin de dossier destination
    for racine, dirs, fichiers in os.walk(destination):
        for fichier in fichiers:
            if fichier[-4:] == "json":
                jsonf = racine + fichier
                aucunJson = False
    
    # On teste les booléens
    if aucunJpg:
        erreurs.append("Le dossier source ne semble pas contenir de fichier .jpg")
    if aucunJson:
        erreurs.append("Le dossier de destination ne semble pas contenir de fichier .json")
    # En cas d'erreur
    if erreurs:
        # On arrête le code et on retourne ce message
        for erreur in erreurs:
            print(erreur)
        return None
    
    # On ouvre le fichier Json contenant les données
    with open(jsonf) as f:
        donneesImages = json.load(f)
    
    # On récupère la liste des images dépourvue de notice
    sansNotice = donneesImages["results"]["no-record"]
    
    # On initie la liste des fichiers à copier
    copier = []
    # On contrôle que les fichiers à importer ne soient pas contenus dans la liste des images sans notice
    for fichier in contenuSource:
        # Si le fichier ne figure pas dans la liste des images sans notice
        if fichier not in sansNotice:
            copier.append(racineSource + fichier)
    
    # On ouvre un fichier pour écrire la liste des images à copier depuis la source
    with open(destination + "copier.txt", mode="w") as f:
        for fichier in copier:
            f.write(fichier + "\n")
    print(f"La liste des images à copier a été correctement écrite dans le fichier {destination}copier.txt")


if __name__ == "__main__":
    importImages()
