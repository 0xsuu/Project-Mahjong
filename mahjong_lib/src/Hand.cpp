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

#include <assert.h>

using std::vector;

using mahjong::Tile;
using mahjong::Hand;


void Hand::sort() {
    std::sort(mTilesData.begin(), mTilesData.end());
}

void Hand::pickTile(Tile t) {
    if (mTilesData.empty()) {
        mTilesData.push_back(t);
    } else {
        for (auto it = mTilesData.begin(); it < mTilesData.end(); it++) {
            if (t <= *it) {
                mTilesData.insert(it, t);
                return;
            }
        }
        mTilesData.push_back(t);
    }
}

void Hand::discardTile(int index) {
    assert(index < mTilesData.size());
    assert(mTilesData[index].getFlag() == Handed);
    mTilesData.erase(mTilesData.begin() + index);
}

void Hand::discardTile(Tile tile) {
    removeTile(tile);
}

inline void winningHandSimple(bool &found, vector <Tile> *hand) {
    if (hand->size() == 0) {
        found = true;
    } else if (hand->size() < 3) {
        // Pass through the end to release memory.
    } else {
        auto it = hand->begin();
        // Quad.
        if (hand->size() >= 4) {
            if (*it == *(it + 1) && *(it + 1) == *(it + 2) && *(it + 2) == *(it + 3)) {
                vector<Tile> *h = new vector<Tile>(*hand);
                long startIndex = std::distance(hand->begin(), it);
                h->erase(h->begin() + startIndex, h->begin() + startIndex + 4);
                winningHandSimple(found, h);
            }
        }
        // Trio.
        if (*it == *(it + 1) && *(it + 1) == *(it + 2)) {
            vector<Tile> *h = new vector<Tile>(*hand);
            long startIndex = std::distance(hand->begin(), it);
            h->erase(h->begin() + startIndex, h->begin() + startIndex + 3);
            winningHandSimple(found, h);
        }
        // Straight.
        auto itNext = std::find(it, hand->end(), *it + 1);
        if (itNext < hand->end() - 1) {
            auto itNextNext = std::find(itNext, hand->end(), *itNext + 1);
            if (itNextNext < hand->end()) {
                vector<Tile> *h = new vector<Tile>(*hand);
                h->erase(h->begin() + std::distance(hand->begin(), itNextNext));
                h->erase(h->begin() + std::distance(hand->begin(), itNext));
                h->erase(h->begin() + std::distance(hand->begin(), it));
                winningHandSimple(found, h);
            }
        }
    }
    delete hand;
}

bool Hand::testWin() {
    vector<Tile> hand(mTilesData);

    // Removing all melded & concealed tiles.
    auto it = hand.begin();
    while ((*it).getFlag() == Melded || (*it).getFlag() == Concealed) {
        it++;
    }
    hand.erase(hand.begin(), it);

    // Removing all possible pairs.
    vector<Tile> removedPair;
    for (auto it = hand.begin(); it < hand.end() - 1; it++) {
        if (*it == *(it + 1)) {
            if (std::find(removedPair.begin(), removedPair.end(), *it) != removedPair.end()) {
                continue;
            } else {
                removedPair.push_back(*it);
                vector<Tile> *h = new vector<Tile>(hand);
                long index = std::distance(hand.begin(), it);
                h->erase(h->begin() + index, h->begin() + index + 2);
                auto itOffset = it + 1;
                while (itOffset == it) {
                    itOffset++;
                }
                it = itOffset;

                bool found = false;
                winningHandSimple(found, h);
                if (found) {
                    return true;
                }
            }
        }
    }
    return false;
}

vector<Tile> Hand::canChi(Tile tile) const {
    if (tile.getType() == Special) {
        return {};
    }

    auto itNext = std::find(mTilesData.begin(), mTilesData.end(), tile + 1);
    auto itNextNext = std::find(mTilesData.begin(), mTilesData.end(), tile + 2);
    auto itPrev = std::find(mTilesData.begin(), mTilesData.end(), tile - 1);
    auto itPrevPrev = std::find(mTilesData.begin(), mTilesData.end(), tile - 2);

    vector<Tile> retVec;
    if (itNext != mTilesData.end() && itNextNext != mTilesData.end()) {
        retVec.push_back(*itNext);
        retVec.push_back(*itNextNext);
    }
    if (itNext != mTilesData.end() && itPrev != mTilesData.end()) {
        retVec.push_back(*itNext);
        retVec.push_back(*itPrev);
    }
    if (itPrev != mTilesData.end() && itPrevPrev != mTilesData.end()) {
        retVec.push_back(*itPrev);
        retVec.push_back(*itPrevPrev);
    }

    return retVec;
}

bool Hand::canPong(Tile tile) const {
    return std::count(mTilesData.begin(), mTilesData.end(), tile) >= 2;
}

bool Hand::canKang(Tile tile) const {
    return std::count(mTilesData.begin(), mTilesData.end(), tile) >= 3;
}
