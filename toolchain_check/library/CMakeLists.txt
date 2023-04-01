cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
project(DummyConanLibrary VERSION 0.1.0)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
set(CMAKE_DISABLE_SOURCE_CHANGES  ON)
if("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
   message(SEND_ERROR "In-source builds are not allowed.")
endif()

set(DCL_MESSAGE_TO_RETURN "Hello World")

set(DCL_GENERATED_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(DCL_GENERATED_INCLUDE_DIR "${DCL_GENERATED_DIR}/include")
set(DCL_GENERATED_CMAKE_DIR "${DCL_GENERATED_DIR}/cmake")

set(DCL_GENERATED_CONFIG_HEADER "${DCL_GENERATED_INCLUDE_DIR}/dcl/config.h")
set(DCL_GENERATED_VERSION_HEADER "${DCL_GENERATED_INCLUDE_DIR}/dcl/version.h")
set(DCL_GENERATED_EXPORT_HEADER "${DCL_GENERATED_INCLUDE_DIR}/dcl/export.h")

file(MAKE_DIRECTORY ${DCL_GENERATED_INCLUDE_DIR})
configure_file(cmake/config.h.in ${DCL_GENERATED_CONFIG_HEADER} @ONLY)
configure_file(cmake/version.h.in ${DCL_GENERATED_VERSION_HEADER} @ONLY)

add_library(dummy_conan_library
    src/library.cpp
)

target_include_directories(dummy_conan_library
   PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/>
   PUBLIC $<BUILD_INTERFACE:${DCL_GENERATED_INCLUDE_DIR}>

   PUBLIC $<INSTALL_INTERFACE:include>
)

set_target_properties(dummy_conan_library PROPERTIES
   OUTPUT_NAME dummy-conan-library

   CXX_STANDARD 17
)

# --- Configure installation settings --- #
include(GenerateExportHeader)
generate_export_header(dummy_conan_library
   BASE_NAME DCL
   EXPORT_FILE_NAME ${DCL_GENERATED_EXPORT_HEADER}
)

include(cmake/install_helper.cmake)
include(cmake/package_helper.cmake)
