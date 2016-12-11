#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../../build_mahjong")
sys.path.append("../../build_players")
sys.path.append("../../build_games")
from libmahjong import *
from libplayers import *
from libgames import *

class StupidPlayer(Player):
    def __init__(self, playerName):
        print "hi"
        super(StupidPlayer, self).__init__(playerName)
    def onTurn(playerID, tile):
        print "onTurn:"

p1 = makeGreedyPlayer("BOT Greedy 1")
p2 = makeGreedyPlayer("BOT Greedy 2")
#p2 = makeUserInputPlayer("Smart Human")
p3 = makeGreedyPlayer("BOT Greedy 3")
p4 = makeGreedyPlayer("BOT Greedy 4")

game = SimpleGame(p1, p2, p3, p4, 1000)

game.startGame()

