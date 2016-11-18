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

#include <algorithm>

#include "Board.h"

using std::vector;

using mahjong::Action;
using mahjong::Board;

void Board::setup(TileSetType tileSetType, Wind roundWind) {
    std::random_device mRandomDevice;
    std::uniform_int_distribution<unsigned int> IDDistribution(10000, 30000);
    std::for_each(mPlayers.begin(), mPlayers.end(), [&](Player p))
    //std::random_shuffle();
}

void Board::reset() {

}

vector<Action> Board::proceedToNextPlayer() {

}

void Board::printBoard(int PlayerID) {

}
