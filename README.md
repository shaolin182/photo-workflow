# Photography Workflow
This project describes my own photography workflow and presents the status of my work in progress about all photography collections I have.
It also shares all scripts I used in order to achieve it.

## Prerequisites

Required tools are : 
- Darktable for classifying and modifying RAW images
- Hugin for making panoramas
- Gwenview for viewing photography
- Digikam for classifying JPG images
- XnView for modifying exif tag

## Step 0 - Preparing images

One of the use case is to import some images into a collection from differents sources.
As pictures will be renamed with their date time, you must ensure that all cameras used for taking photos have been configured in the same timezone
Otherwise, you will need to update photo tags for modifying data time.

## Step 1 - Importing images

Importing images consist of copying some pictures from source folder (ex:sd card) into target folder and applying some basic process on it. Pictures can be RAW images or JPG images

Imported images are saved in this directory structure : 
- \<YEAR\>/\<YEAR\>-\<MONTH\>/\<YEAR\>-\<MONTH\>_\<COLLECTION_NAME\>

RAW and JPG images use the same directory structure but have different base path :
- RAW images are imported in "RAW" directory
- JPG images are imported in "Photos" directory

When images are imported : 
- they are renamed, filename matches this pattern : **YYYY-MM-DD\_HH:MI:SS\_\<SUFFIX\>**
- some EXIF tags are applied for organizing images

EXIF tags are : 
- Vacances\|\<YEAR\>\|\<COUNTRY\>\|\<CITY\> (ex : Vacances|2018|France|Dordogne)
- Sorties\|\<YEAR\>\|Amis/Familles\|\<EVENT\> (ex : Sorties|2018|Famille|Noel_Girard)
- Projet\|\<YEAR\>\|\<TOPIC\>
- Personnes\|\<FIRSTNAME\>\|\<YEAR\> (ex: Personnes|Mathis|2017)

Finally, those images are imported in : 
- Darktable for raw pictures
- Digikam for other images

Those actions can be performed by running this script
```shell
workflow-photo import <source> <dest> <suffix> <collection>
```

If images are already on imported, you can skipped those parts and only applies some parts of the scripts.
More details on help

## Step 2 - Panorama

After importing photos, we start by identifying paranoma images in darktable.
All images found must be tagged  with a green color tag and added to a group.

Then, export those images in JPG format and use Hugin sotware to create panorama.

If needed, edit pictures on darktable and recreate panorama with Hugin

## Step 3 - Sort images

Sorting images consist of manually identifying which images i want to save and images i want to delete (blur images, duplicate, ...)

### RAW images
I use darktable software for sorting raw images by using color labels : 
- red color : to delete
- yellow color : must take a deeper look to know if i deleted it or not

After sorting images, i delete images tagged with a red label, then i synchronize collections between RAW images and JPG images in order to also delete JPG images
TODO : Sync scripts

### JPG images

Same process as darktable in digikam

## Step 4 - Classify images

Classing images consist of attributing a 5 star rank to best images

## Step 5 - Edit images

Use darktable for modifying photographies with higher rangking

## Step 6 - Export images from RAW to JPG

Through darktable export images from RAW format to JPG

# Backup images

BAckup image to :
- NAS
- External hard drive
- Google drive

TODO : script

# Work in progress

