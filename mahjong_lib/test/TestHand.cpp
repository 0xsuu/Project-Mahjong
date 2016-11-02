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

#include <Hand.h>

#include <algorithm>

using mahjong::Tile;
using mahjong::Hand;

using mahjong::Handed;

using mahjong::Character;
using mahjong::Dot;
using mahjong::Bamboo;
using mahjong::Special;

TEST(TestHand, Creations) {
    Hand h1 = Hand();
    Hand h2({Tile(Handed, Character, 1),
             Tile(Handed, Dot, 2),
             Tile(Handed, Bamboo, 3),
             Tile(Handed, Special, 4)});
    h1.addTile(Tile(Handed, Character, 1));
    h1.addTile(Tile(Handed, Dot, 2));
    h1.addTile(Tile(Handed, Bamboo, 3));
    h1.addTile(Tile(Handed, Special, 4));
    EXPECT_EQ(h1.getHand(), h2.getHand());
}

TEST(TestHand, Sorting) {

}