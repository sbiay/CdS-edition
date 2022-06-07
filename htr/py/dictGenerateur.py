import click
import json
import csv
import os
from lxml import etree
from constantes import FRANTEXT, DICTGENERAL


@click.command()
def dictGenerateur():
    tousMots = []
    fichiersTraites = []
    # On analyse l'arborescence du dossier des fichiers exportés de Frantext
    for root, dirs, files in os.walk(FRANTEXT):
        # On boucle sur chaque fichier
        for fichier in files:
            if fichier[-3:] == "xml":
                fichiersTraites.append(fichier)
                with open(root + fichier) as f:
                    xml = etree.parse(f)
                # On implémente l'espace de nom alto
                nsmap = {'x': "http://www.atilf.fr/allegro"}
                mots = xml.xpath("//x:wf/@word", namespaces=nsmap)
                for mot in mots:
                    tousMots.append(mot)
                # On délivre un message de fin de lecture du fichier
                print(f"Le fichier {fichier} a été lu correctement.")
        
    print("Le comptage des occurrences a commencé, cela peut plusieurs minutes…")
    
    # On renseigne un dictionnaire pour le comptage de tous les mots du corpus
    dictMots = {}
    for mot in tousMots:
        mot = mot.replace(' ', '')
        if not dictMots.get(mot) and mot[0] not in "0123456789":
            comptage = tousMots.count(mot)
            if comptage > 0:
                dictMots[mot] = comptage
    
    with open(DICTGENERAL, mode="w") as f:
        json.dump(dictMots, f, indent=3, ensure_ascii=False, sort_keys=True)
        
    print(f"BRAVO !!! C'est terminé ! Le fichier {DICTGENERAL} a été écrit correctement.")
    
    # On récupère le contenu du fichier CSV inventaire de notre recherche sur Frantext
    contenuCSV = []
    with open("./py/dicos/frantext/recherche-frantext.csv") as csvf:
        lecteur = csv.reader(csvf, delimiter=',', quotechar='"')
    
        for ligne in lecteur:
            contenuCSV.append(ligne)
    
    # On écrit dans un fichier CSV la liste des textes contenus dans le dictionnaire général
    with open("./py/dicos/frantext/contenu-dictgeneral.csv", mode="w") as csvf:
        ecriveur = csv.writer(csvf, delimiter="\t", quotechar="|")
    
        for index, ligne in enumerate(contenuCSV):
            if index == 0:
                ecriveur.writerow(ligne)
            if ligne[0] in fichiersTraites:
                ecriveur.writerow(ligne)
                

if __name__ == "__main__":
    dictGenerateur()
