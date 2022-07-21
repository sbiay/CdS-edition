from lxml import etree


def body(root, data):
    text = etree.SubElement(root, "text")
    body = etree.SubElement(text, "body")
    div = etree.SubElement(body, "div")
    opener = etree.SubElement(div, "opener")
    header = None
    title = None
    dateline = None
    salute = None
    annotations = None
    closer = None
    postscriptsigned = False
    
    last_element = div[-1]
    lastCloserElt = None
    
    # On assigne un booléen pour délimiter le opener
    zoneOpener = True
    zoneMain = False
    zoneCloser = False

    # On assigne un booléen pour les problèmes de numérotation de ligne
    prblmNum = False
    
    for index, line in enumerate(data):
        # On écrit un pb si le numéro de la ligne est 1
        if int(line.n) == 1:
            pb = etree.Element("pb", corresp=f"#{line.page_id}")
            # Si le dernier élément n'est pas un fw (header, note, marge)
            if last_element.tag != "fw":
                if last_element.tag == "lg":
                    # Si oui, on ajoute le pb au dernier enfant
                    last_element.getchildren()[-1].append(pb)
                else:
                    # Sinon on l'ajoute à la div
                    last_element.append(pb)
            # Si le dernier élément est un fw (header, note, marge)
            else:
                div.append(pb)
            last_element = div[-1]
        
        # prepare attributes for the text block's zone
        zone_atts = {"corresp": f"#{line.zone_id}", "type": line.zone_type}
        # prepare <lb/> with this line's xml:id as @corresp
        lb = etree.Element("lb", corresp=f"#{line.id}")
        # Contenu des lignes de texte
        lb.tail = f"{line.text}"

        # NumberingZone, QuireMarksZone, and RunningTitleZone line
        if line.zone_type == "NumberingZone" or line.zone_type == "RunningTitleZone":
            # enclose any page number, quire marks, or running title inside a <fw>

            # Si le dernier élément n'est pas un fw
            if last_element.tag != "fw":
                fw = etree.Element("fw", zone_atts)
                fw.append(lb)
                last_element.addnext(fw)
                last_element = div[-1]
                comment = etree.Comment("Vérifier que le numéro corresponde à la lettre et mettre à jour le type : "
                                        "pageNum si numéro de page, letterNum si numéro de lettre")
                fw.append(comment)
            # Si le dernier élément est un fw
            else:
                last_element.append(lb)

        # MarginTextZone
        elif line.zone_type == "MarginTextZone":
            # create a <note> if one is not already the preceding sibling
            if last_element.tag != "note":
                note = etree.Element("note", zone_atts)
                note.append(lb)
                comment = etree.Comment("Vérifier que la note corresponde à la lettre et mettre à jour le type")
                note.append(comment)
                div.append(note)
                last_element = div[-1]
            else:
                last_element.append(lb)
        
        # Pour les autres types de zones
        else:
            # Si on rencontre une DefaultLine, c'est que le opener est terminé
            if line.line_type == "DefaultLine":
                zoneOpener = False
                zoneMain = True
            
            # Si on rencontre une signature, c'est que l'on commence le closer
            if line.line_type == "CustomLine:signature" and not last_element.tag == "postscript":
                zoneOpener = False
                zoneMain = False
                zoneCloser = True

            # Cas rare d'une signature dans un post-scriptum
            elif line.line_type == "CustomLine:signature" and last_element.tag == "postscript":
                zoneOpener = False
                zoneMain = False
                zoneCloser = True
                if not postscriptsigned:
                    signed = etree.SubElement(last_element, "signed")
                    comment = etree.Comment("Salut")
                    signed.append(lb)
                    signed.append(comment)
                    
                    postscriptsigned = True
                else:
                    signed.append(lb)

            # Si on rencontre une mention de date en cours de traitement de la zoneMain, on passe au closer
            elif line.line_type == "CustomLine:dateline" and zoneMain:
                # Si le type de la ligne suivante est DefaultLine, on a probablement affaire à problème de numérotation de ligne
                if data[index + 1].line_type == "DefaultLine":
                    # On traite la ligne en tant que MainZone
                    zoneOpener = False
                    zoneMain = True
                    zoneCloser = False
                    prblmNum = True
                # Si le type de la ligne suivante n'est pas DefaultLine, tout est normal
                else:
                    # On traite la ligne en tant que Closer
                    zoneOpener = False
                    zoneMain = False
                    zoneCloser = True
            
            if zoneOpener:
                # Header
                if line.line_type in "CustomLine:header":
                    if header is None:
                        header = etree.SubElement(opener, "fw")
                        header.set("type", "letterhead")
                    header.append(lb)
                # Titre
                if line.line_type in "HeadingLine:title":
                    if title is None:
                        title = etree.SubElement(opener, "title")
                    title.append(lb)
                # Dateline
                if line.line_type in "CustomLine:dateline":
                    if dateline is None:
                        dateline = etree.SubElement(opener, "dateline")
                    dateline.append(lb)
                # Salute
                if line.line_type in "CustomLine:salute":
                    if salute is None:
                        salute = etree.SubElement(opener, "salute")
                    salute.append(lb)
                # Notes
                if line.line_type in "CustomLine:annotations":
                    if annotations is None:
                        annotations = etree.SubElement(opener, "note")
                    annotations.append(lb)
                # TODO poser des resp et construire des éléments handNote
                # On met à jour le dernier enfant de la div
                last_element = div[-1]
            
            # CORPS DE LA LETTRE
            elif zoneMain:
                # Corrections interlinéaires
                if line.line_type == "InterlinearLine":
                    comment = etree.Comment("Correction interlinéaire")
                    choice = etree.Element("choice")
                    choice.append(comment)
                    corr = etree.SubElement(choice, "corr")
                    corr.append(lb)
                    # Pour ajouter une correction à la fin d'un vers
                    if last_element.getchildren()[-1].tag == "l":
                        last_element.getchildren()[-1].append(choice)
                    # Pour ajouter une correction dans un paragraphe
                    else:
                        last_element.append(choice)
                # Vers
                elif line.line_type == "CustomLine:verse":
                    # Si le vers est précédé d'un paragraphe
                    if last_element.tag == "p":
                        # On crée un élément lg
                        lg = etree.SubElement(last_element, "lg")
                        l = etree.SubElement(lg, "l")
                        l.append(lb)
                        lg.append(l)
                        div.append(lg)
                        last_element = div[-1]
                    elif last_element.tag == "lg":
                        l = etree.SubElement(lg, "l")
                        l.append(lb)
                        lg.append(l)
                    elif last_element.tag == "postscript":
                        # Si le vers est précédé d'un paragraphe
                        if last_postscript_elt.tag == "p":
                            # On crée un élément lg
                            lg = etree.SubElement(last_element, "lg")
                            l = etree.SubElement(lg, "l")
                            l.append(lb)
                            lg.append(l)
                            postscript.append(lg)
                            last_postscript_elt = postscript[-1]
                        elif last_postscript_elt.tag == "lg":
                            l = etree.SubElement(lg, "l")
                            l.append(lb)
                            lg.append(l)

                # Pour les autres types de lignes
                else:
                    # On instancie un premier p avec la première ligne DefaultLine ou après une partie versifiée
                    # ou après un saut de page
                    if last_element.tag != "p" and last_element.tag != "closer":
                        p = etree.SubElement(div, "p")
                        p.append(lb)
                        last_element = div[-1]
                    elif last_element.tag == "p":
                        last_element.append(lb)
                        # Dateline
                        if line.line_type in "CustomLine:dateline" and prblmNum:
                            comment = etree.Comment("Mention de date mal placée dans l'ordre des lignes")
                            last_element.append(comment)
                            last_element.append(lb)
                    # Post-scriptum
                    elif last_element.tag == "closer":
                        postscript = etree.SubElement(div, "postscript")
                        p = etree.SubElement(postscript, "p")
                        p.append(lb)
                        last_element = div[-1]
                        last_postscript_elt = postscript[-1]
                        
            # CLOSER
            elif zoneCloser:
                # Si le closer n'a pas été créé
                if closer is None:
                    # On le crée
                    closer = etree.SubElement(div, "closer")
                    last_element = div[-1]
                
                # Signature
                if line.line_type == "CustomLine:signature" and not postscriptsigned:
                    # Si le closer a déjà un enfant
                    if last_element.getchildren():
                        # Si le dernier enfant n'est pas un élément signed
                        if last_element.getchildren()[-1].tag != "signed":
                            signed = etree.Element("signed")
                            signed.append(lb)
                            last_element.append(signed)
                        # Si le dernier enfant est un élément signed
                        else:
                            last_element.getchildren()[-1].append(lb)
                    # Si le closer n'a pas encore d'enfant
                    else:
                        signed = etree.Element("signed")
                        signed.append(lb)
                        last_element.append(signed)
                # Date
                elif line.line_type == "CustomLine:dateline":
                    # Si le closer a déjà un enfant
                    if last_element.getchildren():
                        # Si le dernier enfant n'est pas un élément signed
                        if last_element.getchildren()[-1].tag != "dateline":
                            dateline = etree.Element("dateline")
                            dateline.append(lb)
                            last_element.append(dateline)
                        # Si le dernier enfant est un élément signed
                        else:
                            last_element.getchildren()[-1].append(lb)
                    else:
                        dateline = etree.Element("dateline")
                        dateline.append(lb)
                        last_element.append(dateline)
                