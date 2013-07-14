echo "\n\nWelcome tos SBW-1.6.3 installation\n\n
 Sharada braille writer is a six key approach to producing
 printmaterials. Letters f, d, s, j, k, l represent 1 2 3 4 5 6 of the
 braille dots respectively. By pressing "f" and "s" together will
 produce letter "k" and like.\n\n"

echo "Installing dependencies"
apt-get install python-glade2 espeak python-espeak python-enchant espeak
echo "\n\n\nRemoving old file's ....."
rm -rf /usr/share/pyshared/sbw
rm -rf /usr/lib/python2.7/dist-packages/sbw
rm /usr/bin/sharada-braille-writer
rm /usr/share/applications/sharada-braille-writer.desktop
echo "Creating folder  ........"
mkdir /usr/share/pyshared/sbw
echo "Copying dara ............"
cp -r data /usr/share/pyshared/sbw/
echo "Copying ui xml's ........"
cp -r ui /usr/share/pyshared/sbw/
echo "Copying source files ...."
cp -r sbw /usr/lib/python2.7/dist-packages/
echo "Copying starter ........."
cp sharada-braille-writer /usr/bin/
echo "Copying icon ............"
cp sharada-braille-writer.desktop /usr/share/applications/

ldconfig
touch /usr/lib/python2.7/dist-packages/sbw/__init__.py
chmod 777 /usr/share/pyshared/sbw/data/abbreviations.txt
