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
from dictComplets.dictCDS import dictCDS

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
            for ligneBrute in contenuXML:
                # Si la ligne de code xml ne contient pas d'élément Unicode,
                # on écrit telle quelle cette ligne dans la sortie
                if "Unicode" not in ligneBrute:
                    xml_corr.write(ligneBrute + "\n")
                else:
                    # Si la ligne contient Unicode, il s'agit de la transcription à corriger
                    # Pour chercher si les mots de la ligne courante sont dans le dictionnaire,
                    # on tokénise cette ligne en commençant par éliminer les signes de ponctuation
                    ponctuation = ",;:!."
                    ligne = ligneBrute
                    for signe in ponctuation:
                        ligne = ligne.replace(signe, " ")
                    # Puis on supprime les éventuelles doubles espaces
                    ligne = ligne.replace("  ", " ")
                    # On supprime également les balises collées au premier et au dernier mot
                    ligne = ligne.replace("<Unicode>", "")
                    ligne = ligne.replace("</Unicode>", "")
                    # Et on découpe chaque mot selon les espaces restantes
                    ligne = ligne.split(" ")
                    # Test sur un mot pour voir comment il est traité
                    if "udrédulite" in ligneBrute:
                        print(ligne)
                    # On initie la ligne corrigée
                    ligneCorr = ligneBrute
                    # On initie la liste des entrées dont on actualisera le contexte dans le dictCDS
                    entreesMAJ = {}
                    # On boucle sur les formes du dictionnaire personnalisé
                    for forme in dictCDS:
                        lemme = dictCDS[forme]["lem"]
                        for index, mot in enumerate(ligne):
                            # Comme la liste des mots contient des vides, on pose une condition d'existence
                            if mot:
                                # Si le mot courant correspond à l'entrée de dictionnaire
                                if forme == mot:
                                    ligneCorr = ligneCorr.replace(forme, lemme)
                                    entreesMAJ[forme] = {
                                        "lem": lemme,
                                        "ctxt": []
                                    }
                    # On renvoie le contexte du mot traité dans le dictionnaire global en reparsant la ligne corrigée
                    for entree in entreesMAJ:
                        # On inscrit dans le dictionnaire le contexte en sélectionnant le noeud texte de l'élément
                        # Unicode par une slice et en mettant en valeur le lemme dans le texte corrigé par une casse
                        # en capitales
                        entreesMAJ[entree]["ctxt"] = [
                            ligneCorr[19:-10].replace(
                                entreesMAJ[entree]["lem"], entreesMAJ[entree]["lem"].upper()
                            )
                        ]
                        
                        # On met à jour le dictCDS avec les contextes actualisés
                        dictCDS[entree] = entreesMAJ[entree]
                        
                    if "udrédulite" in ligneBrute:
                        print(ligneCorr)
                        
                    xml_corr.write(ligneCorr + "\n")

# On transforme le dictCDS pour l'indenter
dictCDS = str(dictCDS).replace("},", "},\n").replace(": {", ":\n\t{").replace("', '", "',\n\t '")

# On met à jour le dictCDS
with open("./py/dictCDS.py", mode="w") as f:
    f.write(
        f"dictCDS = {dictCDS}"
    )
