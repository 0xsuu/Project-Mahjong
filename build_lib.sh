#!/bin/bash

set -e

BASEDIR=$(dirname "$0")

# Go to project directory.
cd "$BASEDIR"/../

if [ ! -d ./Project-Mahjong ]; then
    echo "Project name must be Project-Mahjong!"
    exit -1
fi

# Create build folder.
mkdir -p ./build_mahjong
cd ./build_mahjong

# Generate Xcode project
if [ "$1" == "xcode" ]; then
	mkdir -p xcode
    cd xcode
    cmake -G Xcode ../../Project-Mahjong/mahjong_lib/
    open Mahjong-lib.xcodeproj
    exit 0
fi

# Run test.
if [ "$1" == "test" ]; then
    cmake ../Project-Mahjong/mahjong_lib/ -DBUILD_TEST="YES"
    make
    ../libma_gtest/libma_test
    exit 0
fi

# Show help.
if [ "$1" == "help" ]; then
    echo "./build_lib.sh [xcode | test]"
    exit 0
fi

cmake ../Project-Mahjong/mahjong_lib/ -DBUILD_TEST=""
make

