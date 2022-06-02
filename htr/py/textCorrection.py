import os
import json
import click
import spacy
from lxml import etree
# Installation de Spacy https://spacy.io/usage#quickstart
# module linguistique fr_core_news_sm
from constantes import XMLaCORRIGER, XMLCORRIGEES, DICTPAGESCORR, DICTCDS


@click.command()
def textCorrectionXML():
    """
    Ce script ouvre les fichiers contenus dans le dossier des prédictions XML-Alto à corriger
    
    - author: Floriane Chiffoleau
    - date: June 2020
    - original version:
    https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Correction/text_correction_XML.py
    """
    # On charge le dictionnaire complet de la correspondance
    with open(DICTCDS) as f:
        dictCDS = json.load(f)
    
    # On dézippe l'objet os pour obtenir la racine, les dossiers et les fichiers du chemin passé en premier argument
    for root, dirs, files in os.walk(XMLaCORRIGER):
        # On boucle sur chaque nom de fichier
        for filename in files:
            # On charge le dictionnaire Json corrigé de la page
            try:
                with open(DICTPAGESCORR + "page_" + filename.replace(".xml", ".json")) as dico:
                    dictPage = json.load(dico)
            except:
                # TODO vérifier pourquoi ce print ne marche pas
                print(f"Le dictionnaire de page page_{filename.replace('.xml', '.json')} n'a pas été chargé " \
                      "correctement.")
                break

            # On ouvre le fichier XML d'entrée
            with open(XMLaCORRIGER + filename) as f:
                xml = etree.parse(f)
            # On implémente l'espace de nom alto
            nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
            # On récupère tous les contenus des lignes de texte
            contenuXML = xml.xpath("//alto:String/@CONTENT", namespaces=nsmap)

            # On ouvre le fichier XML de sortie
            with open(XMLCORRIGEES + filename, 'w') as xml_corr:
                # On initie l'index des lignes d'écriture
                index = 0
                # On boucle sur chaque ligne du contenuXML
                for ligneBrute in contenuXML:
                    print(ligneBrute)
                    # On initie la liste des entrées dont on actualisera le contexte dans le dictCDS
                    entreesMAJ = {}
                    ligne = ligneBrute
                    # On remplace l'encodage XML des apostrophes
                    ligne = ligne.replace("&#39;", "'")
                    # On supprime l'indentation
                    ligne = ligne.replace("          ", "")
                    # On supprime également les balises collées au premier et au dernier mot
                    ligne = ligne.replace('''<String CONTENT=''', "").replace('"', '')
    
                    # Avant de tokéniser on doit procéder au remplacement des formes avec apostrophe
                    # et des formes avec espace au milieu
                    # TODO Condition utile seulement pour les tests
                    if dictPage.get(str(index)):
                        for forme in dictPage[str(index)]:
                            lemme = None
                            if " " in forme or "'" in forme:
                                # On n'intervient que si la valeur de lemme n'est pas "null"
                                if dictPage[str(index)][forme]["lem"]:
                                    # On peut se retrouver avec une liste dont le seul élément est "null"
                                    if dictPage[str(index)][forme]["lem"][0]:
                                        # La correction retenue ou "lemme"
                                        # est le premier item de la liste-valeur de la clé "lem"
                                        lemme = dictPage[str(index)][forme]["lem"][0]
                            if lemme:
                                ligne = ligne.replace(forme, lemme)
                                entreesMAJ[forme] = {
                                    "lem": [lemme],
                                    "ctxt": []
                                }
    
                    # On tokénise la ligne
                    nlp = spacy.load("fr_core_news_sm")
                    doc = nlp(ligne)
                    ligne = [token.text for token in doc]
                    # On initie la ligne corrigée
                    ligneCorr = []
                    # On boucle sur chaque mot
                    for mot in ligne:
                        # On initie le lemme ou correction
                        lemme = None
                        # TODO Condition utile seulement pour les tests (voir si on peut la retirer plus tard)
                        if dictPage.get(str(index)):
                            for forme in dictPage[str(index)]:
                                # On n'intervient que si la valeur de lemme n'est pas "null"
                                if forme == mot and dictPage[str(index)][forme]["lem"]:
                                    # On peut se retrouver avec une liste dont le seul élément est "null"
                                    if dictPage[str(index)][forme]["lem"][0]:
                                        # La correction retenue ou "lemme"
                                        # est le premier item de la liste-valeur de la clé "lem"
                                        lemme = dictPage[str(index)][forme]["lem"][0]
                        # S'il y a bien une correction proposée
                        if lemme:
                            # On ajoute le mot corrigé à la ligne
                            ligneCorr.append(lemme)
                            entreesMAJ[mot] = {
                                "lem": [lemme],
                                "ctxt": []
                            }
                        # Si le lemme est resté None, il n'y a pas de correction à appliquer
                        else:
                            ligneCorr.append(mot)
    
                    # On recompose la ligne en tant que chaîne
                    ligneCorr = ' '.join(ligneCorr)
                    # On élimine les espaces en trop
                    ligneCorr = ligneCorr.replace(' ,', ',').replace(' .', '.') \
                        .replace('( ', '(').replace(' )', ')') \
                        .replace("' ", "'")
                    # On renvoie le contexte du mot traité dans le dictionnaire global
                    # en reparsant la ligne corrigée
                    for entree in entreesMAJ:
                        # On pose d'abord comme condition qu'il y ait un lemme
                        if entreesMAJ[entree]["lem"]:
                            # On inscrit la ligne corrigée comme contexte de l'entrée du dictionnaire
                            entreesMAJ[entree]["ctxt"] = ligneCorr.replace(
                                entreesMAJ[entree]["lem"][0], entreesMAJ[entree]["lem"][0].upper()
                            )
                            # On met à jour le dictCDS avec les contextes actualisés
                            # Si la forme n'existe pas déjà
                            if not dictCDS.get(entree):
                                dictCDS[entree] = entreesMAJ[entree]
                            # Si la forme existe déjà
                            else:
                                # Si le lemme que l'on propose n'est pas encore référencé
                                if not entreesMAJ[entree]["lem"][0] in dictCDS[str(entree)]["lem"]:
                                    dictCDS[entree]["lem"].append(entreesMAJ[entree]["lem"][0])
                                    dictCDS[entree]["ctxt"] = "AMBIGU"
    
                    # On réencode les apostrophes et le balisage Unicode
                    ligneCorr = ligneCorr.replace("' ", "&#39;")
                    ligneCorr = f'''<String CONTENT="{ligneCorr}"'''
                    # On écrit la ligne dans le fichier XML de sortie
                    xml_corr.write(ligneCorr + "\n")
    
                    # On implémente l'index pour la ligne suivante
                    index += 1
            
            print(f"Le fichier {filename} a été corrigé avec succès")
            
            # On remplace le fichier correctionsCDS.json avec les contextes actualisés
            with open(DICTCDS, mode="w") as f:
                json.dump(dictCDS, f, indent=3, ensure_ascii=False)


if __name__ == "__main__":
    textCorrectionXML()
