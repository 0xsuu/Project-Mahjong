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

#ifndef MAHJONG_LIB_PLAYER_H
#define MAHJONG_LIB_PLAYER_H

#include <map>
#include <string>
#include <vector>

#include "Action.h"
#include "Board.h"
#include "Constants.h"
#include "Hand.h"
#include "Tile.h"

namespace mahjong {
class Player {
 public:
    Player(const std::string playerName) : mPlayerName(playerName) {}
    virtual ~Player() {}

    void setupPlayer(const int ID, Wind seatPosition, Hand initialHand, Board *board);
    void resetPlayer(Hand hand);

    void shiftSeatPosition();
    void discardTile(Tile t);
    void pickTile(Tile t);

    // Callback interface.
    /**
     * This is called when each player plays.
     *
     * Note: When it is your turn, the tile you received is added to your hand automatically,
     * the parameter tile is just for information.
     *
     * @param tile: The tile they discarded or the tile you received.
     * @return An ActionState indicate what action you gonna make.
     */
    virtual Action onTurn(int playerID, Tile tile) = 0;

    virtual Action onOtherPlayerMakeAction(int playerID, std::string playerName, Action action) = 0;

    void onRoundFinished(bool drained, Player *winner) {

    }

    // Accessors.
    int getID() { return mID; }
    std::string getPlayerName() { return mPlayerName; }
    Wind getSeatPosition() { return mSeatPosition; }
    Hand getHand() { return mHand; }
    std::map<int, std::string> getPlayerIDAndDiscardedTiles();
    std::string getPrintable();
    int getPoint() { return point; }
    void addPoint(int number) { point += number; }

 protected:
    bool mIsMyTurn;
    int mCurrentPlayerID = 0;

    int point;

 private:
    int mID;
    std::string mPlayerName;
    Wind mSeatPosition;
    Hand mHand;
    Board *mBoard;
};

struct PlayerWrapper : Player {
    PlayerWrapper(std::string playerName) : Player(playerName) {}

    Action onTurn(int playerID, Tile tile) override {
        throw std::runtime_error("PlayerWrapper class cannot be called.");
    }
    Action onOtherPlayerMakeAction(int playerID,
                                   std::string playerName,
                                   Action action) override {
        throw std::runtime_error("PlayerWrapper class cannot be called.");
    }
};
} // namespace mahjong.

#endif // MAHJONG_LIB_PLAYER_H
