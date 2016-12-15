
cmake_minimum_required (VERSION 2.8)

project (Mahjong-lib)

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
ENABLE_TESTING()

#
# Setting variables
#

set(PROJECT_ROOT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_ROOT_DIRECTORY}/../../libma_gtest")
set(CMAKE_SOURCE_DIR "${PROJECT_ROOT_DIRECTORY}/src")
set(CMAKE_INCLUDE_DIR "${PROJECT_ROOT_DIRECTORY}/include")
set(CMAKE_JSON_INCLUDE_DIR "${PROJECT_ROOT_DIRECTORY}/json")

include_directories(${CMAKE_INCLUDE_DIR}/ ${CMAKE_JSON_INCLUDE_DIR}/)

file(GLOB_RECURSE SOURCE_FILES ${CMAKE_SOURCE_DIR}/*.cpp)
file(GLOB_RECURSE HEADER_FILES ${CMAKE_INCLUDE_DIR}/*.h)
file(GLOB_RECURSE JSON_HEADER_FILES ${CMAKE_JSON_INCLUDE_DIR}/*.h)

source_group("Headers" FILES ${HEADER_FILES})

# Add gtest headers and libs
include_directories(${CMAKE_INCLUDE_DIR}/ /usr/local/include)
link_directories(/usr/local/lib/)

#
# Build targets
#

# Static lib.
if( CMAKE_BUILD_TYPE STREQUAL "Coverage" )
    include(${PROJECT_ROOT_DIRECTORY}/CodeCoverage.cmake)

    set(TEMP_CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
    set(TEMP_CMAKE_C_FLAGS "${CMAKE_C_FLAGS}")
    set(TEMP_CMAKE_EXE_LINKER_FLAGS ${CMAKE_EXE_LINKER_FLAGS})

    set(CMAKE_CXX_FLAGS "${COVERAGE_FLAGS}")
    set(CMAKE_C_FLAGS "${COVERAGE_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS ${COVERAGE_FLAGS})

    message("[+L] Will build mahjong library for coverage")
    add_library(mahjong ${SOURCE_FILES} ${HEADER_FILES})

    set(CMAKE_CXX_FLAGS "${TEMP_CMAKE_CXX_FLAGS}")
    set(CMAKE_C_FLAGS "${TEMP_CMAKE_C_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS ${TEMP_CMAKE_EXE_LINKER_FLAGS})
else()
    add_library(mahjong ${SOURCE_FILES} ${HEADER_FILES})
    set_property(TARGET mahjong PROPERTY POSITION_INDEPENDENT_CODE ON)
endif()

# Dynamic lib, uses the same name as the static one.
# This also automatically include the python interface.
if(APPLE)
    set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
endif(APPLE)

add_library(dmahjong SHARED ${SOURCE_FILES} ${PROJECT_ROOT_DIRECTORY}/PythonInterface/MahjongLibInterface.cpp)
set_target_properties(dmahjong PROPERTIES OUTPUT_NAME mahjong)
set_property(TARGET dmahjong PROPERTY POSITION_INDEPENDENT_CODE ON)
if( PYTHON_VERSION STREQUAL "" )
    target_link_libraries(dmahjong -lpython -lboost_python)
else()
    set(PYTHON_VERSION_SHORT "")
    string(REPLACE "." "" PYTHON_VERSION_SHORT ${PYTHON_VERSION})
    target_link_libraries(dmahjong -lpython${PYTHON_VERSION}m -lboost_python-py${PYTHON_VERSION_SHORT})
endif()
#
# Build gtest (Require installation gtest)
#

# pthread
find_package(Threads)

message("Building Unit Test.")
file(GLOB_RECURSE GTEST_FILES ${PROJECT_ROOT_DIRECTORY}/test/*.cpp)
add_executable(libma_test ${GTEST_FILES})
add_dependencies(libma_test mahjong)
target_link_libraries(libma_test gtest "${PROJECT_ROOT_DIRECTORY}/../../build_mahjong/libmahjong.a" "${CMAKE_THREAD_LIBS_INIT}")
add_test(NAME libma_test COMMAND libma_test)

if( CMAKE_BUILD_TYPE STREQUAL "Coverage" )
    SETUP_TARGET_FOR_COVERAGE(coverage "make test || true" coverage_report)
endif()
