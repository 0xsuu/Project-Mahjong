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

from adft_player import *
from random_player import *
from ui_player import *
from rl_players.mcnn_player import *
from rl_players.mc_player import *
from rl_players.q_player import *
from rl_players.dqn_player import *


def main():
    player1 = RandomPlayer("Smart Human")
    player2 = RandomPlayer("Q BOT 1")
    player3 = DQNPlayer("DQN BOT TRAIN", TRAIN)
    player4 = DQNPlayer("DQN BOT SELF_PLAY", SELF_PLAY)

    game = Game(1, [player1, player2, player3, player4])
    game.play()


if __name__ == "__main__":
    main()

