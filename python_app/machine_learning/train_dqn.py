#!/usr/bin/env python
# -*- coding: utf-8 -*-

from players.dqcnn_player import *

p1 = makeRandomPlayer("BOT Random 1")
p2 = makeRandomPlayer("BOT Random 2")
p3 = makeRandomPlayer("BOT Random 3")
dqcnn = DQCNNPlayer("Bot DQCNN", TRAIN)
p4 = makePythonPlayer(dqcnn)

game = SimpleGame(p4, p2, None, None, 10000000)

game.startGame()

