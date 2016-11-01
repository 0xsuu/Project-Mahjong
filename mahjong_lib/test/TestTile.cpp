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

#include <gtest/gtest.h>

#include <Tile.h>

using mahjong::Tile;
using mahjong::Hand;
using mahjong::Meld;
using mahjong::Conceal;
using mahjong::Character;
using mahjong::Dot;
using mahjong::Bamboo;
using mahjong::Special;

TEST(TileTest, CreateNewTile) {
    Tile testTile(Meld, Special, 5);
    EXPECT_EQ(testTile.getFlag(), Meld);
    EXPECT_EQ(testTile.getType(), Special);
    EXPECT_EQ(testTile.getNumber(), 5);
}
