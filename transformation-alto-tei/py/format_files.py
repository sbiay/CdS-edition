import re
from collections import namedtuple

class Files:
    def __init__(self, document, filepaths):
        self.d = document
        self.fl = filepaths  # list

    def order_files(self):
        File = namedtuple("File", ["num", "filepath"])
        # On récupère le modèle du nom de chemin complet vers un fichier
        exempleChemin = str(self.fl[0])
        exempleNom = exempleChemin.split("/")[-1]
        
        # On adapte l'ordonnancement des fichiers à CDS
        if exempleNom[:3] == "CdS":
            # Modèle de nom CdS02_Konv002-02_0027
            ordered_files = sorted([File(int(re.search(r"(CdS\d+_Konv\d+-?\d*_)(\d+)", f.name).group(2)), f)
                                    for f in self.fl])
        else:
            ordered_files = sorted([File(int(re.search(r"(.*f)(\d+)", f.name).group(2)), f) for f in self.fl])
        
        return ordered_files
