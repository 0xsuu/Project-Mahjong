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

    mTileData = flag | type | numberToNumberID(type, number, dora);
}

Tile::Tile(const uint8_t data) {
    mTileData = data;
}

TileFlag Tile::getFlag() {
    return static_cast<TileFlag>(mTileData & TILE_FLAG_FILTER);
}
TileType Tile::getType() {
    return static_cast<TileType>(mTileData & TILE_TYPE_FILTER);
}
int Tile::getNumber() {
    return numberIDToNumber(getNumberID());
}
bool Tile::isDora() {
    return getNumberID() == TILE_DORA_NUMBER_ID;
}

string Tile::getPrintable() {
    return getTypeID() == TILE_TYPE_ID_SPECIAL ? MAHJONG_SPECIAL[getNumberID() - TILE_NUMBER_OFFSET] :
            MAHJONG_NUMBER[getNumberID() - TILE_NUMBER_OFFSET] + MAHJONG_TYPE[getTypeID()];
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
    return Tile(static_cast<uint8_t>(mTileData + n));
}

// Private functions.

inline uint8_t Tile::getTypeID() {
    return static_cast<uint8_t >((mTileData & TILE_TYPE_FILTER) >> 4);
}
inline int Tile::getNumberID() {
    return mTileData & TILE_NUMBER_FILTER;
}

inline int Tile::numberIDToNumber(int id) {
    return (getType() != Special && id > 5) ? id - 1 : id;
}

inline int Tile::numberToNumberID(TileType type, int number, bool dora = false) {
    if (type == Special) {
        return number;
    }
    else {
        return ((!dora && number > 5) || (dora && number == 5)) ? number + 1 : number;
    }
}
