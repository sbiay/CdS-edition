from fud import donneesFud


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
    fud = donneesFud()
    print(fud)
    
noticeImage("CdS02_Konv002-02_0067")