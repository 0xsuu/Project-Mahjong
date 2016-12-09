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

## Build Instructions
[Build Instructions](https://github.com/al1enSuu/Project-Mahjong/wiki/Compile-Instructions)

## GTest Install Instructions
Run sudo first.
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
