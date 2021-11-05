cmake_minimum_required(VERSION 3.9)

project(mylib VERSION 1.0.1 DESCRIPTION "sandbox library")

enable_testing()

add_subdirectory( src )

add_test(NAME MyTest COMMAND Test)

add_subdirectory( test )
