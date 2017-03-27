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

TERMINAL_BLUE = "\033[94m"
TERMINAL_GREEN = "\033[92m"
TERMINAL_END = "\033[0m"


class UserInputPlayer(Player):
    def tile_picked(self):
        Player.tile_picked(self)
        for i in self.hand:
            if i <= 9:
                print(TERMINAL_BLUE + "A" + str(int(i)) + TERMINAL_END, end="\t")
            else:
                print(TERMINAL_GREEN + "B" + str(int(i - 9)) + TERMINAL_END, end="\t")
        print()
        if self.test_win():
            print("You won!")
            return WIN, -1
        print("0\t1\t2\t3\t4")
        choice = input(":")
        return DISCARD, choice

    def game_ends(self, win, drain=False):
        Player.game_ends(self, win, drain)
        if not win:
            print("Player lose.")
