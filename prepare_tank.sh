#!/bin/bash
./download.sh
BAK=tmp/tank_bak
SOURCE=tmp/tank
TARGET=tmp/target
rm -rf "$TARGET"
rsync -a --delete $BAK/ $SOURCE/

echo "fix 2011-28-01"
mv $SOURCE/2011-28-01 $SOURCE/2011-01-28

echo "fix 2014_11_13/10708063_10204320160419761_2049798806_n.jpg"
touch $SOURCE/2014_11_13/10708063_10204320160419761_2049798806_n.jpg
mv $SOURCE/2014_11_13/10708063_10204320160419761_2049798806_n.jpg $SOURCE/2014_11_13/martin.jpg

echo "remove icons"
rm -rf $SOURCE/icons

echo "add image from doc"
cp tmp/2011-05-07_eva.png $SOURCE/