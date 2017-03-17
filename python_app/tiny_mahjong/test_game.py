#!/usr/bin/env python3

import numpy as np

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
