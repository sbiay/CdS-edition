import click
import json
import os
import shutil
from lxml import etree

@click.command()
@click.argument("SOURCE")
@click.argument("SORTIE")
def distributionFichiers(source, sortie):
    # On contrôle l'écriture des chemins de dossiers
    if source[-1] != "/":
        source = source + "/"
    if sortie[-1] != "/":
        sortie = sortie + "/"
    
    # On récupère le fichier de données
    try:
        with open(source + "donnees.json") as jsonf:
            donneesImages = json.load(jsonf)
    except:
        print(f"Le fichier des données-images n'a pas pu être ouvert (existe-t-il dans le dossier {source} ?)")
    
    # On initie les erreurs pour les prédictions manquantes par rapport aux données de l'inventaire
    erreurs = []
    
    # Lire le fichier de données et distribuer les images dans les dossiers par notice
    for record in donneesImages["results"]["records"]:
        try:
            os.mkdir(sortie + record)
        except FileExistsError:
            True
        
        # On boucle sur les images de chaque notice
        for index, image in enumerate(donneesImages["results"]["records"][record]["Images"]):
            try:
                # On copie le fichier image vers la destination, dans le dossier de notice courant
                shutil.copy(f"{source}{image[:-4]}.xml", sortie + record)
            except:
                erreurs.append(image[:-4] + ".xml")
                
    # On délivre le message d'erreur
    print(f"Les fichiers suivants n'ont pas été trouvés : {erreurs}")
    
    # TODO Purger les fichiers des Textblock non pertinents
    # On initie une liste d'erreur pour le contrôle des fichiers de prédiction
    erreurs = []
    # On récupère les identifiants des zones ayant un titre
    regionAvecTitre = None
    # On récupère l'arbre XML correspondant à l'image courante
    """
    try:
        xml = etree.parse(source + image[:-4] + ".xml") #TODO on prendra les XMLCORRIGEES
        nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
        regionAvecTitre = xml.xpath("//alto:TextBlock[descendant::alto:TextLine[@TAGREFS=//alto:OtherTag["
                                    "@LABEL='HeadingLine:title']/@ID]]/@ID",
                                    namespaces=nsmap)
    except:
        erreurs.append(image[:-4] + ".xml")
    """

distributionFichiers()