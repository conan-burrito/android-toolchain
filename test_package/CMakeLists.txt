project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

add_executable(example example.cpp)
target_link_libraries(example ${CONAN_LIBS} log)
