import csv

def donneesFud():
    """
    Cette fonction ouvre les fichiers CSV contenant les données exportées de la base FuD
    Pour chaque enregistrement, elles retourne un dictionnaire selon le modèle suivant :
     {
      'idno': 'CdS-b2-009a',
      'Nr. der Digitalisate': 'CDS//012-014',
      'Bearbeitungsstatus': '80 - Freigabe',
      'Images': [
        'C_de_Salm_96_012.jpg',
        'C_de_Salm_96_013.jpg',
        'C_de_Salm_96_014.jpg'
        ]
      }
    :returns: liste des métadonnées contenues dans les fichiers exportés du FuD
    :return type: list
    """
    # On charge les données exportées de Fud
    fud = []
    with open("./20220408_exportFuD_principal.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
        # On inscrit dans la liste fud des dictionnaires décrivant les attributs des enregistrements
        for index, ligne in enumerate(lecteur):
            enregistrement = {}
            enregistrement["idno"] = ligne['idno']
            enregistrement["Nr. der Digitalisate"] = ligne["Nr. der Digitalisate"]
            enregistrement["Bearbeitungsstatus"] = ligne["Bearbeitungsstatus"]
            enregistrement["Images"] = [ligne["Digitalisat 1"]]

            # Pour ajouter toutes les images, on pose comme condition qu'il existe une image avec un numéro au-dessus
            compteur = 1
            while ligne.get(f"Digitalisat {compteur + 1}"):
                enregistrement["Images"].append(ligne[f"Digitalisat {compteur + 1}"])
                compteur += 1
            fud.append(enregistrement)
            
    with open("./20220408_exportFuD_complement.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
        # On inscrit dans la liste fud des dictionnaires décrivant les attributs des enregistrements
        for index, ligne in enumerate(lecteur):
            enregistrement = {}
            enregistrement["idno"] = ligne['idno']
            enregistrement["Nr. der Digitalisate"] = ligne["Nr. der Digitalisate"]
            enregistrement["Bearbeitungsstatus"] = ligne["Bearbeitungsstatus"]
            enregistrement["Images"] = [ligne["Digitalisat 1"]]
    
            # Pour ajouter toutes les images, on pose comme condition qu'il existe une image avec un numéro au-dessus
            compteur = 1
            while ligne.get(f"Digitalisat {compteur + 1}"):
                enregistrement["Images"].append(ligne[f"Digitalisat {compteur + 1}"])
                compteur += 1
            fud.append(enregistrement)
                
    return fud

def donneesZenodo():
    zenodo = {}
    with open("./20211116_Constance_de_Salm_Korrespondenz_Inventar_Briefe.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
        
        for index, ligne in enumerate(lecteur):
            zenodo[ligne['FuD-Key']] = {
                "Nr. der Digitalisate": ligne['Nr.'],
                "URL": ligne['URL']
            }
            
    with open("./20211116_Constance_de_Salm_Korrespondenz_Inventar_weitere_Quellen.csv") as csvf:
        lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")

        for index, ligne in enumerate(lecteur):
            zenodo[ligne['FuD-Key']] = {
                "Nr. der Digitalisate": ligne['Nr.'],
                "URL": ligne['URL']
            }
            
    return zenodo