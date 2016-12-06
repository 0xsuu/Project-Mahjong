#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../../../build_mahjong")
sys.path.append("../../../build_players")
sys.path.append("../../../build_games")
from libmahjong import *
from libplayers import *
from libgames import *

p1 = GreedyPlayer("BOT Greedy 1")
p2 = UserInputPlayer("Smart Human")
p3 = GreedyPlayer("BOT Greedy 2")
p4 = GreedyPlayer("BOT Greedy 3")

game = SimpleGame(p1, p2, p3, p4, 1)

game.startGame()

