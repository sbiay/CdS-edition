import json
import os
from lxml import etree
from py.tags_dict import Tags


def triFichiers(dossier):
    """
    Cette fonction prend comme argument le chemin relatif d'un dossier
    et retourne la liste des chemins relatifs des fichiers qu'il contient, triés alpha-numériquement
    :param dossier: chemin relatif d'un dossier
    :type dossier: str
    :return: liste des chemins relatifs des fichiers triés
    :type return: list
    """
    
    # On trie alpha-numériquement les fichiers, en commençant par initier la liste triée
    tri = []
    # On analyse l'arborescence du dossier des prédictions
    for root, dirs, files in os.walk(dossier):
        # On boucle sur chaque fichier
        for filename in files:
            # On ajoute la liste le chemin relatif de chaque fichier
            tri.append(root + filename)
    # On trie la liste
    tri = sorted(tri)
    
    return tri


def selectionBlocs(self, donnees):
    """
    :param self: pièce à éditer
    :param donnees: chemin de fichier
    :return: liste des identifiants de lignes dans les fichiers Alto de la pièce à éditer
    :return type: list
    """

    idPiece = self.d
    # TODO test
    test = None
    # On récupère le contenu des métadonnées du dossier
    with open(donnees) as jsonf:
        donneesDossier = json.load(jsonf)
    # Si la pièce concernée existe dans le fichier de données
    if donneesDossier["results"]["records"].get(idPiece):
        # On récupère les données de la pièce courante
        donneesPiece = donneesDossier["results"]["records"][idPiece]
    else:
        return None

    # On récupère les chemins des prédictions
    tousFichiers = triFichiers("data/" + idPiece + "/")
    predictionsImport = []
    # On ne retient que les fichiers XML
    for fichier in tousFichiers:
        if fichier[-3:] == "xml":
            predictionsImport.append(fichier)

    # On récupère les lignes du début de la lettre (région contenant le header et le titre
    positionTitre = donneesDossier["results"]["records"][idPiece]["title_position"]

    nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}

    regionsPiece = []
    # On initie un header, zone qui n'est pas présente dans toutes les pièces
    codeHeader = None
    
    # On boucle sur chaque fichier
    for index, fichier in enumerate(predictionsImport):
        # On initie la liste contenant
        xml = etree.parse(fichier)
        # On traite le début de la lettre
        if index == 0:
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
            
            # Si l'on ne trouve pas de titre
            if not zoneTitre:
                return []
            
            idTitre = zoneTitre[0].xpath(f"@ID", namespaces=nsmap)
            idTitre = str(idTitre[0])
            # On récupère le header éventuel dans le bloc précédent
            blocsPrecedents = xml.xpath(
                f"//alto:TextBlock[@ID='{idTitre}']/preceding-sibling::alto:TextBlock",
                namespaces=nsmap)
        
            if blocsPrecedents:
                blocPrecedent = blocsPrecedents[-1]
                tagBlocPrec = blocPrecedent.xpath(f"@TAGREFS", namespaces=nsmap)[0]
                # Si le tag répond au code CustomZone:header
                if tagBlocPrec == codeHeader:
                    regionsPiece.append(blocPrecedent)
        
            # On ajoute après l'éventuel header la zone contenant le titre
            regionsPiece.append(zoneTitre[0])
        
            # On récupère les mainZone qui suivent celles du titre (ce sont les blocs de textes frères suivants
            # qui sont de type mainZone et ne contiennent pas de ligne de titre)
            blocsSuivants = xml.xpath(
                f"//alto:TextBlock[@ID='{idTitre}']/"
                f"following-sibling::alto:TextBlock[@TAGREFS='{codeMain}']",
                namespaces=nsmap)
        
            # On récupère les autres types de régions
            blocsAutres = xml.xpath(
                f"//alto:TextBlock[@ID='{idTitre}']/"
                f"following-sibling::alto:TextBlock[not(@TAGREFS='{codeMain}')][not(@TAGREFS='{codeHeader}')]",
                namespaces=nsmap)
            
            # S'il existe des régions d'écriture après la première
            if blocsSuivants:
                # On boucle sur chaque région
                for bloc in blocsSuivants:
                    # On récupère les éventuelles lignes de titre de la région
                    titre = bloc.xpath(f"child::alto:TextLine[@TAGREFS='{codeTitre}']", namespaces=nsmap)
                    # S'il n'y a pas de titre
                    if not titre:
                        # La région est pertinente
                        regionsPiece.append(bloc)
                    # S'il y a un titre
                    else:
                        # On arrête la boucle
                        break
            if blocsAutres:
                for bloc in blocsAutres:
                    regionsPiece.append(bloc)
    
        # On traite le milieu de la lettre quand elle s'étend sur plus de deux fichiers
        elif len(predictionsImport) > 2 and index != 0 and index != len(predictionsImport) - 1:
            # On ouvre la prediction
            blocsSuivants = xml.xpath(
                f"//alto:TextBlock",
                namespaces=nsmap)
            if blocsSuivants:
                for bloc in blocsSuivants:
                    regionsPiece.append(bloc)
    
        # On traite la fin de la lettre
        elif index == len(predictionsImport) - 1:
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
                f"//alto:TextBlock[@ID='{idPrem}']/"
                f"following-sibling::alto:TextBlock[@TAGREFS='{codeMain}']",
                namespaces=nsmap)
            # S'il existe des régions d'écriture après la première
            if blocsSuivants:
                # On boucle sur chaque région
                for bloc in blocsSuivants:
                    # On récupère les éventuelles lignes de titre de la région
                    titre = bloc.xpath(f"child::alto:TextLine[@TAGREFS='{codeTitre}']", namespaces=nsmap)
                    # S'il n'y a pas de titre
                    if not titre:
                        # La région est pertinente
                        regionsPiece.append(bloc)
                    # S'il y a un titre
                    else:
                        # On arrête la boucle
                        break
        
            # On récupère les autres types de régions
            blocsAutres = xml.xpath(
                f"//alto:TextBlock[not(@TAGREFS='{codeMain}')][not(@TAGREFS='{codeHeader}')]",
                namespaces=nsmap)
            if blocsAutres:
                for bloc in blocsAutres:
                    regionsPiece.append(bloc)
    
    # On récupère les identifiants de chaque ligne
    idlignesPiece = []
    for region in regionsPiece:
        idLignes = region.xpath(
                f"child::alto:TextLine/@ID",
                namespaces=nsmap)
        for index, id in enumerate(idLignes):
            idlignesPiece.append(id)
            
    
    return idlignesPiece