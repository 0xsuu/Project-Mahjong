#!/usr/bin/env python3

import os
import sys

ABSOLUTE_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/"

sys.path.append(ABSOLUTE_FILE_PATH + "../../../../build_mahjong/")
sys.path.append(ABSOLUTE_FILE_PATH + "../../../../build_players/")
sys.path.append(ABSOLUTE_FILE_PATH + "../../../../build_games/")
sys.path.append(ABSOLUTE_FILE_PATH + "../../utils/")
sys.path.append(ABSOLUTE_FILE_PATH + "../../keras_models/")
sys.path.append(ABSOLUTE_FILE_PATH + "../../rl_algorithms/")
