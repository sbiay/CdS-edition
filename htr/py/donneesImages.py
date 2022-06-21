import json
import click
import os
from toutesDonnees import donneesFud, donneesZenodo


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
        item["incipit"] = zenodo[item["idno"]].get("incipit")
        item["URL"] = zenodo[item["idno"]]["URL"]
    
    return notices


@click.command()
@click.argument("SOURCE")
@click.argument("SORTIE")
def donneesImages(source, sortie):
    """
    Cette fonction prend comme argument un chemin de dossier SOURCE contenant des images
    et retourne dans un fichier Json situé dans le dossier SORTIE plusieurs listes ("results") et statistiques ("stats")
    - results :
        - images : dictionnaire des images du dossier SOURCE indiquant le nombre de notices associées et détaillant :
            - identifiant
            - incipit de la lettre
            - URL de la notice en ligne
        - records : dictionnaire des notices liées aux images du dossier SOURCE, détaillant :
            - l'incipit de la lettre
            - l'URL de la notice en ligne
            - l'image contenant le début de la lettre
            - la position du titre de cette lettre
              (relativement aux autres titres de lettres inventoriées dans la même image)
            - la liste complète des images
            
    :param source: chemin du dossier où se trouvent les images
    :param sortie: chemin du dossier où placer le fichier de résultat
    :return: None
    """
    # On contrôle l'écriture des chemins de dossiers
    if source[-1] != "/":
        source = source + "/"
    if sortie[-1] != "/":
        sortie = sortie + "/"
    
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
    # On boucle sur chaque image du dossier source
    for image in listeImages:
        # On récupère les données relatives à l'image grâce à la fonction noticeImage()
        if noticeImage(image):
            notices = noticeImage(image)
            selection = []
            # On boucle sur les notices renvoyées par la fonction
            for notice in notices:
                # On écrit le dictionnaire organisant les images par notices
                parNotice[notice["idno"]] = {
                    "incipit": notice["incipit"],
                    "URL": notice["URL"],
                    "Images": notice["Images"]
                }
                donnees = {
                    "idno": notice["idno"],
                    "incipit": notice["incipit"],
                    "URL": notice["URL"]
                }
                selection.append(donnees)
            # On ajoute la sélection des données et une stat à la liste parImages
            parImages[image] = {
                "record_nb": len(notices),
                "records": selection
            }
        
        # Si l'image n'a pas de notice
        else:
            sansNotice.append(image)

    # On écrit l'objet final
    resultats = {
        "results": {
            "images": parImages,
            "records": dict(sorted(parNotice.items())),
            "no-record": sorted(sansNotice)
        },
        "stats": {
            "images": len(parImages),
            "records": len(listeImages) - len(sansNotice),
            "no-record": len(sansNotice),
            "total": len(listeImages)
        }
    }
    
    # On initie la liste des titres de pièces (qui permettra d'associer titre et notice par position dans une image)
    enchainTitres = {}
    # Lire le fichier de données et distribuer les images dans les dossiers par notice
    for record in resultats["results"]["records"]:
        # On boucle sur les images de chaque notice
        for index, image in enumerate(resultats["results"]["records"][record]["Images"]):
            # Si l'index de l'image est 0
            # elle est en début de lettre (le titre se trouve donc dans l'image)
            if index == 0:
                if not enchainTitres.get(image):
                    enchainTitres[image] = [record]
                else:
                    enchainTitres[image].append(record)
    
    # On boucle sur l'enchainement des titres pour chaque image
    # afin de récupérer la position de chaque titre dans chaque image
    for image in enchainTitres:
        for index, item in enumerate(enchainTitres[image]):
            resultats["results"]["records"][item]["init_image"] = image
            resultats["results"]["records"][item]["title_position"] = index + 1
            # On renomme la liste des images en la plaçant en fin de dictionnaire
            resultats["results"]["records"][item]["images"] = resultats["results"]["records"][item]["Images"]
            # On retire la clé d'origine des images
            resultats["results"]["records"][item].pop("Images")
    
    with open(f"{sortie}donnees.json", mode="w") as jsonf:
        json.dump(resultats, jsonf, ensure_ascii=False, indent=3)
    print(f"Le fichier {sortie}donnees.json a été écrit avec succès.")


if __name__ == "__main__":
    donneesImages()
