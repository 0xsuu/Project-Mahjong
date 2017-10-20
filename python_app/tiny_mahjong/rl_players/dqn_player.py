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

from model_generator import tiny_mahjong_dqn_model
from prioritised_double_dqn import PrioritisedDoubleDQN
from dqn_interface import *

from game import *

DQN_WEIGHTS_FILE = "tm_dqn_weights.h5"

WIN_REWARD = 1.0
DISCARD_REWARD = -0.01
LOSE_REWARD = -1.0

HAND_SIZE = 5


class DDQNTinyMahjong(PrioritisedDoubleDQN):
    def __init__(self, mode, load=True):
        PrioritisedDoubleDQN.__init__(self, action_count=5, weights_file_path=DQN_WEIGHTS_FILE,
                                      replay_memory_size=100000, mode=mode,
                                      target_update_interval=10000, load_previous_model=load)

    @staticmethod
    def _pre_process(input_data):
        assert len(input_data) == HAND_SIZE
        reshaped_input = np.array([[0] * 18] * 5)
        for tile_index in range(HAND_SIZE):
            tile = int(input_data[tile_index]) - 1
            if tile >= 0:
                reshaped_input[tile_index][tile] = 1
        reshaped_input = reshaped_input.reshape(1, 5, 18, 1)
        return reshaped_input

    @staticmethod
    def _create_model(input_shape=None, action_count=None):
        return tiny_mahjong_dqn_model()


class DQNPlayer(Player):
    def __init__(self, name, mode):
        Player.__init__(self, name)
        self._mode = mode

        self._dqn_model = DDQNTinyMahjong(mode)

        self._prev_hand = None
        self._prev_action = None

        self._drain_rounds = 0

        self._total_rounds = 0

    def initial_hand_obtained(self):
        Player.initial_hand_obtained(self)
        self._prev_hand = None
        self._prev_action = None

        self._total_rounds += 1

    def tile_picked(self):
        Player.tile_picked(self)
        training = self._prev_hand is not None and self._mode == TRAIN
        if self.test_win():
            if training:
                self._dqn_model.notify_reward(WIN_REWARD)
                self._dqn_model.append_memory_and_train(self._prev_hand,
                                                        self._prev_action,
                                                        WIN_REWARD,
                                                        self.hand,
                                                        True)
            return WIN, -1
        else:
            if training:
                self._dqn_model.notify_reward(DISCARD_REWARD)
            action = self._dqn_model.make_action(self.hand)
            if training:
                self._dqn_model.append_memory_and_train(self._prev_hand,
                                                        self._prev_action,
                                                        DISCARD_REWARD,
                                                        self.hand,
                                                        False)
            self._prev_hand = np.copy(self.hand)
            self._prev_action = action
            return DISCARD, action

    def player_discarded(self, discarded_tile):
        training = self._prev_hand is not None and self._mode == TRAIN
        if self.test_win_hand(self.hand, discarded_tile):
            if training:
                self._dqn_model.notify_reward(WIN_REWARD)
                self._dqn_model.append_memory_and_train(self._prev_hand,
                                                        self._prev_action,
                                                        WIN_REWARD,
                                                        np.append(self.hand, 0),
                                                        True)
            return WIN
        else:
            return PASS

    def game_ends(self, win, lose, self_win=False, drain=False):
        Player.game_ends(self, win, lose, self_win, drain)

        if lose:
            training = self._prev_hand is not None and self._mode == TRAIN
            if training:
                if self_win:
                    final_reward = DISCARD_REWARD
                else:
                    final_reward = LOSE_REWARD
                if self.hand.shape[0] == 4:
                    self.hand = np.append(self.hand, 0)
                self._dqn_model.notify_reward(final_reward)
                self._dqn_model.append_memory_and_train(self._prev_hand,
                                                        self._prev_action,
                                                        final_reward,
                                                        self.hand,
                                                        True)

        # Summary.
        if drain:
            self._drain_rounds += 1

        self._dqn_model.episode_finished({"Win rate":
                                          self.rounds_won * 1.0 / self._total_rounds,
                                          "Lose rate":
                                          self.rounds_lost * 1.0 / self._total_rounds,
                                          "Drain rate":
                                          self._drain_rounds * 1.0 / self._total_rounds})

        if self._mode == PLAY:
            print(self.name + ":")
            if win:
                print("Won!")
        elif self._mode == EVAL:
            print(self.name + ":")
            print("Win rate:", str(self.rounds_won * 100.0 / self._total_rounds) + "%, Lose rate:",
                  str(self.rounds_lost * 100.0 / self._total_rounds) + "%")
        elif self._mode == DEBUG:
            if win:
                print(self.name, "won!")
