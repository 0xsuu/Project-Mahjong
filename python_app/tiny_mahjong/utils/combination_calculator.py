#!/usr/bin/env python3

'''
This util calculates all the possible combinations of Tiny Mahjong game.
72 Tiles of 2 kinds, 1 - 9.
A hand of 5 tiles.
'''
def get_combinations():
    combinations = []
    for i0 in range(1, 19-1):
        for i1 in range(i0, 19):
            for i2 in range(i1, 19):
                for i3 in range(i2, 19):
                    for i4 in range(i3, 19):
                        if i0 == i1 and i1==i2 and i2==i3 and i3==i4:
                            continue
                        else:
                            combinations.append([i0,i1,i2,i3,i4])

