import json
from constantes import DONNEES

import click
from toutesDonnees import donneesFud


@click.command()
def differenceZenodoFuD():
    """
    Ce script compare les fichiers de données issus de la plateforme Zenodo et de la base FuD
    et imprime le nombre et la liste des notices
    """
    # On charge les données exportées de FuD
    fud = donneesFud()
    # On récupère les enregistrements n'ayant pas le statut de publiable
    nonPubliables = []
    for enregistrement in fud:
        # Les enregistrement non publiables ont un statut inférieur à 80
        if enregistrement["Bearbeitungsstatus"][:2] < "80":
            nonPubliables.append(enregistrement)
    
    # On imprime les enregistrements non publiables dans un fichier
    with open(DONNEES + "notices-non-publiables.json", mode="w") as jsonf:
        json.dump(nonPubliables, jsonf)
        print(f"Le fichier {DONNEES}notices-non-publiables.json a été écrit avec succès.")

differenceZenodoFuD()