#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../../build_mahjong")
from libmahjong import *

testTile = Tile()
assert testTile.isNull()

testTile = Tile(TileFlag.Melded, TileType.Special, 5)
assert testTile.getType() == TileType.Special
assert testTile.getPrintable() == "中"

