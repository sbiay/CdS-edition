import cv2
import os
from pathlib import Path


def PagesDivider(RelativePathSource, OutputPath):
    """
    To be runned, this function needs the cv2, os and pathlib.Path packages.
    It is best used to divide a double-paged photography of a document into a single-paged one.
    The separation between the two pages needs to be centred in order for this function results to be useable afterwards.
    """
    
    # On crée la liste des chemins de chaque fichiers contenus dans notre dossiers se terminant par l'extension .tif
    pathlist = Path(RelativePathSource).glob('*tif')
    
    # On boucle dans cette liste :
    for path in pathlist:
        
        # On convertit l'objet path en chaine de caractères :
        path = str(path)
        
        # Du chemin, on extrait le nom du fichier avec l'extension puis sans l'extension.
        file = os.path.basename(path)
        fileName = os.path.splitext(file)[0]
        
        # On lit l'image.
        im = cv2.imread(path)
        
        # On attribue les dimensions de l'image à des variables.
        height, width, depth = im.shape
        
        # On pose une condition : si la largeur est plus grande que la hauteur :
        if width > height:
            # On crée une variable qui équivaut à la moitié de la largeur.
            widthcutoff = width // 2
            
            # On crée des images qui correspondent respectivement à la moitié gauche et droite de l'image et on les sauvegarde dans le fichier cible.
            s1 = im[:, :widthcutoff]
            cv2.imwrite(OutputPath + fileName + "_left.jpeg", s1)
            s2 = im[:, widthcutoff:]
            cv2.imwrite(OutputPath + fileName + "_right.jpeg", s2)


PagesDivider('./../', './../traite/')
