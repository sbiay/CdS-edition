import csv

def donneesFud():
    """
    Cette fonction ouvre les fichiers CSV contenant les données exportées de la base FuD
    :return:
    """
    # On charge les données exportées de Fud
    fud = []
    with open("./donnees/20220408_exportFuD_principal.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
        # On inscrit dans la liste fud des dictionnaires décrivant les attributs des enregistrements
        for index, ligne in enumerate(lecteur):
            fud.append({
                "idno": ligne['idno'],
                "Nr. der Digitalisate": ligne["Nr. der Digitalisate"],
                "Bearbeitungsstatus": ligne["Bearbeitungsstatus"]
            })
    
    with open("./donnees/20220408_exportFuD_complement.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
        # On inscrit dans la liste fud des dictionnaires décrivant les attributs des enregistrements
        for index, ligne in enumerate(lecteur):
            fud.append({
                "idno": ligne['idno'],
                "Nr. der Digitalisate": ligne["Nr. der Digitalisate"],
                "Bearbeitungsstatus": ligne["Bearbeitungsstatus"]
            })
    return fud