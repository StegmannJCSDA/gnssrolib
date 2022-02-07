cmake_minimum_required(VERSION 3.9)

project(gnssrolib VERSION 1.0.1 DESCRIPTION "GNSS RO library")

enable_testing()

find_package(Boost 1.36.0)
if(Boost_FOUND)
  include_directories(${Boost_INCLUDE_DIRS})
  add_subdirectory( src )
endif()

add_test(NAME MyTest COMMAND Test)
add_test(NAME PointTest COMMAND Test_Point)

add_subdirectory( test )
