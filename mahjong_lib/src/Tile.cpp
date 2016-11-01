//
//  Copyright © 2016 Project Mahjong. All rights reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//

#include <assert.h>

#include "Tile.h"

using mahjong::Tile;
using mahjong::TileFlag;
using mahjong::TileType;

Tile::Tile(const TileFlag flag, const TileType type, const int number) {
    // Make sure the number is legal.
    assert(number <= 9 && number >= 1);

    mTileData = flag << 6 | type << 4 | number;
}

TileFlag Tile::getFlag() {
    return static_cast<TileFlag>(mTileData >> 6);
}

TileType Tile::getType() {
    return static_cast<TileType>(mTileData >> 4 & 0b11);
}

int Tile::getNumber() {
    return mTileData & 0b1111;
};
