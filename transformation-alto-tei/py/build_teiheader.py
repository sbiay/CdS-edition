from py.default_teiheader import DefaultTree
from lxml import etree
from py.full_teiheader import FullTree

NS = {"s":"http://www.loc.gov/zing/srw/", "m":"info:lc/xmlns/marcxchange-v2"}


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
    # On récupère l'élément teiheader
    teiheader = root.xpath("//teiHeader", namespaces=nsmap)[0]
    #p = etree.SubElement(teiheader, "p")
    
    
    return root
