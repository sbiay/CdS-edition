import os
from lxml import etree
from bs4 import BeautifulSoup
from spellchecker import SpellChecker
from constantes import XMLaCORRIGER, DICTGENERAL, DICTPAGES, VERITESTERRAIN as VT
from dictComplets.dictCDS import dict


def get_lemmes():
    """
    Cette fonction parse le contenu des vérités de terrain et retourne un set des mots qu'elles contiennent.
    :returns: mots contenus dans les vérités de terrain.
    :return type: set
    """
    ponctuation = ",;':!.()"
    chiffres = "1234567890"
    motsParses = []
    # On boucle sur chaque fichier contenu dans le dossier des vérités de terrain
    for root, dirs, files in os.walk(VT):
        for filename in files:
            # On ouvre le fichier
            with open(VT + filename) as f:
                xml = etree.parse(f)
            racine = xml.getroot()
            nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
            textes = xml.xpath("//alto:String/@CONTENT", namespaces=nsmap)
            for ligne in textes:
                # On nettoie le texte de sa ponctuation
                for signe in ponctuation:
                    ligne = ligne.replace(signe, " ").replace("  ", " ")
                # On nettoie le texte de sa ponctuation
                for signe in chiffres:
                    ligne = ligne.replace(signe, " ").replace("  ", " ")
                mots = ligne.split(' ')
                for mot in mots:
                    # On verifie que le mot ne soit pas vide et pas césuré
                    if mot and mot[-1] != '-':
                        motsParses.append(mot)
    
    # On convertit les mots récoltés en set pour éliminer les doublons et on ajoute les nouveaux au set lemmes
    motsParses = set(motsParses)
    return motsParses


def suppress_punctuation(text):
    """ Suppress punctuation in a text
    
    :param text str: Text to clean up
    :returns: Text without punctuation
    :rtype: str
    """
    punctuation = "!:;\",?'’."
    for sign in punctuation:
        text = text.replace(sign, " ")
    return text


def spellcheck_texts_page_XML():
    """
    - author: Floriane Chiffoleau
    - date: February 2021
    - description: Recovering orthographic errors in PAGE XML files
    - input: PAGE XML files
    - output: Python dictionnaries
    - usage :
        ======
        python name_of_this_script.py arg1 arg2 arg3
    
        arg1: folder of the PAGE XML files
        arg2: folder for the Python dictionnaries
        arg3: local dictionary adapted to the content's language of the PAGE XML
    
    """
    # On charge le dictionnaire local dans un fichier Json pour pouvoir le passer à SpellChecker
    spell = SpellChecker(language=None, local_dictionary=DICTGENERAL, case_sensitive=True)
    # With 'case_sensitive=True', we precise that all the words are processed as they are written in the text
    # This means that all the uppercase words will be considered wrong but that helps correct them
    # To use that technique, we have to call a local dictionary
    
    for root, dirs, files in os.walk(XMLaCORRIGER):
        for filename in files:
            dictionary = {}
            # On ouvre le fichier XML d'entrée
            with open(XMLaCORRIGER + filename, 'r') as xml_file:
                print("reading from " + XMLaCORRIGER + filename)
                soup = BeautifulSoup(xml_file, 'lxml')
            for unicode in soup.find_all('unicode'):
                content = unicode.string
                content = suppress_punctuation(content)
                
                words = content.split(" ")
                # On boucle sur chaque mot de l'élément Unicode courant
                for index, mot in enumerate(words):
                    contexte = content.replace(mot, mot.upper())
                    # On cherche chaque mot dans les lemmes des vérités de terrain
                    if mot not in get_lemmes():
                        # On cherche chaque mot dans le dictCDS
                        if dict.get(mot):
                            # On vérifie que la solution ne soit pas ambiguë (id est qu'il existe bien un lemme)
                            if dict[mot].get('lem'):
                                # On écrit l'entrée du dictionnaire pour préciser le contexte
                                dictionary[mot] = {
                                    'lem': dict[mot]['lem'],
                                    'ctxt': contexte.replace("'", ' '),
                                    'deja utilisé': dict[mot]['ctxt']
                                }
                        # On cherche les mots dans dictionnaireComplet grâce à la fonction spell
                        elif spell.unknown(mot):
                            # On écrit l'entrée du dictionnaire pour préciser le contexte
                            dictionary[mot] = {
                                'lem': spell.correction(mot),
                                'ctxt': contexte.replace("'", ' ')
                            }
                        # S'il n'a aucune proposition de correction identifiée
                        else:
                            dictionary[mot] = {
                                'lem': None,
                                'ctxt': contexte.replace("'", ' ')
                            }
            # On re-type et indente le dictionnaire pour la sortie
            dictionary = str(dictionary).replace("},", "},\n").replace(": {", ":\n\t{").replace("', '", "',\n\t '")
            
            # On écrit le résultat dans un fichier de sortie au format .py
            with open(DICTPAGES.strip() + "/Dict" + filename.replace(".xml", ".py"), "w") as file_out:
                print("writing to " + DICTPAGES + "/Dict" + filename.replace(".xml", ".py"))
                file_out.write("dictPage = ")
                file_out.write(dictionary)

spellcheck_texts_page_XML()