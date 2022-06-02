import click
import os
import json
from lxml import etree
from constantes import XMLaCORRIGER, VERITESTERRAIN as VT, TESTREC


def recupTranscriptions(dossier):
    """
    Cette fonction analyse le contenu d'un dossier contenant des fichiers XML-Alto, sélectionne les fichiers XML,
    parse les lignes de texte de ces fichiers et retourne un dictionnaire
    dont les clés primaires sont les noms des fichiers et les valeurs sont un couple clé-valeur dont :
    - les clés sont les valeurs de TextLine/@ID
    - les valeurs sont la chaîne TextLine/String/@CONTENT
    :param dossier: dossier contenant des fichiers XML-Alto
    :return: dict
    """
    transcriptions = {}
    
    # On boucle sur les fichiers du dossier
    for root, dirs, files in os.walk(dossier):
        for filename in files:
            # On pose comme condition de ne traiter que des fichiers XML (le dossier contient aussi des images)
            if filename[-3:] == "xml":
                # On initie le dictionnaire des lignes du fichier
                transcrFichier = {}
                # On ouvre le fichier
                with open(dossier + filename) as f:
                    xml = etree.parse(f)
                # On implémente l'espace de nom alto
                nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
                # On récupère tous les id des lignes de texte
                ids = xml.xpath("//alto:TextLine/@ID", namespaces=nsmap)
                # On récupère tous les contenus des lignes de texte
                textes = xml.xpath("//alto:String/@CONTENT", namespaces=nsmap)
                
                # On boucle sur chaque ligne
                for index, id in enumerate(ids):
                    # On inscrit le couple id-texte dans le dictionnaire des transcriptions du fichier courant
                    transcrFichier[id] = textes[index]
                
                # On ajoute le dictionnaire des transcriptions du fichier au dictionnaire de synthèse
                transcriptions[filename] = transcrFichier
    
    return transcriptions


@click.command()
def injectTranscript():
    """
    Cette fonction récupère l'ensemble des transcriptions manuelles sous la forme d'un dictionnaire,
    parse les fichiers XML de la prédiction HTR et remplace leurs lignes d'écriture
    lorsqu'il existe une transcription manuelle pour le même identifiant de ligne.
    :return: None
    """
    
    # RECUPERATION DES TRANSCRIPTIONS MANUELLES
    
    # On récupère les transcriptions manuelles à l'aide de la fonction recupTranscriptions(dossier)
    transcriptions = {}
    transcrVT = recupTranscriptions(VT)
    transcrTest = recupTranscriptions(TESTREC)
    
    # On réunit les transcriptions dans un seul dict
    for cle in transcrVT:
        transcriptions[cle] = transcrVT[cle]
    for cle in transcrTest:
        # On vérifie que les id de lignes soient bien uniques
        if transcriptions.get(cle):
            print(f"Attention ! l'id. {cle} est utilisé deux fois !")
            return None
        # Si l'id est unique, on inscrit le couple clé-valeur dans le dict "transcriptions"
        else:
            transcriptions[cle] = transcrTest[cle]
    
    # TODO export test
    with open("./transcriptions.json", mode="w") as f:
        json.dump(transcriptions, f)
    
    # REMPLACEMENT DES PREDICTIONS PAR LES TRANSCRIPTIONS MANUELLES
    
    # On analyse le contenu du dossier contenant les prédictions
    for root, dirs, files in os.walk(XMLaCORRIGER):
        for filename in files:
            # On pose comme condition de ne traiter que du XML et que le fichier aient une transcription manuelle
            if filename[-3:] == "xml" and transcriptions.get(filename):
                transcrFichier = {}
                # On ouvre le fichier
                with open(XMLaCORRIGER + filename) as f:
                    xml = etree.parse(f)
                # On implémente l'espace de nom alto
                nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
                
                # On récupère tous les id des lignes de texte
                ids = xml.xpath("//alto:TextLine/@ID", namespaces=nsmap)
                # On récupère tous les contenus des lignes de texte
                textes = xml.xpath("//alto:String/@CONTENT", namespaces=nsmap)
                
                # On boucle sur chaque ligne
                for index, id in enumerate(ids):
                    # On inscrit le couple id-texte dans le dictionnaire des transcriptions du fichier courant
                    transcrFichier[id] = textes[index]
                
                # On boucle sur chaque ligne du fichier
                for id in transcrFichier:
                    if id == "eSc_line_7d5a2fa7":
                        print("trouvé")
                    # On vérifie que l'identifiant existe aussi dans le dictionnaire des transcriptions manuelles
                    if transcriptions[filename].get(id):
                        # On récupère l'élément String pour chaque ligne de la prédiction
                        prediction = xml.xpath(f"//alto:TextLine[@ID='{id}']/alto:String", namespaces=nsmap)
                        prediction = prediction[0]
                        # On remplace la valeur de l'attribut @CONTENT par la transcription manuelle
                        prediction.attrib['CONTENT'] = transcriptions[filename][id]
                
                # On écrit l'arbre dans un fichier de sortie du même nom que le fichier d'entrée
                xml.write(XMLaCORRIGER + filename)


if __name__ == "__main__":
    injectTranscript()
