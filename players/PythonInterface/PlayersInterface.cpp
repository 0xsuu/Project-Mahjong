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

#include <AlwaysDiscardFirstPlayer.h>
#include <GreedyPlayer.h>
#include <UserInputPlayer.h>

using mahjong::AlwaysDiscardFirstPlayer;
using mahjong::GreedyPlayer;
using mahjong::UserInputPlayer;

using mahjong::Hand;
using mahjong::Player;
using mahjong::Tile;

Player *makeGreedyPlayer(std::string playerName) {
    return new GreedyPlayer(playerName);
}
Player *makeUserInputPlayer(std::string playerName) {
    return new UserInputPlayer(playerName);
}

BOOST_PYTHON_MODULE(libplayers) {
    using boost::python::bases;
    using boost::python::class_;
    using boost::python::def;
    using boost::python::enum_;
    using boost::python::init;

    def("makeGreedyPlayer", makeGreedyPlayer, boost::python::return_value_policy<boost::python::manage_new_object>());
    def("makeUserInputPlayer", makeUserInputPlayer, boost::python::return_value_policy<boost::python::manage_new_object>());

    class_<AlwaysDiscardFirstPlayer>("AlwaysDiscardFirstPlayer",
                                     init<std::string>())
            .def("onTurn", &AlwaysDiscardFirstPlayer::onTurn)
            .def("onOtherPlayerMakeAction", &AlwaysDiscardFirstPlayer::onOtherPlayerMakeAction);

    class_<UserInputPlayer>("UserInputPlayer",
                                     init<std::string>())
            .def("onTurn", &UserInputPlayer::onTurn)
            .def("onOtherPlayerMakeAction", &UserInputPlayer::onOtherPlayerMakeAction);

    class_<GreedyPlayer>("GreedyPlayer",
                            init<std::string>())
            .def("onTurn", &GreedyPlayer::onTurn)
            .def("onOtherPlayerMakeAction", &GreedyPlayer::onOtherPlayerMakeAction);
}