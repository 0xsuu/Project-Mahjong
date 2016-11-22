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

#include "SimpleGame.h"

#include <iostream>

using std::cout;

using mahjong::SimpleGame;

// Callback implementations.
void SimpleGame::onRoundStart() {
    cout << "Round "<< 1 <<" start.";
}

void SimpleGame::onTileDrawToPlayer(Player *player, Tile tile) {

}

void SimpleGame::onPlayerDiscardTile(Player *player, Tile tile) {

}

void SimpleGame::onPlayerPass(Player *player) {

}

void SimpleGame::onRoundFinished(bool drained, Player *winner) {

}

// Rule implementation.
int SimpleGame::calculateScore(Hand mHand) {

}
