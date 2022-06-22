import os
import json
import click
import spacy
from lxml import etree
# Installation de Spacy https://spacy.io/usage#quickstart
# module linguistique fr_core_news_sm
from outils import triFichiers
from constantes import XMLaCORRIGER, XMLCORRIGEES, DICTPAGESCORR, DICTCDS


@click.command()
@click.option("-n", "--no-update", is_flag=True, default=False, help="Ne réapplique pas les corrections aux fichiers "
                                                                     "déjà créés")
def textCorrectionXML(no_update):
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

    # On trie la liste des fichiers contenus dans le dossier de prédictions
    tri = triFichiers(XMLaCORRIGER)
    # On récupère la liste des fichiers XML déjà corrigés
    corriges = triFichiers(XMLCORRIGEES)
    
    # On définit la liste des fichiers à traiter en fonction de l'option --no-update
    atraiter = []
    if no_update:
        for fichier in tri:
            # On sépare le nom du fichier de son chemin complet
            chemin = fichier.split("/")
            fichierSSchemin = chemin[-1]
            # On cherche le nom du fichier dans le dossier des prédictions corrigées
            if "./predic-corrigees/" + fichierSSchemin not in corriges:
                atraiter.append(fichier)
    else:
        atraiter = tri
    
    # On boucle sur chaque nom de fichier
    for fichier in atraiter:
        # On charge le dictionnaire Json corrigé de la page
        try:
            with open(DICTPAGESCORR + "page_" + fichier[len(XMLaCORRIGER):].replace(".xml", ".json")) as dico:
                dictPage = json.load(dico)
        except:
            print(f"Le dictionnaire {DICTPAGESCORR}page_{fichier[len(XMLaCORRIGER):].replace('.xml', '.json')} "
                  f"n'a pas été chargé correctement (existe-t-il ? est-il valide ?).")
            break
        
        # On ouvre le fichier XML d'entrée
        with open(fichier) as f:
            xml = etree.parse(f)
        # On implémente l'espace de nom alto
        nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
        # On récupère tous les id des lignes de texte
        ids = xml.xpath("//alto:TextLine/@ID", namespaces=nsmap)
        # On récupère tous les contenus des lignes de texte
        contenuXML = xml.xpath("//alto:String/@CONTENT", namespaces=nsmap)
        
        # On ouvre le fichier XML de sortie
        print(f"Le fichier {fichier[len(XMLaCORRIGER):]} est en cours de correction.")
        # On initie l'index des lignes d'écriture
        index = 1
        # On boucle sur chaque ligne du contenuXML
        for ligne in contenuXML:
            # On initie la liste des entrées dont on actualisera le contexte dans le dictCDS
            entreesMAJ = {}
            # On convertit la valeur ligne en str
            ligne = str(ligne)
            
            # Avant de tokéniser on doit procéder au remplacement des formes avec apostrophe
            # et des formes avec espace au milieu
            # On pose d'abord comme condition que la ligne du texte soit référencée dans le dictionnaire de page
            if dictPage.get(str(index)):
                # On boucle sur chaque forme possédant une correction
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
                # On pose d'abord comme condition que la ligne du texte soit référencée dans le dictionnaire de page
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
            
            # On récupère l'élément XML contenant la ligne en cours de correction
            prediction = xml.xpath(f"//alto:TextLine[@ID='{ids[index - 1]}']/alto:String", namespaces=nsmap)
            prediction = prediction[0]
            # On remplace la valeur de l'attribut @CONTENT par la ligne corrigée
            prediction.attrib['CONTENT'] = ligneCorr
            
            # On écrit l'arbre dans un fichier de sortie
            xml.write(XMLCORRIGEES + fichier[len(XMLaCORRIGER):], method="xml", pretty_print=True, xml_declaration=True,
                      encoding="UTF-8")
            
            # On implémente l'index pour la ligne suivante
            index += 1
        
        print(f"Le fichier {fichier[len(XMLaCORRIGER):]} a été corrigé avec succès.\n")
        
        # On remplace le fichier correctionsCDS.json avec les contextes actualisés
        with open(DICTCDS, mode="w") as f:
            json.dump(dictCDS, f, indent=3, ensure_ascii=False)


if __name__ == "__main__":
    textCorrectionXML()
