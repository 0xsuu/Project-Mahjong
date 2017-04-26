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
from utils.combination_calculator import get_combinations

TRAIN = 100
PLAY = 200
EVAL = 300
DEBUG = 400
ALL_COMBINATIONS = get_combinations()
COMBINATIONS_SIZE = len(ALL_COMBINATIONS)
Q_VALUES_FILE = "q_values.txt"
EPSILON = 0.01
LAMBDA = 0.1
ALPHA = 0.1
WIN_REWARD = 100
DISCARD_REWARD = -1


class QPlayer(Player):
    def __init__(self, name, mode):
        Player.__init__(self, name)
        self._mode = mode
        if os.path.isfile(Q_VALUES_FILE):
            self.all_q_values = np.loadtxt(Q_VALUES_FILE)
        else:
            self.all_q_values = np.array([[0.0, 0.0, 0.0, 0.0, 0.0]] * COMBINATIONS_SIZE)
            # self.all_q_values = np.array([np.random.uniform(-10, 10, 5)])
            # for i in range(COMBINATIONS_SIZE - 1):
            #     self.all_q_values = \
            #         np.append(self.all_q_values, [np.random.uniform(-10, 10, 5)], axis=0)
        self.current_episode = 0
        self.last_hand = None
        self.last_discard = None
        self.last_reward = None

    @staticmethod
    def _get_hand_index(hand):
        return ALL_COMBINATIONS.index(hand)

    def _epsilon_greedy_choose(self):
        if np.random.uniform(0, 1.0, 1)[0] < EPSILON and self._mode == TRAIN:
            self.last_discard = int(np.random.uniform(0, 5.0, 1)[0])
        else:
            q_values = self.all_q_values[self._get_hand_index(self.hand.tolist())]
            # Choose the maximum Q's index as a policy.
            self.last_discard = np.random.choice(
                np.array([i for i, j in enumerate(q_values) if j == max(q_values)]))
            if self._mode == DEBUG:
                print(self.name)
                print("Hand    : ", end="")
                for i in self.hand:
                    if i <= 9:
                        print("A" + str(int(i)), end="  ")
                    else:
                        print("B" + str(int(i - 9)), end="  ")
                print()
                print("Q values:", q_values, "\ndiscarding", self.last_discard)
                print()

        return self.last_discard

    def update_q_value(self, hand, action, reward, next_hand):
        hand_index = self._get_hand_index(hand.tolist())
        next_hand_index = self._get_hand_index(next_hand.tolist())
        self.all_q_values[hand_index][action] += \
            ALPHA * (reward + LAMBDA * max(self.all_q_values[next_hand_index]) -
                     self.all_q_values[hand_index][action])

    def initial_hand_obtained(self):
        Player.initial_hand_obtained(self)
        self.current_episode += 1
        self.last_hand = None
        self.last_discard = None
        self.last_reward = None

    def tile_picked(self):
        Player.tile_picked(self)

        if self.last_hand is not None:
            self.update_q_value(self.last_hand, self.last_discard, self.last_reward, self.hand)

        if self.test_win():
            self.last_reward = WIN_REWARD
            if self.last_hand is not None:
                self.update_q_value(self.last_hand, self.last_discard, self.last_reward, self.hand)
            return_action = WIN
            return_discard_tile = -1
        else:
            self.last_reward = DISCARD_REWARD
            return_action = DISCARD
            return_discard_tile = self._epsilon_greedy_choose()

        self.last_hand = self.hand
        return return_action, return_discard_tile

    def game_ends(self, win, drain=False):
        Player.game_ends(self, win, drain)
        if self._mode == TRAIN:
            if self.current_episode % 100 == 0:
                print("Finished", self.current_episode, "episodes.")
                if os.path.isfile(Q_VALUES_FILE):
                    print("Error since last save:",
                          sum((np.loadtxt(Q_VALUES_FILE) - self.all_q_values)[:, 1] ** 2))
                np.savetxt(Q_VALUES_FILE, self.all_q_values, fmt='%f')
        elif self._mode == PLAY:
            print(self.name + ":")
            if win:
                print("Won!")
            old_values = np.loadtxt(Q_VALUES_FILE)
            state_increase = len(np.argwhere(self.all_q_values[:, 0] != 0)) - \
                len(np.argwhere(old_values[:, 0] != 0))
            if state_increase > 0:
                print("New states:", state_increase)
            print("Value adjustment error:", sum((old_values[:, 1] - self.all_q_values[:, 1]) ** 2))
            np.savetxt(Q_VALUES_FILE, self.all_q_values, fmt='%f')
        elif self._mode == EVAL:
            print(self.name + ":")
            print("Win rate:", str(self.rounds_won * 100.0 / self.current_episode) + "%")
        elif self._mode == DEBUG:
            if win:
                print(self.name, "won!")
