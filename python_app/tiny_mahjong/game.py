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
import random
from sklearn.utils import shuffle

TILE_SET = np.array(
    [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3,
        4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6,
        7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
        10, 10, 10, 10, 11, 11, 11, 11,
        12, 12, 12, 12, 13, 13, 13, 13,
        14, 14, 14, 14, 15, 15, 15, 15,
        16, 16, 16, 16, 17, 17, 17, 17,
        18, 18, 18, 18])

WIN = 6666
DISCARD = 1111


class Player:
    def __init__(self, name):
        assert name != ""
        self.name = name
        self.hand = np.array([])

    def initial_hand_obtained(self):
        pass

    def tile_picked(self):
        pass

    def game_ends(self, win, drain=False):
        pass

    def test_win(self):
        for i in range(len(self.hand)-1):
            if self.hand[i] == self.hand[i+1]:
                copy_hand = np.copy(self.hand)
                copy_hand = np.delete(copy_hand, [i, i+1])
                if (copy_hand[0] <= 9 and copy_hand[1] <= 9 and copy_hand[2] <= 9) or \
                        (copy_hand[0] > 9 and copy_hand[1] > 9 and copy_hand[2] > 9):
                    if (copy_hand[0] == copy_hand[1] and copy_hand[1] == copy_hand[2]) or \
                            (copy_hand[0] == copy_hand[1]-1 and copy_hand[1] == copy_hand[2]-1):
                                return True
        return False

    def insert(self, tile):
        self.hand = np.append(self.hand, tile)
        self.sort_hand()

    def sort_hand(self):
        self.hand = np.sort(self.hand)


class Game:
    def __init__(self, round_count, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.round_count = round_count
        self.current_round = 0
        self.tiles = None
        self.start_player = None
        self.current_player = None

    def setup(self):
        self.tiles = shuffle(np.copy(TILE_SET), random_state=0)
        self.start_player = random.choice([self.player1, self.player2])
        self.current_player = self.start_player

        self.player1.hand = np.array([])
        self.player2.hand = np.array([])
        for i in range(5):
            self.player1.hand = np.append(self.player1.hand, self.tiles[0])
            self.tiles = np.delete(self.tiles, 0)
            self.player2.hand = np.append(self.player2.hand, self.tiles[0])
            self.tiles = np.delete(self.tiles, 0)
        self.player1.sort_hand()
        self.player2.sort_hand()
        self.player1.initial_hand_obtained()
        self.player2.initial_hand_obtained()

    def next_player(self):
        if self.current_player == self.player1:
            return self.player2
        else:
            return self.player1

    def play_round(self):
        self.setup()
        while True:
            self.current_player.insert(self.tiles[0])
            self.tiles = np.delete(self.tiles, 0)
            action, index = self.current_player.tile_picked()
            if action == WIN:
                self.current_player.game_ends(True)
                self.next_player().game_ends(False)
                return self.current_player.name
            elif action == DISCARD:
                self.current_player.hand = \
                    np.delete(self.current_player.hand, index)
            if len(self.tiles) == 0:
                self.player1.game_ends(False, drain=True)
                self.player2.game_ends(False, drain=True)
                return ""
            self.current_player = self.next_player()

    def play(self):
        counter = {self.player1.name: 0, self.player2.name: 0, "": 0}
        for i in range(self.round_count):
            print("Current Round:", self.current_round)
            counter[self.play_round()] += 1
            self.current_round += 1
        print(self.player1.name + "'s win rate: " + str(counter[self.player1.name] / self.round_count) + "%")
        print(self.player2.name + "'s win rate: " + str(counter[self.player2.name] / self.round_count) + "%")
