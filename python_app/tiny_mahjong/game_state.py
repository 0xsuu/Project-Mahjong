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

FULL_DISCARD_COUNT = 32


class GameState:
    def __init__(self, other_player_ids, disclose_all):
        self._player_hand = None
        self._opponents_hands = None
        self._player_discards = []
        assert len(other_player_ids) != 0
        self._other_player_ids = other_player_ids
        self._other_player_discards = {}
        for i in other_player_ids:
            self._other_player_discards[i] = []
        self.__disclose_all = disclose_all

    # Player's hand update.

    def on_player_default_hand_obtained(self, hand):
        hand = np.append(hand, 0)
        assert hand.shape[0] == 5
        self._player_hand = hand

    def on_player_pick_new_tile(self, hand):
        self._player_hand = hand

    # Opponents' hands update (for disclose option).

    def on_other_players_hands_obtained(self, hands):
        self._opponents_hands = hands

    # Players' discards update.

    def on_player_discard(self, tile):
        self._player_discards.append(tile)

    def on_other_player_discard(self, player_id, tile):
        self._other_player_discards[player_id].append(tile)

    def get(self):
        # Append player's hand.
        result = np.array(self._player_hand)

        # If the disclose option is enabled, append opponents' hands.
        if self.__disclose_all:
            result = np.append(result, self._opponents_hands)

        # Append player's discards.
        result = np.append(result, self._player_discards)

        # Fill up 0s for non-full games. i.e. use fixed size input, thus the maximum number of discards are used.
        for i in range(FULL_DISCARD_COUNT - len(self._player_discards)):
            result = np.append(result, 0)

        # Append opponents' discards and fill up with 0s.
        for p in self._other_player_discards:
            result = np.append(result, self._other_player_discards[p])
            for k in range(FULL_DISCARD_COUNT - len(self._other_player_discards[p])):
                result = np.append(result, 0)

        other_players_count = len(self._other_player_ids)
        assert result.shape[0] == (other_players_count + 1) * FULL_DISCARD_COUNT + 5 + \
            self.__disclose_all * other_players_count * 5

        return result
