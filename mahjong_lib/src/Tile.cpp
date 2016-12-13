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

Tile::Tile(const TileFlag flag, const TileType type, const int number, bool dora) {
    // Make sure the number is legal.
    assert(number <= 9 && number >= 1);
    if (dora) {
        assert(number == 5);
        assert(type != Special);
    }

    mTileData  = flag | type | number;
    mIsDora = dora;
}

Tile::Tile(const uint8_t data, bool dora) {
    mTileData = data;
    mIsDora = dora;
}

TileFlag Tile::getFlag() const {
    return static_cast<TileFlag>(mTileData & TILE_FLAG_FILTER);
}
TileType Tile::getType() const {
    return static_cast<TileType>(mTileData & TILE_TYPE_FILTER);
}
int Tile::getNumber() const {
    return mTileData & TILE_NUMBER_FILTER;
}
bool Tile::isDora() const {
    return mIsDora;
}

bool Tile::isNull() const {
    return mTileData == 0;
}

string Tile::getPrintable() const {
    assert(!isNull());
    return getTypeID() == TILE_TYPE_ID_SPECIAL ? MAHJONG_SPECIAL[getNumber() - TILE_NUMBER_OFFSET] :
           ((isDora() ? MAHJONG_DORA_POINT : MAHJONG_NUMBER[getNumber() - TILE_NUMBER_OFFSET])
                                            + MAHJONG_TYPE[getTypeID()]);
}

void Tile::setMeld() {
    mTileData = static_cast<uint8_t>((mTileData & TILE_REMOVE_FLAG_FILTER) | Melded);
}
void Tile::setConceal() {
    mTileData = static_cast<uint8_t>((mTileData & TILE_REMOVE_FLAG_FILTER) | Concealed);
}

// Operator overloads.

bool Tile::operator==(Tile t) const {
    return mTileData == t.getData();
}
bool Tile::operator!=(Tile t) const {
    return mTileData != t.getData();
}
bool Tile::operator<(Tile t) const {
    return mTileData < t.getData();
}
bool Tile::operator<=(Tile t) const {
    return mTileData <= t.getData();
}
Tile Tile::operator+(int n) const {
    return Tile(getData() + static_cast<uint8_t>(n), mIsDora && n == 0);
}
Tile Tile::operator-(int n) const {
    return Tile(getData() - static_cast<uint8_t>(n), mIsDora && n == 0);
}

// Private functions.

inline uint8_t Tile::getTypeID() const {
    return static_cast<uint8_t>((mTileData & TILE_TYPE_FILTER) >> 4);
}
