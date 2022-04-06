# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: June 2020
- description: Correcting orthographic errors in XML files
- input: text files and a Python dictionary
- output: corrected text files
- usage :
    ======
    python name_of_this_script.py arg1 arg2

    arg1: folder of the files to correct (attention à faire suivre le nom du dossier de "/")
    arg2: folder for the files corrected (attention à faire suivre le nom du dossier de "/")

    Commentaire : on procède à un parsage des documents XML d'entrée sous forme d'une liste de chaînes de caractères
    afin d'éviter la modification du format des balises qui survient lorsqu'on les parse avec lxml ou BeautifulSoup,
    ce qui entraîne des problèmes de compatibilité au moment de réimporter les fichiers dans eScriptorium.
"""

import os
import sys
from lxml import etree
from dictGlobal import dictGlobal

# On dézippe l'objet os.walk pour obtenir la racine, les dossiers et les fichiers du chemin passé en premier argument
for root, dirs, files in os.walk(sys.argv[1]):
    # On boucle sur chaque nom de fichier
    for filename in files:
        print(f"On lit le fichier {filename}")
        # On ouvre le fichier XML d'entrée et on récupère le contenu dans une list de lignes
        with open(sys.argv[1] + filename, 'r') as xml_orig:
            contenuXML = xml_orig.read().split("\n")
            
        # On ouvre le fichier XML de sortie
        with open(sys.argv[2] + filename, 'w') as xml_corr:
            # On boucle sur chaque ligne du contenuXML
            for ligne in contenuXML:
                # Si la ligne de code xml ne contient pas d'élément Unicode,
                # on écrit telle quelle cette ligne dans la sortie
                if "Unicode" not in ligne:
                    xml_corr.write(ligne + "\n")
                else:
                    # On boucle sur les entrées du dictionnaire
                    for cle, valeur in dictGlobal.items():
                        if cle in ligne:
                            ligne = ligne.replace(cle, valeur)
                    xml_corr.write(ligne + "\n")
