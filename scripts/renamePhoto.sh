#!/bin/bash

EXPECTED_ARGS=2

function help
{
	echo "Usage : `basename $0` [name] [file(s)]"
	echo "Exemple : ./renamePhoto.sh Julien '/media/DATA/Photos/2012-04_Londres/*.JPG'" 
	exit 0
}

function interactiveScript
{
	read -p "Suffixe à appliquer aux fichiers : "  suffix

	defaultPath="$PWD/*.JPG"
	read -p "Liste des photos à modifier [$defaultPath]: " path
	path="${path:-$defaultPath}"

	rename "$suffix" "$path"

}

function rename
{
	exiv2 -F -r"%Y-%m-%d_%H-%M-%S_$1" rename $2
}

if [ $# -ne $EXPECTED_ARGS ] ; 
then
	interactiveScript
else
	rename $1 $2
fi

exit 0
