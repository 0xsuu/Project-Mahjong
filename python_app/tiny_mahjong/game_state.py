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

TILE_STACK_COUNT = 72
PLAYER_COUNT = 2
INITIAL_HAND_COUNT = 4
FULL_DISCARD_COUNT = int((TILE_STACK_COUNT - PLAYER_COUNT * INITIAL_HAND_COUNT) / PLAYER_COUNT)


class GameState:
    def __init__(self, other_player_ids, disclose_all):
        self._player_hand = None
        self._opponents_hands = None
        self._player_discards = []
        self._other_player_discards = {}
        if other_player_ids is not None:
            if len(other_player_ids) != 0:
                self._other_player_ids = other_player_ids
                for i in other_player_ids:
                    self._other_player_discards[i] = []
            else:
                raise ValueError("Empty number of player ids.")

        self.__disclose_all = disclose_all

    def copy(self):
        copy_object = GameState(None, self.__disclose_all)
        if self._player_hand is not None:
            copy_object._player_hand = self._player_hand.copy()
        if self._opponents_hands is not None:
            copy_object._opponents_hands = self._opponents_hands.copy()
        copy_object._player_discards = self._player_discards.copy()
        copy_object._other_player_ids = self._other_player_ids.copy()
        for player_id in copy_object._other_player_ids:
            copy_object._other_player_discards[player_id] = self._other_player_discards[player_id].copy()
        return copy_object

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

    def on_player_discard(self, tile, new_hand):
        self._player_discards.append(tile)
        self._player_hand = new_hand

    def on_other_player_discard(self, player_id, tile, new_hand):
        self._other_player_discards[player_id].append(tile)
        self._opponents_hands = new_hand

    # Accessors.

    def get(self):
        """ Get the vector of the whole state information. """

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

    def get_player_hand(self):
        return self._player_hand

    def calc_shanten(self):
        # Try remove the combo first.
        found_combo = False
        for i in range(self._player_hand.shape[0] - 2):
            # Avoid duplicate initial tile.
            if i > 0 and self._player_hand[i] == self._player_hand[i-1]:
                continue
            if self._player_hand[i] == self._player_hand[i+1] and self._player_hand[i+1] == self._player_hand[i+2]:
                removed_trio_hand = self._player_hand.copy()
                removed_trio_hand = np.delete(removed_trio_hand, i+2)
                removed_trio_hand = np.delete(removed_trio_hand, i+1)
                removed_trio_hand = np.delete(removed_trio_hand, i)
                # If a trio is removed, we can derive the shanten directly.
                if removed_trio_hand.shape[0] == 1:
                    return 1
                if removed_trio_hand.shape[0] == 2:
                    if removed_trio_hand[0] == removed_trio_hand[1]:
                        return 0
                    else:
                        return 1
            for j in range(i + 1, self._player_hand.shape[0] - 1):
                if self._player_hand[i] <= 9 < self._player_hand[j] or self._player_hand[i] > 9 >= self._player_hand[j]:
                    # Break the loop if the suit does not match.
                    break
                if self._player_hand[i] == self._player_hand[j] - 1:
                    for k in range(j + 1, self._player_hand.shape[0]):
                        if self._player_hand[j] <= 9 < self._player_hand[k] or \
                                self._player_hand[j] > 9 >= self._player_hand[k]:
                            # Break the loop if the suit does not match.
                            break
                        if self._player_hand[j] == self._player_hand[k] - 1:
                            removed_straight_hand = self._player_hand.copy()
                            removed_straight_hand = np.delete(removed_straight_hand, k)
                            removed_straight_hand = np.delete(removed_straight_hand, j)
                            removed_straight_hand = np.delete(removed_straight_hand, i)
                            # If a trio is removed, we can find the minimum shanten.
                            if removed_straight_hand.shape[0] == 1:
                                found_combo = True
                            if removed_straight_hand.shape[0] == 2:
                                if removed_straight_hand[0] == removed_straight_hand[1]:
                                    return 0
                                else:
                                    found_combo = True
        if found_combo:
            return 1

        found_one_potential_combo = False
        for i in range(self._player_hand.shape[0] - 1):
            # Avoid duplicate initial tile.
            if i > 0 and self._player_hand[i] == self._player_hand[i - 1]:
                continue
            tile_i = self._player_hand[i]
            temp_hand = self._player_hand.copy()
            temp_hand = np.delete(temp_hand, i)
            for j in range(len(temp_hand)):
                tile_j = temp_hand[j]
                if tile_i <= 9 < tile_j or tile_i > 9 >= tile_j:
                    # Break the loop if the suit does not match.
                    break
                if tile_i == tile_j + 1 or tile_i == tile_j - 1 or \
                        tile_i == tile_j + 2 or tile_i == tile_j - 2:
                    found_one_potential_combo = True
                    remove_one_hand = temp_hand.copy()
                    remove_one_hand = np.delete(remove_one_hand, j)
                    for i2 in range(remove_one_hand.shape[0] - 1):
                        for j2 in range(i2 + 1, remove_one_hand.shape[0]):
                            if remove_one_hand[i2] == remove_one_hand[j2]:
                                return 1
        if found_one_potential_combo:
            return 2
        else:
            for i in range(self._player_hand.shape[0] - 1):
                for j in range(i + 1, self._player_hand.shape[0]):
                    if self._player_hand[i] == self._player_hand[j]:
                        return 2
            return 3

    def get_player_discards(self):
        return self._player_discards

    def get_opponents_discards(self):
        return self._other_player_discards
