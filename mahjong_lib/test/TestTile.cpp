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
using mahjong::Handed;
using mahjong::Melded;
using mahjong::Concealed;
using mahjong::Character;
using mahjong::Dot;
using mahjong::Bamboo;
using mahjong::Special;

TEST(TileTest, CreateNewTile) {
    Tile testTile(Melded, Special, 5);
    EXPECT_EQ(testTile.getFlag(), Melded);
    EXPECT_EQ(testTile.getType(), Special);
    EXPECT_EQ(testTile.getNumber(), 5);
}

TEST(TileTest, ChangeTileFlag) {
    Tile testTile(Handed, Special, 5);
    EXPECT_EQ(testTile.getFlag(), Handed);
    testTile.setMeld();
    EXPECT_EQ(testTile.getFlag(), Melded);
    testTile.setConceal();
    EXPECT_EQ(testTile.getFlag(), Concealed);
}

TEST(TileTest, PrintableTest) {
    Tile C1(Handed, Character, 1);
    Tile C2(Handed, Character, 2);
    Tile C3(Handed, Character, 3);
    Tile D4(Handed, Dot, 4);
    Tile D5(Handed, Dot, 5);
    Tile D5D(Handed, Dot, 5, true);
    Tile D6(Handed, Dot, 6);
    Tile B7(Handed, Bamboo, 7);
    Tile B8(Handed, Bamboo, 8);
    Tile B9(Handed, Bamboo, 9);
    Tile S1(Handed, Special, 1);
    Tile S2(Handed, Special, 2);
    Tile S3(Handed, Special, 3);
    Tile S4(Handed, Special, 4);
    Tile S5(Handed, Special, 5);
    Tile S6(Handed, Special, 6);
    Tile S7(Handed, Special, 7);

    testing::internal::CaptureStdout();
    std::cout << C1.getPrintable() << C2.getPrintable() << C3.getPrintable() <<
              D4.getPrintable() << D5.getPrintable() << D5D.getPrintable() << D6.getPrintable() <<
              B7.getPrintable() << B8.getPrintable() << B9.getPrintable() <<
              S1.getPrintable() << S2.getPrintable() << S3.getPrintable() <<
              S4.getPrintable() << S5.getPrintable() << S6.getPrintable() <<
              S7.getPrintable();
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output, "一萬二萬三萬四筒五筒.五筒六筒七條八條九條東南西北中發白");
}

TEST(TileTest, DoraTileTest) {
    Tile testTile(Melded, Dot, 5, true);
    EXPECT_TRUE(testTile.isDora()) << "Dora D5";
    EXPECT_EQ(testTile.getNumber(), 5) << "Dora D5";
    Tile testTile2(Melded, Special, 5);
    EXPECT_FALSE(testTile2.isDora());
    Tile testTile3(Melded, Dot, 7);
    EXPECT_EQ(testTile3.getNumber(), 7);
    Tile testTile4(Melded, Dot, 2);
    EXPECT_EQ(testTile4.getNumber(), 2);
    Tile testTile5(Melded, Dot, 5);
    EXPECT_FALSE(testTile5.isDora()) << "Not Dora D5";
    EXPECT_EQ(testTile5.getNumber(), 5) << "Not Dora D5";
    Tile testTile6(Melded, Special, 6);
    EXPECT_EQ(testTile6.getNumber(), 6);
    Tile testTile7(Melded, Special, 2);
    EXPECT_EQ(testTile7.getNumber(), 2);
}
