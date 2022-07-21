import click
import json
import os
import shutil
from lxml import etree


@click.command()
@click.argument("SOURCE")
def distributionFichiers(source):
    """
    Cette fonction prend comme argument un chemin de dossier contenant des prédictions au format XML,
    analyse le contenu du fichier de données contenu au même emplacement et créé pour chaque pièce inventoriée
    dans ce dernier un dossier contenant les prédictions pertinentes.
    :param source: Chemin de dossier contenant les prédictions et devant contenir un fichier donnees.json
    """
    # On contrôle l'écriture des chemins de dossiers
    if source[-1] != "/":
        source = source + "/"

    # On récupère le fichier de données
    try:
        with open(source + "donnees.json") as jsonf:
            donneesImages = json.load(jsonf)
    except:
        print(f"Le fichier des données-images n'a pas pu être ouvert (existe-t-il dans le dossier {source} ?)")
    
    # EVALUER LES DOSSIER À CRÉER
    
    # On initie la liste des pièces à créer et des prédictions importées
    aCreer = []
    predictionsImport = []
    
    # On analyse le contenu du dossier importé
    for chemin, dossiers, fichiers in os.walk(source):
        for nomFichier in fichiers:
            predictionsImport.append(nomFichier)
    
    # On boucle sur chaque notice décrites par le fichier de données
    for record in donneesImages["results"]["records"]:
        # On initie un booléen pour le contrôle de présence de toutes les prédictions d'une notice
        complet = True
        # On boucle sur les images de chaque notice
        for index, image in enumerate(donneesImages["results"]["records"][record]["images"]):
            # On renomme l'image pour obtenir le nom de la prédiction correspondante
            label = image.replace(".jpg", ".xml")
            # On contrôle que la prédiction soit dans le dossier d'import
            if label not in predictionsImport:
                complet = False
        if complet:
            aCreer.append(record)
    
    # DISTRIBUER LES PRÉDICTIONS DANS DES DOSSIERS PROPRES À CHAQUE NOTICE
    
    # On boucle sur chaque notice
    for record in aCreer:
        # On crée le dossier de la pièce s'il n'existe pas déjà
        try:
            os.mkdir("./data/" + record)
            print("Le dossier ./data/" + record + "a été créé avec succès.")
        except FileExistsError:
            True
        
        # On boucle sur les images de chaque notice
        for index, image in enumerate(donneesImages["results"]["records"][record]["images"]):
            # On copie le fichier image vers la destination, dans le dossier de notice courant
            shutil.copy(f"{source}{image[:-4]}.xml", "./data/" + record)
            shutil.copy(f"{source}{image[:-4]}.jpg", "./data/" + record)


distributionFichiers()
