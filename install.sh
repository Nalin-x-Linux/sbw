#!/bin/bash

if [ $UID -ne 0 ];
then
echo "Please run this script as root"
exit
fi

echo "================= Sharada Braille  Wrieter =======================
 Sharada braille writer is a six key approach to producing
 printmaterials. Letters f, d, s, j, k, l represent 1 2 3 4 5 6 of the
 braille dots respectively. By pressing "f" and "s" together will
 produce letter "k" and like."


echo "============ Checking and Installing dependencies ================"
apt-get install python-glade2 espeak python-espeak python-enchant espeak

echo "============ Checking and removing existing files ================"
if [ -d /usr/share/pyshared/sbw ];
then 
rm -rf /usr/share/pyshared/sbw
echo "Removing existing Data...............Ok"
fi

if [ -d /usr/lib/python2.7/dist-packages/sbw ];
then 
rm -rf /usr/lib/python2.7/dist-packages/sbw
echo "Removing existing source.............Ok"
fi


if [ -e /usr/bin/sharada-braille-writer ];
then 
rm /usr/bin/sharada-braille-writer
echo "Removing bin ........................Ok"
fi

if [ -e /usr/share/applications/sharada-braille-writer.desktop ];
then 
rm /usr/share/applications/sharada-braille-writer.desktop
echo "Removing icon .......................Ok"
fi

echo "==================== Copying new files ==========================="
echo "Creating sbw folder  ................OK"
mkdir /usr/share/pyshared/sbw
echo "Copying dara ........................OK"
cp -r data /usr/share/pyshared/sbw/
echo "Copying ui xml's ....................OK"
cp -r ui /usr/share/pyshared/sbw/
echo "Copying source files ................OK"
cp -r sbw /usr/lib/python2.7/dist-packages/
echo "Copying starter .....................OK"
cp sharada-braille-writer /usr/bin/
echo "Copying icon ........................OK"
cp sharada-braille-writer.desktop /usr/share/applications/

ldconfig
touch /usr/lib/python2.7/dist-packages/sbw/__init__.py
chmod 555 /usr/share/pyshared/sbw/data/*
chmod 777 /usr/share/pyshared/sbw/data/abbreviations.txt
echo "============ Compleated==========================================="
