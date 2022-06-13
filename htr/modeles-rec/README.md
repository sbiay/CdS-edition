Modèles de reconnaissance d'écriture
====================================

Les modèles extérieurs au projet que l'on a utilisés sont téléchargeables sur le [Gitlab du laboratoire Inria](https://gitlab.inria.fr/dh-projects/kraken-models/-/tree/master/transcription%20models) :
- **generic_lectaurep_26.mlmodel** : modèle mixte, entraîné *from scratch* à partir d'une variété d'écritures administratives du XIXe siècle (LECTAUREP)
- **cm_ft_mrs15_11.mlmodel** : entraîné en affinant (44 pages) sur les contrats de mariage le modèle **mixte_mrs_15**, lui -même entraîné *from scratch* à partir d'une varété d'écritures administratives du XIXe siècle (LECTAUREP)

Les modèles propres au projet sont :
- **souvay.mlmodel** : entraîné *from scratch* à partir d'un petit nombre de vérités de terrain [source](https://github.com/dhi-digital-humanities/constance-de-salm/blob/main/HTR/Training%20Models/CdS02_Konv002-02-03/Models/model_best.mlmodel)
- **cds_lectcm_04_mains_01.mlmodel** : entraîné en affinant (40ne de pages) à partir du modèle **cm_ft_mrs15_11.mlmodel**
