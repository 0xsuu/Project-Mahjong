#!/usr/bin/env python
# -*- coding: utf-8 -*-

from players.dqcnn_player import *

p1 = make_random_player("BOT Random 1")
p2 = make_random_player("BOT Random 2")
p3 = make_random_player("BOT Random 3")
dqcnn = DQCNNPlayer("Bot DQCNN", TRAIN)
dqcnn_self_play = DQCNNPlayer("BOT SELF_PLAY", SELF_PLAY)
p4 = make_python_player(dqcnn)
p5 = make_python_player(dqcnn_self_play)

game = SimpleGame(p4, p5, None, None, 10000000)

game.start_game()
