
cmake_minimum_required (VERSION 2.8)

project (Mahjong-games)

#
# Checking environment
#

include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++1z" COMPILER_SUPPORTS_CXX1Z)
if(COMPILER_SUPPORTS_CXX1Z)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++1z")
    set(COVERAGE_FLAGS "-std=c++1z -g -O0 -fprofile-arcs -ftest-coverage")
elseif(COMPILER_SUPPORTS_CXX11)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
    set(COVERAGE_FLAGS "-std=c++11 -g -O0 -fprofile-arcs -ftest-coverage")
elseif(COMPILER_SUPPORTS_CXX0X)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
    set(COVERAGE_FLAGS "-std=c++0x -g -O0 -fprofile-arcs -ftest-coverage")
else()
    message(STATUS "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
endif()

#
# Setting variables
#

set(PROJECT_ROOT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")
set(PROJECT_MAHJONG "${PROJECT_ROOT_DIRECTORY}/../")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_MAHJONG}/../Mahjong-games")
set(MAHJONG_LIB_INCLUDE_PATH "${PROJECT_MAHJONG}/mahjong_lib/include")

# Players
set(USER_INPUT_PLAYER_INCLUDE_PATH "${PROJECT_MAHJONG}/players/UserInputPlayer/include")
set(DUMB_PLAYERS_INCLUDE_PATH "${PROJECT_MAHJONG}/players/DumbPlayers/include")
set(NON_LEARNING_PLAYERS_INCLUDE_PATH "${PROJECT_MAHJONG}/players/NonLearningPlayers/include")

set(PLAYERS_LIB_PATH "${PROJECT_MAHJONG}/../build_players/libplayers.a")

include_directories(${MAHJONG_LIB_INCLUDE_PATH}/ ${USER_INPUT_PLAYER_INCLUDE_PATH}/ ${DUMB_PLAYERS_INCLUDE_PATH}/ ${NON_LEARNING_PLAYERS_INCLUDE_PATH}/)

#
# Build targets
#

set(CMAKE_SM_SOURCE_DIR "${PROJECT_ROOT_DIRECTORY}/SimpleMahjong/src")
set(CMAKE_SM_INCLUDE_DIR "${PROJECT_ROOT_DIRECTORY}/SimpleMahjong/include")

include_directories(${CMAKE_SM_INCLUDE_DIR}/)

file(GLOB_RECURSE SM_SOURCE_FILES ${CMAKE_SM_SOURCE_DIR}/*.cpp)
file(GLOB_RECURSE SM_HEADER_FILES ${CMAKE_SM_INCLUDE_DIR}/*.h ${MAHJONG_LIB_INCLUDE_PATH}/*.h)

source_group("SimpleMahjongHeaders" FILES ${SM_HEADER_FILES})

add_executable(SimpleMahjong ${SM_SOURCE_FILES})
target_link_libraries(SimpleMahjong "${PROJECT_MAHJONG}/../build_mahjong/libmahjong.a" ${PLAYERS_LIB_PATH})

add_library(dGames SHARED
        ${SM_SOURCE_FILES}
        ${PROJECT_ROOT_DIRECTORY}/PythonInterface/GamesInterface.cpp)
set_target_properties(dGames PROPERTIES OUTPUT_NAME games)
target_link_libraries(dGames "${PROJECT_MAHJONG}/../build_mahjong/libmahjong.a" ${PLAYERS_LIB_PATH})
set_property(TARGET dGames PROPERTY POSITION_INDEPENDENT_CODE ON)
target_link_libraries(dGames -lboost_python)
