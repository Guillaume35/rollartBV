#!/bin/bash

echo "Welcome to Rollart Unchaine build tool for Linux !"
echo "--------------------------------------------------"
echo ""

echo "Control and install dependencies"
echo "--------------------------------"

sudo apt-get install python3-dev python3-pip
sudo pip3 install pyinstaller
sudo pip3 --upgrade pyinstaller 
echo "End of pre-process"
echo ""

echo "Start building process"
echo "----------------------"

BASEDIR=$(dirname $0)
cd $BASEDIR

pyinstaller rollartBV.py --distpath './dist/linux' --add-data="LICENSE:." --add-data="assets:assets"

echo ""
echo "You program is stored in dist folder"
echo "CONGRATULATION !"