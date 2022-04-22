import click
import os
import json
from lxml import etree
from spellchecker import SpellChecker
from constantes import XMLaCORRIGER, DICTCDS, DICTGENERAL, DICTPAGESNONCORR, VERITESTERRAIN as VT


def suppress_punctuation(text):
    """ Suppress punctuation in a text

    :param text str: Text to clean up
    :returns: Text without punctuation
    :rtype: str
    """
    punctuation = "!:;\",?’."
    for sign in punctuation:
        text = text.replace(sign, " ")
    return text


def collecte_mots():
    """
    Cette fonction parse le contenu des vérités de terrain et retourne dictionnaire
    dont les clés sont les mots et les valeurs leur nombre d'ocurrences.
    :returns: comptage des occurrences de mots dans les vérités de terrain
    :return type: dict
    """
    chiffres = "1234567890"
    motsParses = []
    # On boucle sur chaque fichier contenu dans le dossier des vérités de terrain
    for root, dirs, files in os.walk(VT):
        for filename in files:
            # On pose comme condition de ne traiter que des fichiers XML (le dossier contient aussi des images)
            if filename[-3:] == "xml":
                # On ouvre le fichier
                with open(VT + filename) as f:
                    xml = etree.parse(f)
                racine = xml.getroot()
                nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
                textes = xml.xpath("//alto:String/@CONTENT", namespaces=nsmap)
                for ligne in textes:
                    # On nettoie le texte de sa ponctuation
                    ligne = suppress_punctuation(ligne)
                    ligne = ligne.replace("  ", " ")
                    # On nettoie le texte de sa ponctuation
                    for signe in chiffres:
                        ligne = ligne.replace(signe, " ").replace("  ", " ")
                    mots = ligne.split(' ')
                    for index, mot in enumerate(mots):
                        # On verifie que le mot ne soit pas vide
                        if mot:
                            # On vérifie que le mot ne soit pas césuré et pas en début de ligne (potentiellement coupé)
                            if index != 0 and mot[-1] != '-':
                                motsParses.append(mot)
    
    # On compte le nombre d'occurrences de chaque mot
    comptage = {}
    for mot in motsParses:
        comptage[mot] = motsParses.count(mot)
    
    # On exporte le comptage des mots pour les contrôler au besoin
    with open("./py/dicos/motsCDS.json", mode="w") as jsonf:
        json.dump(comptage, jsonf, ensure_ascii=False, indent=1)
    
    return comptage


def ordreOccurrences(liste):
    """
    Cette fonction prend comme argument une liste de mot,
    récupère le nombre d'occurrences de chacun parmi les vérités de terrain
    et retourne la liste de ces mots classées par ordre descendant de nombres d'occurrences
    :param liste: liste de mots
    :type liste: list
    :returns: liste classée
    :type return: list
    """
    # On charge tous les mots des vérités de terrain
    tousMots = collecte_mots()
    
    # On récupère le nombre d'occurrences des mots de la liste passée en argument
    comptage = {}
    for mot in liste:
        if tousMots.get(mot):
            comptage[mot] = tousMots[mot]
    
    # On détermine quel est le nombre maximal d'occurrences pour les mots de la liste
    max = 0
    for mot in comptage:
        if comptage[mot] > max:
            max = comptage[mot]
    
    # On écrit une nouvelle liste classée par nombre d'occurrences
    nouvListe = []
    compteur = max
    while compteur > 0:
        for mot in comptage:
            if comptage[mot] == compteur:
                nouvListe.append(mot)
        compteur -= 1
    
    return nouvListe


