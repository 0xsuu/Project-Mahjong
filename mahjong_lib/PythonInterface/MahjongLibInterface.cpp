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
#include <Tile.h>

using mahjong::Hand;
using mahjong::Tile;
using mahjong::TileGroup;
using mahjong::TileFlag;
using mahjong::TileType;

BOOST_PYTHON_MODULE(libmahjong) {
    using boost::python::class_;
    using boost::python::enum_;
    using boost::python::init;

    /**
     * Wrap for enums.
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

    /**
     * Wrap for Tile class.
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
            .def("EQ", &Tile::operator==)
            .def("NE", &Tile::operator!=)
            .def("LT", &Tile::operator<)
            .def("LE", &Tile::operator<=)
            .def("plus", &Tile::operator+)
            .def("minus", &Tile::operator-);
}
