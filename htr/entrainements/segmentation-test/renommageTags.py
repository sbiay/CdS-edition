import csv
import os

corrections = []

with open("sources/segmentation-test/renommageTags.csv") as csvf:
    lecteur = csv.reader(csvf, delimiter="\t", quotechar="|")
    for ligne in lecteur:
        correction = (ligne[0], ligne[1])
        corrections.append(correction)

cheminsFichiers = []
for root, dirs, files in os.walk("./sources/"):
    for fichier in files:
        if fichier[-3:] == "xml":
            cheminsFichiers.append(root + '/' + fichier)
            
for fichier in cheminsFichiers:
    with open(fichier) as f:
        contenu = f.read()
        contenu = contenu.split("\n")
    
    with open(fichier, mode="w") as f:
        for ligne in contenu:
            if "Tag" in ligne:
                for modif in corrections:
                    if modif[0] in ligne:
                        ligne = ligne.replace(modif[0], modif[1])
            f.write(ligne + "\n")