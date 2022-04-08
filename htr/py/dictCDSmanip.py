import click

@click.command()
def dictCDStransform():
    """
    USAGE UNIQUE
    
    Ce script transforme le fichier dictCDS original, dont la structure est simplement une série de couples clé-valeur
    en un dictionnaire plus élaboré, dont les valeurs sont des dictionnaires avec des clé "lem" pour lemme
    et "ctxt" pour contexte.
    """
    
    from py.dictCDScorr import dict
    
    nouveauDict = {}
    
    for cle in dict:
        nouveauDict[cle] = {
            "lem": dict[cle],
            "ctxt": []
        }
    
    nouveauDict = str(nouveauDict).replace("},", "},\n").replace(": {", ":\n\t{").replace("', '", "',\n\t '")
    
    with open("./py/dictCDScorr.py", mode="w") as f:
        f.write(
            f"dictCDS = {nouveauDict}"
        )


@click.command()
@click.argument("SOURCE")
def dictCDSintegration(source):
    """
    Ce script prend comme paramètres une source consistant en un dictionnaire python d'entrée
    le compare au contenu de dictCDS, intègre les entrées nouvelles et retourne des messages d'alertes
    pour les entrées générant un conflit d'intégration.
    :param source: dictionnaire python issu de la correction automatisée d'une page de transcription
    :type source: chemin de fichier
    """

