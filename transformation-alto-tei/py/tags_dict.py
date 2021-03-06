from collections import defaultdict
from lxml import etree

class Tags:
    """Creates a dictionary of a tag's ID (key) and its LABEL (value).
        The IDs are unique to each document and must be recalculated for each directory.
    """    
    def __init__(self, filepath, document, ns):
        self.filepath = filepath
        self.document = document
        self.ns = ns
        
    def labels(self):
        # On retype le chemin de fichier en chaîne pour éviter TypeError: cannot parse from 'PosixPath'
        chemin = str(self.filepath)
        xml = etree.parse(chemin)
        root = xml.getroot()
        elements = [t.attrib for t in root.findall('.//a:OtherTag', namespaces=self.ns)]
        collect = defaultdict(dict)
        for d in elements:
            collect[d["ID"]] = d["LABEL"]
        self.tags = dict(collect)

        return self.tags
