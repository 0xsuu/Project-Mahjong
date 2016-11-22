#!/bin/bash

set -e

BASEDIR=$(dirname "$0")

cd "$BASEDIR"/
PROJECT_MAHJONG="${PWD##*/}"

# Go to project directory.
cd ../

if [ ! -f ./build_mahjong/libmahjong.a ]; then
    ./"$PROJECT_MAHJONG"/build_lib.sh
else
    echo "Mahjong lib found!"
fi

mkdir -p build_games
cd build_games

if [ "$1" == "simple" ]; then
    echo "Building SimpleMahjong..."
    cmake ../"$PROJECT_MAHJONG"/games/SimpleMahjong/
    ../SimpleMahjong/SimpleMahjong
    exit 0
fi

