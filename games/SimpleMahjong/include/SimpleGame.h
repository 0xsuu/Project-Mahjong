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

#include <Board.h>
#include <Game.h>

namespace mahjong {
class SimpleGame : public Game {
 public:
    SimpleGame(Player *p1, Player *p2, Player *p3, Player *p4, int roundCount);
    ~SimpleGame() {
        delete mBoard;
    }

    void startGame() override;

    // Callback interfaces.
    void onRoundSetup() override { /* Not used */ }
    void onRoundStart() override;
    void onBeforePlayerPickTile(Player *player, Tile tile) override;
    void onAfterPlayerPickTile(Player *player, Tile tile) override;
    void onPlayerDiscardTile(Player *player, Tile tile) override;
    void onPlayerPass(Player *player) override;
    void onRoundFinished(bool drained, Player *winner) override;
    void onNextRound(bool eastWin) override;

    void onGameOver();

    // Rule interfaces.
    int calculateScore(Hand mHand) override;

 private:
    std::map<Player *, int> mPlayerWinCount;
    Board *mBoard;

    void printPlayer(Player *p);
    void printBoard();
};
} // namespace mahjong.

#endif // SIMPLE_MAHJONG_SIMPLE_GAME_H