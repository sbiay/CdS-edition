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
    # On récupère l'élément titre
    title = root.xpath("//teiHeader//title", namespaces=nsmap)[0]
    
    # TODO
    # <title xml:lang="en">Letter from Ludwig Tieck to Friedrich von Raumer (Ziebingen, 30 March 1815)</title>
    
    auteur = nom(metadata['Verfasser'])
    destinataire = nom(metadata['Empfänger'])
    date = metadata['Datierung_JJJJ-MM-TT']
    date = date.split("-")
    mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre',
            'novembre', 'décembre']
    date = f"{date[2]} {mois[int(date[1]) - 1]} {date[0]}"
    lieuExp = metadata["Ausstellungsort"]
    title.text = f"Lettre de {auteur} à {destinataire} ({lieuExp}, le {date})"
    
    return root
