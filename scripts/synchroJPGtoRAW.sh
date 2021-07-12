#!/bin/bash

# First part allow to delete raw files when JPG files does not exist anymore

# Some constant
EXPECTED_ARGS=1
DATA_PATH=/media/julien/RAID/Images
PHOTO_PATH=$DATA_PATH/Photos
RETOUCHE_PATH=$DATA_PATH/RAW
TEMP_DIR=$DATA_PATH/RAW/TO_DELETE

if [ $# -ne $EXPECTED_ARGS ] ; 
then
	echo "Parameter missing - Set the path to synchronize (example : 2014-03_Martinique) - Path must be the same between Photo DIR and Retouche DIR"
	exit 1
fi


# Display help message in a function does not match required parameters
# $1 : number expected parameters
# $2 : current Number parameter 
# $3 : function name
function testNbParameter {

	if [ $2 -ne $1 ] ; 
	then
		echo "Error in $3 function - Wrong parameters"
		exit 1
	fi
}

# Return the value of the given tag
# If value is empty, we delete tag
# $1 : tag name
# $2 : source file
# $3 : dest file
function getTagValue {

	VALUE_TAG=$(exiv2 -g $1 -Pv $2)
	if [[ -z $VALUE_TAG ]]
	then
		exiv2 -M"set $1" $3
		echo "EMPTY"
	else
		echo "$VALUE_TAG"
	fi
}

# Update a data from a file to 2nd file
# $1 = Name of the tag
# $2 = source file
# $3 = dest file
function updateMetadataListXMP {

	EXPECTED_ARGS_FUNC=3
	testNbParameter $EXPECTED_ARGS_FUNC $# "updateMetadataXMP"

	VALUE_TAG=$(getTagValue $1 $2 $3)
	if [[ "$VALUE_TAG" != "EMPTY" ]]
	then
		IFS=',' read -a array <<< "$VALUE_TAG"
		# Erase then, add
		#echo "exiv2 -M'del $1' $3"
		exiv2 -M"reg lr http://ns.adobe.com/lightroom/1.0/" -M"del $1" $3
		for element in "${array[@]}"; 
		do 
			echo "updateMetadataListXMP tag : $1 with value : $element on file : $3"
			exiv2 -M"reg lr http://ns.adobe.com/lightroom/1.0/" -M"set $1 XmpSeq $element" $3; 
		done
		
	fi
}

# Update a data from a file to 2nd file
# $1 = Name of the tag
# $2 = source file
# $3 = dest file
function updateMetadataSingleXMP {

	EXPECTED_ARGS_FUNC=3
	testNbParameter $EXPECTED_ARGS_FUNC $# "updateMetadataXMP"

	VALUE_TAG=$(getTagValue $1 $2 $3)
	if [[ "$VALUE_TAG" != "EMPTY" ]]
	then
		echo "updateMetadataSingleXMP tag : $1 with value : $VALUE_TAG on file : $3" 
		exiv2 -M"set $1 $VALUE_TAG" $3
	fi
}

# Update a data from a file to 2nd file
# $1 = Name of the tag
# $2 = source file
# $3 = dest file
function updateMetadataIPTC {

	EXPECTED_ARGS_FUNC=3
	testNbParameter $EXPECTED_ARGS_FUNC $# "updateMetadataIPTC"

	VALUE_TAG=$(getTagValue $1 $2 $3)
	if [[ "$VALUE_TAG" != "EMPTY" ]]
	then
		echo "Tag $1 exist"

		if [[ $VALUE_TAG == *\n* ]]
		then
			echo "List"
			# Erase then, add
			#echo "exiv2 -M'del $1' $3"
			exiv2 -M"del $1" $3
			I=0
			while read line; 
			do 
				echo "$line";
				exiv2 -M"set $1 $line" $3; 

			done <<< "$VALUE_TAG"
		else
			echo "Single Value" 
			exiv2 -M"set $1 $VALUE_TAG" $3
		fi
	fi
}

# One parameter is mandatory, the directory where RAW and JPG files are stored
# We assume that both directories has the same name
SYNC_PATH=$1

# First, assure that raw files and jpg files have the same filename
cd $RETOUCHE_PATH/$SYNC_PATH

for i in `find . -name "*.NEF"`; 
do
	FILENAME=$(basename "$i")
	JPGFOUND=$(find $PHOTO_PATH/2016/$SYNC_PATH/ -iname "${FILENAME%.*}*" | wc -l)
 	#echo "find $PHOTO_PATH/2016/$SYNC_PATH/ -iname "${FILENAME%.*}*" | wc -l"
	
	if [ $JPGFOUND -eq 0 ]
	then 
		echo "No match found for ${FILENAME%.*} in $PHOTO_PATH/2016/$SYNC_PATH/ - move it to temp folder"
		
		mv "$i" "$TEMP_DIR/$FILENAME"
	fi
done

# Then, synchronize some metadata from JPG file to RAW file
# Field to synchronize : #
#  - Xmp.xmp.Rating
#  - Xmp.lr.hierarchicalSubject
#  - Xmp.MicrosoftPhoto.LastKeywordXMP
#  - Xmp.dc.subject
#  - Xmp.digiKam.TagsList
#  - Iptc.Application2.Keywords (*4)

# Loop on all JPG photo
#cd le chemin syncpath
#on boucle sur tous les fichiers pour mettre à jour les meta données
