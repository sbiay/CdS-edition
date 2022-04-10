import click
import importlib
import os
from constantes import DICTPAGES

@click.command()
def dictCDStransform():
    """
    USAGE UNIQUE
    
    Ce script transforme le fichier dictCDS original, dont la structure est simplement une série de couples clé-valeur
    en un dictionnaire plus élaboré, dont les valeurs sont des dictionnaires avec des clé "lem" pour lemme
    et "ctxt" pour contexte.
    """
    
    from py.dictComplets.dictCDS import dict
    
    nouveauDict = {}
    
    for cle in dict:
        nouveauDict[cle] = {
            "lem": dict[cle],
            "ctxt": []
        }
    
    nouveauDict = str(nouveauDict).replace("},", "},\n").replace(": {", ":\n\t{").replace("', '", "',\n\t '")
    
    with open("./py/dictCDS.py", mode="w") as f:
        f.write(
            f"dictCDS = {nouveauDict}"
        )


def dictCDSintegration():
    """
    Ce script prend comme paramètres une source consistant en un dictionnaire python d'entrée
    le compare au contenu de dictCDS, intègre les entrées nouvelles et retourne des messages d'alertes
    pour les entrées générant un conflit d'intégration.
    :param source: dictionnaire python issu de la correction automatisée d'une page de transcription
    :type source: chemin de fichier
    """
    # On boucle sur les fichiers du dossier dictPages
    for root, dirs, files in os.walk(DICTPAGES):
        for filename in files:
            with open(DICTPAGES.strip() + "/Dict" + filename.replace(".xml", ".py"), "w") as file_out:
                print("writing to " + DICTPAGES + "/Dict" + filename.replace(".xml", ".py"))
                file_out.write("dictPage = ")
                file_out.write(dictionary)
    
    #with open("./py/dictPages/DictCdS02_Konv002-02_0067.json", mode="w", encoding="UTF-8") as f:
    #    On écrit le contenu du dictionnaire au format Jsonn en s'assurant d'encoder en UTF-8 et non en ASCII
    #    json.dump(dictPage, f, indent=2, ensure_ascii=False)

dictCDSintegration()