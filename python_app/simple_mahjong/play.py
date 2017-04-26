#!/usr/bin/env python
# -*- coding: utf-8 -*-

from players.dqcnn_player import *

p1 = make_greedy_player("BOT Greedy 1")
p2 = make_greedy_player("BOT Greedy 2")
p3 = make_greedy_player("BOT Greedy 3")
dqcnn = DQCNNPlayer("Bot DQCNN", PLAY)
p4 = make_python_player(dqcnn)

game = SimpleGame(p1, p2, p3, p4, 1000)

game.start_game()
