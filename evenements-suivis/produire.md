Transformation md => tex
========================

- Pour intégrer à mon rapport :
    - Produire sans lier la biblio :
        ```shell
        pandoc -r markdown-auto_identifiers --standalone DocumentsAnciensReconnaissance2022.md -o sorties/DocumentsAnciensReconnaissance2022.tex
        ```
    
    - Transformer les références par regex :
        ```txt
        {[}@marguin-hamonDiscoursOuverturePresentation2022{]} .
        ```

- Pour publier en dehors
    - Produire en liant la biblio, avec un style auteur-date et une liste bibliographique à la fin
        ```shell
        pandoc DocumentsAnciensReconnaissance2022.md --bibliography=../documentation/biblio.bib --csl=/home/sbiay/travail-archive-intermediaire/outils/zotero/french3.csl -o sorties/DocumentsAnciensReconnaissance2022.odt
        ```
    - Transformations
        - Supprimer les notes et les résumés ("Résumés et notes")
        - Placer le titre "Liste des interventions" avant la bibliographie
        - Reprendre la bibliographie nettoyée
        - Mettre deux réf. dans la même parenthèse ; sortie txt ainsi :
            ```txt
            (Leblanc et Jacsont, 2022) (Paupe, 2022)
            ```
        - Supprimer tous les `, 2022` des réf. entre parenthèses