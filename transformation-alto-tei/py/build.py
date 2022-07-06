import json
import os
from py.iiif_data import IIIF_API
from py.sru_data import SRU_API
from py.build_teiheader import teiheader
from py.build_sourcedoc import sourcedoc
from py.build_body import body
from py.segment import segment
from py.text_data import Text
from py.tags_dict import Tags
from py.cdsFonctions import triFichiers, selectionBlocs
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
        # TODO Test avec des données forgées pour CDS
        # On récupère les métadonnées fabriquées dans le fichier Json
        with open("./donnees-test-cds/metadata-cds.json") as jsonf:
            metadata = json.load(jsonf)
            self.metadata = metadata
            self.tags = Tags(self.p[0], self.d, self.NS).labels()  # (tags_dict.py) get dictionary of tags {label:ref} for this document

        with open("./donnees-test-cds/exemple-tags.json", mode="w") as f:
            json.dump(self.tags, f, ensure_ascii=False, indent=3)

        # TODO On exporte les métadonnées pour les visualiser
        with open("./donnees-test-cds/exemple-metadata.json", mode="w") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=3)
            
    # -- PHASE 2 -- XML-TEI construction of <teiHeader> and <sourceDoc>
    def build_tree(self):
        """Parse and map data from ALTO files to an XML-TEI tree's <teiHeader> and <sourceDoc>.
        """        
        # instantiate the XML-TEI root for this document and assign the root basic attributes
        tei_root_att = {"xmlns":"http://www.tei-c.org/ns/1.0", "{http://www.w3.org/XML/1998/namespace}id":f"ark_12148_{self.d}"}
        self.root = etree.Element("TEI", tei_root_att)
        # build <teiHeader>
        teiheader(self.metadata, self.d, self.root, len(self.p))  # (build_teiheader.py)
        # build <sourceDoc>
        sourcedoc(self.d, self.root, self.p, self.tags)  # (build_sourcedoc.py)
    
    # -- PHASE 3 -- extract and annotate text in <body> and <standoff>
    def annotate_text(self, donnees):
        """Parse and map data from the <sourceDoc> to XML-TEI elements in <body>.
        """
        
        # SÉLECTIONNER LES LIGNES PERTINENTES
        lignesPertinentes = selectionBlocs(self=self, donnees=donnees)

        text = Text(self.root)
        sourcedoc = text.data
        
        # On élimine du contenu les lignes dont l'identifiant n'est pas dans lignesPertinentes
        contenu = []
        for ligne in sourcedoc:
            if ligne[7] in lignesPertinentes:
                contenu.append(ligne)

        # TODO Visualiser le contenu de text.data
        with open(f"./test/{self.d}-sourcedoc.json", mode="w") as jsonf:
            json.dump(sourcedoc, jsonf)
        with open(f"./test/{self.d}-pertinent.json", mode="w") as jsonf:
            json.dump(contenu, jsonf)

        # IMPLÉMENTER LES ÉLÉMENTS
        if self.d == "CdS-b1-06p9":
            print("\n" + self.d)
            body(root=self.root, data=contenu)
            print(f"La pièce {self.d} est OK")
            #segment(self.root, text.main)

        
