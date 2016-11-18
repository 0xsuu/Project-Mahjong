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

#include "Hand.h"
#include "Tile.h"

#define ACTION_STATE_WIN   0b00001;
#define ACTION_STATE_CHI   0b00010;
#define ACTION_STATE_PONG  0b00100;
#define ACTION_STATE_KANG  0b01000;
#define ACTION_STATE_CKANG 0b10000;

namespace mahjong {
enum SeatPosition {
    East = 0,
    South = 1,
    West = 2,
    North = 3
};

class Player {
 public:
    Player(std::string playerName) : mPlayerName(playerName) {}

    void setupPlayer(int ID, SeatPosition seatPosition, Hand initialHand);

    void shiftSeatPosition();

    // Listener interface.
    virtual void onNextPlayerDiscard(int actionState, Tile tile); // AS: Chi, Pong, Kang, Win
    virtual Tile onYourTurn(int actionState); // AS: CKang, Win
    virtual void onCanWin();

    // Accessors.
    int getID() { return mID; }
    std::string getPlayerName() { return mPlayerName; }
    SeatPosition getSeatPosition() { return mSeatPosition; }
    Hand getHand() { return mHand; }

 protected:
    void makeDiscardTile(Tile tile);
    void makeDiscardTile(int index);

 private:
    int mID;
    std::string mPlayerName;
    SeatPosition mSeatPosition;
    Hand mHand;
};
} // namespace mahjong.

#endif // MAHJONG_LIB_PLAYER_H
