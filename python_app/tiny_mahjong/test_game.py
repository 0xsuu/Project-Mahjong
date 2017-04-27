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


test_player = Player("test")
test_player.hand = np.array([1, 2, 3, 4, 5])
assert not test_player.test_win()
test_player.hand = np.array([1, 1, 2, 3, 4])
assert test_player.test_win()
test_player.hand = np.array([1, 1, 1, 2, 3])
assert test_player.test_win()
test_player.hand = np.array([9, 9, 9, 10, 11])
assert not test_player.test_win()

test_game = Game(1, [test_player])
test_game.setup()
assert test_player.get_remaining_tiles() == 72 - 4
total_probability = 0.0
for i in range(1, 19):
    total_probability += test_player.get_pick_tile_probability(i)
assert total_probability == 1.0
