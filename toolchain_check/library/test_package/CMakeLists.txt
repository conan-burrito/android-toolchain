cmake_minimum_required(VERSION 3.1)
project(test_package)

find_package(DummyConanLibrary REQUIRED)

add_executable(test_package test_package.cpp)
target_link_libraries(test_package PRIVATE DummyConanLibrary::library)
