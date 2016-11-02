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

#include <iostream>
#include <string>

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

TEST(TileTest, ChangeTileFlag) {
    Tile testTile(Hand, Special, 5);
    EXPECT_EQ(testTile.getFlag(), Hand);
    testTile.setMeld();
    EXPECT_EQ(testTile.getFlag(), Meld);
    testTile.setConceal();
    EXPECT_EQ(testTile.getFlag(), Conceal);
}

TEST(TileTest, PrintableTest) {
    Tile C1(Hand, Character, 1);
    Tile C2(Hand, Character, 2);
    Tile C3(Hand, Character, 3);
    Tile D4(Hand, Dot, 4);
    Tile D5(Hand, Dot, 5);
    Tile D6(Hand, Dot, 6);
    Tile B7(Hand, Bamboo, 7);
    Tile B8(Hand, Bamboo, 8);
    Tile B9(Hand, Bamboo, 9);
    Tile S1(Hand, Special, 1);
    Tile S2(Hand, Special, 2);
    Tile S3(Hand, Special, 3);
    Tile S4(Hand, Special, 4);
    Tile S5(Hand, Special, 5);
    Tile S6(Hand, Special, 6);
    Tile S7(Hand, Special, 7);

    testing::internal::CaptureStdout();
    std::cout << C1.getPrintable() << C2.getPrintable() << C3.getPrintable() <<
              D4.getPrintable() << D5.getPrintable() << D6.getPrintable() <<
              B7.getPrintable() << B8.getPrintable() << B9.getPrintable() <<
              S1.getPrintable() << S2.getPrintable() << S3.getPrintable() <<
              S4.getPrintable() << S5.getPrintable() << S6.getPrintable() <<
              S7.getPrintable();
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output, "一萬二萬三萬四筒五筒六筒七條八條九條東南西北中發白");
}
