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
import numpy.random as random
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
        self.turn_count = 0
        self.average_turn = 0
        self.rounds_won = 0

    def initial_hand_obtained(self):
        assert len(self.hand) == 4
        self.turn_count = 0

    def tile_picked(self):
        assert len(self.hand) == 5
        self.turn_count += 1

    def game_ends(self, win, drain=False):
        if win:
            self.rounds_won += 1
            self.average_turn += 1/self.rounds_won * (self.turn_count - self.average_turn)

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
    def __init__(self, round_count, players):
        self.players = players
        self.round_count = round_count
        self.current_round = 0
        self.tiles = None
        self.start_player = None
        self.current_player = None

    def setup(self):
        self.tiles = shuffle(np.copy(TILE_SET))
        self.start_player = random.choice(self.players)
        self.current_player = self.start_player

        for player in self.players:
            player.hand = np.array([])
        for i in range(4):
            for player in self.players:
                player.hand = np.append(player.hand, self.tiles[0])
                self.tiles = np.delete(self.tiles, 0)
        for player in self.players:
            player.sort_hand()
            player.initial_hand_obtained()

    def next_player(self):
        index = self.players.index(self.current_player)
        if index >= len(self.players):
            index = 0
        return self.players[index]

    def play_round(self):
        self.setup()
        while True:
            self.current_player.insert(self.tiles[0])
            self.tiles = np.delete(self.tiles, 0)
            action, index = self.current_player.tile_picked()
            if action == WIN:
                self.current_player.hand = \
                    np.delete(self.current_player.hand, index)
                self.current_player.game_ends(True)
                self.next_player().game_ends(False)
                return self.current_player.name
            elif action == DISCARD:
                self.current_player.hand = \
                    np.delete(self.current_player.hand, index)
            if len(self.tiles) == 0:
                for player in self.players:
                    player.game_ends(False, drain=True)
                return ""
            self.current_player = self.next_player()

    def play(self):
        counter = {"": 0}
        for player in self.players:
            counter[player.name] = 0
        for i in range(self.round_count):
            print("Current Round:", self.current_round)
            counter[self.play_round()] += 1
            self.current_round += 1
        for player in self.players:
            print(player.name + "'s win rate: " + str(counter[player.name] / self.round_count * 100) + "%" +
                  ", average turn to win: " + str(player.average_turn))
