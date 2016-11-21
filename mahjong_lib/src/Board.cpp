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
#include <iostream>

#include "Board.h"

using std::vector;

using mahjong::Action;
using mahjong::Board;

Board::Board(Game *game, Player *p1, Player *p2, Player *p3, Player *p4, bool enableDora, int doraStackSize) :
        mGame(game), mEnableDora(enableDora), mDoraStackSize(doraStackSize) {
    mPlayers = new vector<Player *>();
    if (p1 != nullptr) {
        mPlayers->push_back(p1);
    }
    if (p2 != nullptr) {
        mPlayers->push_back(p2);
    }
    if (p3 != nullptr) {
        mPlayers->push_back(p3);
    }
    if (p4 != nullptr) {
        mPlayers->push_back(p4);
    }
    mPlayerCount = mPlayers->size();
}

void Board::setup(TileSetType tileSetType, Wind roundWind) {
    // Few initialisations.
    mTileSetType = tileSetType;
    mRoundWind = roundWind;
    mTileStack.setup(tileSetType, mEnableDora, mDoraStackSize);

    // Callback.
    mGame->onRoundStart();

    // Shuffle the players first, i.e. seat positions randomised.
    std::random_shuffle(mPlayers->begin(), mPlayers->end());

    // Generate an unique ID for each player.
    std::random_device randomDevice;
    std::uniform_int_distribution<unsigned int> IDDistribution(10000, 30000);

    // Assign initial hands and other setups.
    vector<Hand> initialHands(mPlayers->size(), Hand());
    for (int i = 0; i < 13; ++i) {
        int indexPlayer = 0;
        std::for_each(mPlayers->begin(), mPlayers->end(), [&](Player *p) {
            Tile t = mTileStack.drawTile();
            mGame->onTileDrawToPlayer(p, t);
            initialHands[indexPlayer].addTile(t);
            indexPlayer++;
        });
    }
    int indexPlayer = 0;
    std::for_each(mPlayers->begin(), mPlayers->end(), [&](Player *p) {
        Hand sortedHand = initialHands[indexPlayer];
        sortedHand.sort();
        p->setupPlayer(IDDistribution(randomDevice), Winds[indexPlayer], sortedHand);
        indexPlayer++;
    });

    mCurrentPlayerIndex = mPlayers->begin();
}

void Board::reset() {
    setup(mTileSetType, mRoundWind);
}

void Board::shiftRoundWind() {
    mRoundWind == North ? mRoundWind = East :
            mRoundWind = static_cast<Wind>(static_cast<int>(mRoundWind) + 1);
}

vector<Action> Board::proceedToNextPlayer() {
    std::for_each(mPlayers->begin(), mPlayers->end(), [&](Player *p) {
        bool isPlayerTurn = p->getID() == (*mCurrentPlayerIndex)->getID();
        Tile t = mTileStack.drawTile();
        mGame->onTileDrawToPlayer(p, t);
        Action a = p->onTurn(isPlayerTurn, t);
        switch (a.getActionState()) {
            case Pass:
                mGame->onPlayerPass(p);
                break;
            case Discard:
                p->getHand().discardTile(a.getTile());
                mGame->onPlayerDiscardTile(p, a.getTile());
                break;
            case Win:
                mGame->onRoundFinished(false, p);
                break;
            default:
                throw std::invalid_argument("ActionState not recognised.");
        }
    });
    mCurrentPlayerIndex++;
    if (mCurrentPlayerIndex == mPlayers->end()) {
        mCurrentPlayerIndex = mPlayers->begin();
    }
}

void Board::printBoard(int PlayerID) {

}
