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

#ifndef MAHJONG_LIB_GAME_H
#define MAHJONG_LIB_GAME_H

#include <string>
#include <vector>

#include "Player.h"
#include "PrintFormat.h"

namespace mahjong {

/**
 * An interface for implementing UI.
 */
class Game {
 public:
    Game(Player *p1, Player *p2, Player *p3, Player *p4, int roundCount) :
            mPlayer1(p1), mPlayer2(p2), mPlayer3(p3), mPlayer4(p4), mRoundCount(roundCount) {}
    virtual ~Game() {}

    virtual void startGame() = 0;

    // Callback interfaces.
    virtual void onRoundSetup() = 0;
    virtual void onRoundStart() = 0;
    virtual void onTileDrawToPlayer(Player *player, Tile tile) = 0;
    virtual void onPlayerDiscardTile(Player *player, Tile tile) = 0;
    virtual void onPlayerPass(Player *player) = 0;
    virtual void onRoundFinished(bool drained, Player *winner) = 0;

    // Rule interfaces.
    virtual int calculateScore(Hand mHand) = 0;

 protected:
    Player *mPlayer1;
    Player *mPlayer2;
    Player *mPlayer3;
    Player *mPlayer4;
    int mRoundCount;
    int mCurrentRound;
    bool mRoundFinished;
};

} // namespace mahjong.

#endif // MAHJONG_LIB_GAME_H
