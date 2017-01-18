# -*- coding: utf-8 -*-
from mahjong.ai.agari import Agari
from mahjong.ai.base import BaseAI
from mahjong.ai.defence import Defence
from mahjong.ai.shanten import Shanten
from mahjong.tile import TilesConverter


class MainAI(BaseAI):
    version = '0.0.6'

    agari = None
    shanten = None
    defence = None

    def __init__(self, table, player):
        super(MainAI, self).__init__(table, player)

        self.agari = Agari()
        self.shanten = Shanten()
        self.defence = Defence(table)

    def discard_tile(self):
        results, shanten = self.calculate_outs()

        if shanten == 0:
            self.player.in_tempai = True

        # we are win!
        if shanten == Shanten.AGARI_STATE:
            return Shanten.AGARI_STATE

        # Disable defence for now
        # if self.defence.go_to_defence_mode():
        #     self.player.in_tempai = False
        #     tile_in_hand = self.defence.calculate_safe_tile_against_riichi()
        #     if we wasn't able to find a safe tile, let's discard a random one
        #     if not tile_in_hand:
        #         tile_in_hand = self.player.tiles[random.randrange(len(self.player.tiles) - 1)]
        # else:
        #     tile34 = results[0]['discard']
        #     tile_in_hand = TilesConverter.find_34_tile_in_136_array(tile34, self.player.tiles)

        tile34 = results[0]['discard']
        tile_in_hand = TilesConverter.find_34_tile_in_136_array(tile34, self.player.tiles)

        return tile_in_hand

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
