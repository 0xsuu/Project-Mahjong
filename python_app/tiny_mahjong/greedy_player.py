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

import copy

from game import *


def calculate_shanten(hand):
    assert hand.shape[0] == 5
    for i in range(hand.shape[0] - 2):
        if (hand[i] == hand[i + 1] and hand[i + 1] == hand[i + 2]) or \
                (hand[i] + 1 == hand[i + 1] and hand[i + 1] + 1 == hand[i + 2]):
            copy_hand = copy.deepcopy(hand)
            copy_hand = np.delete(copy_hand, [i, i + 1, i + 2])
            if copy_hand[0] == copy_hand[1]:
                return 0
            else:
                return 1

    assert hand.shape[0] == 5
    for i in range(hand.shape[0] - 1):
        if hand[i] == hand[i + 1]:
            copy_hand = copy.deepcopy(hand)
            copy_hand = np.delete(copy_hand, [i, i + 1])
            if copy_hand[0] == copy_hand[1] or \
                    copy_hand[1] == copy_hand[2] or \
                    copy_hand[0] + 1 == copy_hand[1] or \
                    copy_hand[1] + 1 == copy_hand[2] or \
                    copy_hand[0] + 2 == copy_hand[1] or \
                    copy_hand[1] + 2 == copy_hand[2]:
                return 1

    assert hand.shape[0] == 5
    for i in range(hand.shape[0] - 1):
        if hand[i] + 1 == hand[i + 1] or \
                hand[i] + 2 == hand[i + 1]:
            return 2

    return 3


class GreedyPlayer(Player):
    def tile_picked(self):
        Player.tile_picked(self)
        if self.test_win():
            return WIN, -1
        expected_shantens = []
        for i in range(5):
            copy_hand = copy.deepcopy(self.hand)
            copy_hand = np.delete(copy_hand, i)
            expected_shanten = 0.0
            for picked_tile in range(1, 19):
                copy_copy_hand = copy.deepcopy(copy_hand)
                copy_copy_hand = np.append(copy_copy_hand, picked_tile)
                copy_copy_hand.sort()
                expected_shanten += self.get_pick_tile_probability(picked_tile) * \
                    calculate_shanten(copy_copy_hand)
            expected_shantens.append(expected_shanten)
        return DISCARD, np.argmin(expected_shantens)
