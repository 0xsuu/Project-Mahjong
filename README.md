# Project-Mahjong

[![Build Status](https://travis-ci.com/0xsuu/Project-Mahjong.svg?token=4by9Ez4yfBLSeZfufxzo&branch=master)](https://travis-ci.com/0xsuu/Project-Mahjong)

## Information links
[Google Drive Folder](https://drive.google.com/open?id=0B0f599yzLN08TDNKWkhPMEh0dHM)

## Obtain Source Code
```bash
mkdir mahjong
cd mahjong
git clone https://github.com/al1enSuu/Project-Mahjong.git
cd Project-Mahjong
```

## Quick Start: Simple Mahjong Game
```bash
./build_mahjong.sh --game simple
```

## Quick Start: Tenhou bot
```bash
./build_mahjong.sh --python
cd python_app/tenhou-bot
python3 main.py
```

## Supporting Environment
### Linux
+ Supporting CMake 2.8+
+ Supporting Clang++ 3.7+
+ Supporting Python 3.4/3.5
+ Supporting boost::python 1.54

### Mac
+ Supporting CMake 2.8+
+ Supporting Clang++ 800
+ Supporting Python 3.4+
+ Python 3.6 not supported for SimpleMahjong Python version.

### Windows
- Not tested.

## Prerequisites
* Build library tests: gtest
* Build python interface: boost-python
* Build for coverage info: lcov-1.12+, clang++3.8(on linux)

## Detailed Build Instructions
[Build Instructions](https://github.com/al1enSuu/Project-Mahjong/wiki/Build-Instructions)
