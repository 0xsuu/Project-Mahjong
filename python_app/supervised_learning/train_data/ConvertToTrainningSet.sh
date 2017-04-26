#!/bin/bash

BASEDIR=$(dirname "$0")
cd "$BASEDIR"/

if [ "$1" == "" ]; then
    echo "Please specify a number of player to generate."
    exit -1
fi
    
python3 TenhouDecoder.py $1

echo "n$1X.csv and n$1y.csv generated."

mv mjlog_pf4-20_n$1/n$1* ./

echo "Always check for the size of the data."
echo "These two should be identical."
wc -l n$1*
echo "These two should be 447 and 27."
wc -L n$1*

