from py.default_teiheader import DefaultTree
from lxml import etree

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
    
    # Auteur et destinataire
    auteur = nom(metadata['Verfasser'])
    destinataire = nom(metadata['Empfänger'])

    # Date d'envoi
    date = metadata['Datierung_JJJJ-MM-TT']
    # On teste l'existence de la date
    if not date:
        date = "s.d."
    else:
        # On découpe la date au format YYYY-MM-JJ
        date = date.split("-")
        mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre',
                'novembre', 'décembre']
        # On recompose une chaîne du type "25 avril 1824"
        date = f"le {date[2]} {mois[int(date[1]) - 1]} {date[0]}"
    
    # Lieu d'expédition
    lieuExp = metadata["Ausstellungsort"]
    # On teste l'existence du lieu d'expédition
    if not lieuExp:
        lieuExp = "s.l."
        # On sauvegarde la forme complète dans une variable
        lieuExpCompl = lieuExp
    else:
        lieuExpCompl = lieuExp
        # On simplifie au besoin le nom du lieu
        if "/" in lieuExp:
            lieuExp = lieuExp.split("/")[1]
        if "(" in lieuExp:
            lieuExp = lieuExp.split("(")[0][:-1]
        if "," in lieuExp:
            lieuExp = lieuExp.split(",")[0]
        if lieuExp[0] == " ":
            lieuExp = lieuExp[1:]
    
    # Titre de la lettre
    title = root.xpath("//teiHeader//title", namespaces=nsmap)[0]
    title.text = f"Lettre de {auteur} à {destinataire} ({lieuExp}, {date})"
    
    # Description de l'archive
    sourceDesc = root.xpath("//sourceDesc", namespaces=nsmap)[0]
    msDesc = etree.SubElement(sourceDesc, "msDesc")
    msIdentifier = etree.SubElement(msDesc, "msIdentifier")
    institution = etree.SubElement(msIdentifier, "institution")
    repository = etree.SubElement(msIdentifier, "repository")
    # On récupère le nom de l'institution de conservation
    if metadata["Bestand"] == "Schloss Dyck":
        institution.text = "Archiv Schloss Dyck"
        repository.text = "Fonds Constance de Salm"
    else:
        institution.text = "Société des Amis du Vieux Toulon et de sa Région"
        repository.text = "Fonds Salm"
    # Cote
    idno = etree.SubElement(msIdentifier, "idno")
    idno.text = metadata["Nr"]

    # Notice de l'inventaire
    biblStruct = etree.SubElement(sourceDesc, "biblStruct")
    analytic = etree.SubElement(biblStruct, "analytic")
    title = etree.SubElement(analytic, "title")
    title.text = metadata["Nr"]
    idno = etree.SubElement(analytic, "idno")
    idno.text = metadata["URL"]
    monogr = etree.SubElement(biblStruct, "monogr")
    title = etree.SubElement(monogr, "title")
    title.text = "La correspondance de Constance de Salm (1767-1845). Inventaire du fonds Salm de la Société des Amis du Vieux Toulon et de sa Région et du fonds Constance de Salm, Archiv Schloss Dyck (Mitgliedsarchiv der Vereinigten Adelsarchive im Rheinland e.V.). Édition numérique"
    imprint = etree.SubElement(monogr, "imprint")
    publisher = etree.SubElement(imprint, "publisher")
    pubPlace = etree.SubElement(imprint, "pubPlace")
    date = etree.SubElement(imprint, "date")
    publisher.text = "DHI Paris"
    pubPlace.text = "Paris"
    date.text = "2021"

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
    if metadata["Geonames_Ausstellungsort"]:
        placeName.attrib["ref"] = metadata["Geonames_Ausstellungsort"]
    # Si le lieu d'expédition n'est pas connu
    else:
        placeName.attrib["ref"] = "unknown"
    placeName.text = lieuExpCompl
    date = etree.SubElement(correspAction, "date")
    # Si la date est connue
    if metadata['Datierung_JJJJ-MM-TT']:
        # On écrit l'attribut when-iso
        date.attrib["when-iso"] = metadata['Datierung_JJJJ-MM-TT']
        date.text = metadata['Datierung_JJJJ-MM-TT']
    # Si la date n'est pas connue
    else:
        date.text = "s.d."
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
