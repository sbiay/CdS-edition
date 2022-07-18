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
        titleStmt = etree.SubElement(fileDesc, "titleStmt")
        title = etree.SubElement(titleStmt, "title")
        respStmt = etree.SubElement(titleStmt, "respStmt")
        resp = etree.SubElement(respStmt, "resp")
        resp.text = config["responsibility"]["text"]
        for i in range(len(config["responsibility"]["resp"])):
            persName = etree.SubElement(respStmt, "persName")
            forename = etree.SubElement(persName, "forename")
            forename.text = config["responsibility"]["resp"][i]["forename"]
            surname = etree.SubElement(persName, "surname")
            surname.text = config["responsibility"]["resp"][i]["surname"]
        publicationStmt = etree.SubElement(fileDesc, "publicationStmt")
        publisher = etree.SubElement(publicationStmt, "publisher")
        publisher.text = config["responsibility"]["publisher"]
        authority = etree.SubElement(publicationStmt, "authority")
        authority.text = config["responsibility"]["authority"]
        availability = etree.SubElement(publicationStmt, "availability", config["responsibility"]["availability"])
        etree.SubElement(availability, "licence", config["responsibility"]["licence"])
        today = datetime.today().strftime('%Y-%m-%d')
        etree.SubElement(publicationStmt, "date", when=today)
        sourceDesc = etree.SubElement(fileDesc, "sourceDesc")
        msdesc = etree.SubElement(sourceDesc, "msDesc")
        msIdentifier = etree.SubElement(msdesc, "msIdentifier")
        langUsage = etree.SubElement(profileDesc, "langUsage")
        self.children["language"] = etree.SubElement(langUsage, "language") # pass to other methods
        self.children["language"].attrib["ident"] = ""
