import click
import json
import os
from constantes import DICTPAGES, DICTCDS

def controleFormes(dictPage):
    """
    Cette fonction prend comme argument un dictionnaire de page, compare son contenu au dictCDS
    et retourne un dictCDS enrichi
    :param dictPage: dictionnaire de page
    :type dictPage: dict
    :return: dictCDS enrichi par de nouvelles formes, erreurs (dict), avertissements (list)
    :return type: tuple
    """
    # On charge le dictionnaire Json global de la correspondance CDS
    with open(DICTCDS) as f:
        dictCDS = json.load(f)
    
    # On boucle sur chaque clé du dictionnaire de page
    for forme in dictPage:
        # On ne traite les formes que si elles sont associés à un lemme qui les corrige
        if dictPage[forme]["lem"]:
            # On initie une liste d'erreurs d'intégration
            avertissements = []
            erreurs = {}
            # Si la forme existe déjà dans dictCDS mais que le lemme est vide (id est la correction est ambiguë)
            if forme in dictCDS and not dictCDS[forme]["lem"]:
                avertissements.append(forme)
            # Si la forme existe déjà dans dictCDS mais que les lemmes ne sont pas identiques
            elif forme in dictCDS and dictPage[forme]["lem"] != dictCDS[forme]["lem"]:
                # Alors on renseigne un journal d'erreurs
                erreurs[forme] = (dictPage[forme]["lem"], dictCDS[forme]["lem"])
            # Si la forme est absente de dictCDS, on l'y inscrit
            elif forme not in dictCDS:
                dictCDS[forme] = {
                    "lem": dictPage[forme]["lem"],
                    "ctxt": dictPage[forme]["ctxt"],
                }
    
    return dictCDS, erreurs, avertissements

@click.command()
@click.option("-f", "--file", type=str, help="Nom de fichier contenu dans le dossier "
                                             "./py/dicos/")
@click.option("-A", "--all", is_flag=True, default=False, help="Prend tous les fichiers du dossier ./py/dicos/")
def dictCDSintegration(file, all):
    """
    Ce script prend comme paramètres une source consistant en un fichier Json d'entrée contenu dans le dossier dicos
    le compare au contenu de corresp.json, intègre les entrées nouvelles et retourne des messages d'alertes
    pour les entrées générant un conflit d'intégration.
    :param fichierdictpages: fichier Json issu de la correction automatisée d'une page de transcription
    :type fichierdictpages: Json
    :returns: None
    """
    if not file and not all:
        print("Aucun argument n'a été passé !")
        print("Pour plus d'information saisissez la commande :\npython3 py/integrationDicts.py --help")
    else:
        
        # Si l'option pour transformer tous les dictionnaires du dossier dicos est active
        if all:
            # On boucle sur les fichiers du dossier dicos qui commencent par "page"
            for root, dirs, files in os.walk(DICTPAGES):
                for filename in files:
                    # On pose comme condition que le fichier est une extension .json
                    if filename[-4:] == "json" and filename[:4] == "page":
                        # On charge le dictionnaire Json global de la correspondance CDS
                        with open(DICTCDS) as f:
                            dictCDS = json.load(f)
                        
                        # On charge le dictionnaire de la page
                        with open(DICTPAGES + filename) as f:
                            dictPage = json.load(f)
                        print(f"Traitement du fichier {filename}")
                        
                        # On traite le contenu du dictionnaire de page avec la fonction controleFormes()
                        dictCDS = controleFormes(dictPage)[0]
                        erreurs = controleFormes(dictPage)[1]
                        avertissements = controleFormes(dictPage)[2]
                        if avertissements:
                            for forme in avertissements:
                                print(f'''La forme "{forme}" a déjà été signalée comme ambiguë (elle a donc été '''
                                f'''ignorée).''')
                        if erreurs:
                            for forme in erreurs:
                                print(f'''La forme "{forme}" que l'on souhaite corriger en "{erreurs[forme][0]}"'''
                                f'''possède déjà une correction en "{erreurs[forme][1]}". Veuillez corriger les '''
                                f'''dictionnaires et relancer le script.''')
                            break
                        # On remplace le fichier corresp.json par la version enrichie
                        with open(DICTCDS, mode="w") as f:
                            json.dump(dictCDS, f, indent=3, ensure_ascii=False)
                            print("\nLe dictionnaire corresp.json est désormais à jour.")
        
        # Si on ne transforme qu'un seul fichier passé en argument
        else:
            # On charge le dictionnaire Json global de la correspondance CDS
            with open(DICTCDS) as f:
                dictCDS = json.load(f)
            
            # On charge le dictionnaire Json passé en argument
            with open(f"./py/dicos/{file}") as f:
                dictPage = json.load(f)
            print(f"Traitement du fichier {file}")
            
            dictCDS = controleFormes(dictPage)[0]
            erreurs = controleFormes(dictPage)[1]
            avertissements = controleFormes(dictPage)[2]
            if avertissements:
                for forme in avertissements:
                    print(f'''La forme "{forme}" a déjà été signalée comme ambiguë (elle a donc été '''
                          f'''ignorée).''')
            if erreurs:
                for forme in erreurs:
                    print(f'''La forme "{forme}" que l'on souhaite corriger en "{erreurs[forme][0]}"'''
                          f'''possède déjà une correction en "{erreurs[forme][1]}". Veuillez corriger les '''
                          f'''dictionnaires et relancer le script.''')
                    break
                    
            # On remplace le fichier corresp.json par la version enrichie
            with open(DICTCDS, mode="w") as f:
                json.dump(dictCDS, f, indent=3, ensure_ascii=False)
                print("Le dictionnaire corresp.json est désormais à jour.")

dictCDSintegration()