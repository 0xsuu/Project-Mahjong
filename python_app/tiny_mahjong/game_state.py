#!/usr/bin/env python3

# -*- coding: utf-8 -*-

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

import numpy as np

FULL_DISCARD_COUNT = 31


class GameState:
    def __init__(self, other_player_ids):
        self._player_hand = None
        self._player_discard = []
        assert len(other_player_ids) != 0
        self._other_player_ids = other_player_ids
        self._other_player_discards = {}
        for i in other_player_ids:
            self._other_player_discards[i] = []

    def on_player_default_hand_obtained(self, hand):
        hand = np.append(hand, -1)
        assert hand.shape[0] == 5
        self._player_hand = hand

    def on_player_pick_new_tile(self, hand):
        self._player_hand = hand

    def on_player_discard(self, tile):
        self._player_discard.append(tile)

    def on_other_player_discard(self, player_id, tile):
        self._other_player_discards[player_id].append(tile)

    def get(self):
        result = np.array(self._player_hand)
        result = np.append(result, self._player_discard)

        for i in range(FULL_DISCARD_COUNT - len(self._player_discard)):
            result = np.append(result, 0)

        for p in self._other_player_discards:
            result = np.append(result, self._other_player_discards[p])
            for k in range(FULL_DISCARD_COUNT - self._other_player_discards[p].shape[0]):
                result = np.append(result, 0)

        assert result.shape[0] == len(self._other_player_ids) * FULL_DISCARD_COUNT + 5

        return result
