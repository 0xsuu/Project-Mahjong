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

#ifndef MAHJONG_LIB_ACTION_H
#define MAHJONG_LIB_ACTION_H

#include "Tile.h"

namespace mahjong {
/**
 * All the possible actions a player can perform.
 * The value means index for output only.
 */
enum ActionState {
    Pass = 0,
    Cancel = 1,
    Discard = 2,
    Richii = 3,
    Chi = 4,
    Pong = 5,
    Kang = 6,
    ConcealedKang = 7,
    Win = 8
};

class Action {
 public:
    Action() {
        mActionState = Pass;
    }
    Action(ActionState actionState, Tile tile) : mActionState(actionState), mTile(tile) {}

    ActionState getActionState() const { return mActionState; }
    Tile getTile() { return mTile; }

    bool operator<(const Action &a) const {
        return static_cast<int>(mActionState) < static_cast<int>(a.getActionState());
    }

 private:
    ActionState mActionState;
    Tile mTile;
};
} // namespace mahjong.

#endif // MAHJONG_LIB_ACTION_H