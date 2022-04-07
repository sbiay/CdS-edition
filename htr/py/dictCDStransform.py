"""
Ce script transforme le fichier dictCDS original, dont la structure est simplement une série de couples clé-valeur
en un dictionnaire plus élaboré, dont les valeurs sont des dictionnaires avec des clé "lem" pour lemme
et "ctxt" pour contexte.
"""

from dictCDS import dictCDS

nouveauDict = {}

for cle in dictCDS:
    nouveauDict[cle] = {
        "lem": dictCDS[cle],
        "ctxt": []
    }
    
nouveauDict = str(nouveauDict).replace("},", "},\n").replace(": {", ":\n\t{").replace("', '", "',\n\t '")

with open("./py/dictCDS.py", mode="w") as f:
    f.write(
        f"dictCDS = {nouveauDict}"
    )