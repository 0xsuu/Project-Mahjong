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

namespace mahjong {

class Tile {
/**
 * @brief Encoding Rule:
 *
 * 1 Tile = 1 Byte
 *
 * 00   | 00   | 0000
 *
 * flag | type | number
 */
 public:
    /**
     * Constructor with information of one tile.
     *
     * @param [in] flag: The first 2 bits of the tile byte.
     * 00: hand.
     * 01: melded.
     * 10: concealed.
     * 11: undefined.
     *
     * @param [in] type: The 3rd and 4th bits of the tile byte.
     * 00: Character.
     * 01: Dot.
     * 10: Bamboo.
     * 11: Special.
     *
     * @param [in] number: The last 4 bits of the tile byte.
     * 0001 - 1001(1 - 9) for C, D and B.
     * 0001 - 0110(1 - 7) for S.
     */
    Tile(const int flag, const int type, const int number);

 private:
    uint8_t mTileData; //!< The byte and the only stores the actual data of the tile.
};

} // namespace mahjong

#endif //MAHJONG_LIB_TILE_H
