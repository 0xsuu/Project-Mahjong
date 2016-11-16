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

using mahjong::Tile;
using mahjong::Hand;

using mahjong::Handed;
using mahjong::Melded;
using mahjong::Concealed;

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
    Hand h({Tile(Handed, Bamboo, 1),
            Tile(Handed, Bamboo, 1),
            Tile(Handed, Bamboo, 1),
            Tile(Melded, Special, 4),
            Tile(Melded, Special, 4),
            Tile(Melded, Special, 4),
            Tile(Handed, Dot, 9),
            Tile(Handed, Character, 3),
            Tile(Handed, Dot, 7),
            Tile(Handed, Character, 5),
            Tile(Handed, Character, 6),
            Tile(Handed, Dot, 8),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7)});
    h.sort();

    Hand h2 ({Tile(Concealed, Special, 7),
              Tile(Concealed, Special, 7),
              Tile(Concealed, Special, 7),
              Tile(Concealed, Special, 7),
              Tile(Melded, Special, 4),
              Tile(Melded, Special, 4),
              Tile(Melded, Special, 4),
              Tile(Handed, Character, 3),
              Tile(Handed, Character, 5),
              Tile(Handed, Character, 6),
              Tile(Handed, Dot, 7),
              Tile(Handed, Dot, 8),
              Tile(Handed, Dot, 9),
              Tile(Handed, Bamboo, 1),
              Tile(Handed, Bamboo, 1),
              Tile(Handed, Bamboo, 1)});

    EXPECT_EQ(h.getHand(), h2.getHand());
}

TEST(TestHand, PickTile) {
    Hand h({Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Melded, Special, 4),
            Tile(Melded, Special, 4),
            Tile(Melded, Special, 4),
            Tile(Handed, Character, 3),
            Tile(Handed, Character, 5),
            Tile(Handed, Character, 6),
            Tile(Handed, Dot, 7),
            Tile(Handed, Dot, 8),
            Tile(Handed, Dot, 9),
            Tile(Handed, Bamboo, 1),
            Tile(Handed, Bamboo, 1),
            Tile(Handed, Bamboo, 1)});
    h.pickTile(Tile(Handed, Character, 2));
    h.pickTile(Tile(Handed, Character, 3));

    Hand h2 ({Tile(Concealed, Special, 7),
              Tile(Concealed, Special, 7),
              Tile(Concealed, Special, 7),
              Tile(Concealed, Special, 7),
              Tile(Melded, Special, 4),
              Tile(Melded, Special, 4),
              Tile(Melded, Special, 4),
              Tile(Handed, Character, 2),
              Tile(Handed, Character, 3),
              Tile(Handed, Character, 3),
              Tile(Handed, Character, 5),
              Tile(Handed, Character, 6),
              Tile(Handed, Dot, 7),
              Tile(Handed, Dot, 8),
              Tile(Handed, Dot, 9),
              Tile(Handed, Bamboo, 1),
              Tile(Handed, Bamboo, 1),
              Tile(Handed, Bamboo, 1)});

    EXPECT_EQ(h.getHand(), h2.getHand());
}

TEST(TestHand, DiscardTile) {
    Hand h({Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Melded, Special, 4),
            Tile(Melded, Special, 4),
            Tile(Melded, Special, 4),
            Tile(Handed, Dot, 7),
            Tile(Handed, Dot, 8),
            Tile(Handed, Dot, 9)});
    h.discardTile(4);
    h.discardTile(4);
    h.discardTile(4);
    h.discardTile(Tile(Handed, Dot, 7));
    h.discardTile(Tile(Handed, Dot, 8));
    h.discardTile(Tile(Handed, Dot, 9));


    Hand h2 ({Tile(Concealed, Special, 7),
              Tile(Concealed, Special, 7),
              Tile(Concealed, Special, 7),
              Tile(Concealed, Special, 7)});

    EXPECT_EQ(h.getHand(), h2.getHand());
}

TEST(TestHand, TestWinningJudgement_Simple) {
    Hand h({Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Melded, Special, 4),
            Tile(Melded, Special, 4),
            Tile(Melded, Special, 4),
            Tile(Handed, Dot, 1),
            Tile(Handed, Dot, 2),
            Tile(Handed, Dot, 3),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 7),
            Tile(Handed, Dot, 7)});
    EXPECT_TRUE(h.testWin());
}

TEST(TestHand, TestWinningJudgement_3ContinuousPairs) {
    Hand h({Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 2),
            Tile(Handed, Character, 2),
            Tile(Handed, Character, 3),
            Tile(Handed, Character, 3),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 7),
            Tile(Handed, Dot, 7)});
    EXPECT_TRUE(h.testWin());
}

TEST(TestHand, TestWinningJudgement_MultipleSolutions) {
    Hand h({Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 2),
            Tile(Handed, Character, 3),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 7),
            Tile(Handed, Dot, 7)});
    EXPECT_TRUE(h.testWin());
}

TEST(TestHand, TestWinningJudgement_MixingPairWithCombinationsSimple) {
    Hand h({Tile(Handed, Character, 1),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 2),
            Tile(Handed, Character, 3),
            Tile(Handed, Character, 4),
            Tile(Handed, Character, 4),
            Tile(Handed, Character, 4),
            Tile(Handed, Dot, 1),
            Tile(Handed, Dot, 2),
            Tile(Handed, Dot, 3),
            Tile(Handed, Special, 7),
            Tile(Handed, Special, 7),
            Tile(Handed, Special, 7)});
    EXPECT_TRUE(h.testWin());
}

TEST(TestHand, TestWinningJudgement_MixingPairWithCombinationsComplex) {
    Hand h({Tile(Handed, Character, 1),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 2),
            Tile(Handed, Character, 2),
            Tile(Handed, Character, 3),
            Tile(Handed, Character, 3),
            Tile(Handed, Dot, 1),
            Tile(Handed, Dot, 2),
            Tile(Handed, Dot, 3),
            Tile(Handed, Special, 7),
            Tile(Handed, Special, 7),
            Tile(Handed, Special, 7)});
    EXPECT_TRUE(h.testWin());
}

TEST(TestHand, TestWinningJudgement_Failure) {
    Hand h({Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Concealed, Special, 7),
            Tile(Handed, Character, 1),
            Tile(Handed, Character, 2),
            Tile(Handed, Character, 2),
            Tile(Handed, Character, 2),
            Tile(Handed, Character, 3),
            Tile(Handed, Character, 3),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 4),
            Tile(Handed, Dot, 7),
            Tile(Handed, Dot, 7)});
    EXPECT_FALSE(h.testWin());
}

