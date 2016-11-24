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

#ifndef MAHJONG_LIB_PRINTFORMAT_H
#define MAHJONG_LIB_PRINTFORMAT_H

/**
 * @brief The terminal printables for Mahjong tiles.
 *
 * A complete tile printable should be one of:
 * - MAHJONG_[NUMBER] + MAHJONG_[C | D | B]
 * - MAHJONG_S[NUMBER]
 * - MAHJONG_HAND
 */

#include <string>

#define TILES_SEPARATE_PATTERN "  "

const std::string MAHJONG_TYPE[] = {"萬", "筒", "條"};
const std::string MAHJONG_NUMBER[] = {"一", "二", "三", "四", "五", ".五", "六", "七", "八", "九"};
const std::string MAHJONG_SPECIAL[] = {"東", "南", "西", "北", "中", "發", "白"};

const std::string MAHJONG_OTHERS[] = {"X"};

#endif //MAHJONG_LIB_PRINTFORMAT_H
