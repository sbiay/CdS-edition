import click
import json
import os
from constantes import DICTPAGES, DICTCDS

# On charge le dictionnaire Json global de la correspondance CDS
with open(f"./py/dictComplets/dictCDS.json") as f:
    dictCDS = json.load(f)

def controleFormes(dictPage):
    """
    Cette fonction prend comme argument un dictionnaire de page, compare son contenu au dictCDS
    et retourne un dictCDS enrichi
    :param dictPage: dictionnaire de page
    :type dictPage: dict
    :return: dictCDS enrichi par de nouvelles formes
    :return type: dict
    """
    # On boucle sur chaque clé du dictionnaire de page
    for forme in dictPage:
        # On ne traite les formes que si elles sont associés à un lemme qui les corrige
        if dictPage[forme]["lem"]:
            # Si la forme existe déjà dans dictCDS mais que les lemmes ne sont pas identiques
            if forme in dictCDS and dictPage[forme]["lem"] != dictCDS[forme]["lem"]:
                # Alors on arrête le code et on délivre un message d'alerte
                print(f"La forme {forme}, que l'on souhaite corriger en {dictPage[forme]['lem']}, "
                      f"possède déjà une correction de référence : "
                      f"{dictCDS[forme]['lem']}")
                print("Veuillez corriger les dictionnaires et relancer le script (si les deux solutions sont "
                      "possibles, inscrivez null en tant que lemme dans les deux dictionnaires, la forme ne sera "
                      "plus corrigée automatiquement).")
                break
            # Si la forme est absente de dictCDS, on l'y inscrit
            elif forme not in dictCDS:
                dictCDS[forme] = {
                    "lem": dictPage[forme]["lem"],
                    "ctxt": dictPage[forme]["ctxt"],
                }
    return dictCDS

@click.command()
@click.option("-f", "--file", type=str, help="Nom de fichier contenu dans le dossier "
                                                                "./py/dictPages/")
@click.option("-A", "--all", is_flag=True, default=False, help="Prend tous les fichiers du dossier ./py/dictPages/")
def dictCDSintegration(file, all):
    """
    Ce script prend comme paramètres une source consistant en un fichier Json d'entrée contenu dans le dossier dictPages
    le compare au contenu de dictCDS.json, intègre les entrées nouvelles et retourne des messages d'alertes
    pour les entrées générant un conflit d'intégration.
    :param fichierdictpages: fichier Json issu de la correction automatisée d'une page de transcription
    :type fichierdictpages: Json
    :returns: None
    """
    
    # Si l'option pour transformer tous les dictionnaires du dossier dictPages est active
    if all:
        # On boucle sur les fichiers du dossier dictPages
        for root, dirs, files in os.walk(DICTPAGES):
            for filename in files:
                # On pose comme condition que le fichier est une extension .json
                if filename[-4:] == "json":
                    with open(DICTPAGES + filename) as f:
                        dictPage = json.load(f)
                    dictCDS = controleFormes(dictPage)
                    print(f"Le fichier {filename} a été traité avec succès.")
                    
    # Si on ne transforme qu'un seul fichier passé en argument
    else:
        # On charge le dictionnaire Json passé en argument
        with open(f"./py/dictPages/{file}") as f:
            dictPage = json.load(f)
        dictCDS = controleFormes(dictPage)
        print(f"Le fichier {file} a été traité avec succès.")
    
    # On remplace le fichier dictCDS.json par la version enrichie
    with open(DICTCDS, mode="w") as f:
        json.dump(dictCDS, f, indent=3, ensure_ascii=False)
    print("Le dictionnaire dictCDS.json est désormais à jour.")
    
dictCDSintegration()