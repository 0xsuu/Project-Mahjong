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

#ifndef MAHJONG_LIB_TILESTACK_H
#define MAHJONG_LIB_TILESTACK_H

namespace Mahjong {

class TileStack {
 public:
    /**
     * Constructor for the Tile Stack, mainly aimed for the abstraction
     * of the randomicity of the game.
     *
     * @param tileCount Number of all the available tiles.
     * @param doraTile Contains dora tile or not.
     * @param notPlayingCount Some leftover tiles for
     * @return
     */
    TileStack(int tileCount, bool doraTile, int notPlayingCount);
};

}
#endif //MAHJONG_LIB_TILESTACK_H
