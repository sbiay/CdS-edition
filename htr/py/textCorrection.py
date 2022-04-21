import os
import json
import click
import spacy
from spacy.lang.fr.examples import sentences
# Installation de Spacy https://spacy.io/usage#quickstart
# module linguistique fr_core_news_sm
from constantes import XMLaCORRIGER, XMLCORRIGEES, DICTPAGESCORR, DICTCDS

# TODO Passer des arguments pour gérer tous les fichiers ou un seul
@click.command()
def textCorrectionXML():
    """
    Ce script ouvre les fichiers contenus dans le dossier ./xmlPage-aCorriger/
    
    - author: Floriane Chiffoleau
    - date: June 2020
    - original version:
    https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Correction/text_correction_XML.py
    """
    # On charge le dictionnaire complet de la correspondance
    with open(DICTCDS) as f:
        dictCDS = json.load(f)
        
    # On dézippe l'objet os.walk pour obtenir la racine, les dossiers et les fichiers du chemin passé en premier argument
    for root, dirs, files in os.walk(XMLaCORRIGER):
        # On boucle sur chaque nom de fichier
        for filename in files:
            # On charge le dictionnaire Json corrigé de la page
            try:
                with open(DICTPAGESCORR + "page_" + filename.replace(".xml", ".json")) as dico:
                    dictPage = json.load(dico)
            except:
                print(f"Le dictionnaire de page page_{filename.replace('.xml', '.json')} n'a pas été chargé " \
                                                                                   "correctement.")
                break
    
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
                        # On initie la liste des entrées dont on actualisera le contexte dans le dictCDS
                        entreesMAJ = {}
                        ligne = ligneBrute
                        # On remplace l'encodage XML des apostrophes
                        ligne = ligne.replace("&#39;", "'")
                        # On supprime l'indentation
                        ligne = ligne.replace("          ", "")
                        # On supprime également les balises collées au premier et au dernier mot
                        ligne = ligne.replace("<Unicode>", "").replace("</Unicode>", "")
                        
                        # TODO avant de tokéniser on doit procéder au remplacement des formes avec apostrophe
                        # TODO et des formes avec espace au milieu
                        """
                        # Si la forme contient une espace, on la traite en premier
                        # en appliquant la correction à la ligne dans son ensemble
                        # (et non à un mot particulier)
                        if len(forme.split(" ")) > 1:
                            if forme in ligneCorr:
                                ligneCorr = ligneCorr.replace(forme, lemme)
                        """
                        # On tokénise la ligne
                        nlp = spacy.load("fr_core_news_sm")
                        doc = nlp(ligne)
                        ligne = [token.text for token in doc]
                        # On initie la ligne corrigée
                        ligneCorr = []
                        # On boucle sur chaque mot
                        for mot in ligne:
                            if "déconomie" in ligne:
                                print(mot)
                                # On effectue une première recherche pour les formes possédant une espace
                                # (ce sont les mots coupés en deux qu'il faut corriger en un seul mot)
                            # On initie le lemme ou correction
                            lemme = None
                            for forme in dictPage:
                                # On n'intervient que si la valeur de lemme n'est pas "null"
                                if forme == mot and dictPage[forme]["lem"]:
                                    # On peut se retrouver avec une liste dont le seul élément est "null"
                                    if dictPage[forme]["lem"][0]:
                                        # La correction retenue ou "lemme"
                                        # est le premier item de la liste-valeur de la clé "lem"
                                        lemme = dictPage[forme]["lem"][0]
                            if lemme:
                                ligneCorr.append(lemme)
                            # Si le lemme est resté None, il n'y a pas de correction à appliquer
                            else:
                                ligneCorr.append(mot)
                            entreesMAJ[forme] = {
                                "lem": lemme,
                                "ctxt": []
                            }
                            
                        # On recompose la ligne en tant que chaîne
                        ligneCorr = ' '.join(ligneCorr)
                        # On élimine les espaces en trop
                        ligneCorr = ligneCorr.replace(' ,', ',').replace(' .', ',')\
                            .replace('( ', '(').replace(' )', ')')
                        if "prudente" in ligneCorr:
                            print(f"LIGNE DEPART : {ligneBrute}")
                            print(f"LIGNE TOKENISEE : {ligne}")
                            print(f"LIGNE CORRIGEE : {ligneCorr}")
                        """
                        # On renvoie le contexte du mot traité dans le dictionnaire global
                        # en reparsant la ligne corrigée
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
                            # Si la forme n'existe pas déjà
                            if not dictCDS.get(entree):
                                dictCDS[entree] = entreesMAJ[entree]
                            # Si la forme existe déjà
                            else:
                                # Si le lemme que l'on propose n'est pas encore référencé
                                if not entreesMAJ[entree]["lem"] in dictCDS[entree]["lem"]:
                                    dictCDS[entree]["lem"].append(entreesMAJ[entree]["lem"])
                                    dictCDS[entree]["ctxt"] = "AMBIGU"
                        
                        """
                        # On réencode les apostrophes et le balisage Unicode
                        ligneCorr = ligneCorr.replace("' ", "&#39;")
                        ligneCorr = f"<Unicode>{ligneCorr}</Unicode>"
                        # On écrit la ligne dans le fichier XML de sortie
                        xml_corr.write(ligneCorr + "\n")
                        
            
            print(f"Le fichier {filename} a été corrigé avec succès")
            
            # On remplace le fichier correctionsCDS.json avec les contextes actualisés
            with open(DICTCDS, mode="w") as f:
                json.dump(dictCDS, f, indent=3, ensure_ascii=False)
    

textCorrectionXML()