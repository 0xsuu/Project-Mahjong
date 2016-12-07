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

#include "TenhouEncoder.h"

#include <prettywriter.h>
#include <algorithm>
#include <Tile.h>
#include <TileGroup.h>

using std::for_each;
using std::string;
using std::vector;

using rapidjson::StringBuffer;
using rapidjson::PrettyWriter;

using mahjong::TenhouEncoder;
using mahjong::Tile;
using mahjong::TileGroup;

void TenhouEncoder::setTitles(vector<string> titles) {
    mWriter.Key("title");
    writeArray(titles);
}
void TenhouEncoder::setPlayerNames(vector<string> names) {
    mWriter.Key("name");
    writeArray(names);
}
void TenhouEncoder::setRules(string ruleName, int aka) {
    mWriter.Key("rule");
    mWriter.StartObject();
    mWriter.Key("disp");
    mWriter.String(ruleName.c_str());
    mWriter.Key("aka");
    mWriter.Int(aka);
    mWriter.EndObject();
}
void TenhouEncoder::setRules(string ruleName, int aka51, int aka52, int aka53) {
    mWriter.Key("rule");
    mWriter.StartObject();
    mWriter.Key("disp");
    mWriter.String(ruleName.c_str());
    mWriter.Key("aka51");
    mWriter.Int(aka51);
    mWriter.Key("aka52");
    mWriter.Int(aka52);
    mWriter.Key("aka53");
    mWriter.Int(aka53);
    mWriter.EndObject();
}
void TenhouEncoder::setLogs(int round, int subRound, int number,
                            vector<int> playerPoints,
                            vector<int> doraTiles, vector<int> hiddenDoraTiles,
                            vector<TileGroup> initialHands,
                            vector<TileGroup> pickedTileGroups,
                            vector<TileGroup> discardedTileGroups,
                            string result,
                            vector<int> pointVariants,
                            vector<int> opponentStates,
                            string winningPointsString,
                            vector<string> winningHandNames) {
    mWriter.Key("log");
    mWriter.StartArray();
    mWriter.StartArray();

    mWriter.StartArray();
    mWriter.Int(round);
    mWriter.Int(subRound);
    mWriter.Int(number);
    mWriter.EndArray();

    writeArray(playerPoints);
    writeArray(doraTiles);
    writeArray(hiddenDoraTiles);

    assert(initialHands.size() == pickedTileGroups.size() &&
                   pickedTileGroups.size() == discardedTileGroups.size());
    for (int i = 0; i < initialHands.size(); i++) {
        auto initialHand = initialHands[i].getData();
        auto pickedTileGroup = pickedTileGroups[i].getData();
        auto discardedTileGroup = discardedTileGroups[i].getData();
        writeArray(initialHand);
        writeArray(pickedTileGroup);
        writeArray(discardedTileGroup);
    }

    mWriter.StartArray();
    mWriter.String(result.c_str());
    writeArray(pointVariants);
    mWriter.StartArray();
    for_each(opponentStates.begin(), opponentStates.end(), [&](int &i) {
        mWriter.Int(i);
    });
    mWriter.String(winningPointsString.c_str());
    for_each(winningHandNames.begin(), winningHandNames.end(), [&](string &s) {
        mWriter.String(s.c_str());
    });
    mWriter.EndArray();
    mWriter.EndArray();

    mWriter.EndArray();
    mWriter.EndArray();
    mWriter.EndObject(); // End the whole JSON session.
}

string TenhouEncoder::getString() {
    return mStringBuffer.GetString();
}

void TenhouEncoder::writeArray(std::vector<string> arr) {
    mWriter.StartArray();
    for_each(arr.begin(), arr.end(), [&](string &s) {
        mWriter.String(s.c_str());
    });
    mWriter.EndArray();
}

void TenhouEncoder::writeArray(std::vector<int> arr) {
    mWriter.StartArray();
    for_each(arr.begin(), arr.end(), [&](int &i) {
        mWriter.Int(i);
    });
    mWriter.EndArray();
}

void TenhouEncoder::writeArray(std::vector<Tile> arr) {
    mWriter.StartArray();
    for_each(arr.begin(), arr.end(), [&](Tile &t) {
        mWriter.Int(toTenhouTile(t));
    });
    mWriter.EndArray();
}

int TenhouEncoder::toTenhouTile(Tile t) {
    return (static_cast<int>(t.getType()) >> 4 + 1) * 10 + t.getNumber();
}
