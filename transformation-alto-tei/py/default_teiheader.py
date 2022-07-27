from lxml import etree
from datetime import datetime
from collections import defaultdict
import yaml

class DefaultTree:
    children = defaultdict(list)
    def __init__(self, document, root, count_pages):
        self.document = document
        self.root = root
        self.count = str(count_pages)

    def build(self):
        with open("py/config.yml") as cf_file:
            config = yaml.safe_load(cf_file.read())

        teiHeader = etree.SubElement(self.root, "teiHeader")
        fileDesc = etree.SubElement(teiHeader, "fileDesc")
        profileDesc = etree.SubElement(teiHeader, "profileDesc")
        
        # titleStmt
        titleStmt = etree.SubElement(fileDesc, "titleStmt")
        title = etree.SubElement(titleStmt, "title")
        principal = etree.SubElement(titleStmt, "principal")
        persName = etree.SubElement(principal, "persName")
        forename = etree.SubElement(persName, "forename")
        forename.text = config["responsibility"]["principal"]["forename"]
        surname = etree.SubElement(persName, "surname")
        surname.text = config["responsibility"]["principal"]["surname"]
        
        # publicationStmt
        publicationStmt = etree.SubElement(fileDesc, "publicationStmt")
        publisher = etree.SubElement(publicationStmt, "publisher")
        publisher.text = config["responsibility"]["publisher"]
        authority = etree.SubElement(publicationStmt, "authority")
        authority.text = config["responsibility"]["authority"]
        availability = etree.SubElement(publicationStmt, "availability", config["responsibility"]["availability"])
        etree.SubElement(availability, "licence", config["responsibility"]["licence"])
        today = datetime.today().strftime('%Y-%m-%d')
        etree.SubElement(publicationStmt, "date", when=today)
        
        # seriesStmt
        seriesStmt = etree.SubElement(fileDesc, "seriesStmt")
        title = etree.SubElement(seriesStmt, "title")
        title.text = config["responsibility"]["title"]
        for index, item in enumerate(config["responsibility"]["resp"]):
            respStmt = etree.SubElement(seriesStmt, "respStmt")
            resp = etree.SubElement(respStmt, "resp")
            resp.text = config["responsibility"]["resp"][index]["role"]
            for indexb, i in enumerate(config["responsibility"]["resp"][index]["persons"]):
                persName = etree.SubElement(respStmt, "persName")
                forename = etree.SubElement(persName, "forename")
                forename.text = config["responsibility"]["resp"][index]["persons"][indexb]["forename"]
                surname = etree.SubElement(persName, "surname")
                surname.text = config["responsibility"]["resp"][index]["persons"][indexb]["surname"]
        
        # sourceDesc
        sourceDesc = etree.SubElement(fileDesc, "sourceDesc")
        langUsage = etree.SubElement(profileDesc, "langUsage")
        self.children["language"] = etree.SubElement(langUsage, "language") # pass to other methods
        self.children["language"].attrib["ident"] = "fr"
