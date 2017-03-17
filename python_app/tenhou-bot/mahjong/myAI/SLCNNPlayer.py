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
    try:
        csvHand = np.array([csvHand])
        return csvHand.reshape(csvHand.shape[0], 1, 14, 8)
    except ValueError:
        print("Temporary fix.")
        return csvHand[0][:112].reshape(csvHand.shape[0], 1, 14, 8)

class SLCNNPlayer(BaseAI):
    version = '0.0.2'

    def __init__(self, table, player):
        super(SLCNNPlayer, self).__init__(table, player)
        self.model = load_model("../CNNModel.h5")
        self.model.load_weights("../CNNModelWeights.h5")
        self.shanten = Shanten()

    def mahjongTileToDiscardTile(self, t):
        return TilesConverter.find_34_tile_in_136_array(t.getNumber() + (t.getType() >> 4) * 9 - 1, self.player.tiles)

    def discard_tile(self):
        h = Hand(TilesConverter.to_one_line_string(self.player.tiles))

        tiles = TilesConverter.to_34_array(self.player.tiles)
        shanten = self.shanten.calculate_shanten(tiles)
        if shanten == 0:
            self.player.in_tempai = True

        types = ['m', 'p', 's', 'z']
        if h.testWin():
            return Shanten.AGARI_STATE
        elif self.player.in_tempai == True:
            results, st = self.calculate_outs()
            tile34 = results[0]['discard']
            tile_in_hand = TilesConverter.find_34_tile_in_136_array(tile34, self.player.tiles)
            return tile_in_hand
        else:
            handData = h.getData()
            it = int(self.model.predict_classes(transformCSVHandToCNNMatrix(expandHandToCSV(handData)), verbose = 0)[0]);
            t = handData[it]
            tile_in_hand = self.mahjongTileToDiscardTile(t)
            return tile_in_hand

    '''
    Adding this bit for calculating which tile to discard when calling Richii.
    '''
    def calculate_outs(self):
        tiles = TilesConverter.to_34_array(self.player.tiles)

        shanten = self.shanten.calculate_shanten(tiles)
        # win
        if shanten == Shanten.AGARI_STATE:
            return [], shanten

        raw_data = {}
        for i in range(0, 34):
            if not tiles[i]:
                continue

            tiles[i] -= 1

            raw_data[i] = []
            for j in range(0, 34):
                if i == j or tiles[j] >= 4:
                    continue

                tiles[j] += 1
                if self.shanten.calculate_shanten(tiles) == shanten - 1:
                    raw_data[i].append(j)
                tiles[j] -= 1

            tiles[i] += 1

            if raw_data[i]:
                raw_data[i] = {'tile': i, 'tiles_count': self.count_tiles(raw_data[i], tiles), 'waiting': raw_data[i]}

        results = []
        tiles = TilesConverter.to_34_array(self.player.tiles)
        for tile in range(0, len(tiles)):
            if tile in raw_data and raw_data[tile] and raw_data[tile]['tiles_count']:
                item = raw_data[tile]

                waiting = []

                for item2 in item['waiting']:
                    waiting.append(item2)

                results.append({
                    'discard': item['tile'],
                    'waiting': waiting,
                    'tiles_count': item['tiles_count']
                })

        # if we have character and honor candidates to discard with same tiles count,
        # we need to discard honor tile first
        results = sorted(results, key=lambda x: (x['tiles_count'], x['discard']), reverse=True)

        return results, shanten

    def count_tiles(self, raw_data, tiles):
        n = 0
        for i in range(0, len(raw_data)):
            n += 4 - tiles[raw_data[i]]
        return n
