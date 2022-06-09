import json
import click
import os
from toutesDonnees import donneesFud, donneesZenodo
from constantes import XMLaCORRIGER
from lxml import etree

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
        # On récupère les débuts de lettres et URL des notices publiées dans le jeu de données Zenodo
        item["incipit"] = zenodo[item["idno"]]["incipit"]
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
    # On contrôle l'écriture des chemins de dossiers
    if source[-1] != "/":
        source = source + "/"
    if sortie[-1] != "/":
        sortie = sortie + "/"
    
    # On charge les données fud
    fud = donneesFud()
    
    listeImages = []
    # On analyse l'arborescence du chemin de dossier passée en argument
    for racine, dirs, fichiers in os.walk(source):
        for fichier in fichiers:
            # On ne sélectionne dans le dossier que les fichiers portant l'extension jpg
            if fichier[-3:] == "jpg":
                listeImages.append(fichier)
    
    # On trie les images dans l'ordre alpha-numérique
    listeImages = sorted(listeImages)
    
    # On initie la liste des résultats pour le classement des images par notices ou sans notice
    parNotice = {}
    sansNotice = []
    # On initie la liste des résultats pour le classement des notices par image
    parImages = {}
    for image in listeImages:
        # On récupère les données relatives à l'image grâce à la fonction noticeImage()
        if noticeImage(image):
            # On boucle sur les notices renvoyées par la fonction
            for notice in noticeImage(image):
                # On écrit le dictionnaire organisant les images par notices
                parNotice[notice["Nr. der Digitalisate"]] = {
                    "incipit": notice["incipit"],
                    "URL": notice["URL"],
                    "Images": notice["Images"]
                }
            # On écrit le dictionnaire organisant les notices par images
            notices = noticeImage(image)
            # On sélectionne une partie des donnees des notices
            selection = []
            for notice in notices:
                donnees = {
                    "idno": notice["idno"],
                    "incipit": notice["incipit"],
                    "URL": notice["URL"]
                }
                selection.append(donnees)
            
            parImages[image] = {
                "record_nb": len(notices),
                "records": selection
            }
            """
            # TODO à placer dans un autre script
            # On récupère les identifiants des zones ayant un titre
            xml = etree.parse("/home/sbiay/telechargments/test/" + image[:-4] + ".xml") #TODO on prendra les
            # XMLCORRIGEES
            nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
            regionAvecTitre = xml.xpath("//alto:TextBlock[descendant::alto:TextLine[@TAGREFS=//alto:OtherTag["
                           "@LABEL='HeadingLine:title']/@ID]]/@ID",
                              namespaces=nsmap)
            for region in regionAvecTitre:
                print(region)
            """
        # Si l'image n'a pas de notice
        else:
            sansNotice.append(image)
    
    # On écrit l'objet final
    resultats = {
        "results": {
            "images": parImages,
            "records": dict(sorted(parNotice.items())),
            "no-record": sansNotice.sort()
        },
        "stats": {
            "images": len(parImages),
            "records": len(listeImages) - len(sansNotice),
            "no-record": len(sansNotice),
            "total": len(listeImages)
        }
    }
    
    with open(f"{sortie}donnees.json", mode="w") as jsonf:
        json.dump(resultats, jsonf, ensure_ascii=False, indent=3)
    print(f"Le fichier {sortie}donnees.json a été écrit avec succès.")


if __name__ == "__main__":
    donneesImages()
