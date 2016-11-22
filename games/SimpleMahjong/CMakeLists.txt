
cmake_minimum_required (VERSION 2.8)

project (SimpleMahjong)

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
set(PROJECT_MAHJONG "${PROJECT_ROOT_DIRECTORY}/../../")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_MAHJONG}/../SimpleMahjong")
set(CMAKE_SOURCE_DIR "${PROJECT_ROOT_DIRECTORY}/src")
set(CMAKE_INCLUDE_DIR "${PROJECT_ROOT_DIRECTORY}/include ${PROJECT_MAHJONG}/mahjong_lib/include")

include_directories(${CMAKE_INCLUDE_DIR}/)

file(GLOB_RECURSE SOURCE_FILES ${CMAKE_SOURCE_DIR}/*.cpp)
file(GLOB_RECURSE HEADER_FILES ${CMAKE_INCLUDE_DIR}/*.h)

source_group("Headers" FILES ${HEADER_FILES})

# Add gtest headers and libs
include_directories(${CMAKE_INCLUDE_DIR}/ /usr/local/include)
link_directories(/usr/local/lib/)

#
# Build targets
#

add_executable(SimpleMahjong ${SOURCE_FILES} "${PROJECT_MAHJONG}/../build_mahjong/libmahjong.a")

