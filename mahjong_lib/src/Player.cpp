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

#include <Board.h>

#include <iostream>

using std::map;
using std::string;
using std::vector;

using mahjong::Hand;
using mahjong::Wind;
using mahjong::Player;

void Player::setupPlayer(int ID,
                         Wind seatPosition,
                         mahjong::Hand initialHand,
                         mahjong::Board *board) {
    mID = ID;
    mSeatPosition = seatPosition;
    mHand = initialHand;
    mBoard = board;
}

void Player::resetPlayer(Hand hand) {
    mHand.clear();
    mHand = hand;
}

void Player::shiftSeatPosition() {
    mSeatPosition == North ? mSeatPosition = East :
       mSeatPosition = static_cast<Wind>(static_cast<int>(mSeatPosition) + 1);
}

void Player::discardTile(Tile t) {
    mHand.discardTile(t);
}

void Player::pickTile(Tile t) {
    mHand.pickTile(t);
}

string Player::getPrintable() {
    string retString = "";
    retString = retString + MAHJONG_SPECIAL[getSeatPosition()] + ": " +
            getPlayerName() + " ID" + std::to_string(getID());
    return retString;
}

map<int, string> Player::getPlayerIDAndDiscardedTiles() {
    map<int, string> retMap;
    auto playerAndDiscardedTiles = mBoard->getPlayerAndDiscardedTiles();
    for (auto it = playerAndDiscardedTiles.begin(); it != playerAndDiscardedTiles.end(); it++) {
        string s = "";
        s += (*it).first->getPrintable() + ":\n" + (*it).second.getPrintable();
        retMap[(*it).first->getID()] = s;
    }
    return retMap;
}
