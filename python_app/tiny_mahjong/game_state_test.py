#!/usr/bin/env python3

# -*- coding: utf-8 -*-

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

import numpy as np

from game_state import GameState

g = GameState("Empty", False)

# # Win states.
# g._player_hand = np.array([1, 1, 2, 3, 4])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (0, 67, [])
# g._player_hand = np.array([1, 2, 2, 2, 3])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (0, 67, [])
# g._player_hand = np.array([1, 2, 3, 3, 3])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (0, 67, [])
#
# # Tenpai states.
# g._player_hand = np.array([1, 2, 3, 4])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 6, [4, 1])
# g._player_hand = np.array([2, 3, 4, 10])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 3, [10])
# g._player_hand = np.array([1, 2, 3, 4, 10])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 6, [])
# g._player_hand = np.array([1, 1, 8, 9, 10])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 4, [])
# g._player_hand = np.array([1, 1, 3, 3, 10])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 4, [])
# g._player_hand = np.array([1, 1, 2, 3])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 6, [4, 1])
# g._player_hand = np.array([1, 1, 2, 2, 3])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 6, [])
# g._player_hand = np.array([1, 1, 5, 6])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 8, [7, 4])
# g._player_hand = np.array([1, 1, 1, 18])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 3, [18])
#
# g._player_hand = np.array([5, 7, 9, 9])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 4, [6])
# g._player_hand = np.array([0, 1, 2, 17, 17])
# assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 4, [3])

g._disclose_all = True
g._player_hand = np.array([0, 12, 14, 17, 18])
g._opponents_hands = np.array([7, 8, 9, 9, 0])
assert g.calc_shanten_tenpai_tiles(g._opponents_hands) == (1, 6, [9, 6])
g._disclose_all = False
g._player_hand = np.array([2, 3, 4, 4, 0])
assert g.calc_shanten_tenpai_tiles(g._player_hand) == (1, 6, [4, 1])

# 2-Shanten states.
g._player_hand = np.array([1, 2, 4, 6])
assert g.calc_shanten_tenpai_tiles(g._player_hand) == (2, 0, [])
g._player_hand = np.array([1, 2, 4, 6, 8])
assert g.calc_shanten_tenpai_tiles(g._player_hand) == (2, 0, [])
g._player_hand = np.array([1, 1, 6, 9, 10])
assert g.calc_shanten_tenpai_tiles(g._player_hand) == (2, 0, [])
g._player_hand = np.array([9, 10, 12, 13, 15])
assert g.calc_shanten_tenpai_tiles(g._player_hand) == (2, 0, [])

# 3-Shanten states.
g._player_hand = np.array([1, 4, 7, 10, 13])
assert g.calc_shanten_tenpai_tiles(g._player_hand) == (3, 0, [])
g._player_hand = np.array([1, 5, 9, 10, 13])
assert g.calc_shanten_tenpai_tiles(g._player_hand) == (3, 0, [])
g._player_hand = np.array([1, 4, 7, 10])
assert g.calc_shanten_tenpai_tiles(g._player_hand) == (3, 0, [])
