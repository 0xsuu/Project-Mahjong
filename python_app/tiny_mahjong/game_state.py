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
FULL_HAND_COUNT = INITIAL_HAND_COUNT + 1
FULL_DISCARD_COUNT = int((TILE_STACK_COUNT - PLAYER_COUNT * INITIAL_HAND_COUNT) / PLAYER_COUNT)
ADDITIONAL_FEATURES = 5


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

        self._disclose_all = disclose_all

    def copy(self):
        copy_object = GameState(None, self._disclose_all)
        if self._player_hand is not None:
            copy_object._player_hand = self._player_hand.copy()
        if self._opponents_hands is not None:
            copy_object._opponents_hands = self._opponents_hands.copy()
        copy_object._player_discards = self._player_discards.copy()
        copy_object._other_player_ids = self._other_player_ids.copy()
        for player_id in copy_object._other_player_ids:
            copy_object._other_player_discards[player_id] = self._other_player_discards[player_id].copy()
        return copy_object

    def calc_expectation_one_lookahead(self, model, action):
        expectation = 0.0
        for i in range(1, 18 + 1):
            new_state = self.copy()
            new_state._player_hand[action] = i
            new_state._player_hand = np.sort(new_state._player_hand)
            new_state._player_discards.append(i)
            transition_probability = new_state.calc_tile_distribution(new_state.calc_tile_count()[1:])[i - 1]
            if transition_probability == 0:
                continue
            state_value = np.max(model.predict_q_values(new_state))
            expectation += new_state.calc_tile_distribution(new_state.calc_tile_count()[1:])[i - 1] * state_value
        return expectation

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

        # Append shanten number and tenpai count if in tenpai state.
        result = np.append(result, np.array(self.calc_shanten_tenpai_tiles(self._player_hand)[:2]))
        # Append count for tiles left in tile stack.
        result = np.append(result, np.array([np.sum(self.calc_tile_count()[1:]) - FULL_HAND_COUNT]))
        # Append major suit's tile count.
        result = np.append(result, np.array([self.calc_major_suit_count()]))
        # Append 2-8 tile count.
        result = np.append(result, np.array([self.calc_two_to_eight_count()]))

        # Append tile stack counts.
        # tile_count = self.calc_tile_count()[1:]
        # tile_not_appeared = np.argwhere(tile_count == 4)
        # result = np.append(result, tile_not_appeared)
        # result = np.append(result, np.array([0] * (18 - tile_not_appeared.shape[0])))

        # Append player's discards.
        result = np.append(result, self._player_discards)

        # Fill up 0s for non-full games. i.e. use fixed size input, thus the maximum number of discards are used.
        result = np.append(result, np.zeros((FULL_DISCARD_COUNT - len(self._player_discards),)))

        # If the disclose option is enabled, append opponents' hands.
        if self._disclose_all:
            result = np.append(result, self._opponents_hands.copy)

        # Append opponents' discards and fill up with 0s.
        for p in self._other_player_discards:
            result = np.append(result, self._other_player_discards[p])
            result = np.append(result, np.zeros((FULL_DISCARD_COUNT - len(self._other_player_discards[p]),)))

        # Check state size.
        other_players_count = len(self._other_player_ids)
        assert result.shape[0] == (other_players_count + 1) * FULL_DISCARD_COUNT + FULL_HAND_COUNT + \
            self._disclose_all * other_players_count * 5 + ADDITIONAL_FEATURES

        return result

    def get_player_hand(self):
        return self._player_hand

    def get_opponents_hands(self):
        return self._opponents_hands

    def get_opponents_discards(self):
        return self._other_player_discards

    def calc_shanten_tenpai_tiles(self, hand):
        """
        :return: Shanten, Tenpai count, Tenpai tiles(only applies to four tiles hand).
        """
        tile_count = self.calc_tile_count(disclose=self._disclose_all)

        player_hand = hand.copy()
        if 0 in player_hand:
            player_hand = np.delete(player_hand, np.argwhere(player_hand == 0))

        # Try remove the combo first.
        found_combo = False
        sum_tenpai = 0
        sum_tenpai_tiles = []
        for i in range(player_hand.shape[0] - 2):
            # Avoid duplicate initial tile.
            if i > 0 and player_hand[i] == player_hand[i - 1]:
                continue
            if player_hand[i] == player_hand[i + 1] and player_hand[i + 1] == player_hand[i + 2]:
                removed_trio_hand = player_hand.copy()
                removed_trio_hand = np.delete(removed_trio_hand, i + 2)
                removed_trio_hand = np.delete(removed_trio_hand, i + 1)
                removed_trio_hand = np.delete(removed_trio_hand, i)
                # If a trio is removed, we can derive the shanten directly.
                if removed_trio_hand.shape[0] == 1:
                    return 1, tile_count[int(removed_trio_hand[0])], [int(removed_trio_hand[0])]
                if removed_trio_hand.shape[0] == 2:
                    if removed_trio_hand[0] == removed_trio_hand[1]:
                        return 0, np.sum(tile_count[1:]), []
                    else:
                        tenpai_count = max(tile_count[int(removed_trio_hand[0])], tile_count[int(removed_trio_hand[1])])

                        return 1, tenpai_count, []
            for j in range(i + 1, player_hand.shape[0] - 1):
                if player_hand[i] <= 9 < player_hand[j] or player_hand[i] > 9 >= player_hand[j]:
                    # Break the loop if the suit does not match.
                    break
                if player_hand[i] == player_hand[j] - 1:
                    for k in range(j + 1, player_hand.shape[0]):
                        if player_hand[j] <= 9 < player_hand[k] or \
                                                player_hand[j] > 9 >= player_hand[k]:
                            # Break the loop if the suit does not match.
                            break
                        if player_hand[j] == player_hand[k] - 1:
                            removed_straight_hand = player_hand.copy()
                            removed_straight_hand = np.delete(removed_straight_hand, k)
                            removed_straight_hand = np.delete(removed_straight_hand, j)
                            removed_straight_hand = np.delete(removed_straight_hand, i)
                            # If a trio is removed, we can find the minimum shanten.
                            if removed_straight_hand.shape[0] == 1:
                                if int(removed_straight_hand[0]) not in sum_tenpai_tiles:
                                    sum_tenpai += tile_count[int(removed_straight_hand[0])]
                                    sum_tenpai_tiles.append(int(removed_straight_hand[0]))
                                found_combo = True
                            if removed_straight_hand.shape[0] == 2:
                                if removed_straight_hand[0] == removed_straight_hand[1]:
                                    return 0, np.sum(tile_count[1:]), []
                                else:
                                    sum_tenpai += \
                                        max(tile_count[int(removed_straight_hand[0])],
                                            tile_count[int(removed_straight_hand[1])])
                                    found_combo = True

        found_one_potential_combo = False
        found_two_potential_combo = False
        max_return_tenpai = -1
        max_tenpai_tiles = []
        for i in range(player_hand.shape[0] - 1):
            # Avoid duplicate initial tile.
            if i > 0 and player_hand[i] == player_hand[i - 1]:
                continue
            tile_i = player_hand[i]
            for j in range(i + 1, player_hand.shape[0]):
                tile_j = player_hand[j]
                if tile_i <= 9 < tile_j or tile_i > 9 >= tile_j:
                    # Break the loop if the suit does not match.
                    break
                if tile_i == tile_j + 1 or tile_i == tile_j - 1 or \
                                tile_i == tile_j + 2 or tile_i == tile_j - 2 or tile_i == tile_j:
                    found_one_potential_combo = True
                    remove_one_hand = player_hand.copy()
                    remove_one_hand = np.delete(remove_one_hand, j)
                    remove_one_hand = np.delete(remove_one_hand, i)
                    for i2 in range(remove_one_hand.shape[0] - 1):
                        for j2 in range(i2 + 1, remove_one_hand.shape[0]):
                            if remove_one_hand[i2] == remove_one_hand[j2]:
                                found_two_potential_combo = True
                                return_tenpai = None
                                tenpai_tiles = None
                                if tile_i == tile_j + 2:
                                    return_tenpai = tile_count[int(tile_i) - 1]
                                    tenpai_tiles = [int(tile_i) - 1]
                                elif tile_i == tile_j - 2:
                                    return_tenpai = tile_count[int(tile_i) + 1]
                                    tenpai_tiles = [int(tile_i) + 1]
                                elif tile_i == tile_j + 1:
                                    return_tenpai = 0
                                    tenpai_tiles = []
                                    if tile_i != 1 and tile_i != 9 and tile_i != 10 and tile_i != 18:
                                        return_tenpai += tile_count[int(tile_i) + 1]
                                        tenpai_tiles.append(int(tile_i) + 1)
                                    if tile_j != 1 and tile_j != 9 and tile_j != 10 and tile_j != 18:
                                        return_tenpai += tile_count[int(tile_j) - 1]
                                        tenpai_tiles.append(int(tile_j) - 1)
                                elif tile_i == tile_j - 1:
                                    return_tenpai = 0
                                    tenpai_tiles = []
                                    if tile_j != 1 and tile_j != 9 and tile_j != 10 and tile_j != 18:
                                        return_tenpai += tile_count[int(tile_j) + 1]
                                        tenpai_tiles.append(int(tile_j) + 1)
                                    if tile_i != 1 and tile_i != 9 and tile_i != 10 and tile_i != 18:
                                        return_tenpai += tile_count[int(tile_i) - 1]
                                        tenpai_tiles.append(int(tile_i) - 1)
                                elif tile_i == tile_j:
                                    return_tenpai = tile_count[int(tile_i)] + tile_count[int(remove_one_hand[i2])]
                                    tenpai_tiles = [int(tile_i), int(remove_one_hand[i2])]
                                if return_tenpai > max_return_tenpai:
                                    max_return_tenpai = return_tenpai
                                    if player_hand.shape[0] == 4:
                                        max_tenpai_tiles = tenpai_tiles
        if found_two_potential_combo:
            if found_combo:
                if max_return_tenpai > sum_tenpai:
                    return 1, max_return_tenpai, max_tenpai_tiles
                else:
                    return 1, sum_tenpai, sum_tenpai_tiles
            else:
                return 1, max_return_tenpai, max_tenpai_tiles
        if found_combo:
            return 1, sum_tenpai, sum_tenpai_tiles
        if found_one_potential_combo:
            return 2, 0, []
        else:
            for i in range(player_hand.shape[0] - 1):
                for j in range(i + 1, player_hand.shape[0]):
                    if player_hand[i] == player_hand[j]:
                        return 2, 0, []
            return 3, 0, []

    def calc_discarded_tile_count(self):
        tile_count = np.array([4] * 19)
        tile_count[0] = -123456789  # A large number made easier for debugging.
        for i in self._player_discards:
            tile_count[int(i)] -= 1
        for i in self._other_player_discards.values():
            for j in i:
                tile_count[int(j)] -= 1
        return tile_count

    def calc_tile_count(self, disclose=False):
        """ Return 19 integers where the index 0 is invalid. """
        tile_count = np.array([4] * 19)
        tile_count[0] = -123456789  # A large number made easier for debugging.
        for i in self._player_hand:
            tile_count[int(i)] -= 1
        if disclose:
            for i in self._opponents_hands:
                tile_count[int(i)] -= 1
        for i in self._player_discards:
            tile_count[int(i)] -= 1
        for i in self._other_player_discards.values():
            for j in i:
                tile_count[int(j)] -= 1
        return tile_count

    def calc_major_suit_count(self):
        major_suit_count = 0
        for i in self._player_hand:
            if i <= 9:
                major_suit_count += 1
        if major_suit_count < int(self._player_hand.shape[0] / 2):
            major_suit_count = self._player_hand.shape[0]

        return major_suit_count

    def calc_two_to_eight_count(self):
        count = 0
        for i in self._player_hand:
            if i != 0 and i != 9 and i != 10 and i != 18:
                count += 1

        return count

    @staticmethod
    def calc_tile_distribution(tile_count):
        """ Take the 18 integer list. """
        return tile_count * 1.0 / np.sum(tile_count)

    @staticmethod
    def suit_shift(tiles):
        tiles[np.argwhere(tiles > 9)] += 11
        return tiles

    def get_player_discards(self):
        return self._player_discards

    def process_dangerousness_input(self):
        processed_inputs = []

        # Get tile probability distribution.
        tile_distribution = self.calc_discarded_tile_count()[1:]
        processed_inputs += tile_distribution.tolist()

        # Calculate tiles left and A/B ratio.
        opponents_and_discards = self.get_opponents_discards()
        opponent_discards = []
        for p in opponents_and_discards:
            opponent_discards = opponents_and_discards[p]
            break
        tiles_left = np.sum(self.calc_tile_count()[1:])
        a_ratio = 0
        b_ratio = 0
        for t in opponent_discards:
            if t <= 9:
                a_ratio += 1
            else:
                b_ratio += 1
        opponent_discard_length = len(opponent_discards)
        if opponent_discard_length == 0:
            return []
        a_ratio /= opponent_discard_length
        b_ratio /= opponent_discard_length

        processed_inputs.append(tiles_left)
        processed_inputs.append(a_ratio)
        processed_inputs.append(b_ratio)

        # Get last five discards.
        if opponent_discard_length < 5:
            copy_discards = opponent_discards.copy()
            for i in range(5 - opponent_discard_length):
                copy_discards.insert(0, 0)
            processed_inputs += copy_discards[-5:]
        else:
            processed_inputs += opponent_discards[-5:]

        return processed_inputs
