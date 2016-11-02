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

#include <string>

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

#define TILE_FLAG_FILTER   0b11000000
#define TILE_TYPE_FILTER   0b00110000
#define TILE_NUMBER_FILTER 0b00001111

#define TILE_TYPE_ID_SPECIAL 3

// The flag may changing while the type and number are static.
#define TILE_REMOVE_FLAG_FILTER 0b00111111

// As the number starts from 1, we have to add an offset to it.
#define TILE_NUMBER_OFFSET 1

typedef enum TileFlag {
    Handed = 0b00000000,
    Melded = 0b01000000,
    Concealed = 0b10000000
} TileFlag;

typedef enum TileType {
    Character = 0b000000,
    Dot = 0b010000,
    Bamboo = 0b100000,
    Special = 0b110000
} TileType;

class Tile {
 public:
    /**
     * Constructor with information of one tile.
     *
     * @param [in] flag: The first 2 bits of the tile byte.
     * encode   | flag
     * -------- | ------
     * 00000000 | Handed
     * 01000000 | Melded
     * 10000000 | Concealed
     * 11000000 | <Undefine>
     *
     * @param [in] type: The 3rd and 4th bits of the tile byte.
     * encode | type
     * ------ | ------
     * 000000 | Character
     * 010000 | Dot
     * 100000 | Bamboo
     * 110000 | Special
     *
     * @param [in] number: The last 4 bits of the tile byte.
     * encode             | applied type
     * ------------------ | -------------
     * 0001 - 1001(1 - 9) | C, D and B.
     * 0001 - 0110(1 - 7) | S.
     */
    Tile(const TileFlag flag, const TileType type, const int number);

    /**
     * Constructor that makes a null tile.
     */
    Tile() {}

    /**
     * Get this tile's flag.
     *
     * @return Flag
     */
    TileFlag getFlag();
    /**
     * Get this tile's type.
     *
     * @return Type
     */
    TileType getType();
    /**
     * Get this tile's number.
     *
     * @return Number
     */
    int getNumber();

    /**
     * Get entire data.
     *
     * @return mTileData
     */
    uint8_t getData() { return mTileData; }

    /**
     * Get the string for display.
     * 
     * @return A string ready for print in terminal.
     */
    std::string getPrintable();

    /**
     * Set this tile to meld.
     */
    void setMeld();
    /**
     * set this tile to conceal.
     */
    void setConceal();

    bool operator = (Tile t);

 private:
    uint8_t mTileData = 0; //!< The byte and the only stores the actual data of the tile.

    /**
     * Get Type ID.
     *
     * @return Type in 2 bits.
     */
    inline uint8_t getTypeID();
};

} // namespace mahjong

#endif //MAHJONG_LIB_TILE_H
