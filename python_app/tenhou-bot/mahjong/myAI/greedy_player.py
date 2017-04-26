#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../../build_mahjong")
sys.path.append("../../build_players")
sys.path.append("../../build_games")
from libmahjong import *
from libplayers import *
from libgames import *

from mahjong.ai.agari import Agari
from mahjong.ai.base import BaseAI
from mahjong.ai.defence import Defence
from mahjong.ai.shanten import Shanten
from mahjong.tile import TilesConverter

class GreedyAII(BaseAI):
    version = '0.0.1'

    def __init__(self, table, player):
        super(GreedyAII, self).__init__(table, player)
        self.shanten = Shanten()

    def discard_tile(self):
        gd_player = GreedyPlayer("Me")
        h = Hand(TilesConverter.to_one_line_string(self.player.tiles))
        t = gd_player.select_best_tile(h)

        tiles = TilesConverter.to_34_array(self.player.tiles)
        shanten = self.shanten.calculate_shanten(tiles)
        if shanten == 0:
            self.player.in_tempai = True

        types = ['m', 'p', 's', 'z']
        if h.test_win():
            return Shanten.AGARI_STATE
        else:
            tile_in_hand = TilesConverter.find_34_tile_in_136_array(
                t.get_number() + (t.get_type() >> 4) * 9 - 1, self.player.tiles)
            return tile_in_hand

