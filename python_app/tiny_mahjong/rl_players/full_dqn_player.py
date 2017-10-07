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

from keras.models import Sequential
from keras.layers import Conv1D, Dense, Dropout, Flatten, MaxPooling1D
from keras.optimizers import Adam

from prioritised_double_dqn import PrioritisedDoubleDQN
from dqn_interface import *

from game import *

DQN_WEIGHTS_FILE = "tm_full_dqn_weights.h5"

WIN_REWARD = 1.0
DISCARD_REWARD = -0.01
LOSE_REWARD = -1.0

HAND_SIZE = 5

STATE_SIZE = 69  # TODO: replace with a more proper way of setting this variable.


class FullDDQNTinyMahjong(PrioritisedDoubleDQN):
    def __init__(self, mode, load=True):
        PrioritisedDoubleDQN.__init__(self, action_count=5, weights_file_path=DQN_WEIGHTS_FILE,
                                      replay_memory_size=1000000, mode=mode,
                                      target_update_interval=10000, load_previous_model=load)

    @staticmethod
    def _pre_process(input_data):
        return input_data.reshape(1, STATE_SIZE, 1)

    @staticmethod
    def _create_model(input_shape=None, action_count=None):
        model = Sequential()
        model.add(Conv1D(input_shape=(STATE_SIZE, 1),
                         filters=32,
                         kernel_size=3,
                         padding="same",
                         activation="relu"))
        model.add(Conv1D(filters=64,
                         kernel_size=3,
                         padding="same",
                         activation="relu"))
        model.add(MaxPooling1D())
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(256, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(5))

        model.compile(loss='mean_squared_error',
                      optimizer=Adam(lr=0.00025),
                      metrics=['accuracy'])

        return model


class FullDQNPlayer(Player):
    def __init__(self, name, mode):
        Player.__init__(self, name)
        self._mode = mode

        self._dqn_model = FullDDQNTinyMahjong(mode)

        self._prev_state = None
        self._prev_action = None

        self._drain_rounds = 0

        self._total_rounds = 0

    def initial_hand_obtained(self):
        Player.initial_hand_obtained(self)
        self._prev_state = None
        self._prev_action = None

        self._total_rounds += 1

    def tile_picked(self):
        Player.tile_picked(self)
        training = self._prev_state is not None and self._mode == TRAIN
        if self.test_win():
            if training:
                self._dqn_model.notify_reward(WIN_REWARD)
                self._dqn_model.append_memory_and_train(self._prev_state,
                                                        self._prev_action,
                                                        WIN_REWARD,
                                                        self.game_state.get(),
                                                        True)
            return WIN, -1
        else:
            action = self._dqn_model.make_action(self.game_state.get())
            if training:
                self._dqn_model.notify_reward(DISCARD_REWARD)
                self._dqn_model.append_memory_and_train(self._prev_state,
                                                        self._prev_action,
                                                        DISCARD_REWARD,
                                                        self.game_state.get(),
                                                        False)
            self._prev_state = self.game_state.get()
            self._prev_action = action
            return DISCARD, action

    def player_discarded(self, discarded_tile):
        training = self._prev_state is not None and self._mode == TRAIN
        if self.test_win_hand(self.hand, discarded_tile):
            if training:
                self._dqn_model.notify_reward(WIN_REWARD)
                temp_state = self.game_state.get()
                temp_state[4] = 0
                self._dqn_model.append_memory_and_train(self._prev_state,
                                                        self._prev_action,
                                                        WIN_REWARD,
                                                        temp_state,
                                                        True)
            return WIN
        else:
            return PASS

    def game_ends(self, win, lose, self_win=False, drain=False):
        Player.game_ends(self, win, lose, drain)

        if lose:
            training = self._prev_state is not None and self._mode == TRAIN
            if training:
                if self_win:
                    final_reward = LOSE_REWARD
                else:
                    final_reward = LOSE_REWARD
                # print(final_reward, self._prev_action, "\n", self._prev_state, "\n", self.game_state.get(), "\n")
                self._dqn_model.notify_reward(final_reward)
                self._dqn_model.append_memory_and_train(self._prev_state,
                                                        self._prev_action,
                                                        final_reward,
                                                        self.game_state.get(),
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
