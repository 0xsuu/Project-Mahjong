#!/bin/bash

set -e

BASEDIR=$(dirname "$0")

cd "$BASEDIR"/
PROJECT_MAHJONG="${PWD##*/}"

# For auto-complete.
if [ "$1" == "--update-code-completion" ]; then
    # Require root.
    mkdir -p /etc/bash_completion.d
    echo "build_mahjong() {
    local cur prev opts
    COMPREPLY=()
    cur=\"\${COMP_WORDS[COMP_CWORD]}\"
    prev=\"\${COMP_WORDS[COMP_CWORD-1]}\"
    opts=\"--help --lib --game --player --update-code-completion --coverage --python\"

    if [[ \${cur} == -* ]] ; then
        COMPREPLY=( \$(compgen -W \"\${opts}\" -- \${cur}) )
        return 0
    fi
}
complete -F build_mahjong build_mahjong.sh" > /etc/bash_completion.d/build_mahjong.sh
fi

# Go to project directory.
cd ../

# Set python include path.
PYTHON_VERSION=3.4 # Set the variable to empty and modify the next line to use default python version.
export CPLUS_INCLUDE_PATH="/usr/include/python$PYTHON_VERSION"

if [ "$1" == "--coverage" ]; then
    mkdir -p ./build_mahjong
    cd ./build_mahjong

    cmake ../"$PROJECT_MAHJONG"/mahjong_lib/ -DCMAKE_BUILD_TYPE=Coverage
    make
    make coverage

    tput setaf 2
    echo "Coverage report generated: $(pwd)coverage_report/index.html"
    tput sgr0
    if [ "$(uname -s)" == "Darwin" ]; then
        open ./coverage_report/index.html
    fi

    exit 0
fi

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
        cmake ../"$PROJECT_MAHJONG"/mahjong_lib/
        make libma_test
        ../libma_gtest/libma_test
        exit 0
    fi

    # Build dynamic lib for Python interface.
    if [ "$2" == "python" ]; then
        cmake ../"$PROJECT_MAHJONG"/mahjong_lib/ -DPYTHON_VERSION=$PYTHON_VERSION
        make dmahjong
        exit 0
    fi

    cmake ../"$PROJECT_MAHJONG"/mahjong_lib/
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
        ../"$PROJECT_MAHJONG"/build_mahjong.sh --player all "-DGAME_TYPE=SIMPLE_MAHJONG"

        cmake ../"$PROJECT_MAHJONG"/games/
        make SimpleMahjong
        if [ ! "$3" == "norun" ]; then
            ../Mahjong-games/SimpleMahjong
        fi
        exit 0
    fi

    # Build dynamic lib for Python interface.
    if [ "$2" == "python" ]; then
        ../"$PROJECT_MAHJONG"/build_mahjong.sh --player all "-DGAME_TYPE=SIMPLE_MAHJONG"

        cmake ../"$PROJECT_MAHJONG"/games/ -DPYTHON_VERSION=$PYTHON_VERSION
        make dGames
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

    if [ "$2" = "dumb" ]; then
        echo "Building DumpPlayers..."
        cmake ../"$PROJECT_MAHJONG"/players/
        make DumbPlayers
        exit 0
    fi

    if [ "$2" = "nonlp" ]; then
        echo "Building NonLearningPlayers..."
        cmake ../"$PROJECT_MAHJONG"/players/
        make NonLearningPlayers
        exit 0
    fi

    if [ "$2" == "python" ]; then
        cmake ../"$PROJECT_MAHJONG"/players/ -DPYTHON_VERSION=$PYTHON_VERSION
        make dPlayers
        exit 0
    fi

    echo "Building all players..."
        if [ "$3" != "" ]; then
            cmake ../"$PROJECT_MAHJONG"/players/ "$3"
        else
            cmake ../"$PROJECT_MAHJONG"/players/
        fi
        make AllPlayers
    exit 0
fi

if [ "$1" == "--python" ]; then
    ./"$PROJECT_MAHJONG"/build_mahjong.sh --lib python
    ./"$PROJECT_MAHJONG"/build_mahjong.sh --player python
    ./"$PROJECT_MAHJONG"/build_mahjong.sh --game python

    exit 0
fi

# Show help.
if [ "$1" == "--help" ]; then
    echo "./build_mahjong.sh --lib [xcode | test] --game [xcode | simple]"
    exit 0
fi

