#!/bin/bash

# Some constant
EXPECTED_ARGS=1
DATA_PATH=/media/julien/RAID/Images
PHOTO_PATH=$DATA_PATH/Photos
RETOUCHE_PATH=$DATA_PATH/RAW
TEMP_DIR=$DATA_PATH/RAW/TO_DELETE

# Test that mandatory parameter are ok
if [ $# -ne $EXPECTED_ARGS ] ; 
then
	echo "Parameter missing - Set the path to synchronize (example : 2014-03_Martinique) - Path must be the same between Photo DIR and RAW DIR"
	exit 1
fi

# Extract year from parameter as it is part of the path and test that directory exists
SYNC_PATH=$1
YEAR_PATH=`echo $SYNC_PATH| cut -d'-' -f 1`

# Control that both directories exists
if [ ! -d "$PHOTO_PATH/$YEAR_PATH/$SYNC_PATH" ]; then
	echo "Directory $PHOTO_PATH/$YEAR_PATH/$SYNC_PATH does not exist"
	exit 1
fi

if [ ! -d "$RETOUCHE_PATH/$SYNC_PATH" ]; then
	echo "Directory $RETOUCHE_PATH/$SYNC_PATH does not exist"
	exit 1
fi

# First, assure that raw files and jpg files have the same filename
cd $RETOUCHE_PATH/$SYNC_PATH

for i in `find . -name "*.NEF"`; 
do
	FILENAME=$(basename "$i")
	JPGFOUND=$(find $PHOTO_PATH/$YEAR_PATH/$SYNC_PATH/ -iname "${FILENAME%.*}*" | wc -l)
	
	if [ $JPGFOUND -eq 0 ]
	then 
		echo "No match found for ${FILENAME%.*} in $PHOTO_PATH/$YEAR_PATH/$SYNC_PATH/ - move it to temp folder"
		mv "$i" "$TEMP_DIR/$FILENAME"
	fi
done