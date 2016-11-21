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

namespace mahjong {
class TileGroup {
 public:
    TileGroup() {}
    TileGroup(std::vector<Tile> tileData) {
        mTilesData = tileData;
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

    /**
     * Accessors.
     */
    Tile getTile(int n) { return mTilesData[n]; }
    Tile operator[](int index) { return getTile(index); }
    std::vector<Tile> getHand() { return mTilesData; }

 //protected:
    std::vector<Tile> mTilesData;
};
}

#endif // MAHJONG_LIB_TILEGROUP_H
