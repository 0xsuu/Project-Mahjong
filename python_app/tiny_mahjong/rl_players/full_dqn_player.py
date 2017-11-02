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
from keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from keras.optimizers import Adam
from keras import backend

from resnet import *

from prioritised_double_dqn import PrioritisedDoubleDQN
from dqn_interface import *

from game import *

DQN_WEIGHTS_FILE = "tm_full_dqn_weights.h5"

WIN_REWARD = 1.0
DISCARD_REWARD = -0.01
LOSE_REWARD = -1.0

HAND_SIZE = 5

# 74 for disclosed, 69 for non-disclosed.
STATE_SIZE = 69  # TODO: replace with a more proper way of setting this variable.


class FullDDQNTinyMahjong(PrioritisedDoubleDQN):
    def __init__(self, mode, load=True):
        PrioritisedDoubleDQN.__init__(self, action_count=5, weights_file_path=DQN_WEIGHTS_FILE,
                                      replay_memory_size=1000000, mode=mode,
                                      target_update_interval=10000, load_previous_model=load)

    @staticmethod
    def _pre_process(input_data):
        """
        NOTE: ONLY FOR DUAL MAHJONG.

        Final shape will be (1, 7, 11, 11).
        Each tile is encoded into suit(2 bits one-hot) following by number(9 bits one-hot).
        The first frame is player's hand.
        The last 6 frames are players' and opponents' discards.
        """
        processed_features = np.zeros([7, 11, 11], dtype=np.int)

        # Set the hand.
        index = 0
        for tile in input_data.get_player_hand():
            processed_features[0][index] = FullDDQNTinyMahjong._encode_tile(tile)
            index += 1

        # Set player discards.
        index = 0
        page = 1
        for tile in input_data.get_player_discards():
            processed_features[page][index] = FullDDQNTinyMahjong._encode_tile(tile)
            if index >= 10:
                index = 0
                page += 1
            else:
                index += 1

        # Set opponent discards.
        index = 0
        page = 4
        opponents_discards = input_data.get_opponents_discards()
        assert len(opponents_discards) == 1
        discards = None
        for i in opponents_discards.values():
            discards = i
        for tile in discards:
            processed_features[page][index] = FullDDQNTinyMahjong._encode_tile(tile)
            if index >= 10:
                index = 0
                page += 1
            else:
                index += 1
        return processed_features.reshape(1, 7, 11, 11)

    @staticmethod
    def _create_model(input_shape=None, action_count=None):
        backend.set_image_dim_ordering("th")
        # model = Sequential()
        # model.add(Conv2D(filters=32,
        #                  input_shape=(7, 11, 11),
        #                  kernel_size=(3, 3),
        #                  padding="same",
        #                  activation="relu"))
        # model.add(Conv2D(filters=64,
        #                  kernel_size=(3, 3),
        #                  padding="same",
        #                  activation="relu"))
        # model.add(MaxPooling2D())
        # model.add(Dropout(0.25))
        #
        # model.add(Flatten())
        # model.add(Dense(256, activation="relu"))
        # model.add(Dropout(0.5))
        # model.add(Dense(5))
        #
        model = ResnetBuilder.build_resnet_18((7, 11, 11), 5)

        model.compile(loss='mean_squared_error',
                      optimizer=Adam(lr=0.00025),
                      metrics=['accuracy'])

        return model

    @staticmethod
    def _encode_tile(tile):
        tile = int(tile)
        result = [0] * 11
        if tile > 9:
            result[1] = 1
            tile -= 9
        else:
            result[0] = 1

        result[tile + 1] = 1
        return result


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
                                                        self.game_state,
                                                        True)
            return WIN, -1
        else:
            action = self._dqn_model.make_action(self.game_state)
            if training:
                self._dqn_model.notify_reward(DISCARD_REWARD)
                self._dqn_model.append_memory_and_train(self._prev_state,
                                                        self._prev_action,
                                                        DISCARD_REWARD,
                                                        self.game_state,
                                                        False)
            self._prev_state = self.game_state
            self._prev_action = action
            return DISCARD, action

    def player_discarded(self, discarded_tile):
        training = self._prev_state is not None and self._mode == TRAIN
        if self.test_win_hand(self.hand, discarded_tile):
            if training:
                self._dqn_model.notify_reward(WIN_REWARD)
                # Hand only has 4 tiles at this stage.
                self._dqn_model.append_memory_and_train(self._prev_state,
                                                        self._prev_action,
                                                        WIN_REWARD,
                                                        self.game_state,
                                                        True)
            return WIN
        else:
            return PASS

    def game_ends(self, win, lose, self_win=False, drain=False):
        Player.game_ends(self, win, lose, self_win, drain)

        if lose:
            training = self._prev_state is not None and self._mode == TRAIN
            if training:
                if self_win:
                    final_reward = LOSE_REWARD / 2
                else:
                    final_reward = LOSE_REWARD
                # print(final_reward, self._prev_action, "\n", self._prev_state, "\n", self.game_state.get(), "\n")
                self._dqn_model.notify_reward(final_reward)
                self._dqn_model.append_memory_and_train(self._prev_state,
                                                        self._prev_action,
                                                        final_reward,
                                                        self.game_state,
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
                if self_win:
                    print(self.name, "self win!")
                else:
                    print(self.name, "win on discard!")
            elif lose:
                if self_win:
                    print(self.name, "lose, opponent self win.")
                else:
                    print(self.name, "lose, opponent win on this discard.")
            else:
                print("Tile stack drained.")
