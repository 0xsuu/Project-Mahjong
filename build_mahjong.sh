#!/bin/bash

set -e

BASEDIR=$(dirname "$0")

cd "$BASEDIR"/
PROJECT_MAHJONG="${PWD##*/}"

if [ ! -f /etc/bash_completion.d/build_mahjong.sh ] || [ "$1" == "--update-code-completion" ]; then
    echo "build_mahjong() {
    local cur prev opts
    COMPREPLY=()
    cur=\"\${COMP_WORDS[COMP_CWORD]}\"
    prev=\"\${COMP_WORDS[COMP_CWORD-1]}\"
    opts=\"--help --lib --game --player --update-code-completion\"

    if [[ \${cur} == -* ]] ; then
        COMPREPLY=( \$(compgen -W \"\${opts}\" -- \${cur}) )
        return 0
    fi
}
complete -F build_mahjong build_mahjong.sh" > /etc/bash_completion.d/build_mahjong.sh
else
    . /etc/bash_completion.d/build_mahjong.sh
fi

# Go to project directory.
cd ../

if [ "$1" == "--lib" ]; then
    # Create build folder.
    mkdir -p ./build_mahjong
    cd ./build_mahjong

    # Generate Xcode project
    if [ "$2" == "xcode" ]; then
    	mkdir -p xcode
        cd xcode
        cmake -G Xcode ../../"$PROJECT_MAHJONG"/mahjong_lib/
        open Mahjong-lib.xcodeproj
        exit 0
    fi

    # Run test.
    if [ "$2" == "test" ]; then
        cmake ../"$PROJECT_MAHJONG"/mahjong_lib/ -DCMAKE_CXX_COMPILER=clang++
        make libma_test
        ../libma_gtest/libma_test
        exit 0
    fi

    cmake ../"$PROJECT_MAHJONG"/mahjong_lib/ -DCMAKE_CXX_COMPILER=clang++
    make mahjong
    exit 0
fi

if [ "$1" == "--game" ]; then
    ./"$PROJECT_MAHJONG"/build_mahjong.sh --lib

    if [ ! -f ./build_mahjong/libmahjong.a ]; then
        echo "Mahjong lib not found!"
        exit -1
    fi

    mkdir -p build_games
    cd build_games

    # Generate Xcode project
    if [ "$2" == "xcode" ]; then
        mkdir -p xcode
        cd xcode
        cmake -G Xcode ../../"$PROJECT_MAHJONG"/games/
        open Mahjong-games.xcodeproj
        exit 0
    fi

    if [ "$2" == "simple" ]; then
        echo "Building SimpleMahjong..."
        cmake ../"$PROJECT_MAHJONG"/games/
        make SimpleMahjong
        ../Mahjong-games/SimpleMahjong
        exit 0
    fi

    echo "Please specify a game to build!"
    exit -1
fi

if [ "$1" == "--player" ]; then
    ./"$PROJECT_MAHJONG"/build_mahjong.sh --lib

    if [ ! -f ./build_mahjong/libmahjong.a ]; then
        echo "Mahjong lib not found!"
        exit -1
    fi

    mkdir -p build_players
    cd build_players

    # Generate Xcode project
    if [ "$2" == "xcode" ]; then
        mkdir -p xcode
        cd xcode
        cmake -G Xcode ../../"$PROJECT_MAHJONG"/players/
        open Mahjong-players.xcodeproj
        exit 0
    fi

    if [ "$2" == "user" ]; then
        echo "Building UserInputPlayer..."
        cmake ../"$PROJECT_MAHJONG"/players/
        make UserInputPlayer
        exit 0
    fi

    echo "Please specify a game to build!"
    exit -1

fi

# Show help.
if [ "$1" == "--help" ]; then
    echo "./build_mahjong.sh --lib [xcode | test] --game [xcode | simple]"
    exit 0
fi
