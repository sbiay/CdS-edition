import csv
import click
import json
import os
from datetime import datetime
from constantes import TRAITNTENCOURS, JOURNALREC


@click.command()
@click.argument("MODELE")
@click.option("-n", "--no-ground-truth", is_flag=True, default=False,
              help="Prend en compte le contenu des dossiers train/")
@click.option("-i", "--ignore", default=list, multiple=True,
              help="Prend comme argument une liste de noms de modèles à ignorer")
def journalReconn(modele, no_ground_truth, ignore):
    """
    Cette fonction prend comme argument le nom d'un modèle de reconnaissance d'écriture,
    si l'option -v est active, elle analyse les données d'entraînement fournies dans le dossier ./sources/veriteTerrain/
    puis inscrit avec la date courante, les données collectées, dans le fichier journal-reconn.json
    :param no_ground_truth: définit si l'on doit ignorer le contenu des dossiers train/
    :param modele: nom de modèle HTR
    :param ignore: liste des collections que l'on ne souhaite pas ajouter au journal
    :type no_ground_truth: bool
    :type modele: str
    :type ignore: list
    """
    
    # On initie la liste des vérités de terrain
    fichiersVT = []
    
    # On récupère la liste des fichiers correspondant à chaque main
    mains = {}
    # On analyse l'arborescence courante
    for racine, dossiers, fichiers in os.walk(TRAITNTENCOURS):
        # On boucle sur les fichiers
        for fichier in fichiers:
            # On ne sélectionne que les fichiers .jpg et les fichiers rangés dans des dossiers de main
            if fichier[-3:] == "jpg" and racine[:22] == f"{TRAITNTENCOURS}main":
                # On récupère le nom de la main en découpant la racine
                main = racine.split("/")[2]
                # Si la main est déjà référencée dans le dict mains, on ajoute l'image à la liste-valeur
                if mains.get(main):
                    mains[main]["all_files"].append(fichier)
                # Si la main n'est pas encore référencée dans le dict mains, on l'ajoute
                else:
                    mains[main] = {
                        "gt_files": [],
                        "test_files": [],
                        "all_files": [fichier]
                    }
                
                # On recherche les chemins de dossiers se terminant pas train ou test
                if len(racine.split("/")) > 3:
                    if racine.split("/")[3] == "train":
                        mains[main]["gt_files"].append(fichier)
                    if racine.split("/")[3] == "test":
                        mains[main]["test_files"].append(fichier)
    
    # On trie les mains par ordre alpanuémrique
    labelsMains = []
    for main in mains:
        labelsMains.append(main)
    tri = sorted(labelsMains)
    
    # On récupère le nombre de fichiers pour chaque main
    donneesMains = []
    for main in tri:
        # On prend en compte la liste des mains à ignorer
        if main not in ignore:
            dico = {
                "label": main,
                "accuracy": 0
            }
            # Si l'option no_ground_truth n'est pas valide, on traite les vérités de terrain
            if not no_ground_truth:
                dico["gt_nb"] = len(mains[main]["gt_files"])
            donneesMains.append(dico)
    
    # On écrit l'entrée du journal
    date = f"{datetime.now().year}.{datetime.now().month}.{datetime.now().day} {datetime.now().hour}:" \
           f"{datetime.now().minute}"
    
    entree = {
        "date": date
    }
    # Si l'option -n n'est pas active, on propose un nom pour le fichier du modèle entraîné
    if not no_ground_truth:
        # Si le modèle concerné est le principal modèle du projet, son nom est du type "cds_lectcm_04_mains_01.mlmodel"
        if modele[:10] == "cds_lectcm":
            nom = modele.replace(".mlmodel", "")
            nom = nom.split("_")
            noMains = int(nom[2])
            noVersion = int(nom[-1])
            # Si le nombre de mains est différent de celui indiqué dans le nom du modèle
            if noMains != len(donneesMains):
                noMains = len(donneesMains)
                noVersion = 1
            # Si le nombre de mains n'est pas différent de celui indiqué dans le nom du modèle
            else:
                # On implémente le numéro de version de 1
                noVersion = noVersion + 1
            # On réécrit les nombres sous forme de chaînes
            if noMains < 10:
                noMains = "0" + str(noMains)
            else:
                noMains = str(noMains)
            if noVersion < 10:
                noVersion = "0" + str(noVersion)
            else:
                noVersion = str(noVersion)
            entree["output"] = f"cds_lectcm_{noMains}_mains_{noVersion}.mlmodel"
        
        # Si le modèle concerné n'est pas le principal modèle du projet
        else:
            modele = modele.replace(".mlmodel", "")
            entree["output"] = f"{modele}_custom.mlmodel"
    
    # On ajoute en dernier les données des mains
    entree["total_item"] = len(donneesMains)
    entree["items"] = donneesMains
    
    # On récupère le contenu du fichier de journal, s'il existe
    try:
        with open(JOURNALREC) as f:
            journal = json.load(f)
    except FileNotFoundError:
        journal = {}
    
    # On initie le modèle s'il n'existe pas dans le journal
    if not journal.get(modele):
        journal[modele] = []
    
    journal[modele].append(entree)
    
    # On écrit le résultat dans un fichier de sortie au format .py
    with open(JOURNALREC, mode="w") as jsonf:
        json.dump(journal, jsonf, indent=3, ensure_ascii=False, sort_keys=False)


if __name__ == "__main__":
    journalReconn()
