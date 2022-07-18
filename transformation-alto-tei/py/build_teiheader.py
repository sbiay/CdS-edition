from py.default_teiheader import DefaultTree
from lxml import etree
from py.full_teiheader import FullTree

NS = {"s":"http://www.loc.gov/zing/srw/", "m":"info:lc/xmlns/marcxchange-v2"}

def nom(chaine):
    if "(CdS)" in chaine:
        chaine = "Constance de Salm"
    elif "," in chaine:
        chaine = chaine.split(',')
        chaine = chaine[1] + " " + chaine[0]
    
    if chaine[0] == " ":
        chaine = chaine[1:]
        
    return chaine

def teiheader(metadata, document, root, count_pages):
    """Create all elements of the <teiHeader>.
    Args:
        document (str): name of directory containing ALTO-encoded transcriptions of the document's pages
        root (etree): XML-TEI tree
        count_pages (string): number of files in directory
    Returns:
        root (etree): XML-TEI tree
    """    
    # step 1 -- generate default <teiHeader>
    elements = DefaultTree(document, root, count_pages)  # deafult_teiheader.py
    elements.build()
    
    # step 2 -- generate full <teiHeader>
    nsmap = {"tei": "http://www.tei-c.org/ns/1.0/"}
    
    # Title
    title = root.xpath("//teiHeader//title", namespaces=nsmap)[0]
    auteur = nom(metadata['Verfasser'])
    destinataire = nom(metadata['Empfänger'])
    date = metadata['Datierung_JJJJ-MM-TT']
    date = date.split("-")
    mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre',
            'novembre', 'décembre']
    date = f"{date[2]} {mois[int(date[1]) - 1]} {date[0]}"
    lieuExp = metadata["Ausstellungsort"]
    title.text = f"Lettre de {auteur} à {destinataire} ({lieuExp}, le {date})"
    
    # correspDesc
    profileDesc = root.xpath("//teiHeader/profileDesc", namespaces=nsmap)[0]
    correspDesc = etree.SubElement(profileDesc, "correspDesc")
    correspAction = etree.SubElement(correspDesc, "correspAction")
    # Expédition
    correspAction.attrib["type"] = "sent"
    persName = etree.SubElement(correspAction, "persName")
    persName.attrib["ref"] = metadata["VIAF_Verfasser"]
    persName.text = metadata['Verfasser']
    placeName = etree.SubElement(correspAction, "placeName")
    placeName.attrib["ref"] = metadata["Geonames_Ausstellungsort"]
    placeName.text = lieuExp
    date = etree.SubElement(correspAction, "date")
    date.attrib["when-iso"] = metadata['Datierung_JJJJ-MM-TT']
    # Réception
    correspAction = etree.SubElement(correspDesc, "correspAction")
    correspAction.attrib["type"] = "received"
    persName = etree.SubElement(correspAction, "persName")
    persName.attrib["ref"] = metadata["VIAF_Empfänger"]
    persName.text = metadata['Empfänger']
    if metadata["Empfangsort"]:
        placeName = etree.SubElement(correspAction, "placeName")
        placeName.attrib["ref"] = metadata["Geonames_Empfangsort"]
        placeName.text = metadata["Empfangsort"]
    
    return root
