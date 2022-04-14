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
                    print(zenodo[item["idno"]])
    
noticeImage("CdS02_Konv002-02_0067.jpg")