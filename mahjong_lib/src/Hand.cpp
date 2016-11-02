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

#include <Hand.h>

#include <algorithm>
#include <iostream>

using std::vector;

using mahjong::Tile;
using mahjong::Hand;

Hand::Hand(vector<Tile> hand) {
    mHand = hand;
}

void Hand::sort() {
    std::sort(mHand.begin(), mHand.end());
}

void Hand::pickTile(Tile t) {
    for (auto it = mHand.begin(); it < mHand.end(); it++) {
        if (t <= *it) {
            mHand.insert(it, t);
            break;
        }
    }
}

void Hand::discardTile(int index) {
    mHand.erase(mHand.begin() + index);
}

void Hand::discardTile(Tile tile) {
    auto indexIt = std::find(mHand.begin(), mHand.end(), tile);
    mHand.erase(indexIt);
}

inline bool winningHand(vector<Tile> hand) {
    while(hand.size() > 0) {
        if (hand[0] == hand[1] && hand[1] == hand[2]) {
            if (hand.size() >= 4 && hand[2] == hand[3]) {
                // Quad.
                hand.erase(hand.begin());
            }
            hand.erase(hand.begin(), hand.begin() + 3);
            // Trio.
            continue;
        } else if (hand[0] + 2 == hand[1] + 1 && hand[1] + 1 == hand[2]) {
            // Straight.
            hand.erase(hand.begin(), hand.begin() + 3);
            continue;
        } else {
            return false;
        }
    }
    return true;
}

bool Hand::canWin() {
    vector<Tile> hand(mHand);

    // Removing all melded & concealed tiles.
    int removedCount = 0;
    auto it = hand.begin();
    while ((*it).getFlag() == Melded || (*it).getFlag() == Concealed) {
        it++;
    }
    hand.erase(hand.begin(), it);

    // Removing all possible pairs.
    for (auto it = hand.begin(); it < hand.end() - 1; it++) {
        if (*it == *(it + 1)) {
            vector<Tile> h(hand);
            long index = std::distance(hand.begin(), it);
            h.erase(h.begin() + index);
            h.erase(h.begin() + index + 1);
            auto itOffset = it + 1;
            while (itOffset == it) {
                itOffset++;
            }
            it = itOffset;

            if (winningHand(h)) {
                return true;
            }
        }
    }
    return false;
}
