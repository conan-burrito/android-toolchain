from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout


class DummyConanExecutableRecipe(ConanFile):
    name = "dummy-conan-executable"
    package_type = "application"
    settings = "os", "arch", "compiler", "build_type"
    version = "0.1.0"
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }
    requires = [
        "dummy-conan-library/0.1.0@conan-burrito/test"
    ]

    no_copy_source = True
    build_policy = 'missing'
    exports_sources = '*', '!.git/*', '!_build/*', '!cmake-build-*', '!test_package/build'

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

        cmake_deps = CMakeDeps(self)
        cmake_deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "DummyConanExecutable")
        self.cpp_info.set_property("cmake_target_name", "DummyConanExecutable::executable")
