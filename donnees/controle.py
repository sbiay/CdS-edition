import csv
import click


@click.command()
def differenceZenodoFuD():
    """
    Ce script compare les fichiers de données issus de la plateforme Zenodo et de la base FuD
    et imprime le nombre et la liste des fichiers marqués comme publiables dans la base FuD
    mais qui ne sont pas présents dans les listes publiées sur Zenodo (et donc sur le site web).
    """
    # On charge les données publiées sur Zenodo
    zenodo = {}
    with open("./donnees/20211116_Constance_de_Salm_Korrespondenz_Inventar_Briefe.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
        
        for index, ligne in enumerate(lecteur):
            zenodo[ligne['FuD-Key']] = None
    with open("./donnees/20211116_Constance_de_Salm_Korrespondenz_Inventar_weitere_Quellen.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
        
        for index, ligne in enumerate(lecteur):
            zenodo[ligne['FuD-Key']] = None
    
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
    
    # On vérifie que l'export de la base Fud contienne bien tous les enregistrements publiés sur Zenodo
    zenodoSeulement = []
    for cle in zenodo:
        if cle not in fud:
            zenodoSeulement.append(cle)
    
    # On compare les jeux de données : on veut savoir si une entrée de fud n'est pas dans zenodo
    difference1 = []
    for enregistrement in fud:
        if enregistrement["idno"] not in zenodo:
            # On pose comme condition que la valeur de l'enregistrement dans FuD (ie son statut de publication) commence
            # par 80 (ie publiable)
            if enregistrement["Bearbeitungsstatus"][:2] == "80":
                difference1.append(enregistrement["idno"])
    
    print(f"Le nombre d'enregistrements qualifiés de publiables dans FuD et qui sont absents du jeu Zenod"
          f"o est de {len(difference1)}.")
    print(f"En voici la liste : {difference1}")
    
    # On compare avec la liste des documents que Florence de Peyronnet a vérifiés en décembre 2021
    floPeyr = [
        "CdS/95/056-057",
        "CdS/96/012-014",
        "CdS/96/016",
        "CdS/96/034",
        "CdS/96/081-082",
        "CdS/96/104",
        "CdS/96/142",
        "CdS/96/154-155",
        "CdS/96/234-236",
        "CdS/96/238",
        "CdS/96/240",
        "CdS/96/245-246",
        "CdS/96/248-249",
        "CdS/96/250-251",
    ]
    difference2 = []
    for enregistrement in fud:
        # Si un enregistrement FUD est dans la liste floPeyr
        if enregistrement["Nr. der Digitalisate"] in floPeyr:
            # Et si cet enregistrement est aussi dans la liste difference1
            if enregistrement["idno"] in difference1:
                difference2.append(enregistrement)
    
    print(f"{len(difference2)} enregistrements parmi ceux vérifiés par Florence de Peyronnet correspondent bien "
          f"à ceux qualifiés de publiables dans FuD et qui sont absents du jeu Zenodo.")
    
    # On cherche quels enregistrements qualifiés de publiables dans FuD et absents du jeu Zenodo
    # n'ont pas été vérifiés par FdP
    difference3 = []
    for enregistrement in fud:
        # Si un enregistrement FUD est dans la liste difference1
        if enregistrement["Nr. der Digitalisate"] not in floPeyr and enregistrement["idno"] in difference1:
            # Et si cet enregistrement est aussi dans la liste difference1
            difference3.append(enregistrement)
    print(f"Les {len(difference3)} enregistrements qualifiés de publiables dans FuD, absents du jeu Zenodo"
          f"et non vérifiés par Florence de Peyronnet sont : "
          f"{[enregistrement['Nr. der Digitalisate'] for enregistrement in difference3]}")

differenceZenodoFuD()