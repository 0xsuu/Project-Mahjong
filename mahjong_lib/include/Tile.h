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

#ifndef MAHJONG_LIB_TILE_H
#define MAHJONG_LIB_TILE_H

#include <stdint.h>

namespace mahjong {

/**
 * @brief This class encode one single tile.
 *
 * @details Encoding Rule:
 *
 * 1 Tile = 1 Byte
 *
 * 1-2 bits | 3-4 bits | 5-8 bits
 * -------- | -------- | --------
 * 00       | 00       | 0000
 * flag     | type     | number
 */

typedef enum TileFlag {
    Hand = 0b00,
    Meld = 0b01,
    Conceal = 0b10
} TileFlag;

typedef enum TileType {
    Character = 0b00,
    Dot = 0b01,
    Bamboo = 0b10,
    Special = 0b11
} TileType;

class Tile {
 public:
    /**
     * Constructor with information of one tile.
     *
     * @param [in] flag: The first 2 bits of the tile byte.
     * encode | flag
     * ------ | ------
     * 00     | Hand
     * 01     | Meld
     * 10     | Conceal
     * 11     | <Undefine>
     *
     * @param [in] type: The 3rd and 4th bits of the tile byte.
     * encode | type
     * ------ | ------
     * 00     | Character
     * 01     | Dot
     * 10     | Bamboo
     * 11     | Special
     *
     * @param [in] number: The last 4 bits of the tile byte.
     * encode             | applied type
     * ------------------ | -------------
     * 0001 - 1001(1 - 9) | C, D and B.
     * 0001 - 0110(1 - 7) | S.
     */
    Tile(const TileFlag flag, const TileType type, const int number);

    /**
     * Get this tile's flag.
     * @return Flag
     */
    TileFlag getFlag();
    /**
     * Get this tile's type.
     * @return Type
     */
    TileType getType();
    /**
     * Get this tile's number.
     * @return Number
     */
    int getNumber();

 private:
    uint8_t mTileData = 0; //!< The byte and the only stores the actual data of the tile.
};

} // namespace mahjong

#endif //MAHJONG_LIB_TILE_H
