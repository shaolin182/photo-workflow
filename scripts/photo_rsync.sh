#!/bin/sh

CUR_DATE=`date +%F`
rsync -av --delete /media/julien/DATA/Photos/ root@192.168.0.37:/media/DATA/Photos/ >> /home/julien/photo-workflow/rsync_${CUR_DATE}.log