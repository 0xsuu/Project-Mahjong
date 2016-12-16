# Project-Mahjong

[![Build Status](https://travis-ci.com/al1enSuu/Project-Mahjong.svg?token=4by9Ez4yfBLSeZfufxzo&branch=master)](https://travis-ci.com/al1enSuu/Project-Mahjong)

## Information links
[Google Drive Folder](https://drive.google.com/open?id=0B0f599yzLN08TDNKWkhPMEh0dHM)

## Install Instructions
```bash
mkdir mahjong
cd mahjong
git clone https://github.com/al1enSuu/Project-Mahjong.git
```

## Supporting Environment
### Linux
+ Supporting CMake 2.8+
+ Supporting Clang++ 3.7+
+ Supporting Python 2.7/3.4 (Set version in build_mahjong.sh)
+ Supporting boost::python 1.54

### Mac
+ Supporting CMake 2.8+
+ Supporting Clang++ 800
+ Supporting Python 3.7

### Windows
- Not tested.

## Prerequisites
* Build library tests: gtest
* Build python interface: boost-python
* Build for coverage info: lcov-1.12+, clang++3.8(on linux)

## Build Instructions
[Build Instructions](https://github.com/al1enSuu/Project-Mahjong/wiki/Compile-Instructions)

## GTest Install Instructions
Run sudo first(to cache the authentication).
```
sudo whoami
```

Then run through(can copy & paste entire block if sudo is not requiring password) the following script.
```bash
git clone https://github.com/google/googletest.git
mkdir -p gtest_build
cd gtest_build
cmake ../googletest
make
sudo make install
cd ..
rm -rf ./googletest ./gtest_build

```
