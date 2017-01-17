# -*- coding: utf-8 -*-
import unittest

from mahjong.tile import TilesConverter


class TileTestCase(unittest.TestCase):

    def test_convert_to_one_line_string(self):
        tiles = [0, 1, 34, 35, 36, 37, 70, 71, 72, 73, 106, 107, 108, 109, 133, 134]
        result = TilesConverter.to_one_line_string(tiles)
        self.assertEqual('1199m1199p1199s1177z', result)

    def test_convert_to_34_array(self):
        tiles = [0, 34, 35, 36, 37, 70, 71, 72, 73, 106, 107, 108, 109, 134]
        result = TilesConverter.to_34_array(tiles)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[8], 2)
        self.assertEqual(result[9], 2)
        self.assertEqual(result[17], 2)
        self.assertEqual(result[18], 2)
        self.assertEqual(result[26], 2)
        self.assertEqual(result[27], 2)
        self.assertEqual(result[33], 1)
        self.assertEqual(sum(result), 14)

    def test_convert_string_to_136_array(self):
        tiles = TilesConverter.string_to_136_array(sou='19', pin='19', man='19', honors='1234567')

        self.assertEqual([0, 32, 36, 68, 72, 104, 108, 112, 116, 120, 124, 128, 132], tiles)

    def test_find_34_tile_in_136_array(self):
        result = TilesConverter.find_34_tile_in_136_array(0, [3, 4, 5, 6])
        self.assertEqual(result, 3)

        result = TilesConverter.find_34_tile_in_136_array(33, [3, 4, 134, 135])
        self.assertEqual(result, 134)

        result = TilesConverter.find_34_tile_in_136_array(20, [3, 4, 134, 135])
        self.assertEqual(result, None)
