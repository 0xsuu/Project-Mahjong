#!/usr/bin/env python3

#  Copyright 2017 Project Mahjong. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
This utility calculates all the possible combinations of Tiny Mahjong game.
72 Tiles of 2 kinds, 1 - 9.
A hand of 5 tiles.
"""


def get_combinations():
    combinations = []
    for i0 in range(1, 19-1):
        for i1 in range(i0, 19):
            for i2 in range(i1, 19):
                for i3 in range(i2, 19):
                    for i4 in range(i3, 19):
                        if i0 == i1 and i1 == i2 and i2 == i3 and i3 == i4:
                            continue
                        else:
                            combinations.append([i0, i1, i2, i3, i4])
    return combinations
