# -*- UTF-8 -*-

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

import os
import sys
from bs4 import BeautifulSoup
from spellchecker import SpellChecker
from constantes import XMLaCORRIGER, DICTPAGES
from dictCDScorr import dict

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

# On charge le dictionnaire local dans un fichier Json pour pouvoir le passer à SpellChecker
spell = SpellChecker(language=None, local_dictionary="./dictComplets/dictGeneral.json", case_sensitive=True)
# With 'case_sensitive=True', we precise that all the words are processed as they are written in the text
# This means that all the uppercase words will be considered wrong but that helps correct them
# To use that technique, we have to call a local dictionary

for root, dirs, files in os.walk(XMLaCORRIGER):
    for filename in files:
        dictionary = {}
        # On ouvre le fichier XML d'entrée
        with open(XMLaCORRIGER + filename, 'r') as xml_file:
            print("reading from "+ XMLaCORRIGER + filename)
            soup = BeautifulSoup(xml_file, 'lxml')
        for unicode in soup.find_all('unicode'):
            content = unicode.string
            content = suppress_punctuation(content)
            words = content.split(" ")
            # On boucle sur chaque mot de l'élément Unicode courant
            for index, mot in enumerate(words):
                # On cherche chaque mot dans le dictCDS
                if dict.get(mot):
                    # On vérifie que la solution ne soit pas ambiguë (id est qu'il existe bien un lemme)
                    if dict[mot].get('lem'):
                        # On initie le contexte comme une liste
                        contexte = []
                        try:
                            contexte.append(words[index - 3])
                            contexte.append(words[index - 2])
                            contexte.append(words[index - 1])
                            contexte.append(dict[mot]['lem'].upper())
                            contexte.append(words[index + 1])
                            contexte.append(words[index + 2])
                            contexte.append(words[index + 3])
                        except IndexError:
                            True
                        contexte = ' '.join(contexte)
                        # On écrit l'entrée du dictionnaire pour préciser le contexte
                        dictionary[mot] = {
                            'lem': dict[mot]['lem'],
                            'ctxt': contexte.replace("'", ' '),
                            'deja utilisé': dict[mot]['ctxt']
                        }
                else:
                    # On cherche les mots dans dictionnaireComplet grâce à la fonction spell
                    misspelled = spell.unknown(mot)
                    # On énumère les mots de la ligne afin de pouvoir inscrire le contexte dans l'entrée de dictionnaire
                    if misspelled:
                        # On initie le contexte comme une liste
                        contexte = []
                        try:
                            contexte.append(words[index - 3])
                            contexte.append(words[index - 2])
                            contexte.append(words[index - 1])
                            contexte.append(spell.correction(mot).upper())
                            contexte.append(words[index + 1])
                            contexte.append(words[index + 2])
                            contexte.append(words[index + 3])
                        except IndexError:
                            True
                        contexte = ' '.join(contexte)
                        # On écrit l'entrée du dictionnaire pour préciser le contexte
                        dictionary[mot] = {
                            'lem': spell.correction(mot),
                            'ctxt': contexte.replace("'", ' ')
                        }
        # On re-type et indente le dictionnaire pour la sortie
        dictionary = str(dictionary).replace("},", "},\n").replace(": {", ":\n\t{").replace("', '", "',\n\t '")
        
        # On écrit le résultat dans un fichier de sortie au format .py
        with open(DICTPAGES.strip() + "/Dict" + filename.replace(".xml", ".py"), "w") as file_out:
            print("writing to "+ DICTPAGES + "/Dict" + filename.replace(".xml", ".py"))
            file_out.write("dictPage = ")
            file_out.write(dictionary)

