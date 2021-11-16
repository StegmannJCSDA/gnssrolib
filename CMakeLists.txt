cmake_minimum_required(VERSION 3.9)

project(mylib VERSION 1.0.1 DESCRIPTION "sandbox library")

enable_testing()

find_package(Boost 1.36.0)
if(Boost_FOUND)
  include_directories(${Boost_INCLUDE_DIRS})
  add_subdirectory( src )
endif()

add_test(NAME MyTest COMMAND Test)

add_subdirectory( test )
