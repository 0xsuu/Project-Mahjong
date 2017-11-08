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

g = GameState(None, False)

# Win states.
g._player_hand = np.array([1, 1, 2, 3, 4])
assert g.calc_shanten() == 0
g._player_hand = np.array([1, 2, 2, 2, 3])
assert g.calc_shanten() == 0
g._player_hand = np.array([1, 2, 3, 3, 3])
assert g.calc_shanten() == 0

# Tenpai states.
g._player_hand = np.array([1, 2, 3, 4])
assert g.calc_shanten() == 1
g._player_hand = np.array([2, 3, 4, 10])
assert g.calc_shanten() == 1
g._player_hand = np.array([1, 2, 3, 4, 10])
assert g.calc_shanten() == 1
g._player_hand = np.array([1, 1, 8, 9, 10])
assert g.calc_shanten() == 1

# 2-Shanten states.
g._player_hand = np.array([1, 2, 4, 6])
assert g.calc_shanten() == 2
g._player_hand = np.array([1, 2, 4, 6, 8])
assert g.calc_shanten() == 2
g._player_hand = np.array([1, 1, 6, 9, 10])
assert g.calc_shanten() == 2

# 3-Shanten states.
g._player_hand = np.array([1, 4, 7, 10, 13])
assert g.calc_shanten() == 3
g._player_hand = np.array([1, 5, 9, 10, 13])
assert g.calc_shanten() == 3
g._player_hand = np.array([1, 4, 7, 10])
assert g.calc_shanten() == 3
