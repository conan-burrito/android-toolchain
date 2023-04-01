cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
project(DummyConanExecutable VERSION 0.1.0)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
set(CMAKE_DISABLE_SOURCE_CHANGES  ON)
if("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
   message(SEND_ERROR "In-source builds are not allowed.")
endif()

set(DCE_GENERATED_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(DCE_GENERATED_INCLUDE_DIR "${DCE_GENERATED_DIR}/include")
set(DCE_GENERATED_CMAKE_DIR "${DCE_GENERATED_DIR}/cmake")

set(DCE_GENERATED_CONFIG_HEADER "${DCE_GENERATED_INCLUDE_DIR}/dce/config.h")
set(DCE_GENERATED_VERSION_HEADER "${DCE_GENERATED_INCLUDE_DIR}/dce/version.h")

file(MAKE_DIRECTORY ${DCE_GENERATED_INCLUDE_DIR})
configure_file(cmake/config.h.in ${DCE_GENERATED_CONFIG_HEADER} @ONLY)
configure_file(cmake/version.h.in ${DCE_GENERATED_VERSION_HEADER} @ONLY)

find_package(DummyConanLibrary 0.1.0 REQUIRED)

add_executable(dummy_conan_executable
    src/binary.cpp
    src/main.cpp
)

target_link_libraries(dummy_conan_executable PUBLIC DummyConanLibrary::library)

target_include_directories(dummy_conan_executable
   PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/>
   PUBLIC $<BUILD_INTERFACE:${DCE_GENERATED_INCLUDE_DIR}>

   PUBLIC $<INSTALL_INTERFACE:include>
)

set_target_properties(dummy_conan_executable PROPERTIES
   OUTPUT_NAME dummy-conan-executable

   CXX_STANDARD 17
)

# --- Configure installation settings --- #
include(GenerateExportHeader)
include(cmake/install_helper.cmake)
include(cmake/package_helper.cmake)
