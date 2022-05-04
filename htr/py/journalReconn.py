import csv
import click
import json
import os
from datetime import datetime
from constantes import JOURNALREC


@click.command()
@click.argument("MODELE")
@click.option("-v", "--veriteterrain", is_flag=True, default=False,
              help="Prend en compte le contenu du dossier ./sources/veriteTerrain")
@click.option("-i", "--ignore", default=False, multiple=True,
              help="Prend comme argument une liste de noms de modèles à ignorer")
def journalReconn(modele, veriteterrain, ignore):
    """
    Cette fonction prend comme argument le nom d'un modèle de reconnaissance d'écriture,
    si l'option -v est active, elle analyse les données d'entraînement fournies dans le dossier ./sources/veriteTerrain/
    puis inscrit avec la date courante, les données collectées, dans le fichier journal-reconn.json
    :param modele: nom de modèle HTR
    :param ignore: liste des collections que l'on ne souhaite pas ajouter au journal
    :type modele: str
    :return: None
    """
    # On récupère la liste des fichiers correspondant à chaque main
    mains = {}
    with open("./sources/mains.csv") as csvf:
        lecteur = csv.reader(csvf, delimiter='\t')
        
        # On lit chaque ligne du CSV
        for index, ligne in enumerate(lecteur):
            if index != 0:
                # Si la main n'est pas encore référencée, on initie sa clé
                if not mains.get(ligne[0]):
                    mains[ligne[0]] = []
                    mains[ligne[0]].append(ligne[1])
                # Si la main est référencée, on ajoute l'image sous forme de liste
                else:
                    mains[ligne[0]].append(ligne[1])
    
    # On analyse le contenu du dossier ./sources/veriteTerrain
    fichiersVT = []
    # Si l'option -v est active, on analyse le contenu du dossier ./sources/veriteTerrain
    if veriteterrain:
        for root, dirs, files in os.walk("./sources/veriteTerrain"):
            for fichier in files:
                # On ne sélectionne que les fichiers .jpg
                if fichier[-3:] == "jpg":
                    fichiersVT.append(fichier)
    
    # On récupère le nombre de fichiers pour chaque main
    donneesMains = []
    for main in mains:
        # On prend en compte la liste des mains à ignorer
        if main not in ignore:
            nb = 0
            for fichier in fichiersVT:
                if fichier in mains[main]:
                    nb += 1
            dico = {
                "nom_main": main,
                "nb_VT": nb,
                "accuracy": 0
            }
            donneesMains.append(dico)
    
    # On écrit l'entrée du journal
    date = f"{datetime.now().year}.{datetime.now().month}.{datetime.now().day} {datetime.now().hour}:" \
           f"{datetime.now().minute}"
    
    entree = {
        "date": date,
        "mains": donneesMains
    }
    
    # On récupère le contenu du fichier de journal
    with open(JOURNALREC) as f:
        journal = json.load(f)
    
    # On initie le modèle s'il n'existe pas dans le journal
    if not journal.get(modele):
        journal[modele] = []
    
    journal[modele].append(entree)
    
    # On écrit le résultat dans un fichier de sortie au format .py
    with open(JOURNALREC, mode="w") as jsonf:
        json.dump(journal, jsonf, indent=3, ensure_ascii=False, sort_keys=False)


if __name__ == "__main__":
    journalReconn()
