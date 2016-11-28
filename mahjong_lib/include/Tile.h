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

// The dora number id.
#define TILE_DORA_NUMBER 5

typedef enum TileFlag {
    Concealed = 0b00000000,
    Melded = 0b01000000,
    Handed = 0b10000000
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
     * 00000000 | Concealed
     * 01000000 | Melded
     * 10000000 | Handed
     * 11000000 | <Undefined>
     *
     * @param [in] type: The 3rd and 4th bits of the tile byte.
     * encode   | type
     * -------- | ------
     * 00000000 | Character
     * 00010000 | Dot
     * 00100000 | Bamboo
     * 00110000 | Special
     *
     * @param [in] number: The last 4 bits of the tile byte.
     * encode                          | applied type
     * ------------------------------- | -------------
     * 0001 - 1010(1 - 9)              | C, D and B.
     * 0001 - 0110(1 - 7)              | S.
     *
     * @param dora: Is dora tile.
     */
    Tile(const TileFlag flag, const TileType type, const int number, bool dora = false);

    /**
     * Constructor that construct from a pre-cooked data.
     */
    Tile(const uint8_t data, bool dora);

    /**
     * Constructor that makes a null tile.
     */
    Tile() { mTileData = 0; }

    /**
     * Get this tile's flag.
     *
     * @return Flag
     */
    TileFlag getFlag() const;
    /**
     * Get this tile's type.
     *
     * @return Type
     */
    TileType getType() const;
    /**
     * Get this tile's number.
     *
     * @return Number
     */
    int getNumber() const;

    /**
     * Get if this tile is a dora tile.
     *
     * @return Is Dora Tile
     */
    bool isDora() const;

    /**
     * Get if this tile is a NULL tile.
     *
     * @return Is null tile
     */
    bool isNull() const;

    /**
     * Get entire data.
     *
     * @return mTileData
     */
    uint8_t getData() const { return mTileData; }

    /**
     * Get the string for display.
     *
     * @return A string ready for print in terminal.
     */
    std::string getPrintable() const;

    /**
     * Set this tile to meld.
     */
    void setMeld();
    /**
     * set this tile to conceal.
     */
    void setConceal();

    bool operator==(Tile t) const;
    bool operator!=(Tile t) const;
    bool operator<(Tile t) const;
    bool operator<=(Tile t) const;
    Tile operator+(int n) const;
    Tile operator-(int n) const;

 private:
    uint8_t mTileData = 0; //!< The byte and the only stores the actual data of the tile.

    /**
     * Get Type ID.
     *
     * @return Type in 2 bits.
     */
    inline uint8_t getTypeID() const;

    bool mIsDora;
};

} // namespace mahjong

#endif //MAHJONG_LIB_TILE_H
