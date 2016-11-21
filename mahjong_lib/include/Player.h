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

#include <string>
#include <vector>

#include "Action.h"
#include "Hand.h"
#include "Tile.h"

namespace mahjong {
enum Wind {
    East = 0,
    South = 1,
    West = 2,
    North = 3
};

const Wind Winds[] = {East, South, West, North};

class Player {
 public:
    Player(std::string playerName) : mPlayerName(playerName) {}

    void setupPlayer(int ID, Wind seatPosition, Hand initialHand);

    void shiftSeatPosition();

    // Listeners interface.
    /**
     * This is called when each player plays.
     *
     * @param tile: The tile they discarded or the tile you received.
     * @return An ActionState indicate what action you gonna make.
     */
    virtual ActionState onTurn(bool isMyTurn, Tile tile);

    // Accessors.
    int getID() { return mID; }
    std::string getPlayerName() { return mPlayerName; }
    Wind getSeatPosition() { return mSeatPosition; }
    Hand getHand() { return mHand; }

 protected:
    void makeDiscardTile(Tile tile);
    void makeDiscardTile(int index);

 private:
    int mID;
    std::string mPlayerName;
    Wind mSeatPosition;
    Hand mHand;
};
} // namespace mahjong.

#endif // MAHJONG_LIB_PLAYER_H
