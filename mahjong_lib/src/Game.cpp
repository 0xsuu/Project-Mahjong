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

#include "Game.h"

#include <iostream>

using mahjong::Game;

Game::Game(Player *p1, Player *p2, Player *p3, Player *p4, int roundCount)  :
        mRoundCount(roundCount) {
    if (p1 != nullptr) {
        mPlayers.push_back(p1);
    }
    if (p2 != nullptr) {
        mPlayers.push_back(p2);
    }
    if (p3 != nullptr) {
        mPlayers.push_back(p3);
    }
    if (p4 != nullptr) {
        mPlayers.push_back(p4);
    }
}

void Game::onRoundStart() {
    std::cerr << "Virtual function, do not call.\n";
}
void Game::onPlayerPass(Player *player) {
    std::cerr << "Virtual function, do not call.\n";
}
void Game::onTileDrawToPlayer(Player *player, Tile tile) {
    std::cerr << "Virtual function, do not call.\n";
}
void Game::onPlayerDiscardTile(Player *player, Tile tile) {
    std::cerr << "Virtual function, do not call.\n";
}
void Game::onRoundFinished(bool drained, Player *winner) {
    std::cerr << "Virtual function, do not call.\n";
}
