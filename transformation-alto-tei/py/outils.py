import os


def triFichiers(dossier):
    """
    Cette fonction prend comme argument le chemin relatif d'un dossier
    et retourne la liste des chemins relatifs des fichiers qu'il contient, triés alpha-numériquement
    :param dossier: chemin relatif d'un dossier
    :type dossier: str
    :return: liste des chemins relatifs des fichiers triés
    :type return: list
    """
    
    # On trie alpha-numériquement les fichiers, en commençant par initier la liste triée
    tri = []
    # On analyse l'arborescence du dossier des prédictions
    for root, dirs, files in os.walk(dossier):
        # On boucle sur chaque fichier
        for filename in files:
            # On ajoute la liste le chemin relatif de chaque fichier
            tri.append(root + filename)
    # On trie la liste
    tri = sorted(tri)
    
    return tri