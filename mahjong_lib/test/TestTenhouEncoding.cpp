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

#include <TenhouEncoder.h>

using mahjong::TenhouEncoder;

TEST(TestTenhouEncoding, TestConstructingExample) {
    TenhouEncoder t;

    t.setTitles({"第二期　天鳳名人戦", "第１節　Ａ卓　１戦目"});
    t.setPlayerNames({"Ⓢ福地誠", "Ⓟ多井隆晴", "Cさん", "Ⓟ石橋伸洋"});
    t.setRules("般南喰赤", 1);
    t.setLogs(0, 0, 0, {30000, 30000, 30000, 30000}, {24}, {},
              {12,17,21,22,25,26,27,32,33,34,37,37,43}, );
    std::cout << t.getString() << '\n';
    ASSERT_NE("{\"title\":[\"第二期　天鳳名人戦\","
                      "\"第１節　Ａ卓　１戦目\"],"
                      "\"name\":[\"Ⓢ福地誠\",\"Ⓟ多井隆晴\",\"Cさん\",\"Ⓟ石橋伸洋\"],"
                      "\"rule\":{\"disp\":\"般南喰赤\",\"aka\":1},"
                      "\"log\":[[[0,0,0],[30000,30000,30000,30000],[24],[],"
                      "[12,17,21,22,25,26,27,32,33,34,37,37,43],"
                      "[39,32,46,35,\"32p3232\",33,\"37p3737\",31],"
                      "[43,39,12,46,21,22,17,60],"
                      "[16,16,19,22,22,23,26,27,29,39,42,45,47],"
                      "[13,28,38,21,26,23,18,12],[19,39,45,38,42,47,13,60],"
                      "[11,11,14,15,16,17,19,28,37,41,43,44,46],"
                      "[41,14,\"1111p11\",38,32,35,37,33,14],"
                      "[28,37,43,60,60,60,60,44,33],"
                      "[11,51,17,18,24,52,32,33,36,36,43,44,45],"
                      "[31,21,26,19,44,18],[43,11,45,44,60,60],"
                      "[\"和了\",[2900,0,-2900,0],[0,2,0,\"30符2飜2900点\",\"断幺九(1飜)\",\"ドラ(1飜)\"]]]]}", "");
}
