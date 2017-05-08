#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Tiles Set:
C 1-9
D 1-9
B 1-9
S 1-7 (East South West North Red Green White)
Total: 136 Tiles

Encoding rule:
C: 1010
D: 1011
B: 1100
S: 1101

Numbers: 0001 - 1001

One storage hand:
[C][Numbers]*[D][Numbers]*[B][Numbers]*[S][Numbers]*

One composing hand:
[[C, D, B, S] << 4 | Numbers]*
'''

C = 0b1010
D = 0b1011
B = 0b1100
S = 0b1101

bytesToWrite = bytearray()

modes = [""]*10
modes.append("萬")
modes.append("筒")
modes.append("條")
sp = ["", "東", "南", "西", "北", "中", "發", "白"]
hanzi = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九"]

def printStorageHand(bytes):
    mode = 0
    for i in bytes:
        i2 = i & 0b1111
        i1 = i >> 4
        iArray = [i1, i2]
        for j in iArray:
            if j >= C and j <= S:
                mode = j
                continue
            elif j > 0 and j < C:
                if mode < S:
                    print hanzi[j] + modes[mode],
                else:
                    print sp[j],
    print

byte = 0;
def pushBits(fourBits):
    if byte == 0:
        byte |= fourBits
    elif byte >> 4 == 0:
        byte = byte << 4
        byte |= fourBits
        bytesToWrite.append(byte)
        byte = 0

def getTile(mode, num):
    return mode << 4 | num

def composeToStorage(composeArray):
    print composeArray

def main():
    totalCount = 967458816.0
    count = 0
    # 雀头 i, j * 2.
    for i in range(C, S + 1):
        for j in range(1, 10):
            for i1 in range(C, S + 1):
                for j1 in range(1, 10):
                    for k1 in range(2):
                        for i2 in range(C, S + 1):
                            for j2 in range(1, 10):
                                for k2 in range(2):
                                    for i3 in range(C, S + 1):
                                        for j3 in range(1, 10):
                                            for k3 in range(2):
                                                for i4 in range(C, S + 1):
                                                    for j4 in range(1, 10):
                                                        for k4 in range(2):
                                                            composeSet = []
                                                            composeSet.append(getTile(i, j))
                                                            composeSet.append(getTile(i, j))
                                                            if k1 == 0:
                                                                composeSet.append(getTile(i1, j1))
                                                                composeSet.append(getTile(i1, j1))
                                                                composeSet.append(getTile(i1, j1))
                                                            elif k1 == 1 and j1 <= 7:
                                                                composeSet.append(getTile(i1, j1))
                                                                composeSet.append(getTile(i1, j1 + 1))
                                                                composeSet.append(getTile(i1, j1 + 2))

                                                            if k2 == 0:
                                                                composeSet.append(getTile(i2, j2))
                                                                composeSet.append(getTile(i2, j2))
                                                                composeSet.append(getTile(i2, j2))
                                                            elif k2 == 1 and j2 <= 7:
                                                                composeSet.append(getTile(i2, j2))
                                                                composeSet.append(getTile(i2, j2 + 1))
                                                                composeSet.append(getTile(i2, j2 + 2))

                                                            if k3 == 0:
                                                                composeSet.append(getTile(i3, j3))
                                                                composeSet.append(getTile(i3, j3))
                                                                composeSet.append(getTile(i3, j3))
                                                            elif k3 == 1 and j3 <= 7:
                                                                composeSet.append(getTile(i3, j3))
                                                                composeSet.append(getTile(i3, j3 + 1))
                                                                composeSet.append(getTile(i3, j3 + 2))

                                                            if k4 == 0:
                                                                composeSet.append(getTile(i4, j4))
                                                                composeSet.append(getTile(i4, j4))
                                                                composeSet.append(getTile(i4, j4))
                                                            elif k4 == 1 and j4 <= 7:
                                                                composeSet.append(getTile(i4, j4))
                                                                composeSet.append(getTile(i4, j4 + 1))
                                                                composeSet.append(getTile(i4, j4 + 2))

                                                            if count == 1:
                                                                composeToStorage(composeSet)
                                                                #print str(count / totalCount * 100.0) + "%"
                                                                quit(0)
                                                            count += 1

if __name__ == "__main__":
    main()
