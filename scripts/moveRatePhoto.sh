#!/bin/sh

echo "moveRatePhoto $1"

RATING=$(exiv2 -Pv -g Xmp.xmp.Rating "$1")

if [ -z "$RATING" ] 
then
	echo "Rating does not exist on $1"
else 
	if [ "$RATING" -eq 5 ]
	then
		cp $1 /media/julien/RAID/Diapo_Martinique/
	fi
fi

