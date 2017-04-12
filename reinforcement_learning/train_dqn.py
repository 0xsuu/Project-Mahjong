#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DQCNNPlayer import *

p1 = makeRandomPlayer("BOT Random 1")
p2 = makeRandomPlayer("BOT Random 2")
p3 = makeRandomPlayer("BOT Random 3")
dqcnn = DQCNNPlayer("Bot DQCNN", TRAIN)
p4 = makePythonPlayer(dqcnn)

game = SimpleGame(p1, p2, p3, p4, 10000000)

game.startGame()