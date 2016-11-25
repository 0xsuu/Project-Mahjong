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

using std::map;
using std::vector;

using mahjong::Action;
using mahjong::Board;

Board::Board(Game *game, Player *p1, Player *p2, Player *p3, Player *p4, bool enableDora, int doraStackSize) :
        mGame(game), mEnableDora(enableDora), mDoraStackSize(doraStackSize) {
    mPlayers = new vector<Player *>({});
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

    mGame->onRoundSetup();

    // Shuffle the players first, i.e. seat positions randomised.
    std::random_device random_device;
    std::mt19937 rd(random_device());
    shuffle(mPlayers->begin(), mPlayers->end(), rd);

    // Generate an unique ID for each player.
    std::random_device randomDevice;
    std::uniform_int_distribution<unsigned int> IDDistribution(10000, 30000);

    // Assign initial hands and other setups.
    vector<Hand> initialHands(mPlayers->size(), Hand());
    for (int i = 0; i < 13; ++i) {
        int indexPlayer = 0;
        std::for_each(mPlayers->begin(), mPlayers->end(), [&](Player *p) {
            Tile t = mTileStack.drawTile();
            mGame->onAfterPlayerPickTile(p, t);
            initialHands[indexPlayer].addTile(t);
            indexPlayer++;
        });
    }
    int indexPlayer = 0;
    vector<unsigned int> allocatedIDs;
    std::for_each(mPlayers->begin(), mPlayers->end(), [&](Player *p) {
        Hand sortedHand = initialHands[indexPlayer];
        sortedHand.sort();
        unsigned int randomID = IDDistribution(randomDevice);
        // Make sure all the IDs are unique.
        while (std::find(allocatedIDs.begin(), allocatedIDs.end(), randomID) != allocatedIDs.end()) {
            randomID = IDDistribution(randomDevice);
        }
        p->setupPlayer(randomID, Winds[indexPlayer], sortedHand, this);
        indexPlayer++;
    });

    mCurrentPlayerIndex = mPlayers->begin();

    mRoundEnded = false;
    mGame->onRoundStart();
}

void Board::reset() {
    setup(mTileSetType, mRoundWind);
}

void Board::shiftRoundWind() {
    mRoundWind == North ? mRoundWind = East :
            mRoundWind = static_cast<Wind>(static_cast<int>(mRoundWind) + 1);
}

void Board::proceedToNextPlayer() {
    // Check drained.
    if (mTileStack.isEmpty()) {
        mRoundEnded = true;
        mGame->onRoundFinished(true, nullptr);
        return;
    }

    // Get a tile from tile stack.
    Tile t = mTileStack.drawTile();
    mGame->onBeforePlayerPickTile(*mCurrentPlayerIndex, t);
    (*mCurrentPlayerIndex)->pickTile(t);
    mGame->onAfterPlayerPickTile(*mCurrentPlayerIndex, t);
    mDiscardedTiles[*mCurrentPlayerIndex].addTile(t);
    map<Action, Player *> allActions;
    std::for_each(mPlayers->begin(), mPlayers->end(), [&](Player *p) {
        bool isPlayerTurn = p->getID() == (*mCurrentPlayerIndex)->getID();
        Action a = p->onTurn(isPlayerTurn, t);
        allActions[a] = p;
        Hand copyHand(p->getHand().getData());
        switch (a.getActionState()) {
            case Pass:
                mGame->onPlayerPass(p);
                break;
            case Discard:
                p->discardTile(a.getTile());
                mGame->onPlayerDiscardTile(p, a.getTile());
                break;
            case Win:
                if (isPlayerTurn) {
                    assert(t == Tile());
                } else {
                    assert(t != Tile());
                    copyHand.pickTile(t);
                }
                if (copyHand.testWin()) {
                    mRoundEnded = true;
                    mGame->onRoundFinished(false, p);
                } else {
                    throw std::invalid_argument("False win.");
                }
                break;
            default:
                throw std::invalid_argument("ActionState not recognised.");
        }

        mRemainTilesCount = mTileStack.getRemainTilesCount();
    });

    // Next player's turn.
    mCurrentPlayerIndex++;
    if (mCurrentPlayerIndex == mPlayers->end()) {
        mCurrentPlayerIndex = mPlayers->begin();
    }
}
