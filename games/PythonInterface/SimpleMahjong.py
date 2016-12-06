#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../../../build_mahjong")
sys.path.append("../../../build_players")
sys.path.append("../../../build_games")
from libmahjong import *
from libplayers import *
from libgames import *

p1 = makeGreedyPlayer("BOT Greedy 1")
p2 = makeUserInputPlayer("Smart Human")
p3 = None
p4 = None

game = SimpleGame(p1, p2, p3, p4, 1000)

game.startGame()

