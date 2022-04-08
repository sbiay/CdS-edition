from lxml import etree
import os
from constantes import VERITESTERRAIN as VT


def get_lemmes():
    """
    Cette fonction parse le contenu des vérités de terrain et retourne un set des mots qu'elles contiennent.
    :returns: mots contenus dans les vérités de terrain.
    :return type: set
    """
    ponctuation = ",;':!.()"
    chiffres = "1234567890"
    motsParses = []
    # On boucle sur chaque fichier contenu dans le dossier des vérités de terrain
    for root, dirs, files in os.walk(VT):
        for filename in files:
            # On ouvre le fichier
            with open(VT + filename) as f:
                xml = etree.parse(f)
            racine = xml.getroot()
            nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
            textes = xml.xpath("//alto:String/@CONTENT", namespaces=nsmap)
            for ligne in textes:
                # On nettoie le texte de sa ponctuation
                for signe in ponctuation:
                    ligne = ligne.replace(signe, " ").replace("  ", " ")
                # On nettoie le texte de sa ponctuation
                for signe in chiffres:
                    ligne = ligne.replace(signe, " ").replace("  ", " ")
                mots = ligne.split(' ')
                for mot in mots:
                    # On verifie que le mot ne soit pas vide et pas césuré
                    if mot and mot[-1] != '-':
                        motsParses.append(mot)
    
    # On convertit les mots récoltés en set pour éliminer les doublons et on ajoute les nouveaux au set lemmes
    motsParses = set(motsParses)
    return motsParses