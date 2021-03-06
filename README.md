# Project-Mahjong

[![Build Status](https://travis-ci.com/0xsuu/Project-Mahjong.svg?token=4by9Ez4yfBLSeZfufxzo&branch=master)](https://travis-ci.com/0xsuu/Project-Mahjong)

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

## Quick Start: Simple Mahjong Game Python
```bash
./build_mahjong.sh --python
cd python_app/simple_mahjong
python3 play.py
```

## Quick Start: Tenhou bot
```bash
./build_mahjong.sh --python
cd python_app/tenhou-bot
python3 main.py
```

## Quick Start: Tiny Mahjong
[Tiny Mahjong README](https://github.com/0xsuu/Project-Mahjong/blob/master/python_app/tiny_mahjong/README.md)

## Mahjong Lib Supporting Environment
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
- Supporting Python 3.5+
- boost::python not tested.

## Prerequisites
* Build library tests: gtest
* Build python interface: boost-python
* Build for coverage info: lcov-1.12+, clang++3.8(on linux)

## Detailed Build Instructions
[Build Instructions](https://github.com/al1enSuu/Project-Mahjong/wiki/Build-Instructions)
