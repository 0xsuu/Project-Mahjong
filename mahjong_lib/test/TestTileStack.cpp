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

#include <numeric>
#include <vector>

#include <gtest/gtest.h>

#include <TileStack.h>

using std::vector;

using mahjong::TileStack;

TEST(TestTileStack, TileStackCreation) {
    TileStack tileStack(mahjong::JAPANESE_MAHJONG_TILE_SET, false, 0);
    TileStack tileStack2(mahjong::COMPETITIVE_MAHJONG_TILE_SET, false, 0);
    (void) tileStack;
    (void) tileStack2;
}

TEST(TestTileStack, TileStackDice) {
    TileStack tileStack(mahjong::JAPANESE_MAHJONG_TILE_SET, false, 0);
    vector<int> diceCount = {0, 0, 0, 0, 0, 0};
    for (int i = 0; i < 100000; ++i) {
        diceCount[tileStack.throwDice() - 1] ++;
    }

    double sum = std::accumulate(diceCount.begin(), diceCount.end(), 0);

    EXPECT_NEAR(1.0 / 6.0, diceCount[0] / sum, 0.01);
    EXPECT_NEAR(1.0 / 6.0, diceCount[1] / sum, 0.01);
    EXPECT_NEAR(1.0 / 6.0, diceCount[2] / sum, 0.01);
    EXPECT_NEAR(1.0 / 6.0, diceCount[3] / sum, 0.01);
    EXPECT_NEAR(1.0 / 6.0, diceCount[4] / sum, 0.01);
    EXPECT_NEAR(1.0 / 6.0, diceCount[5] / sum, 0.01);
}

TEST(TestTileStack, TileStackDrawAllTiles) {
    TileStack tileStack(mahjong::JAPANESE_MAHJONG_TILE_SET, false, 0);
    vector<int> tileSet(9 * 3 + 7, 0);
    for (int i = 0; i < static_cast<int>(mahjong::JAPANESE_MAHJONG_TILE_SET); ++i) {
        mahjong::Tile tile = tileStack.drawTile();
        int offset;
        switch (tile.getType()) {
            case mahjong::Character:
                offset = 0;
                break;
            case mahjong::Dot:
                offset = 1;
                break;
            case mahjong::Bamboo:
                offset = 2;
                break;
            case mahjong::Special:
                offset = 3;
                break;
            default:
                FAIL();
        }
        tileSet[offset * 9 + tile.getNumber() - TILE_NUMBER_OFFSET]++;
    }
    ASSERT_TRUE(tileStack.isEmpty());

    int count = 0;
    std::for_each(tileSet.begin(), tileSet.end(), [&count](int &c) {
        EXPECT_EQ(c, 4) << "Wrong ID: " << count;
        count++;
    });
}

TEST(TestTileStack, TileStackDrawRandomicity) {
    int count = 0;
    for (int i = 0; i < 12000; i++) {
        TileStack tileStack(mahjong::JAPANESE_MAHJONG_TILE_SET, false, 0);
        if (tileStack.drawTile() == mahjong::Tile(mahjong::Handed, mahjong::Character, 1)) {
            count++;
        }
    }
    EXPECT_NEAR(4.0 / static_cast<double>(mahjong::JAPANESE_MAHJONG_TILE_SET), count / 12000.0, 0.005);
}
