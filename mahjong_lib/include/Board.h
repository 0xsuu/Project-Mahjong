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

#ifndef MAHJONG_LIB_BOARD_H
#define MAHJONG_LIB_BOARD_H

#include <string>
#include <map>
#include <vector>

#include "Game.h"
#include "Hand.h"
#include "Player.h"
#include "TileGroup.h"
#include "TileStack.h"

namespace mahjong {
/**
 * This class controls the rules of the game.
 */
class Board {
 public:
    Board(Game *game, Player *p1, Player *p2, Player *p3, Player *p4, bool enableDora, int doraStackSize);
    ~Board() {
        delete mPlayers;
    }

    /**
     * Step 1: Setup TileStack.
     * Step 2: Assign random IDs, seat positions and initial hands.
     * Step 3: Sort players by wind.
     *
     * This should only be called once in a complete game.
     * If you need to reset after a round, just call reset().
     *
     * @param tileSetType
     * @param roundWind
     */
    void setup(TileSetType tileSetType, Wind roundWind);
    void reset();

    void shiftRoundWind();

    void proceedToNextPlayer();

    void saveBoard();

    std::vector<Player *> *getPlayers() {
        return mPlayers;
    }

 protected:
    Game *mGame;
    unsigned long mPlayerCount;
    std::vector<Player *> *mPlayers;
    bool mEnableDora;
    int mDoraStackSize;

    TileSetType mTileSetType;
    Wind mRoundWind;
    TileStack mTileStack;
    std::vector<Player *>::iterator mCurrentPlayerIndex;

    std::map<Player *, TileGroup> mDiscardedTiles;

    // Information for showing.
    bool mRoundEnded = true;
    int mRemainTilesCount = 0;
};

} // namespace mahjong.

#endif // MAHJONG_LIB_BOARD_H
