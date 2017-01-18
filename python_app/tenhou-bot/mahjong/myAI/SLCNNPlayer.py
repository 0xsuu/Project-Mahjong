#!/usr/bin/env python3

import sys
sys.path.append("../../../build_mahjong")
sys.path.append("../../../build_players")
sys.path.append("../../../build_games")
from libmahjong import *
from libplayers import *
from libgames import *

from keras.models import load_model

import numpy as np

from mahjong.ai.agari import Agari
from mahjong.ai.base import BaseAI
from mahjong.ai.defence import Defence
from mahjong.ai.shanten import Shanten
from mahjong.tile import TilesConverter

def expandHandToCSV(byteHand):
    retHand = []
    for i in byteHand:
        retHand += list(bin(i.getData())[2:].zfill(8))
    return retHand

def transformCSVHandToCNNMatrix(csvHand):
    csvHand = np.array([csvHand])
    return csvHand.reshape(csvHand.shape[0], 1, 14, 8)

class SLCNNPlayer(BaseAI):
    version = '0.0.2'

    def __init__(self, table, player):
        super(SLCNNPlayer, self).__init__(table, player)
        self.model = load_model("../CNNModel.h5")
        self.model.load_weights("../CNNModelWeights.h5")
        self.shanten = Shanten()

    def discard_tile(self):
        h = Hand(TilesConverter.to_one_line_string(self.player.tiles))

        tiles = TilesConverter.to_34_array(self.player.tiles)

        shanten = self.shanten.calculate_shanten(tiles)
        if shanten == 0:
            self.player.in_tempai = True

        types = ['m', 'p', 's', 'z']
        if h.testWin():
            return Shanten.AGARI_STATE
        else:
            handData = h.getData()
            it = int(self.model.predict_classes(transformCSVHandToCNNMatrix(expandHandToCSV(handData)), verbose = 0)[0]);
            t = handData[it]
            tile_in_hand = TilesConverter.find_34_tile_in_136_array(t.getNumber() + (t.getType() >> 4) * 9 - 1, self.player.tiles)
            return tile_in_hand

