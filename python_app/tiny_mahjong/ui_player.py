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
        choice = None
        while choice is None:
            opponent_names_discards = self.game_state.get_opponents_discards()
            for player in opponent_names_discards.keys():
                print(player.name, "discards:")
                for tile in opponent_names_discards[player]:
                    self.print_tile(tile)
                print("\n")

            print("Your discards:")
            for tile in self.game_state.get_player_discards():
                self.print_tile(tile)
            print("\n")

            for tile in self.hand:
                self.print_tile(tile)
            print()

            if self.test_win():
                print("You won!")
                return WIN, -1
            print("0\t1\t2\t3\t4")

            choice = input(":")
            try:
                choice = int(choice)
            except ValueError:
                choice = None
                print("Illegal input, please re-input your choice.\n")
                continue

            if choice < 0 or choice >= 5:
                choice = None
                print("Illegal input, please re-input your choice.\n")
                continue

        return DISCARD, choice

    def game_ends(self, win, lose, self_win=False, drain=False):
        Player.game_ends(self, win, lose, self_win, drain)
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
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

    @staticmethod
    def print_tile(tile):
        if tile <= 9:
            print(TERMINAL_BLUE + "A" + str(int(tile)) + TERMINAL_END, end="\t",)
        else:
            print(TERMINAL_GREEN + "B" + str(int(tile - 9)) + TERMINAL_END, end="\t",)
