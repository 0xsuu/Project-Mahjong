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

from game import *
import os.path
import pymp
from utils.combination_calculator import get_combinations

TRAIN = 100
PLAY = 200
EVAL = 300
DEBUG = 400
ALL_COMBINATIONS = get_combinations()
COMBINATIONS_SIZE = len(ALL_COMBINATIONS)
MC_VALUES_FILE = "mc_values.txt"
EPSILON = 0.01
GAMMA = 0.1
WIN_REWARD = 100
DISCARD_REWARD = -1


class MCPlayer(Player):
    def __init__(self, name, mode):
        Player.__init__(self, name)
        self._mode = mode
        if os.path.isfile(MC_VALUES_FILE):
            self.values = np.loadtxt("mc_values.txt")
        else:
            self.values = np.array([[0, 0]] * COMBINATIONS_SIZE)
        self.current_episode = 0
        self.hand_tuple_visits = {}
        self.gain = 0.0

    @staticmethod
    def _get_hand_index(hand):
        return ALL_COMBINATIONS.index(hand)

    def _get_hand_value(self, hand):
        return self.values[self._get_hand_index(hand.tolist())][1]

    def _epsilon_greedy_choose(self):
        if np.random.uniform(0, 1.0, 1)[0] < EPSILON and self._mode == TRAIN:
            return int(np.random.uniform(0, 5.0, 1)[0])
        else:
            q_values = pymp.shared.array((5, ), dtype="float16")
            with pymp.Parallel(5) as p:
                for i in p.range(5):
                    discarded_hand = np.delete(self.hand, i)
                    max_reward = DISCARD_REWARD
                    for picked_tile in range(1, 19):
                        if not self.has_tile_in_stack(picked_tile):
                            continue
                        picked_hand = np.append(discarded_hand, picked_tile)
                        picked_hand.sort()
                        if self.test_win_hand(picked_hand):
                            max_reward = WIN_REWARD
                        q_values[i] += self.get_pick_tile_probability(picked_tile) * \
                            self._get_hand_value(picked_hand)
                    q_values[i] += max_reward
            # Choose the maximum Q's index as a policy.
            choice = np.random.choice(np.array([i for i, j in enumerate(q_values) if j == max(q_values)]))
            if self._mode == DEBUG:
                print(self.name)
                print("Hand    : ", end="")
                for i in self.hand:
                    if i <= 9:
                        print("A" + str(int(i)), end="  ")
                    else:
                        print("B" + str(int(i - 9)), end="  ")
                print()
                print("Current value:", self._get_hand_value(self.hand))
                print("Q values:", q_values, "\ndiscarding", choice)
                print()
            return choice

    def initial_hand_obtained(self):
        Player.initial_hand_obtained(self)
        self.current_episode += 1
        self.hand_tuple_visits = {}
        self.gain = 0.0

    def tile_picked(self):
        Player.tile_picked(self)
        if tuple(self.hand.tolist()) in self.hand_tuple_visits.keys():
            self.hand_tuple_visits[tuple(self.hand.tolist())] += 1
        else:
            self.hand_tuple_visits[tuple(self.hand.tolist())] = 1
        if self.test_win():
            self.gain = WIN_REWARD
            return WIN, -1
        else:
            self.gain = DISCARD_REWARD + GAMMA * self.gain
            return DISCARD, self._epsilon_greedy_choose()

    def game_ends(self, win, drain=False):
        Player.game_ends(self, win, drain)
        for visited_hand_tuple in self.hand_tuple_visits:
            index = self._get_hand_index(list(visited_hand_tuple))
            last_count = self.values[index][0]
            last_average = self.values[index][1]
            occurrence_count = self.hand_tuple_visits[visited_hand_tuple]
            self.values[index][0] += occurrence_count
            self.values[index][1] += occurrence_count / (last_count + occurrence_count) * (self.gain - last_average)
        if self._mode == TRAIN:
            if self.current_episode % 10 == 0:
                print("Finished", self.current_episode, "episodes.")
                print("State Coverage:",
                      str(len(np.argwhere(self.values[:, 0] != 0)) * 100.0 / COMBINATIONS_SIZE) + "%")
                print("Error since last save:", sum((np.loadtxt("mc_values.txt") - self.values)[:, 1] ** 2))
                np.savetxt(MC_VALUES_FILE, self.values, fmt='%f')
        elif self._mode == PLAY:
            print(self.name + ":")
            old_values = np.loadtxt("mc_values.txt")
            state_increase = len(np.argwhere(self.values[:, 0] != 0)) - len(np.argwhere(old_values[:, 0] != 0))
            if state_increase > 0:
                print("New states:", state_increase)
            print("Value adjustment error:", sum((old_values[:, 1] - self.values[:, 1]) ** 2))
            np.savetxt(MC_VALUES_FILE, self.values, fmt='%f')
        elif self._mode == EVAL:
            print(self.name + ":")
            print("Win rate:", str(self.rounds_won * 100.0 / self.current_episode) + "%")
        elif self._mode == DEBUG:
            if win:
                print(self.name, "won!")
