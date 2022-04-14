import os
import json
import click

from constantes import XMLaCORRIGER, XMLCORRIGEES, DICTCDS

@click.command()
def textCorrectionXML():
    """
    Ce script ouvre les fichiers contenus dans le dossier ./xmlPage-aCorriger/
    
    - author: Floriane Chiffoleau
    - date: June 2020
    - original version:
    https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Correction/text_correction_XML.py
    """
    # On charge le dictionnaire Json global de la correspondance CDS
    with open(DICTCDS) as f:
        dictCDS = json.load(f)
    
    # On dézippe l'objet os.walk pour obtenir la racine, les dossiers et les fichiers du chemin passé en premier argument
    for root, dirs, files in os.walk(XMLaCORRIGER):
        # On boucle sur chaque nom de fichier
        for filename in files:
            # On ouvre le fichier XML d'entrée et on récupère le contenu dans une list de lignes
            with open(XMLaCORRIGER + filename, 'r') as xml_orig:
                contenuXML = xml_orig.read().split("\n")
            
            # On ouvre le fichier XML de sortie
            with open(XMLCORRIGEES + filename, 'w') as xml_corr:
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
                        # On initie la ligne corrigée
                        ligneCorr = ligneBrute
                        # On initie la liste des entrées dont on actualisera le contexte dans le dictCDS
                        entreesMAJ = {}

                        # On effectue une première recherche pour les formes possédant une espace
                        # (ce sont les mots coupés en deux qu'il faut corriger en un seul mot)
                        for forme in dictCDS:
                            lemme = dictCDS[forme]["lem"]
                            if len(forme.split(" ")) > 1:
                                if forme in ligneCorr:
                                    ligneCorr = ligneCorr.replace(forme, lemme)

                            # On pose comme condition que le lemme ne soit pas "None" (id est ambigu)
                            elif lemme:
                                for index, mot in enumerate(ligne):
                                    # Comme la liste des mots contient des vides, on pose une condition d'existence
                                    if mot:
                                        # Si le mot courant correspond à l'entrée de dictionnaire
                                        if forme == mot:
                                            # Si le mot est en milieu de ligne
                                            ligneCorr = ligneCorr.replace(f" {forme}", f" {lemme}")
                                            # Si le mot est placé juste après la balise unicode
                                            ligneCorr = ligneCorr.replace(f">{forme}", f">{lemme}")
                                            # Si le mot est placé juste après une apostrophe
                                            ligneCorr = ligneCorr.replace(f"&#39;{forme}", f"&#39;{lemme}")
                                            entreesMAJ[forme] = {
                                                "lem": lemme,
                                                "ctxt": []
                                            }

                        # On renvoie le contexte du mot traité dans le dictionnaire global en reparsant la ligne corrigée
                        for entree in entreesMAJ:
                            # On inscrit dans le dictionnaire le contexte en sélectionnant le noeud texte de l'élément
                            # Unicode par une slice et en mettant en valeur le lemme dans le texte corrigé par une casse
                            # en capitales
                            # On pose d'abord comme condition qu'il y ait un lemme
                            if entreesMAJ[entree]["lem"]:
                                entreesMAJ[entree]["ctxt"] = [
                                    ligneCorr[19:-10].replace(
                                        entreesMAJ[entree]["lem"], entreesMAJ[entree]["lem"].upper()
                                    )
                                ]
                            
                            # On met à jour le dictCDS avec les contextes actualisés
                            dictCDS[entree] = entreesMAJ[entree]
                        
                        xml_corr.write(ligneCorr + "\n")
            
            print(f"Le fichier {filename} a été corrigé avec succès")
    
    # On remplace le fichier corresp.json avec les contextes actualisés
    with open(DICTCDS, mode="w") as f:
        json.dump(dictCDS, f, indent=3, ensure_ascii=False)
    print("Le dictionnaire corresp.json est désormais à jour.")

textCorrectionXML()