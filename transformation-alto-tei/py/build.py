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
from py.outils import triFichiers
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
        
        # On assigne l'identifiant de la pièce courante
        idPiece = self.d
        # On récupère le contenu des métadonnées du dossier
        with open(donnees) as jsonf:
            donneesDossier = json.load(jsonf)
        # On récupère les données de la pièce courante
        donneesPiece = donneesDossier["results"]["records"][idPiece]
        
        # On récupère les chemins des prédictions
        predictionsImport = triFichiers("data/" + idPiece + "/")
        
        # On récupère les lignes du début de la lettre (région contenant le header et le titre
        positionTitre = donneesDossier["results"]["records"][idPiece]["title_position"]

        nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
        # On boucle sur chaque fichier
        for index, fichier in enumerate(predictionsImport):
            # On initie la liste contenant
            regionsPiece = []
            xml = etree.parse(fichier)
            
            # On traite le début de la lettre
            if index == 0:
                # TODO test
                #print(f"Id. de la pièce : {idPiece} -- Nom du fichier de début : {fichier}")
                
                # On récupère les codes des régions et des lignes
                tags = Tags(self.p[0], self.d, self.NS).labels()
                # On boucle sur les couples pour récupérer les codes des tags
                for tag in tags:
                    if tags[tag] == "HeadingLine:title":
                        codeTitre = tag
                    if tags[tag] == "MainZone":
                        codeMain = tag
                    if tags[tag] == "CustomZone:header":
                        codeHeader = tag
        
                # On récupère la zone de titre de la pièce
                zoneTitre = xml.xpath(
                    f"//alto:TextBlock[@TAGREFS='{codeMain}'][child::alto:TextLine[@TAGREFS='"
                    f"{codeTitre}']][position()={positionTitre}]", namespaces=nsmap)
                
                idTitre = zoneTitre[0].xpath(f"@ID", namespaces=nsmap)
                idTitre = str(idTitre[0])
                # On récupère le header éventuel dans le bloc précédent
                header = None
                blocsPrecedents = xml.xpath(
                    f"//alto:TextBlock[@ID='{idTitre}']/preceding-sibling::alto:TextBlock",
                    namespaces=nsmap)
                
                if blocsPrecedents:
                    blocPrecedent = blocsPrecedents[-1]
                    tagBlocPrec = blocPrecedent.xpath(f"@TAGREFS", namespaces=nsmap)[0]
                    # Si le tag répond au code CustomZone:header
                    if tagBlocPrec == codeHeader:
                        header = blocPrecedent
                        regionsPiece.append(header[0])
        
                # On ajoute après l'éventuel header la zone contenant le titre
                regionsPiece.append(zoneTitre[0])
                
                # On récupère les mainZone qui suivent celles du titre (ce sont les blocs de textes frères suivants
                # qui sont de type mainZone et ne contiennent pas de ligne de titre)
                blocsSuivants = xml.xpath(
                    f"//alto:TextBlock[@ID='{idTitre}']/"
                    f"following-sibling::alto:TextBlock[@TAGREFS='{codeMain}']"
                    f"[not(child::alto:TextLine[@TAGREFS='{codeTitre}'])]",
                    namespaces=nsmap)
                
                # On récupère les autres types de régions
                blocsAutres = xml.xpath(
                    f"//alto:TextBlock[@ID='{idTitre}']/"
                    f"following-sibling::alto:TextBlock[not(@TAGREFS='{codeMain}')][not(@TAGREFS='{codeHeader}')]",
                    namespaces=nsmap)
                
                regionsPiece.append(blocsSuivants)
                regionsPiece.append(blocsAutres)
                
            # On traite le milieu de la lettre quand elle s'étend sur plus de deux fichiers
            elif len(predictionsImport) > 2 and index != 0 and index != len(predictionsImport) -1 :
                # TODO à tester
                # On ouvre la prediction
                blocsSuivants = xml.xpath(
                    f"//alto:TextBlock",
                    namespaces=nsmap)
                for bloc in blocsSuivants:
                    regionsPiece.append(bloc)
            
            # On traite la fin de la lettre
            elif index == len(predictionsImport) -1:
                # On récupère les codes des régions et des lignes
                tags = Tags(self.p[0], self.d, self.NS).labels()
                # On boucle sur les couples pour récupérer les codes des tags
                for tag in tags:
                    if tags[tag] == "HeadingLine:title":
                        codeTitre = tag
                    if tags[tag] == "MainZone":
                        codeMain = tag
                    if tags[tag] == "CustomZone:header":
                        codeHeader = tag
                
                # On récupère la première mainZone
                mainZones = xml.xpath(
                    f"//alto:TextBlock[@TAGREFS='{codeMain}']", namespaces=nsmap)
                zonePremiere = mainZones[0]
                regionsPiece.append(zonePremiere)
                
                # On récupère les éventuelles maineZones suivantes, sauf si elles comportent un titre
                idPrem = zonePremiere.xpath(f"@ID", namespaces=nsmap)
                idPrem = str(idPrem[0])
                blocsSuivants = xml.xpath(
                    f"//alto:TextBlock[@ID='{idPrem}']/following-sibling::alto:TextBlock[@TAGREFS='{codeMain}']"
                    f"[not(child::alto:TextLine[@TAGREFS='{codeTitre}'])]",
                    namespaces=nsmap)
                if blocsSuivants:
                    for bloc in blocsSuivants:
                        regionsPiece.append(bloc)
                
                # On récupère les autres types de régions
                blocsAutres = xml.xpath(
                    f"//alto:TextBlock[not(@TAGREFS='{codeMain}')][not(@TAGREFS='{codeHeader}')]",
                    namespaces=nsmap)
                if blocsAutres:
                    for bloc in blocsAutres:
                        regionsPiece.append(bloc)

            # TODO contrôle
            if self.d == "CdS-b1-06pa" and fichier == "data/CdS-b1-06pa/CdS02_Konv002-03_0057.xml":
                for region in regionsPiece:
                    print(region.xpath(f"@ID", namespaces=nsmap))
                #print(f'Id. calculé du main suivant et final :')
                #print("La solution est : eSc_textblock_7cb7eef8")
            
            # TODO RÉÉCRIRE LE fichier AVEC UNIQUEMENT LES BLOCS CONTENUS DANS regionsPiece
            
        # IMPLÉMENTER LES ÉLÉMENTS
        text = Text(self.root)
        body(self.root, text.data)
        segment(self.root, text.main)

        # TODO Visualiser le contenu de text.data
        donnees = text.data
        with open(f"./test/{self.d}-text.data.json", mode="w") as jsonf:
            json.dump(donnees, jsonf)
