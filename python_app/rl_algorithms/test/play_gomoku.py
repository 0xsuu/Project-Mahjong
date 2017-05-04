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

from gomoku_test import *


class GomokuEnvUI(GomokuEnv):
    def __init__(self, player_color, opponent, board_size, agent=None):
        GomokuEnv.__init__(self, player_color, opponent, board_size)
        self._agent = agent

    def dqn_wrapper(self, curr_state, prev_state, prev_action):
        return self._agent.make_action(curr_state.board.encode())

    def _reset_opponent(self, board):
        if self.opponent == "dqn":
            self.opponent_policy = self.dqn_wrapper
        else:
            super()._reset_opponent(board)


def input_to_action(input_string):
    input_string = input_string.capitalize()
    x_coord = ord(input_string[0]) - ord("A")
    y_coord = int(input_string[1]) - 1
    return y_coord * 9 + x_coord


def main():
    agent = DQNGomoku(GomokuEnv("black", "random", 9).action_space.n, mode=PLAY)
    env = GomokuEnvUI("black", "dqn", 9, agent)

    env.reset()
    done = False
    while not done:
        env.render()
        _, reward, done, _ = env.step(input_to_action(input(":")))
        if done:
            if reward > 0:
                print("Player win!")
            else:
                print("Bot win!")

if __name__ == "__main__":
    main()