@click.command()
def spellcheck_texts_page_XML():
    """
    Ce script ouvre les fichiers XML-Page contenus dans un dossier défini (constante XMLaCORRIGER)
    analyse chaque mot en le confrontant :
    - à ceux contenus dans les vérités de terrain (constante VERITESTERRAIN).
    - aux formes listées dans le dictionnaire de corrections de la correspondance (constante DICTCDS).
    Il applique aux formes non identifiées précédemment le module SpellChecker.
    En sortie, on écrit pour chaque fichier XML-Page un fichier Json contenant des propositions de correction.
    
    Source :
    - author: Floriane Chiffoleau.
    - date: February 2021.
    - URL: https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Correction/spellcheck_texts_PAGEXML.py
    """
    spell = SpellChecker(language=None, local_dictionary=DICTGENERAL, case_sensitive=True, distance=2)
    # With 'case_sensitive=True', we precise that all the words are processed as they are written in the text
    # This means that all the uppercase words will be considered wrong but that helps correct them
    # To use that technique, we have to call a local dictionary
    
    # On charge le contenu du dictionnaire de la correspondance
    with open(DICTCDS) as jsonf:
        correctionsCDS = json.load(jsonf)
    
    # On charge les lemmes des vérités de terrain
    tousMots = collecte_mots()
    
    # On boucle sur chaque fichier du dossier défini par la constante XMLaCORRIGER
    for root, dirs, files in os.walk(XMLaCORRIGER):
        for filename in files:
            # On initie le dictionnaire de page
            dictPage = {}
            
            # On ouvre le fichier XML d'entrée
            xml = etree.parse(XMLaCORRIGER + filename)
            print("Le fichier " + XMLaCORRIGER + filename + " est en cours de lecture.")
            # TODO prévoir une gestion de plusieurs formats XML
            nsmap = {'page': "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"}
            tous_unicode = xml.xpath("//page:Unicode", namespaces=nsmap)
            
            # On parse les lignes de transcription du fichier XML-Page
            for index, unicode in enumerate(tous_unicode):
                content = unicode.text
                # Les traitements ne peuvent avoir lieu que si le contenu de la ligne n'est pas vide
                if content:
                    content = suppress_punctuation(content)
                    words = content.split(" ")
                    # On initie un dictionnaire pour les corrections de la ligne
                    dictLigne = {}
                    # On initie la liste des mots inconnus que l'on passera au SpellChecker
                    motsrestants = []
                    
                    # On boucle sur chaque mot
                    for forme in words:
                        # TODO on teste en éliminant les mots des VT
                        if forme not in tousMots.keys():
                            # On n'ajoute qu'une seule fois chaque forme au dictionnaire de page (même si plusieurs
                            # résolutions différentes seraient souhaitables)
                            if forme and not dictPage.get(forme):
                                # On récupère le contexte de la forme en l'y inscrivant en capitales
                                contexte = content.replace(forme, forme.upper())
                                # On cherche chaque mot dans la liste personnalisée des corrections
                                if correctionsCDS.get(forme):
                                    # Si le mot est ambigu (plusieurs propositions)
                                    if len(correctionsCDS[forme]['lem']) > 1:
                                        # On ordonne les propositions de correction de la plus fréquente à la moins fréquente
                                        # grâce à la fonction ordreOccurrences()
                                        propositions = ordreOccurrences(correctionsCDS[forme]['lem'])
                                        # On écrit l'entrée du dictionnaire pour préciser le contexte
                                        dictLigne[forme] = {
                                            'lem': propositions,
                                            'ctxt': contexte.replace("'", ' '),
                                        }
                                    # Si le mot n'est pas ambigu
                                    else:
                                        dictLigne[forme] = {
                                            'lem': correctionsCDS[forme]['lem'],
                                            'ctxt': contexte.replace("'", ' '),
                                        }
                                
                                # Si la forme n'est pas dans la liste personnalisée des corrections
                                elif forme:
                                    # Si elle ne figure pas parmi les mots connus des vérités de terrain
                                    if forme in tousMots.keys():
                                        dictLigne[forme] = {
                                            'lem': [None],
                                            'ctxt': contexte.replace("'", ' '),
                                        }
                                    # Si elle ne figure pas non plus parmi les mots connus des vérités de terrain
                                    else:
                                        # Alors on l'ajoute à la liste des mots restants à traiter
                                        motsrestants.append(forme)
    
                    # On analyse les mots restants
                    if motsrestants:
                        misspelled = spell.unknown(motsrestants)
                        # On boucle sur les mots pour chercher ceux ne faisant l'objet d'aucune proposition
                        for forme in motsrestants:
                            contexte = content.replace(forme, forme.upper())
                            if forme not in misspelled:
                                dictLigne[forme] = {
                                    'lem': [None],
                                    'ctxt': contexte.replace("'", ' ')
                                }
                        # On boucle sur les propositions de corrections
                        for forme in misspelled:
                            contexte = content.replace(forme, forme.upper())
                            dictLigne[forme] = {
                                'lem': [spell.correction(forme)],
                                'ctxt': contexte.replace("'", ' ')
                            }
                    # On boucle à nouveau sur chaque mot pour ajouter les propositions de correction dans l'ordre
                    dictLigneOrd = {}
                    for forme in words:
                        if dictLigne.get(forme):
                            dictLigneOrd[forme] = dictLigne[forme]
                    # On ajoute le dictionnaire ligne ordonné au dictionnaire page
                    dictPage[index] = dictLigneOrd
            
            # On écrit le résultat dans un fichier de sortie au format .py
            with open(DICTPAGESNONCORR.strip() + "page_" + filename.replace(".xml", ".json"), "w") as jsonf:
                json.dump(dictPage, jsonf, indent=3, ensure_ascii=False, sort_keys=False)
                print(f"=> Le dictionnaire {DICTPAGESNONCORR.strip() + 'page_' + filename.replace('.xml', '.json')}"
                      f" a été écrit correctement.\n")


if __name__ == "__main__":
    spellcheck_texts_page_XML()
