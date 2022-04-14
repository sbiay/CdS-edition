Contrôle des données
====

Nous avons contrôlé le 11 avril 2022 la liste des données figurant dans les fichiers publiés sur [Zenodo](https://zenodo.org/record/5707822) avec un export de tous les enregistrements de la base **FuD**. Les fichiers concernés, contenus dans ce dossier, sont les suivants :
- Fichiers publiés sur **Zenodo** :
    - 20211116_Constance_de_Salm_Korrespondenz_Inventar_Briefe.csv
    - 20211116_Constance_de_Salm_Korrespondenz_Inventar_weitere_Quellen.csv
- Export **FuD** :
    - 20220408_exportFuD_principal.csv
    - 20220408_exportFuD_complement.csv

Nous avons comparé ces listes grâce aux clés suivantes (au moyen du script [controle.py](./controle.py)]) :
- Jeu Zenodo : `FuD-Key`
- Export FuD : `idno`

Nous n'avons pris en compte pour cette comparaison que les enregistrements de l'export FuD ayant sous l'attribut `Bearbeitungsstatus` la valeur **"80 - Freigabe"** (*ie* publiable).

Le nombre d'enregistrements qualifiés de publiables dans FuD et qui sont absents du jeu Zenodo est de **14**.
En voici la liste : ['CdS/96/250-251', 'CdS/96/248-249', 'CdS/96/245-246', 'CdS/96/240', 'CdS/96/238', 'CdS/96/234-236', 'CdS/96/154-155', 'CdS/96/142', 'CdS/96/104', 'CdS/96/081-082', 'CdS/95/056-058', 'CDS//012-014', 'CdS/96/016', 'CdS/96/034'].

Ces enregistrements correspondent aux 14 dernières lignes du fichier **20220408_exportFuD_complement.csv**. Nous avons contrôlé que les enregistrements du même fichier :
- Sont bien publiés sur le site https://constance-de-salm.de
- Ont bien été enrichis par H. Souvay (cf. [correspondance.csv](https://github.com/dhi-digital-humanities/constance-de-salm/blob/main/Fud_Tables/CSV/correspondance.csv)).

Par exemple, dans le tableau **20220408_exportFuD_complement.csv**, l'un des derniers de la liste à être commun au jeu Zenodo (**…_weitere_Quellen.csv**) et à avoir 80 est `CdS-b2-008i`; il a bien été enrichi ([notice](https://constance-de-salm.de/archiv/#/document/11375)).

En revanche, les 14 enregistrements ayant le statut de **"80 - Freigabe"** et non présents dans l'inventaire publié sur Zenodo n'ont pas été enrichis.

12 enregistrements parmi ceux vérifiés par **Florence de Peyronnet** correspondent bien à ceux qualifiés de publiables dans FuD et qui sont absents du jeu Zenodo.

Les 2 enregistrements qualifiés de publiables dans FuD, absents du jeu Zenodoet non vérifiés par Florence de Peyronnet sont : ['CdS/95/056-058', 'CDS//012-014'].

On vérifie que les enregistrements vérifiés par **Florence de Peyronnet** n'ont pas été enrichis en recherchant les `Nr. der Digitalisate` dans la liste [correspSearch.csv](./correspSearch.csv), qui correspond à celle déposée par H. Souvay sous le titre [Ready2CMI.csv](https://github.com/dhi-digital-humanities/constance-de-salm/blob/main/CorrespSearch/Ready2CMI.csv) : en effet **aucun** de ces enregistrements n'a été enrichi.