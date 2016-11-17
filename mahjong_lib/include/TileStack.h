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

#ifndef MAHJONG_LIB_TILESTACK_H
#define MAHJONG_LIB_TILESTACK_H

#include <random>
#include <vector>

#include "Tile.h"

enum TileSetType {
    COMPETITIVE_MAHJONG_TILES_COUNT = 144,
    JAPANESE_MAHJONG_TILES_COUNT = 136
};

namespace mahjong {

class TileStack {
 public:
    /**
     * Constructor for the Tile Stack, mainly aimed for the abstraction
     * of the randomicity of the game.
     *
     * @param tileCount Number of all the available tiles.
     * @param doraTile Contains dora tile or not.
     * @param notPlayingCount Some leftover tiles for
     * @return
     */
    TileStack(TileSetType tileSetType, bool doraTile, int notPlayingCount);

    /**
     * Throw a dice.
     *
     * @return Dice point.
     */
    int throwDice();

 private:
    TileSetType mTileSetType;
    int mPlayingTileCount;
    bool mEnableDoraTiles;

    std::random_device mRandomDevice;
    std::vector<Tile> mRemainTiles;
};

}
#endif //MAHJONG_LIB_TILESTACK_H
