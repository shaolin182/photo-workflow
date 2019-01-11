# Photography Workflow
This project describes my own photography workflow and presents the status of my work in progress about all photography collections I have.
It also shares all scripts I used in order to achieve it.

## Step 1 - Importing images
Each images imported should have : 
- a filename which matches this pattern : **YYYY-MM-DD\_HH:MI:SS\_\<SUFFIX\>**
- some exif tags used for ordering photo collection

You can perform thos action by running this script
```
workflow-photo import <source> <dest> <suffix> <collection>
```

This scripts works for raw images as well as compressed images 

If images are already on imported, you can skipped those parts and only applies some parts of the scripts.
More details on help

## Step 2 - Import photos in software

### RAW images
RAW images are imported in darktable
TODO : Create a script for importing photos automatically and create preset for filtering collections

### JPG images
JPG images are imported in Digikam
TODO : Create a script for importing photos automatically

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

## Step 4 - Class images

Classing images consist of attributing a 5 star rank to best images

## Step 4 - Improve images

Use darktable for modifying photographies with higher rangking

## Step 5 - Export images from RAW to JPG

Through darktable export images from RAW format to JPG

# Backup images

BAckup image to :
- NAS
- External hard drive
- Google drive

TODO : script

# Work in progress

| Collection | Import  | Sort | Class | Improve |
|------------|:-------:|:----:|:-----:|:-------:|
|2015-04_Berlin|X||||
|2018-08_Dordogne|X|X|||
|...|||||

# Collections

Collection tags are : 
- Vacances|<YEAR>|<COUNTRY>|<CITY> (ex : Vacances|2018|France|Dordogne)
- Sorties|<YEAR>|Amis/Familles|<EVENT> (ex : Sorties|2018|Famille|Noel_Girard)
- Projet|<YEAR>|<TOPIC>