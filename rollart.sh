#!/bin/bash

echo "Script executed from: ${PWD}"

BASEDIR=$(dirname $0)
echo "Script location: ${BASEDIR}"

echo "Now we are going to start Rollart Unchained. Welcome !"

python3 $BASEDIR/rollartBV.py