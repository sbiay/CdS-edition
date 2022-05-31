import click
from lxml import etree

@click.command()
@click.argument("ALTO")
@click.argument("PAGE")
def supprPage(alto, page=["gauche", "droite"]):
    """
    Cette fonction prend comme argument un chemin de fichier XML-Alto, parse ce fichier et sélectionne le bloc de texte
    correspondant au type de région CustomeZone:page selon l'argument "page". Elle écrit en sortie un fichier
    XML-Alto contenant uniquement la page passée en argument
    :param alto: chemin de fichier Alto
    :param page: les valeurs sont "gauche" et "droite"
    :return: None
    """
    
    # On ouvre le fichier Alto passé en argument
    with open(alto) as altof:
        xml = etree.parse(altof)
        nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
        # On récupère l'identifiant des régions annotées CustomZone:page
        idPage = xml.xpath("//alto:OtherTag[@LABEL='CustomZone:page']/@ID", namespaces=nsmap)
        # On récupère les régions annotées CustomZone:page
        blocPage = xml.xpath(f"//alto:TextBlock[@TAGREFS='{idPage[0]}']", namespaces=nsmap)
        # On analyse l'argument "page"
        if page == "gauche":
            # La page de gauche correspond à la première région annotée CustomZone:page
            blocPage = blocPage[0]
        else:
            # Sinon, on sélectionne la page de droite
            blocPage = blocPage[1]
        
    
if __name__ == "__main__":
    supprPage()
