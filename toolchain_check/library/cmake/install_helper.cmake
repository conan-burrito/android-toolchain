include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

set(DCL_VERSION_CONFIG "${DCL_GENERATED_CMAKE_DIR}/${PROJECT_NAME}ConfigVersion.cmake")
set(DCL_PROJECT_CONFIG "${DCL_GENERATED_CMAKE_DIR}/${PROJECT_NAME}Config.cmake")

set(DCL_INSTALL_CMAKE_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")

set(DCL_TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
set(DCL_INSTALL_NAMESPACE "${PROJECT_NAME}::")

write_basic_package_version_file("${DCL_VERSION_CONFIG}" COMPATIBILITY SameMajorVersion)
configure_package_config_file(cmake/Config.cmake.in
   "${DCL_PROJECT_CONFIG}"
   INSTALL_DESTINATION "${DCL_INSTALL_CMAKE_DIR}"
)

set(DCL_INSTALL_TARGETS dummy_conan_library)

install(
   TARGETS ${DCL_INSTALL_TARGETS}

   EXPORT ${DCL_TARGETS_EXPORT_NAME}

   RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
           COMPONENT   DCL_Runtime

   LIBRARY DESTINATION        ${CMAKE_INSTALL_LIBDIR}
           COMPONENT          DCL_Runtime
           NAMELINK_COMPONENT DCL_Development

   ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
           COMPONENT   DCL_Development

   INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(DIRECTORY ${DCL_GENERATED_INCLUDE_DIR}/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(
   FILES
      ${DCL_GENERATED_EXPORT_HEADER}
   DESTINATION
      "${CMAKE_INSTALL_INCLUDEDIR}/dcl"
)

install(
   FILES
      ${DCL_PROJECT_CONFIG}
      ${DCL_VERSION_CONFIG}
   DESTINATION
      ${DCL_INSTALL_CMAKE_DIR}
)

set_target_properties(dummy_conan_library PROPERTIES EXPORT_NAME library)
add_library(${DCL_INSTALL_NAMESPACE}library ALIAS dummy_conan_library)

install(
   EXPORT ${DCL_TARGETS_EXPORT_NAME}
   DESTINATION ${DCL_INSTALL_CMAKE_DIR}
   NAMESPACE ${DCL_INSTALL_NAMESPACE}
   COMPONENT DCL_Development
)

