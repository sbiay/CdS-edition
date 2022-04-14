import csv
import click
from toutesDonnees import donneesFud, donneesZenodo


@click.command()
def differenceZenodoFuD():
    """
    Ce script compare les fichiers de données issus de la plateforme Zenodo et de la base FuD
    et imprime le nombre et la liste des fichiers marqués comme publiables dans la base FuD
    mais qui ne sont pas présents dans les listes publiées sur Zenodo (et donc sur le site web).
    """
    # On charge les données publiées sur Zenodo
    zenodo = donneesZenodo()
    
    # On peut vérifier que l'export de la base Fud contienne bien tous les enregistrements publiés sur Zenodo
    zenodoSeulement = []
    fud = donneesFud()
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
                difference1.append(enregistrement)
    
    print(f"Le nombre d'enregistrements qualifiés de publiables dans FuD et qui sont absents du jeu Zenod"
          f"o est de {len(difference1)}.")
    print(f"En voici la liste : {[enregistrement['Nr. der Digitalisate'] for enregistrement in difference1]}")
    
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
    print(f"Le nombre d'enregistrements vérifiés par Florence de Peyronnet est de {len(floPeyr)}.")
    
    difference2 = []
    for enregistrement in fud:
        # Si un enregistrement FUD est dans la liste floPeyr
        if enregistrement["Nr. der Digitalisate"] in floPeyr:
            # Et si cet enregistrement est aussi dans la liste difference1
            idnoDiff1 = [item['idno'] for item in difference1]
            if enregistrement["idno"] in idnoDiff1:
                difference2.append(enregistrement)
    
    print(f"{len(difference2)} enregistrements parmi ceux vérifiés par Florence de Peyronnet sont bien présents dans "
          f"FuD (et figurent parmi ceux absents du jeu Zenodo).")
    
    # On cherche quels enregistrements qualifiés de publiables dans FuD et absents du jeu Zenodo
    # n'ont pas été vérifiés par FdP
    difference3 = []
    for enregistrement in fud:
        # Si un enregistrement FUD est dans la liste difference1
        if enregistrement["Nr. der Digitalisate"] not in floPeyr and enregistrement["idno"] in idnoDiff1:
            # Et si cet enregistrement est aussi dans la liste difference1
            difference3.append(enregistrement)
    print(f"Il y a {len(difference3)} enregistrements, qualifiés de publiables dans FuD, absents du jeu Zenodo "
          f"et non vérifiés par Florence de Peyronnet : "
          f"{[enregistrement['Nr. der Digitalisate'] for enregistrement in difference3]}")

    # On charge les données de la liste correspSearch
    correspSearch = []
    with open("./donnees/correspSearch.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter=',', quotechar='"')
        # On inscrit dans la liste des dictionnaires décrivant les attributs des enregistrements
        for index, ligne in enumerate(lecteur):
            correspSearch.append({
                "Nr. der Digitalisate": ligne['edition'],
            })
    nrDigitCorresp = [item["Nr. der Digitalisate"] for item in correspSearch]
    
    # On cherche les enregistrements vérifiés par FdP qui aurait été enrichis pour correspSeach
    floPeyrEnrichis = []
    for item in floPeyr:
        if item in nrDigitCorresp:
            floPeyrEnrichis.append(item)
    print(f"{len(floPeyrEnrichis)} enregistrements vérifiés par FdP ont été enrichis pour correspSeach.")

differenceZenodoFuD()