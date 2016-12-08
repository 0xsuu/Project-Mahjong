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
#include <ctime>

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
        mInitialHands[p] = initialHand;
        indexPlayer++;
    });

    mCurrentPlayerIndex = mPlayers->begin();

    mRoundEnded = false;
    mGame->onRoundStart();
}

void Board::reset() {
    mTileStack.reset();
    mInitialHands.clear();
    mPickedTiles.clear();
    mDiscardedTiles.clear();
    mWinningYaku.clear();
    mTenhouUrl = "";
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
        mInitialHands[*it] = initialHand;
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
        finishRound(Ryuukyoku, nullptr, calculatePoints(Ryuukyoku, nullptr, -1), nullptr);
        return;
    }

    // Get a tile from tile stack.
    Tile t = mTileStack.drawTile();
    mGame->onBeforePlayerPickTile(*mCurrentPlayerIndex, t);
    (*mCurrentPlayerIndex)->pickTile(t);
    mPickedTiles[*mCurrentPlayerIndex].addTile(t);
    mGame->onAfterPlayerPickTile(*mCurrentPlayerIndex, t);

    mRemainTilesCount = mTileStack.getRemainTilesCount();

    Player *currentPlayer = *mCurrentPlayerIndex;
    Action a = currentPlayer->onTurn((*mCurrentPlayerIndex)->getID(), t);
    switch (a.getActionState()) {
        case Discard: {
            currentPlayer->discardTile(a.getTile());
            mDiscardedTiles[currentPlayer].addTile(a.getTile());
            mGame->onPlayerDiscardTile(currentPlayer, a.getTile());

            // Notify all the other players that player p has discarded a tile.
            map<Action, Player *> allActions;
            int playerIndex = 0;
            std::for_each(mPlayers->begin(), mPlayers->end(), [&](Player *playerForReaction) {
                if (currentPlayer != playerForReaction) {
                    Action act = playerForReaction->onOtherPlayerMakeAction(
                            currentPlayer->getID(), currentPlayer->getPlayerName(), a);
                    allActions[act] = playerForReaction;

                    Hand copyHand(playerForReaction->getHand());
                    switch (act.getActionState()) {
                        case Pass:
                            mGame->onPlayerPass(playerForReaction);
                            break;
                        case Win:
                            assert(!act.getTile().isNull());
                            copyHand.pickTile(act.getTile());
                            if (copyHand.testWin()) {
                                mRoundEnded = true;

                                finishRound(Ron, playerForReaction,
                                            calculatePoints(Ron, playerForReaction, playerIndex),
                                            currentPlayer);
                                return;
                            } else {
                                throw std::invalid_argument("False win.");
                            }
                        default:
                            throw std::invalid_argument("ActionState not recognised.");
                    }
                }
                playerIndex++;
            });
            break;
        }
        case Win:
            assert(a.getTile().isNull());
            if (currentPlayer->getHand().testWin()) {
                mRoundEnded = true;
                currentPlayer->getHand().setTsumo();
                finishRound(Tsumo, currentPlayer, calculatePoints(Tsumo, currentPlayer, -1), nullptr);
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

void Board::finishRound(Result result, Player *winner, vector<int> pointVariants, Player *loser) {
    mGame->onRoundFinished(result == Ryuukyoku, winner);

    // Get current time.
    time_t _tm =time(NULL);
    struct tm * currentTime = localtime (&_tm);

    TenhouEncoder logGenerator;
    std::string roundTitle = "Round ";
    roundTitle += std::to_string(mRoundNumber);

    logGenerator.setTitles({roundTitle, asctime(currentTime)});

    vector<std::string> playerNames;
    vector<int> playerPoints;
    vector<TileGroup> playerInitialHands;
    vector<TileGroup> playerPickedTiles;
    vector<TileGroup> playerDiscardedTiles;
    std::for_each(mPlayers->begin(), mPlayers->end(), [&](Player *p) {
        playerNames.push_back(p->getPlayerName());
        playerPoints.push_back(p->getPoint());
        playerInitialHands.push_back(mInitialHands[p]);
        playerPickedTiles.push_back(mPickedTiles[p]);
        playerDiscardedTiles.push_back(mDiscardedTiles[p]);
    });
    logGenerator.setPlayerNames(playerNames);
    logGenerator.setRules("", 0);

    vector<std::string> winningYakuNames;
    std::for_each(mWinningYaku.begin(), mWinningYaku.end(), [&winningYakuNames](Yaku &yaku) {
        winningYakuNames.push_back(yaku.getName());
    });

    logGenerator.setLogs((mRoundNumber - 1) % 16, 0 /* TODO: add sub-round */, 0,
                         playerPoints,
                         {}, {}, playerInitialHands, playerPickedTiles, playerDiscardedTiles,
                         MAHJONG_RESULT_TYPES[result], pointVariants,
                         vector<int>(mPlayers->size() - 1, 0), "Win", winningYakuNames);

    mTenhouUrl = logGenerator.getUrl();
}

vector<int> Board::calculatePoints(Result result, Player *player, int loserIndex) {
    if (player != nullptr) {
        assert(player->getHand().testWin() && "This player cannot win.");
    }

    vector<int> resultPoints(mPlayers->size(), 0);

    switch (result) {
        case Ron:
            resultPoints[std::distance(mPlayers->begin(),
                                 std::find(mPlayers->begin(), mPlayers->end(), player))] = 1;
            resultPoints[loserIndex] = -1;
            mWinningYaku.push_back(YAKU_PINFU);
            break;
        case Tsumo:
            std::for_each(resultPoints.begin(), resultPoints.end(), [](int &point) { point = -1; });
            resultPoints[std::distance(mPlayers->begin(),
                                       std::find(mPlayers->begin(), mPlayers->end(), player))] = 1;
            mWinningYaku.push_back(YAKU_TSUMOHOU);
            break;
        case Ryuukyoku:
            break;
        default:
            throw std::runtime_error("You shouldn't get here!");
    }

    return resultPoints;
}
