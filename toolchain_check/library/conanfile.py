from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout


class DummyConanLibraryRecipe(ConanFile):
    name = "dummy-conan-library"
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    version = "0.1.0"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    no_copy_source = True
    build_policy = 'missing'
    exports_sources = '*', '!.git/*', '!_build/*', '!cmake-build-*', '!test_package/build'

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["DCL_MESSAGE_TO_RETURN"] = "Hello Conan"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "DummyConanLibrary")
        self.cpp_info.set_property("cmake_target_name", "DummyConanLibrary::library")
        self.cpp_info.libs = ["dummy-conan-library"]
