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

[Work in progress](doc/progress.md)

