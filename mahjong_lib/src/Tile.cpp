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

#include <cassert>

#include "Tile.h"
#include "PrintFormat.h"

using std::string;

using mahjong::Tile;
using mahjong::TileFlag;
using mahjong::TileType;

Tile::Tile(const TileFlag flag, const TileType type, const int number) {
    // Make sure the number is legal.
    assert(number <= 9 && number >= 1);

    mTileData = flag | type | number;
}

TileFlag Tile::getFlag() {
    return static_cast<TileFlag>(mTileData & TILE_FLAG_FILTER);
}

TileType Tile::getType() {
    return static_cast<TileType>(mTileData & TILE_TYPE_FILTER);
}

int Tile::getNumber() {
    return mTileData & TILE_NUMBER_FILTER;
}

string Tile::getPrintable() {
    return getTypeID() == 3 ? MAHJONG_SPECIAL[getNumber() - TILE_NUMBER_OFFSET] :
            MAHJONG_NUMBER[getNumber() - TILE_NUMBER_OFFSET] + MAHJONG_TYPE[getTypeID()];
}

void Tile::setMeld() {
    mTileData = static_cast<uint8_t>(mTileData & TILE_REMOVE_FLAG_FILTER | Meld);
}

void Tile::setConceal() {
    mTileData = static_cast<uint8_t>(mTileData & TILE_REMOVE_FLAG_FILTER | Conceal);
}

// Private functions.

inline uint8_t Tile::getFlagID() {
    return static_cast<uint8_t >((mTileData & TILE_FLAG_FILTER) >> 6);
}

inline uint8_t Tile::getTypeID() {
    return static_cast<uint8_t >((mTileData & TILE_TYPE_FILTER) >> 4);
}
