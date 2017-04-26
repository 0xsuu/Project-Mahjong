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
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include <AlwaysDiscardFirstPlayer.h>
#include <GreedyPlayer.h>
#include <RandomPlayer.h>
#include <UserInputPlayer.h>

using mahjong::AlwaysDiscardFirstPlayer;
using mahjong::GreedyPlayer;
using mahjong::RandomPlayer;
using mahjong::UserInputPlayer;

using mahjong::Hand;
using mahjong::Player;
using mahjong::PlayerWrapper;
using mahjong::Tile;

namespace mahjong {
class PythonPlayer : public Player {
public:
    PythonPlayer(std::string playerName, PyObject *pyClassObject) : Player(playerName) {
        assert(pyClassObject != nullptr);
        mPythonClassObject = pyClassObject;
    }

    Action onTurn(int playerID, Tile tile) override {
        return boost::python::call_method<Action>(mPythonClassObject, "on_turn", this, playerID, tile);
    }
    Action onOtherPlayerMakeAction(int playerID, std::string playerName, Action action) override {
        return boost::python::call_method<Action>(mPythonClassObject, "on_other_player_make_action", this,
                                                  playerID, playerName, action);
    }

private:
    PyObject *mPythonClassObject;
};

Player *makeRandomPlayer(std::string playerName) {
    return new RandomPlayer(playerName);
}
Player *makeGreedyPlayer(std::string playerName) {
    return new GreedyPlayer(playerName);
}
Player *makeUserInputPlayer(std::string playerName) {
    return new UserInputPlayer(playerName);
}
Player *makePythonPlayer(PyObject *classObject) {
    return new PythonPlayer(boost::python::call_method<std::string>(classObject, "get_player_name"),
                            classObject);
}
} // namespace mahjong.

BOOST_PYTHON_MODULE(libplayers) {
    using boost::python::bases;
    using boost::python::class_;
    using boost::python::def;
    using boost::python::enum_;
    using boost::python::init;

    def("make_random_player", mahjong::makeRandomPlayer, boost::python::return_value_policy<boost::python::manage_new_object>());
    def("make_greedy_player", mahjong::makeGreedyPlayer, boost::python::return_value_policy<boost::python::manage_new_object>());
    def("make_user_input_player", mahjong::makeUserInputPlayer, boost::python::return_value_policy<boost::python::manage_new_object>());
    def("make_python_player", mahjong::makePythonPlayer, boost::python::return_value_policy<boost::python::manage_new_object>());

    class_<AlwaysDiscardFirstPlayer>("AlwaysDiscardFirstPlayer",
                                     init<std::string>())
            .def("on_turn", &AlwaysDiscardFirstPlayer::onTurn)
            .def("on_other_player_make_action", &AlwaysDiscardFirstPlayer::onOtherPlayerMakeAction);
    class_<RandomPlayer>("RandomPlayer",
                                     init<std::string>())
            .def("on_turn", &RandomPlayer::onTurn)
            .def("on_other_player_make_action", &RandomPlayer::onOtherPlayerMakeAction);
    class_<GreedyPlayer, bases<PlayerWrapper>>("GreedyPlayer",
                            init<std::string>())
            .def("on_turn", &GreedyPlayer::onTurn)
            .def("on_other_player_make_action", &GreedyPlayer::onOtherPlayerMakeAction)
            .def("select_best_tile", &GreedyPlayer::selectBestTile);
    class_<UserInputPlayer>("UserInputPlayer",
                                     init<std::string>())
            .def("on_turn", &UserInputPlayer::onTurn)
            .def("on_other_player_make_action", &UserInputPlayer::onOtherPlayerMakeAction);

    class_<mahjong::PythonPlayer>("PythonPlayer",
                         init<std::string, PyObject *>())
            .def("on_turn", &mahjong::PythonPlayer::onTurn)
            .def("on_other_player_make_action", &mahjong::PythonPlayer::onOtherPlayerMakeAction)
            .def("get_id", &PlayerWrapper::getID)
            .def("get_hand", &PlayerWrapper::getHand);
    class_<std::vector<Tile> >("TileVec")
            .def(boost::python::vector_indexing_suite<std::vector<Tile>>());
}
