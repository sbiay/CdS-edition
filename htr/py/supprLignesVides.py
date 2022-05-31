import click
from lxml import etree


@click.command()
@click.argument("ALTO")
def supprLignesVides(alto):
    """
    Cette fonction prend comme argument un chemin de fichier au format alto et en supprime les lignes vides
    (//String/@CONTENT="").
    :param alto: chemin de fichier XML-Alto
    :return: None
    """
    
    if alto == "CHEMIN-DE-FICHIER":
        print("Il faut remplacer le CHEMIN-DE-FICHIER par un chemin de fichier XML-Alto.")
        return None
    
    # On ouvre le fichier Alto passé en argument
    with open(alto) as altof:
        xml = etree.parse(altof)
        # On implémente l'espace de nom
        nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
        
        # On sélectionne toutes les lignes vides
        lignesVides = xml.xpath('''//alto:TextLine[descendant::alto:String/@CONTENT=""]''',
                                namespaces=nsmap)
        
        # On boucle sur chaqe ligne vide
        for l in lignesVides:
            # On supprime chacune de l'arbre XML
            l.getparent().remove(l)
        
        # On écrit l'arbre dans un fichier de sortie
        xml.write(alto)
    
    print(f"Le fichier {alto} a été transformé correctement.")

if __name__ == "__main__":
    supprLignesVides()
