#!/bin/bash

BASEDIR=$(dirname "$0")
cd "$BASEDIR"/

if [ "$1" == "" ];
    echo "Please specify a number of player to generate."
    exit -1
    
python3 TenhouDecoder.py $1

echo "n$1X.csv and n$1y.csv generated."

