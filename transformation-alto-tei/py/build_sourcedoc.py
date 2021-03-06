from py.format_files import Files
from py.sourcedoc_attributes import Attributes
from py.surface_and_desc import SurfaceTree
from lxml import etree

NS = {'a':"http://www.loc.gov/standards/alto/ns-v4#"}  # namespace for the Alto xml


def sourcedoc(document, tei_root, filepath_list, tags):
    """Creates the <sourceDoc> for an XML-TEI file using data parsed from a series of ALTO files.
        The <sourceDoc> collates each ALTO file, which represents one page of a document, into a wholistic
        description of the document.
    """
    ordered_files = Files(document, filepath_list).order_files()  # format_files.py
    
    # create <sourceDoc> and its child <surfaceGrp>
    sourceDoc = etree.SubElement(tei_root, "sourceDoc")
    surfaceGrp = etree.SubElement(sourceDoc, "surfaceGrp")

    for file in ordered_files:
        lines_on_page = 0
        # On retype le chemin de fichier en chaîne pour éviter TypeError: cannot parse from 'PosixPath'
        chemin = str(file.filepath)
        # On récupère le nom du fichier
        fichier = f"./{(chemin.split('/')[1] + '/' + chemin.split('/')[2]).replace('xml', 'jpg')}"
        alto_root = etree.parse(chemin).getroot()
        attributes = Attributes(document, fichier, alto_root, tags)  # sourcedoc_attributes.py
        stree = SurfaceTree(document, fichier, alto_root)  # surface_and_desc.py (surface element and descendants)

        # -- SURFACE --
        # for every page in the document, create a <surface> and assign its attributes
        surface = stree.surface(surfaceGrp, attributes.surface())

        # -- TEXTBLOCK --
        # for every <Page> in this ALTO file, create a <zone> for every <TextBlock> and assign the latter's attributes
        textblock_atts, processed_textblocks = attributes.zone("PrintSpace/", "TextBlock")
        for textblock_count, processed_textblock in enumerate(processed_textblocks):
            text_block = stree.zone1(surface, textblock_atts, textblock_count)

            # -- TEXTLINE --
            # for every <TextBlock> in this ALTO file that has at least one <TextLine>, create a <zone> and assign its attributes
            textline_atts, processed_textlines = attributes.zone(f'TextBlock[@ID="{processed_textblock}"]/', "TextLine")
            if len(processed_textlines) > 0:
                for textline_count, processed_textline in enumerate(processed_textlines):
                    lines_on_page+=1
                    text_line = stree.zone2(lines_on_page, text_block, textblock_count, textline_atts, textline_count, processed_textline)

                    # -- LINE --
                    # for every <TextLine> in this ALTO file that has a <String>, create a <line>
                    if alto_root.find(f'.//a:TextLine[@ID="{processed_textline}"]/a:String', namespaces=NS).get("CONTENT") is not None:
                        stree.line(text_line, textblock_count, textline_count, processed_textline)
    return tei_root
    