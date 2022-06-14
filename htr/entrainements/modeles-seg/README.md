Modèles de segmentation
===

# Modèles importés

- **blla.mlmodel** : modèle de base de blla de Kraken (cf. GitHub de Kraken)
- **lineandregionscomplexefinetune__49.mlmodel** : premier modèle entrainé par A. Pinche avec des données segmOnto sur des manuscrits et des incunables

# Modèles entraînés

1. Avec une CustomZone:opener
    - **martini-01.mlmodel** : entraîné de 0  avec 21 p. de la correspondance Martini (échec de reconnaissance des lignes)
    - **martini-02.mlmodel** : entraîné à partir de blla.mlmodel  avec 21 p. de la correspondance Martini (échec de reconnaissance des lignes)
    - **martini-03.mlmodel** : personnalisation de lineandregionscomplexefinetune__49.mlmodel avec 21 p. de la correspondance Martini (succès)
    - **copie-deux-01.mlmodel** : personnalisation de lineandregionscomplexefinetune__49.mlmodel avec 36 p. des recueils (2nde copie)
    - **copie-deux-02.mlmodel** : personnalisation de blla.mlmodel avec 54 d.p. des recueils
    - **copie-deux-03.mlmodel** : personnalisation de blla.mlmodel avec 79 d.p. des recueils
2. Sans CustomZone:opener
    - **copie-deux-04.mlmodel** : personnalisation de blla.mlmodel avec 123 d.p. des recueils