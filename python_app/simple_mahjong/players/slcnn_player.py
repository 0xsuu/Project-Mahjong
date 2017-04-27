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

from keras.models import load_model

from libgames import *
from libmahjong import *
from libplayers import *

from mahjong_hand_converter import *


class SLCNNPlayer(Player):
    def __init__(self, player_name):
        super(SLCNNPlayer, self).__init__(player_name)
        self.model = load_model("../../supervised_learning/cnn_model.h5")
        self.model.load_weights("../../supervised_learning/cnn_weights.h5")

    def on_turn(self, this, player_id, tile):
        if player_id == this.get_id():
            if this.get_hand().test_win():
                return Action(ActionState.Win, Tile())

            hand_data = this.get_hand().get_data()
            it = int(self.model.predict_classes(
                transform_one_hot_to_cnn_matrix(
                    transform_hand_to_one_hot(hand_data)), verbose=0)[0])

            return Action(ActionState.Discard, hand_data[it])
        else:
            return Action()

    def on_other_player_make_action(self, player_id, player_name, action):
        return Action()
