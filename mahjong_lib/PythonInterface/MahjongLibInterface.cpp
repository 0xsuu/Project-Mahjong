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

#include <boost/python.hpp>

#include <Hand.h>
#include <Player.h>

using mahjong::Action;
using mahjong::ActionState;
using mahjong::Board;
using mahjong::Game;
using mahjong::Hand;
using mahjong::Tile;
using mahjong::TileGroup;
using mahjong::TileFlag;
using mahjong::TileType;
using mahjong::TileSetType;
using mahjong::Player;
using mahjong::PlayerWrapper;
using mahjong::Wind;

BOOST_PYTHON_MODULE(libmahjong) {
    using boost::python::class_;
    using boost::python::enum_;
    using boost::python::init;
    using boost::python::def;

    /**
     * Expose enums.
     */
    enum_<TileFlag>("TileFlag")
            .value("Concealed", mahjong::Concealed)
            .value("Melded", mahjong::Melded)
            .value("Handed", mahjong::Handed);
    enum_<TileType>("TileType")
            .value("Character", mahjong::Character)
            .value("Dot", mahjong::Dot)
            .value("Bamboo", mahjong::Bamboo)
            .value("Special", mahjong::Special);
    enum_<ActionState>("ActionState")
            .value("Pass", mahjong::Pass)
            .value("Cancel", mahjong::Cancel)
            .value("Discard", mahjong::Discard)
            .value("Richii", mahjong::Richii)
            .value("Chi", mahjong::Chi)
            .value("Pong", mahjong::Pong)
            .value("Kang", mahjong::Kang)
            .value("ConcealedKang", mahjong::ConcealedKang)
            .value("Win", mahjong::Win);
    enum_<Wind >("Wind")
            .value("East", mahjong::East)
            .value("South", mahjong::South)
            .value("West", mahjong::West)
            .value("North", mahjong::North);

    /**
     * Expose Tile class.
     */
    class_<Tile>("Tile",
                 init<>())
            .def(init<const TileFlag, const TileType, const int, bool>())
            .def(init<const TileFlag, const TileType, const int>())
            .def(init<const uint8_t, bool>())
            .def("get_flag", &Tile::getFlag)
            .def("get_type", &Tile::getType)
            .def("get_umber", &Tile::getNumber)
            .def("is_dora", &Tile::isDora)
            .def("is_null", &Tile::isNull)
            .def("get_data", &Tile::getData)
            .def("get_printable", &Tile::getPrintable)
            .def("set_meld", &Tile::setMeld)
            .def("set_conceal", &Tile::setConceal)
            .def("__eq__", &Tile::operator==)
            .def("__ne__", &Tile::operator!=)
            .def("__lt__", &Tile::operator<)
            .def("__le__", &Tile::operator<=)
            .def("__add__", &Tile::operator+)
            .def("__sub__", &Tile::operator-);

    /**
     * Expose Hand Class.
     */
    bool (Hand::*testSelfWin)() = &Hand::testWin;
    bool (Hand::*testDiscardWin)(Tile) = &Hand::testWin;
     class_<Hand>("Hand",
                  init<>())
             .def(init<std::string>())
             .def("test_win", testSelfWin)
             .def("test_win", testDiscardWin)
             .def("get_data", &Hand::getData);

    /**
     * Expose Player class.
     */
    class_<PlayerWrapper>("Player",
                          init<std::string>())
            .def("on_turn", &PlayerWrapper::onTurn)
            .def("on_other_player_make_action", &PlayerWrapper::onOtherPlayerMakeAction)
            .def("get_player_name", &PlayerWrapper::getPlayerName)
            .def("get_hand", &PlayerWrapper::getHand)
            .def("get_id", &PlayerWrapper::getID)
            .def("setup_player", &PlayerWrapper::setupPlayer);

    /**
     * Expose Action class.
     */
    class_<Action>("Action",
                   init<>())
            .def(init<ActionState, Tile>())
            .def("get_action_state", &Action::getActionState)
            .def("get_tile", &Action::getTile)
            .def("__lt__", &Action::operator<);

    /**
     * Expose Board class.
     */
    class_<Board>("Board",
                  init<>());
}
