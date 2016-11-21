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
#include <cassert>

#include "Board.h"

using std::vector;

using mahjong::Action;
using mahjong::Board;

void Board::setup(TileSetType tileSetType, Wind roundWind) {
    // Does not supporting more than 4 players.
    assert(mPlayers.size() <= 4);

    // Callback.
    mGame.onRoundStart();

    // Shuffle the players first, i.e. seat positions randomised.
    std::random_shuffle(mPlayers.begin(), mPlayers.end());

    // Generate an unique ID for each player.
    std::random_device randomDevice;
    std::uniform_int_distribution<unsigned int> IDDistribution(10000, 30000);

    // Assign initial hands and other setups.
    vector<Hand> initialHands(mPlayers.size(), Hand());
    for (int i = 0; i < 14; ++i) {
        int indexPlayer = 0;
        std::for_each(mPlayers.begin(), mPlayers.end(), [&indexPlayer](Player &p) {
            Tile t = mTileStack.drawTile();
            mGame.onTileDrawToPlayer(p, t);
            initialHands[indexPlayer].pickTile(t);
            indexPlayer++;
        });
    }
    int indexPlayer = 0;
    std::for_each(mPlayers.begin(), mPlayers.end(), [&](Player &p) {
        p.setupPlayer(IDDistribution(randomDevice), Winds[indexPlayer], initialHands[indexPlayer]);
        indexPlayer++;
    });
}

void Board::reset() {

}

vector<Action> Board::proceedToNextPlayer() {

}

void Board::printBoard(int PlayerID) {

}
