#!/bin/bash

# First part allow to delete JPG files when RAW files does not exist anymore

# Some constant
EXPECTED_ARGS=1
RETOUCHE_PATH=$DATA_PATH/Retouche_Photo
TEMP_DIR=$DATA_PATH/Retouche_Photo/TO_DELETE

if [ $# -ne $EXPECTED_ARGS ] ; 
then
	echo "Parameter missing - Set the path to synchronize (example : 2014-03_Martinique) - Path must be the same between Photo DIR and Retouche DIR"
	exit 1
fi

# One parameter is mandatory, the directory where RAW and JPG files are stored
# We assume that both directories has the same name
SYNC_PATH=$1

# First, assure that raw files and jpg files have the same filename
cd $PHOTO_PATH/$SYNC_PATH

for i in `find . -name "*.JPG"`; 
do
	FILENAME=$(basename "$i")
	RAWFOUND=$(find $RETOUCHE_PATH/$SYNC_PATH/ -iname "${FILENAME%.*}.NEF" | wc -l)
	
	if [ $RAWFOUND -eq 0 ]
	then 
		echo "No match found for $FILENAME - move it to temp folder"
		
		# mv "$i" "$TEMP_DIR/$FILENAME"
	fi
done

