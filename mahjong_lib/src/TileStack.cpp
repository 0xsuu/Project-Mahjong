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

#include <stdexcept>
#include <iostream>

#include "TileStack.h"

using std::vector;

using mahjong::TileStack;

TileStack::TileStack(TileSetType tileSetType, bool doraTile, int notPlayingCount) {
    mTileSetType = tileSetType;
    mEnableDoraTiles = doraTile;
    mPlayingTileCount = static_cast<int>(tileSetType) - notPlayingCount;

    vector<Tile> candidateTiles;
    switch (tileSetType) {
        case JAPANESE_MAHJONG_TILES_COUNT:
            for (int i = 0; i < 4; ++i) {
                for (int j = 1; j <= 9; ++j) {
                    candidateTiles.push_back(Tile(mahjong::Handed, mahjong::Character, j));
                    candidateTiles.push_back(Tile(mahjong::Handed, mahjong::Dot, j));
                    candidateTiles.push_back(Tile(mahjong::Handed, mahjong::Bamboo, j));
                    if (j <= 7) {
                        candidateTiles.push_back(Tile(mahjong::Handed, mahjong::Special, j));
                    }
                }
            }
            break;
        case COMPETITIVE_MAHJONG_TILES_COUNT:
            // Not implemented.
            break;
        default:
            throw std::invalid_argument("Tile Set Type not recognised.");
    }
}

int TileStack::throwDice() {
    std::uniform_int_distribution<int> diceDistribution(1, 6);
    return diceDistribution(mRandomDevice);
}
