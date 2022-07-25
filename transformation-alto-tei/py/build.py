import csv
from py.build_teiheader import teiheader
from py.build_sourcedoc import sourcedoc
from py.build_body import body
from py.text_data import Text
from py.tags_dict import Tags
from py.cdsFonctions import triFichiers, selectionBlocs
from py.constantes import DONNEES
from lxml import etree


class XMLTEI:
    metadata = {"sru":None, "iiif":None}
    tags = {}
    root = None
    NS = {'a':"http://www.loc.gov/standards/alto/ns-v4#"}  # namespace for the ALTO xml
    def __init__(self, document, filepaths):
        self.d = document  # (str) this document's name / name of directory contiaining the ALTO files
        self.p = filepaths  # (list) paths of ALTO files
        self.metadata  # (dict) dict with two keys ("iiif", "sru"), each of which is equal to its own dictionary of metadata
        self.tags  # (dict) a label-ref pair for each tag used in this document's ALTO files
        self.root  # (etree_Element) root for this document's XML-TEI tree
    
   # -- PHASE 1 -- metadata preparation
    def prepare_data(self):
        """Parse data from APIs and ALTO files to prepare dictionaries of document data.
            The value of self.metadata's key "iiif" is updated from None to the dictionary that the SRU_API.clean() method returns.
            The value of self.metadata's key "sru" is updated from None to the dictionary that the SRU_API.clean() method returns.
            The dictionary self.tags is reassigned to a dictionary that the Tags.labels() method returns.
        """
        # Récupération des métadonnées
        metadata = {}
        # On charge les données Zenodo : partie 1
        with open(DONNEES + "20211116_Constance_de_Salm_Korrespondenz_Inventar_Briefe.csv") as csvf:
            lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
            # On boucle sur chaque ligne
            for index, ligne in enumerate(lecteur):
                # Si l'identifiant du dossier courant correspond à la clé FUD
                if ligne["FuD-Key"] == self.d:
                    # On implémente le dict des métadonnées
                    metadata = ligne
        # On charge les données Zenodo : partie 2
        with open(DONNEES + "20211116_Constance_de_Salm_Korrespondenz_Inventar_weitere_Quellen.csv") as csvf:
            lecteur = csv.DictReader(csvf, delimiter='\t', quotechar="|")
            for ligne in lecteur:
                if ligne["FuD-Key"] == self.d:
                    metadata = ligne
        # On modifie la typographie des clés des métadonnées
        nouvmetada = {}
        for cle in metadata:
            nouvcle = ""
            nouvcle = cle.replace(" ", "_").replace(".", "").replace("(", "_").replace(")", "").replace("__", "_")
            if nouvcle[0] == "_":
                print
                nouvcle = nouvcle[1:]
            nouvmetada[nouvcle] = metadata[cle]
        # On réassigne les nouvelles métadonnées à l'ancienne variable
        self.metadata = nouvmetada
        self.tags = Tags(self.p[0], self.d, self.NS).labels()  # (tags_dict.py) get dictionary of tags {label:ref} for this document

    # -- PHASE 2 -- XML-TEI construction of <teiHeader> and <sourceDoc>
    def build_tree(self):
        """Parse and map data from ALTO files to an XML-TEI tree's <teiHeader> and <sourceDoc>.
        """        
        # instantiate the XML-TEI root for this document and assign the root basic attributes
        tei_root_att = {
            "xmlns":"http://www.tei-c.org/ns/1.0",
            "{http://www.w3.org/XML/1998/namespace}id":self.d
        }
        self.root = etree.Element("TEI", tei_root_att)
        # build <teiHeader>
        teiheader(self.metadata, self.d, self.root, len(self.p))  # (build_teiheader.py)
        # build <sourceDoc>
        sourcedoc(self.d, self.root, self.p, self.tags)  # (build_sourcedoc.py)
    
    # -- PHASE 3 -- extract and annotate text in <body> and <standoff>
    def annotate_text(self, securite, donnees):
        """Parse and map data from the <sourceDoc> to XML-TEI elements in <body>.
        """

        # SÉLECTIONNER LES LIGNES PERTINENTES
        lignesPertinentes = selectionBlocs(self=self, donnees=donnees)
                
        text = Text(self.root)
        sourcedoc = text.data
        
        # Si aucune ligne n'a été trouvée
        if lignesPertinentes is None:
            # La fonction est interrompue
            securite = True
            return donnees, securite

        # On élimine du contenu les lignes dont l'identifiant n'est pas dans lignesPertinentes
        contenu = []
        # Si l'on n' pas trouvé de ligne de titre
        if not lignesPertinentes:
            contenu = text.data
        else:
            for ligne in sourcedoc:
                if ligne[7] in lignesPertinentes:
                    contenu.append(ligne)


        # IMPLÉMENTER LES ÉLÉMENTS
        body(root=self.root, data=contenu)
        
