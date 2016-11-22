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

#ifndef SIMPLE_MAHJONG_SIMPLE_GAME_H
#define SIMPLE_MAHJONG_SIMPLE_GAME_H

#include <string>

#include <Game.h>
#include <Player.h>

namespace mahjong {
class SimpleGame : public Game {
 public:
    SimpleGame(Player *p1, Player *p2, Player *p3, Player *p4, int roundCount) :
            Game(p1, p2, p3, p4, roundCount) {}
    ~SimpleGame() {}

    // Callback interfaces.
    void onRoundStart();
    void onTileDrawToPlayer(Player *player, Tile tile);
    void onPlayerDiscardTile(Player *player, Tile tile);
    void onPlayerPass(Player *player);
    void onRoundFinished(bool drained, Player *winner);

    // Rule interfaces.
    int calculateScore(Hand mHand);
};
} // namespace mahjong.

#endif // SIMPLE_MAHJONG_SIMPLE_GAME_H