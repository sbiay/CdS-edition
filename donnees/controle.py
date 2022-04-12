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
    fud = {}
    with open("./donnees/20220408_exportFuD_principal.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
        # On inscrit comme clé l'identifiant de l'enregistrement, et en valeur le statut (ex. 80 - Freigabe)
        for index, ligne in enumerate(lecteur):
            fud[ligne['idno']] = ligne["Bearbeitungsstatus"]
    
    with open("./donnees/20220408_exportFuD_complement.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
        
        for index, ligne in enumerate(lecteur):
            fud[ligne['idno']] = ligne["Bearbeitungsstatus"]

    # On vérifie que l'export de la base Fud contienne bien tous les enregistrements publiés sur Zenodo
    zenodoSeulement = []
    for cle in zenodo:
        if cle not in fud:
            zenodoSeulement.append(cle)
    if zenodoSeulement:
        print(f"Les enregistrements suivants figurent parmi les données publiées sur Zenodo "
              f"mais pas dans l'export FuD : {zenodoSeulement}")
    
    # On compare les jeux de données : on veut savoir si une entrée de fud n'est pas dans zenodo
    difference = []
    for idno in fud:
        if idno not in zenodo:
            # On pose comme condition que la valeur de l'enregistrement dans FuD (ie son statut de publication) commence
            # par 80 (ie publiable)
            if fud[idno][:2] == "80":
                difference.append(idno)
    
       
    print(f"Le nombre d'enregistrements qualifiés de publiables dans FuD et qui sont absents du jeu Zenod"
          f"o est de {len(difference)}.")
    print(f"En voici la liste : {difference}")

differenceZenodoFuD()