| Collection | Import  | Panorama | Sort RAW | Sort JPG | Class | Improve |
|------------|:-------:|:--------:|:--------:|:--------:|:-----:|:-------:|
|2004-09 Week end intégration à  quiberon|X|-|-|X|-|-|
|2005-06_Slovenie|X|-|-|||||
|2005-09 WEI|X|-|-|||||
|2005-10 anniv Gwenn|X|-|-|||||
|2006-01 Nouvel an|X|-|-|||||
|2006-01 Treveneuc|X|-|-|||||
|2006-04_Soiree des anciens_Tremelin|X|-|-|||||
|2006-05 JNM|X|-|-|||||
|2006-07_Anniv|X|-|-|||||
|2006-07_Coloc|X|-|-|||||
|2006-08_St_Malo|X|-|-|||||
|2006-09 Anniv Celine|X|-|-|||||
|2006-09_Soiree_Rennes|X|-|-|||||
|2006-09 WEI|X|-|-|||||
|2006-10 Anniversaire Gwenn|X|-|-|||||
|2006-10 Anniv Florent|X|-|-|||||
|2006-11_Fac|X|-|-|||||
|2006-12 Noël MIAGE|X|-|-|||||
|2007-01_Nouvel_An|X|-|-|||||
|2007-04 Anniv Laya|X|-|-|||||
|2007-04 Journée des Anciens|X|-|-|||||
|2007-07 Anniversaire Julien|X|-|-|||||
|2007-07_Anniv_Sophie|X|-|-|||||
|2007-07 Sandball Erdeven|X|-|-|||||
|2007-07_Toulouse|X|-|-|||||
|2007-08 Week end Lannion chez Aurélien|X|-|-|||||
|2007-09 Patinoire Claire|X|-|-|||||
|2007-10 Anniversaire Gwenn à Nantes|X|-|-|||||
|2007-10 Samhain sur Rennes|X|-|-|||||
|2008-03_Ski_Flaines|X|-|-|||||
|2008-04 Anniv Laya|X|-|-|||||
|2008-04 Barbecue Sopra|X|-|-|||||
|2008-04 JDA|X|-|-|||||
|2008-07 Anniv sophie|X|-|-|||||
|2008-07 Sandball Erdeven|X|-|-|||||
|2008-09 Super Auguste Pavie Party Number One|X|-|-|||||
|2008-10 anniv Gwenn|X|-|-|||||
|2008-12_Soirée_Raclette|X|-|-|||||
|2009-03 Metallica - Bercy|X|-|-|||||
|2009-03 Ski Orcieres|X|-|-|||||
|2009-03_Soirée_Laura|X|-|-|||||
|2009-04 JDA|X|-|-|||||
|2009-04 Picnic Gayeulles|X|-|-|||||
|2009-04 Pointe du Grouin|X|-|-|||||
|2009-04-Tartiflette Laura|X|-|-|||||
|2009-05 Mariscada|X|-|-|||||
|2009-05 Soirée Spaguetti Bolognese|X|-|-|||||
|2009-06 Baule|X|-|-|||||
|2009-06 Concert CE|X|-|-|||||
|2009-06_St_Jean|X|-|-|||||
|2009-08 Week end Normandie|X|-|-|||||
|2009-09_Barcelone_Rome_Naples|X|-|-|||||
|2009-09_Parachute|X|-|-|||||
|2009-11 Anniv Laura|X|-|-|||||
|2010-02_Ski_Les_Arcs|X|-|-|||||
|2010-03 Madrid|X|-|-|||||
|2010-03 MSB|X|-|-|||||
|2010-04 Chateau de la Loire|X|-|-|||||
|2010-04 JDA|X|-|-|||||
|2010-05_Cuba|X|-|-|||||
|2010-05 Enterrement de vie de garçon Etienne|X|-|-|||||
|2010-06 Mariage Etienne|X|-|-|||||
|2010-07 St Jean d'Assé|X|-|-|||||
|2010-09_Canada_New-York|X|-|-|||||
|2010-10 Montpellier|X|-|-|||||
|2011-01 Crémaillère Kro (Soirée Moustache|X|-|-|||||
|2011-01 Nouvel an|X|-|-|||||
|2011-03 Kayak Saint Lunaire|X|-|-|||||
|2011-03_Soirée_Rennes|X|-|-|||||
|2011-04 Weekend Bruxelles|X|-|-|||||
|2011-06_Thaïlande_Chine_Mongolie|X|-|-|||||
|2011-07 St Jean d'Assé|X|-|-|||||
|2011-08 Week-end Groupe de projet - musée|X|-|-|||||
|2011-09_Anniv_Sandra|X|-|-|||||
|2011-10_La_Réunion|X|-|-|||||
|2012-01 japanantes|X|-|-|||||
|2012-02 Ski Risoul|X|-|-|||||
|2012-04_Les_Rousseaux_A_Rennes|X|-|-|||||
|2012-04_Londres|X|-|-|||||
|2012-07_Soiree_Fruit_de_mer|X|-|-|||||
|2012-07_St_Jean|X|-|-|||||
|2012-07_Zoo_La_Fleche|X|-|-|||||
|2012-08_Majorque|X|-|-|||||
|2012-08 Saint-Malo|X|-|-|||||
|2012-09_Harlem_Globe_Trotters|X|-|-|||||
|2012-10_Ouest_des_Etats_Unis|X|-|-|||||
|2012-11_La_Bodega_Nantes|X|-|-|||||
|2013-03_Marathon_Photo|X|-|-|||||
|2013-04_Maroc|X|-|-|||||
|2013-05_Anniv_Orange|X|-|-|||||
|2013-05_Ecluse_St_Grégoire|X|-||||||
|2013-06_Fleurs|X|-||||||
|2013-06_HellFest|X|-|-|||||
|2013-06_Kayak_Nantes|X|-|-|||||
|2013-06_Roland_Garros|X|-||||||
|2013-07-09 30 ans Rennes|X|-|-|||||
|2013-07_St_Jean|X|-||||||
|2013-08_Anniv_Sophie_30ans|X|-||||||
|2013-08_Croatie|X|-||||||
|2013-10_Anniv_Sophie_Légende|X|-||||||
|2013-11_Anniv_Gwenn_Orange|X|-||||||
|2013-11_Art_to_play|X|-||||||
|2013-11_Sortie_Cesson|X|-||||||
|2014-01_Nouvel_An|X|-||||||
|2014-03_Anniv_Philou_Sésé_30ans|X|-||||||
|2014-03_Martinique|X|-||||||
|2014-04_Carnaval_Nantes|X|-||||||
|2014-05_30ans_Shawi|X|-|-|||||
|2014-06_HellFest|X|-|-|||||
|2014-06_Saut_Elastique|X|-||||||
|2014-07 Soiree tague la tapisserie|X|-||||||
|2014-08_Genève|X|-||||||
|2014-08_St_Jean|X|-||||||
|2014-09_Corse|X|-||||||
|2014-10_30_ans_Gwenn|X|-||||||
|2014-10_Slovénie|X|-||||||
|2014-11_30_ans|X|-||||||
|2014-12_Cremaillère_sophie|X|-||||||
|2014-12_Noël|X|-||||||
|2015-04_Berlin|X|X|X||||||
|2015-05_ACDC|X|-|-|||||
|2015-05_Danemark|X|-||||||
|2015-06_EVG_Alex|X|-||||||
|2015-06_Saut_Elastique|X|-||||||
|2015-07_St_Jean|X|-||||||
|2015-08_Quiberon|X|-||||||
|2015-08_Weekend_basket_France_Ukraine|X|-|-|||||
|2015-09_Mariage_Celine_Alex|X|-||||||
|2015-09_Saut_Elastique_BichLan|X|-||||||
|2015-10_Japon|X|-||||||
|2016-04_Prague|X|-||||||
|2016-07_Clisson|X|-||||||
|2016-07_St_Jean|X|-||||||
|2016-08_Sud_France|X|-||||||
|2016-10_Milan|X|-||||||
|2016-12_Noël_Froger|X|-||||||
|2016-12_USA|X||X|||||
|2017-03_Grossesse|X|-||||||
|2017-05_Mont_Saint_Michel|X|-||||||
|2017-05_Weekend_Bouée|X|-||||||
|2017-06_Sortie_ULM_Papa_Marion|X|-||||||
|2017-07_St_Jean|X|-||||||
|2017-08_Pays_Basque|X|-||||||
|2017-09_Londres|X|X|X|||||||||
|2017-10_Mathis_Naissance|X|-|-|||||
|2017-11_Mathis_Mon_1er_Mois|X|-|X|||||
|2017-12_Famille_Noel_A_La_Maison|X|-|-|||||
|2017-12_Famille_Noel_Froger|X|-|-|||||
|2017-12_Famille_Noel_Girard|X|-|-|||||
|2017-12_Mathis_Mon_2nd_Mois|X|-|X|||||
|2018-01_Mathis_Mon_3eme_Mois|X|-||||||
|2018-01_Nouvel_An|X|-||||||
|2018-02_Mathis_Mon_4eme_Mois|X|-||||||
|2018-03_Mathis_Mon_5eme_Mois|X|-||||||
|2018-04_Mathis_Mon_6eme_Mois|X|-||||||
|2018-05_Chateaux_de_la_Loire|X|-||||||
|2018-05_Mathis_Mon_7eme_Mois|X|-||||||
|2018-06_Famille_Froger|X|-||||||
|2018-06_Mathis_Mon_8mois_Mois|X|-||||||
|2018-07_Famille_Froger_Anniversaire|X|-||||||
|2018-07_Mathis_Mon_9mois_Mois|X|-||||||
|2018-07_St_Jean|X|-||||||
|2018-08_Dordogne|/||X|||||||||
|2018-08_Mathis_10_mois|X|-||||||
|2018-08_Pointe_du_Grouin|X|-||||||
|2018-09_60ans_Maman|X|-||||||
|2018-09_Mathis_11_mois|X|-||||||
|2018-10_Famille_Froger_1an_Mathis|X|-||||||
|2018-10_Mathis_12_mois|X|-||||||
|2018-10_Mathis_Anniversaire_1_an|X|-||||||
|2018-11_Famille_Girard_1an_Mathis|X|-||||||
|2018-11_Mathis|X|-||||||
|2018-12_Famille_Froger_Noel|x|-||||||
|2018-12_Famille_Girard_Noel|X|-||||||
|2018-12_Mathis|X|-||||||
|2018-12_Noel|X|-||||||
|2019-01_Chateau_Chantilly|X|-||||||
|2019-01_Mathis|X|-||||||
|2019-02_Mathis|X|-||||||
|2019-02_Quiberon|X|-||||||
|2019-03_Mathis|X|-||||||
|2019-04_Famille_Froger_Paques|X|-||||||
|2019-04_Mariage|X|-|X|||||
|2019-04_Mathis|X|-||||||
|2019-04_Normandie|X|-||||||
|2019-05_Broceliande|X|-||||||
|2019-05_Mathis|X|-||||||
|2019-06_Mariage|/|-||||||
|2019-06_Mathis|X|-||||||
|...||||||||


Legend : 
X : Done
/ : In progress
- : Not concerned