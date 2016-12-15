
cmake_minimum_required (VERSION 2.8)

project (Mahjong-players)

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

set(CMAKE_MACOSX_RPATH 1)

#
# Setting variables
#

set(PROJECT_ROOT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")
set(PROJECT_MAHJONG "${PROJECT_ROOT_DIRECTORY}/../")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_MAHJONG}/../Mahjong-players")
set(MAHJONG_LIB_INCLUDE_PATH "${PROJECT_MAHJONG}/mahjong_lib/include")

include_directories(${MAHJONG_LIB_INCLUDE_PATH}/)

IF (NOT DEFINED GAME_TYPE)
    SET(GAME_TYPE SIMPLE_MAHJONG)
ENDIF()
ADD_DEFINITIONS(-D${GAME_TYPE}=YES)

#
# Build targets
#

# User Input Player.
set(CMAKE_UIP_SOURCE_DIR "${PROJECT_ROOT_DIRECTORY}/UserInputPlayer/src")
set(CMAKE_UIP_INCLUDE_DIR "${PROJECT_ROOT_DIRECTORY}/UserInputPlayer/include")

include_directories(${CMAKE_UIP_INCLUDE_DIR}/)

file(GLOB_RECURSE UIP_SOURCE_FILES ${CMAKE_UIP_SOURCE_DIR}/*.cpp)
file(GLOB_RECURSE UIP_HEADER_FILES ${CMAKE_UIP_INCLUDE_DIR}/*.h ${MAHJONG_LIB_INCLUDE_PATH}/*.h)

# Static lib.
add_library(UserInputPlayer ${UIP_SOURCE_FILES})
target_link_libraries(UserInputPlayer "${PROJECT_MAHJONG}/../build_mahjong/libmahjong.a")

# Dumb Players.
set(CMAKE_DUP_SOURCE_DIR "${PROJECT_ROOT_DIRECTORY}/DumbPlayers/src")
set(CMAKE_DUP_INCLUDE_DIR "${PROJECT_ROOT_DIRECTORY}/DumbPlayers/include")

include_directories(${CMAKE_DUP_INCLUDE_DIR}/)

file(GLOB_RECURSE DUP_SOURCE_FILES ${CMAKE_DUP_SOURCE_DIR}/*.cpp)
file(GLOB_RECURSE DUP_HEADER_FILES ${CMAKE_DUP_INCLUDE_DIR}/*.h ${MAHJONG_LIB_INCLUDE_PATH}/*.h)

add_library(DumbPlayers ${DUP_SOURCE_FILES})
target_link_libraries(DumbPlayers "${PROJECT_MAHJONG}/../build_mahjong/libmahjong.a")

# Non-Learning Players.
set(CMAKE_NONLP_SOURCE_DIR "${PROJECT_ROOT_DIRECTORY}/NonLearningPlayers/src")
set(CMAKE_NONLP_INCLUDE_DIR "${PROJECT_ROOT_DIRECTORY}/NonLearningPlayers/include")

include_directories(${CMAKE_NONLP_INCLUDE_DIR}/)

file(GLOB_RECURSE NONLP_SOURCE_FILES ${CMAKE_NONLP_SOURCE_DIR}/*.cpp)
file(GLOB_RECURSE NONLP_HEADER_FILES ${CMAKE_NONLP_INCLUDE_DIR}/*.h ${MAHJONG_LIB_INCLUDE_PATH}/*.h)

add_library(NonLearningPlayers ${NONLP_SOURCE_FILES})
target_link_libraries(NonLearningPlayers "${PROJECT_MAHJONG}/../build_mahjong/libmahjong.a")

# Static lib.
add_library(AllPlayers STATIC
        ${UIP_SOURCE_FILES}
        ${DUP_SOURCE_FILES}
        ${NONLP_SOURCE_FILES})
set_target_properties(AllPlayers PROPERTIES OUTPUT_NAME players)
set_property(TARGET AllPlayers PROPERTY POSITION_INDEPENDENT_CODE ON)
target_link_libraries(AllPlayers "${PROJECT_MAHJONG}/../build_mahjong/libmahjong.a")

# Dynamic lib, uses the same name as the static one.
# This also automatically include the python interface.
if(APPLE)
    set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
endif(APPLE)

add_library(dPlayers SHARED
        ${UIP_SOURCE_FILES}
        ${DUP_SOURCE_FILES}
        ${NONLP_SOURCE_FILES}
        ${PROJECT_ROOT_DIRECTORY}/PythonInterface/PlayersInterface.cpp)
set_target_properties(dPlayers PROPERTIES OUTPUT_NAME players)
set_property(TARGET dPlayers PROPERTY POSITION_INDEPENDENT_CODE ON)
if( PYTHON_VERSION STREQUAL "" )
    target_link_libraries(dPlayers "${PROJECT_MAHJONG}/../build_mahjong/libmahjong.a" -lpython -lboost_python)
else()
    set(PYTHON_VERSION_SHORT "")
    string(REPLACE "." "" PYTHON_VERSION_SHORT ${PYTHON_VERSION})
    target_link_libraries(dPlayers "${PROJECT_MAHJONG}/../build_mahjong/libmahjong.a"
            -lpython${PYTHON_VERSION}m -lboost_python-py${PYTHON_VERSION_SHORT})
endif()
