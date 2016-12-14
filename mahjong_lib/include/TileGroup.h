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

#ifndef MAHJONG_LIB_TILEGROUP_H
#define MAHJONG_LIB_TILEGROUP_H

#include <algorithm>
#include <assert.h>
#include <iostream>
#include <map>

#include "PrintFormat.h"

namespace mahjong {
class TileGroup {
 public:
    TileGroup() {}
    TileGroup(std::vector<Tile> tileData) {
        mTilesData = tileData;
    }
    /**
     * From Tenhou tiles string.
     */
    TileGroup(std::string tileString) {
        auto currentIt = tileString.begin();
        char types[] = {'m', 'p', 's', 'z'};
        std::map<char, TileType> typesMap = {{'m', Character}, {'p', Dot},
                                             {'s', Bamboo}, {'z', Special}};
        for (int i = 0; i < 4; i++) {
            auto findIt = std::find(currentIt, tileString.end(), types[i]);
            if (findIt == tileString.end()) {
                continue;
            } else {
                std::for_each(currentIt, findIt, [&](const char &c) {
                    assert(c <= '9' && c >= '1');
                    mTilesData.push_back(Tile(Handed, typesMap[types[i]], c - '0'));
                });
                currentIt = findIt + 1;
            }
        }
    }

    /**
     * Add tile.
     *
     * Sorting is not guarenteed.
     *
     * @param t The picked tile.
     */
    void addTile(Tile t) {
        mTilesData.push_back(t);
    }

    void removeTile(Tile t) {
        auto indexIt = std::find(mTilesData.begin(), mTilesData.end(), t);
        assert(indexIt != mTilesData.end() && "Cannot discard this tile: not found!");
        assert((*indexIt).getFlag() == Handed && "Cannot discard this tile: not in your hand!");
        mTilesData.erase(indexIt);
    }

    std::string getPrintable() {
        std::string printableString = "";
        std::for_each(mTilesData.begin(), mTilesData.end(), [&printableString](Tile &t) {
            printableString += t.getPrintable();
            printableString += TILES_SEPARATE_PATTERN;
        });
        return printableString;
    }

    void addCombinationIndex(int index, std::vector<Tile> restTiles) {
        Tile t = getTile(index);
        assert(t.getFlag() == Melded ||
               t.getFlag() == Concealed);
        mCombinationIndexes[index] = restTiles;
    }
    void addCurrentCombinationIndex(std::vector<Tile> restTiles) {
        addCombinationIndex(mTilesData.size() - 1, restTiles);
    }

    /**
     * Accessors.
     */
    Tile getTile(int n) { return mTilesData[n]; }
    Tile operator[](int index) { return getTile(index); }
    std::vector<Tile> getData() { return mTilesData; }
    std::map<int, std::vector<Tile>> getCombinationIndexes() { return mCombinationIndexes; }

 protected:
    std::vector<Tile> mTilesData;

    std::map<int, std::vector<Tile>> mCombinationIndexes;
};
}

#endif // MAHJONG_LIB_TILEGROUP_H
