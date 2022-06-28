Transformation md => tex
========================

- Pour intégrer à mon rapport :
    - Produire sans lier la biblio :
        ```shell
        pandoc -r markdown-auto_identifiers --standalone DocumentsAnciensReconnaissance2022.md -o DocumentsAnciensReconnaissance2022.tex
        ```
    
    - Transformer les références par regex :
        ```txt
        {[}@marguin-hamonDiscoursOuverturePresentation2022{]} .
        ```

- Pour publier en dehors
    - Produire en liant la biblio
