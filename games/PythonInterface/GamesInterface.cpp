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

#include <SimpleGame.h>

using mahjong::SimpleGame;
using mahjong::Player;

BOOST_PYTHON_MODULE(libgames) {
    using boost::python::class_;
    using boost::python::enum_;
    using boost::python::init;

    class_<SimpleGame>("SimpleGame",
                       init<Player *, Player *, Player *, Player *, int>())
            .def("startGame", &SimpleGame::startGame);
}
