#!/bin/bash

set -e

BASEDIR=$(dirname "$0")

cd "$BASEDIR"/
PROJECT_MAHJONG="${PWD##*/}"

# Go to project directory.
cd ../

./"$PROJECT_MAHJONG"/build_lib.sh

if [ ! -f ./build_mahjong/libmahjong.a ]; then
    echo "Mahjong lib not found!"
fi

mkdir -p build_games
cd build_games

if [ "$1" == "simple" ]; then
    echo "Building SimpleMahjong..."
    cmake ../"$PROJECT_MAHJONG"/games/SimpleMahjong/
    make
    ../SimpleMahjong/SimpleMahjong
    exit 0
fi

echo "Please specify a game to build!"
exit -1

