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


def expandHandToCSV(byte_hand):
    ret_hand = []
    for i in byte_hand:
        i = i.get_data()
        # Convert to one hot encoding.
        converted_hand = 1 << (2 - ((i & 0b11000000) >> 6))
        converted_hand <<= 13
        converted_hand |= 1 << (3 - ((i & 0b110000) >> 4) + 9)
        converted_hand |= 1 << (9 - (i & 0b1111))
        ret_hand += list(bin(converted_hand)[2:].zfill(16))
    return ret_hand


def transformCSVHandToCNNMatrix(csv_hand):
    try:
        csv_hand = np.array([csv_hand])
        return csv_hand.reshape(csv_hand.shape[0], 14, 16, 1)
    except ValueError:
        print("Temporary fix.")
        return csv_hand[0][:224].reshape(csv_hand.shape[0], 14, 16, 1)


class SLCNNPlayer(BaseAI):
    version = '0.0.2'

    def __init__(self, table, player):
        super(SLCNNPlayer, self).__init__(table, player)
        self.model = load_model("../supervised_learning/cnn_model.h5")
        self.model.load_weights("../supervised_learning/cnn_weights.h5")
        self.shanten = Shanten()

    def mahjong_tile_to_discard_tile(self, t):
        return TilesConverter.find_34_tile_in_136_array(
            t.get_number() + (t.get_type() >> 4) * 9 - 1, self.player.tiles)

    def discard_tile(self):
        h = Hand(TilesConverter.to_one_line_string(self.player.tiles))

        tiles = TilesConverter.to_34_array(self.player.tiles)
        shanten = self.shanten.calculate_shanten(tiles)
        if shanten == 0:
            self.player.in_tempai = True

        if h.test_win():
            return Shanten.AGARI_STATE
        elif self.player.in_tempai:
            results, st = self.calculate_outs()
            tile34 = results[0]['discard']
            tile_in_hand = TilesConverter.find_34_tile_in_136_array(tile34, self.player.tiles)
            return tile_in_hand
        else:
            hand_data = h.get_data()
            it = int(self.model.predict_classes(
                transformCSVHandToCNNMatrix(expandHandToCSV(hand_data)), verbose=0)[0])
            t = hand_data[it]
            tile_in_hand = self.mahjong_tile_to_discard_tile(t)
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
                raw_data[i] = {'tile': i,
                               'tiles_count': self.count_tiles(raw_data[i], tiles),
                               'waiting': raw_data[i]}

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

