#!/usr/bin/env python

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

# Mahjong lib imports.
from libgames import *
from libmahjong import *
from libplayers import *

from double_dqn import DoubleDQN
from dqn_interface import *
from mahjong_hand_converter import *
from model_generator import simple_mahjong_dqn_model

DQCNN_WEIGHTS_FILE = "sm_dqcnn_weights.h5"

DRAIN_REWARD = 0.0
DISCARD_REWARD = 0.0
LOSE_REWARD = -1.0
SAFE_REWARD = 0.1
WIN_REWARD = 1.0


class DQNSimpleMahjong(DoubleDQN):
    def __init__(self, mode, load=True):
        DoubleDQN.__init__(self, action_count=14, weights_file_path=DQCNN_WEIGHTS_FILE,
                           mode=mode, load_previous_model=load)

    @staticmethod
    def _pre_process(input_data):
        return transform_one_hot_to_cnn_matrix(transform_hand_to_one_hot(input_data))

    @staticmethod
    def _create_model(input_shape=None, action_count=None):
        return simple_mahjong_dqn_model()


class DQCNNPlayer(Player):
    def __init__(self, name, mode):
        super(DQCNNPlayer, self).__init__(name)
        self._mode = mode

        self._dqn_model = DQNSimpleMahjong(mode)

        self._last_hand = None
        self._last_discard = None
        self._reward = None
        self._this_hand = None
        self._done = None
        self.is_discard = False

        self._win_rounds = 0
        self._lost_rounds = 0
        self._drain_rounds = 0
        self._total_rounds = 0

    def on_turn(self, this, player_id, tile):
        if player_id == this.get_id():
            self._this_hand = list(this.get_hand().get_data())
            # Process result of last discard.
            if self._last_hand is not None and self._mode == TRAIN:
                self._reward = DISCARD_REWARD
                self._done = False
                self._dqn_model.notify_reward(self._reward)
                self._dqn_model.append_memory_and_train(self._last_hand,
                                                        self._last_discard,
                                                        self._reward,
                                                        self._this_hand,
                                                        self._done)
            # Test if hand can win.
            if this.get_hand().test_win():
                # Player win.
                self._reward = WIN_REWARD
                self._done = True
                self.game_ends(True, False)
                return Action(ActionState.Win, Tile())
            else:
                it = self._dqn_model.make_action(
                    this.get_hand().get_data())
                self.is_discard = True
                self._last_hand = self._this_hand
                self._last_discard = it
                return Action(ActionState.Discard, self._this_hand[it])
        else:
            return Action()

    def on_other_player_make_action(self, this, player_id, player_name, action):
        # Tile stack drained.
        if player_id == -1 and player_name == "":
            self._reward = DRAIN_REWARD
            self._done = True
            self.game_ends(False, False, True)
            return Action()

        if action.get_action_state() == ActionState.Win:
            if self.is_discard:
                # Player lost.
                self._reward = LOSE_REWARD
                self._done = True
                self.game_ends(False, True)
            else:
                # Player safe.
                self._reward = SAFE_REWARD
                self._done = True
                self.game_ends(False, False)
        elif action.get_action_state() == ActionState.Discard:
            if this.get_hand().test_win(action.get_tile()):
                # Player win.
                self._reward = WIN_REWARD
                self._done = True
                self.game_ends(True, False)
                return Action(ActionState.Win, action.get_tile())
        else:
            self.is_discard = False

        return Action()

    def game_ends(self, win, lose, drain=False):
        self._total_rounds += 1
        if win:
            self._win_rounds += 1
        if lose:
            self._lost_rounds += 1
        if drain:
            self._drain_rounds += 1

        if self._last_hand is not None and self._mode == TRAIN:
            assert self._last_discard is not None
            assert self._reward is not None
            assert self._this_hand is not None
            assert self._done is not None
            self._dqn_model.notify_reward(self._reward)
            self._dqn_model.append_memory_and_train(self._last_hand,
                                                    self._last_discard,
                                                    self._reward,
                                                    self._this_hand,
                                                    self._done)

        # Summary.
        if self._mode == TRAIN:
            self._dqn_model.episode_finished({
                "Win rate": float(self._win_rounds) / self._total_rounds,
                "Lose rate": float(self._lost_rounds) / self._total_rounds,
                "Drain rate": float(self._drain_rounds) / self._total_rounds
            })

        # Reset.
        self.is_discard = False
        self._last_hand = None
        self._last_discard = None
        self._reward = None
        self._this_hand = None
        self._done = None
        self.is_discard = False
