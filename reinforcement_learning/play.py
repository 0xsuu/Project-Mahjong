#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DQCNNPlayer import *

p1 = makeGreedyPlayer("BOT Greedy 1")
p2 = makeGreedyPlayer("BOT Greedy 2")
p3 = makeGreedyPlayer("BOT Greedy 3")
dqcnn = DQCNNPlayer("Bot DQCNN", PLAY)
p4 = makePythonPlayer(dqcnn)

game = SimpleGame(p1, p2, p3, p4, 1000)

game.startGame()