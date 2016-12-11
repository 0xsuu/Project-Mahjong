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

    /**
     * Expose Tile class.
     */
    class_<Tile>("Tile",
                 init<>())
            .def(init<const TileFlag, const TileType, const int, bool>())
            .def(init<const TileFlag, const TileType, const int>())
            .def(init<const uint8_t, bool>())
            .def("getFlag", &Tile::getFlag)
            .def("getType", &Tile::getType)
            .def("getNumber", &Tile::getNumber)
            .def("isDora", &Tile::isDora)
            .def("isNull", &Tile::isNull)
            .def("getData", &Tile::getData)
            .def("getPrintable", &Tile::getPrintable)
            .def("setMeld", &Tile::setMeld)
            .def("setConceal", &Tile::setConceal)
            .def("__eq__", &Tile::operator==)
            .def("__ne__", &Tile::operator!=)
            .def("__lt__", &Tile::operator<)
            .def("__le__", &Tile::operator<=)
            .def("__add__", &Tile::operator+)
            .def("__sub__", &Tile::operator-);

    /**
     * Expose Hand Class.
     */
     class_<Hand>("Hand",init<>())
             .def("testWin", &Hand::testWin)
             .def("getData", &Hand::getData);

    /**
     * Expose Player class.
     */
    class_<PlayerWrapper>("Player",
                          init<std::string>())
            .def("onTurn", &PlayerWrapper::onTurn)
            .def("onOtherPlayerMakeAction", &PlayerWrapper::onOtherPlayerMakeAction)
            .def("getPlayerName", &PlayerWrapper::getPlayerName)
            .def("getHand", &PlayerWrapper::getHand)
            .def("getID", &PlayerWrapper::getID);

    /**
     * Expose Action class.
     */
    class_<Action>("Action",
                   init<>())
            .def(init<ActionState, Tile>())
            .def("getActionState", &Action::getActionState)
            .def("getTile", &Action::getTile)
            .def("__lt__", &Action::operator<);
}
