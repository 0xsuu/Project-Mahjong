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
#include "TenhouEncoder.h"

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
    std::random_device random_device;
    mRandomDevice = std::mt19937(random_device());
}

void Board::setup(TileSetType tileSetType, Wind roundWind) {
    // Few initialisations.
    mTileSetType = tileSetType;
    mRoundWind = roundWind;
    mTileStack.setup(tileSetType, mEnableDora, mDoraStackSize);

    mGame->onRoundSetup();

    // Shuffle the players first, i.e. seat positions randomised.
    shuffle(mPlayers->begin(), mPlayers->end(), mRandomDevice);

    // Generate an unique ID for each player.
    std::uniform_int_distribution<unsigned int> IDDistribution(10000, 30000);

    // Assign initial hands and other setups.
    int indexPlayer = 0;
    vector<unsigned int> allocatedIDs;
    std::for_each(mPlayers->begin(), mPlayers->end(), [&](Player *p) {
        Hand initialHand;
        for (int i = 0; i < 13; ++i) {
            Tile t = mTileStack.drawTile();
            mGame->onAfterPlayerPickTile(p, t);
            initialHand.addTile(t);
        }
        initialHand.sort();
        unsigned int randomID = IDDistribution(mRandomDevice);
        // Make sure all the IDs are unique.
        while (std::find(allocatedIDs.begin(), allocatedIDs.end(), randomID) != allocatedIDs.end()) {
            randomID = IDDistribution(mRandomDevice);
        }
        p->setupPlayer(randomID, Winds[indexPlayer], initialHand, this);
        indexPlayer++;
    });

    mCurrentPlayerIndex = mPlayers->begin();

    mRoundEnded = false;
    mGame->onRoundStart();
}

void Board::reset() {
    mTileStack.reset();
    mPickedTiles.clear();
    mDiscardedTiles.clear();
    for (auto it = mPlayers->begin(); it < mPlayers->end(); it++) {
        // Assign initial hands.
        Hand initialHand;
        for (int i = 0; i < 13; ++i) {
            Tile t = mTileStack.drawTile();
            mGame->onAfterPlayerPickTile(*it, t);
            initialHand.addTile(t);
        }
        initialHand.sort();
        (*it)->resetPlayer(initialHand);
        if ((*it)->getSeatPosition() == East) {
            mCurrentPlayerIndex = it;
        }
    }
    mGame->onRoundStart();
}

void Board::shiftToNextRound() {
    std::for_each(mPlayers->begin(), mPlayers->end(), [](Player *p) {
        p->shiftSeatPosition();
    });
    if (mRoundNumber >= 4) {
        mRoundNumber = 1;
        mRoundWind == North ? mRoundWind = East :
                mRoundWind = static_cast<Wind>(static_cast<int>(mRoundWind) + 1);
    } else {
        mRoundNumber++;
    }
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
    mPickedTiles[*mCurrentPlayerIndex].addTile(t);
    mGame->onAfterPlayerPickTile(*mCurrentPlayerIndex, t);

    mRemainTilesCount = mTileStack.getRemainTilesCount();

    Player *p = *mCurrentPlayerIndex;
    Action a = p->onTurn((*mCurrentPlayerIndex)->getID(), t);
    switch (a.getActionState()) {
        case Discard: {
            p->discardTile(a.getTile());
            mDiscardedTiles[p].addTile(a.getTile());
            mGame->onPlayerDiscardTile(p, a.getTile());

            // Notify all the other players that player p has discarded a tile.
            map<Action, Player *> allActions;
            std::for_each(mPlayers->begin(), mPlayers->end(), [&](Player *player) {
                if (p != player) {
                    Action act = player->onOtherPlayerMakeAction(p->getID(), p->getPlayerName(), a);
                    allActions[act] = player;

                    Hand copyHand(player->getHand());
                    switch (act.getActionState()) {
                        case Pass:
                            mGame->onPlayerPass(player);
                            break;
                        case Win:
                            assert(!act.getTile().isNull());
                            copyHand.pickTile(act.getTile());
                            if (copyHand.testWin()) {
                                mRoundEnded = true;
                                mGame->onRoundFinished(false, player);
                                return;
                            } else {
                                throw std::invalid_argument("False win.");
                            }
                        default:
                            throw std::invalid_argument("ActionState not recognised.");
                    }
                }
            });
            break;
        }
        case Win:
            assert(a.getTile().isNull());
            if (p->getHand().testWin()) {
                mRoundEnded = true;
                mGame->onRoundFinished(false, p);
                return;
            } else {
                throw std::invalid_argument("False win.");
            }
        default:
            throw std::invalid_argument("ActionState not recognised, or"
                                                "player returned action with onTurn() when it is not his turn.");
    }

    // Next player's turn.
    mCurrentPlayerIndex++;
    if (mCurrentPlayerIndex == mPlayers->end()) {
        mCurrentPlayerIndex = mPlayers->begin();
    }
}
