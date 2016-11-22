#!/bin/bash

set -e

BASEDIR=$(dirname "$0")

cd "$BASEDIR"/
PROJECT_MAHJONG="${PWD##*/}"

# Go to project directory.
cd ../

# Create build folder.
mkdir -p ./build_mahjong
cd ./build_mahjong

# Generate Xcode project
if [ "$1" == "xcode" ]; then
	mkdir -p xcode
    cd xcode
    cmake -G Xcode ../../"$PROJECT_MAHJONG"/mahjong_lib/
    open Mahjong-lib.xcodeproj
    exit 0
fi

# Run test.
if [ "$1" == "test" ]; then
    cmake ../"$PROJECT_MAHJONG"/mahjong_lib/ -DCMAKE_CXX_COMPILER=clang++
    make libma_test
    ../libma_gtest/libma_test
    exit 0
fi

# Show help.
if [ "$1" == "help" ]; then
    echo "./build_lib.sh [xcode | test]"
    exit 0
fi

cmake ../"$PROJECT_MAHJONG"/mahjong_lib/ -DCMAKE_CXX_COMPILER=clang++
make mahjong

