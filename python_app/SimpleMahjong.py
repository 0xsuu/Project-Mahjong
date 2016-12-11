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
    def onTurn(self, playerID, tile):
        print "onTurn"
        if playerID == getID():
            if getHand().testWin():
                return Action(Win, Tile())

            handData = getHand().getData()
            it = handData.begin()
            while it.getFlag() != Handed:
                it += 1
            return Action(Discard, it)
        else:
            return Action()
    def onOtherPlayerMakeAction(self, playerID, playerName, action):
        print "onOtherPlayerMakeAction:"
        return Action()

p1 = makeGreedyPlayer("BOT Greedy 1")
p2 = makeGreedyPlayer("BOT Greedy 2")
#p2 = makeUserInputPlayer("Smart Human")
p3 = makeGreedyPlayer("BOT Greedy 3")
SB = StupidPlayer("SB")
p4 = makePythonPlayer(SB)

game = SimpleGame(p1, p2, p3, p4, 1000)

game.startGame()

