import os

from conans import ConanFile, tools


class AndroidNdkConan(ConanFile):
    name = 'android-toolchain'
    version = 'r21d'
    license = 'Apache License 2.0'
    description = 'The Android NDK is a toolset that lets you implement parts ' \
                  'of your app in native code, using languages such as C and ' \
                  'C++. For certain types of apps, this can help you reuse ' \
                  'code libraries written in those languages'

    homepage = 'https://developer.android.com/ndk'
    url = 'https://github.com/conan-burrito/android-toolchain'

    settings = 'os', 'arch', 'os_build', 'arch_build', 'compiler'

    options = {'fPIC': [True, False], 'fPIE': [True, False]}
    default_options = {'fPIC': True, 'fPIE': True}

    no_copy_source = True
    build_policy = 'missing'

    # The android toolchain contains a lot of files with giant paths and names so we have to use shor paths here
    short_paths = True

    # This file will be included by conan CMake build helper by setting the CONAN_CMAKE_TOOLCHAIN_FILE environment
    # variable and in turn include the Android NDK Toolchain file after setting some CMake variables
    exports_sources = 'android-toolchain-wrapper.cmake'

    @staticmethod
    def conan_arch_to_ndk_arch(conan_arch):
        return {
            'armv7': 'armeabi-v7a',
            'armv7hf': 'armeabi-v7a',
            'armv8': 'arm64-v8a'
        }.get(conan_arch, conan_arch)

    @property
    def ndk_arch(self):
        return self.conan_arch_to_ndk_arch(str(self.settings.arch))

    @property
    def platform_id(self):
        return '{os_name}-{target}'.format(os_name=self.os_name, target=self.settings.arch_build)

    @property
    def ndk_folder(self):
        return '{revision}-{platform}'.format(revision=self.ndk_version, platform=self.platform_id)

    @property
    def ndk_version(self):
        return self.version

    @property
    def compiler_version(self):
        return '9.0.8'

    @property
    def android_triple_prefix(self):
        return {
            'armv8': 'aarch64',
            'armv7': 'arm',
            'armv7s': 'arm',
            'armv7k': 'arm',
            'armv7hf': 'arm',
            'x86': 'i686',
            'x86_64': 'x86_64',
        }[str(self.settings.arch)]

    @property
    def android_triple_suffix(self):
        return 'androideabi' if self.android_triple_prefix == 'arm' else 'android'

    @property
    def android_triple(self):
        return '%s-linux-%s' % (self.android_triple_prefix, self.android_triple_suffix)

    @property
    def os_name(self):
        if self.settings.os_build == 'Linux':
            return 'linux'
        elif self.settings.os_build == 'Windows':
            return 'windows'
        elif self.settings.os_build == 'Macos':
            return 'darwin'
        else:
            raise Exception('Unsupported build OS')

    def configure(self):
        if self.settings.os_build == 'Windows':
            self.output.info('Using Android toolchain under Windows requires the MSYS environment, adding it to the requirements list')
            self.requires('msys2/20200517@conan-burrito/stable')

        api_levels = {
            'aarch64' : (21, 30),
            'arm': (16, 30),
            'i686': (16, 30),
            'x86_64': (21, 30),
        }
        min_level, max_level = api_levels[self._clang_libs_arch(str(self.settings.arch))]
        int_level = int(str(self.settings.os.api_level))
        if int_level < min_level or int_level > int_level:
            raise Exception('API Level unsupported: min=%s, max=%s, selected=%s' % (min_level, max_level, int_level))

    def source(self):
        # build tools have to download files in build method when the
        # source files downloaded will be different based on architecture or OS
        pass

    def build(self):
        # We are using the build step because sources are different for each platform
        def get_uri(file_id):
            return 'https://dl.google.com/android/repository/android-ndk-{fid}.zip'.format(fid=file_id)

        hashes = {
            'r21d-windows-x86_64': '99175ce1210258f2280568cd340e0666c69955c7',
            'r21d-darwin-x86_64': 'ef06c9f9d7efd6f243eb3c05ac440562ae29ae12',
            'r21d-linux-x86_64': 'bcf4023eb8cb6976a4c7cff0a8a8f145f162bf4d',
        }

        file_id = self.ndk_folder

        try:
            expected_hash = hashes[file_id]
        except KeyError:
            raise Exception('Not supported OS or architecture')

        self.output.info('Downloading: %s' % file_id)
        tools.download(get_uri(file_id), 'ndk.zip')
        tools.check_sha1('ndk.zip', expected_hash)
        tools.unzip('ndk.zip', keep_permissions=True)
        os.remove('ndk.zip')

    def _clang_libs_arch(self, arch):
        return {
            'armv8': 'aarch64',
            'armv7': 'arm',
            'armv7s': 'arm',
            'armv7k': 'arm',
            'armv7hf': 'arm',
            'x86': 'i686',
            'x86_64': 'x86_64',
        }[arch]

    def copy_ndk_libs(self, arch):
        """ On Android standard library and all the sanitizer support libraries
        are stored under the not very obvious, architecture-specific paths. We
        collect all the relevant ones and put them into a more intuitive
        directories.
            Because we are using the same NDK package for all the architectures,
        we can't just put them into the `lib` folder. We can't also put them into
        any `lib/` subdirectory, otherwise import will be bad-defined (all the
        libraries will be imported)."""
        ndk_arch = self.conan_arch_to_ndk_arch(arch)
        clang_libs_arch = self._clang_libs_arch(arch)

        target_path = os.path.join('android-lib', arch)

        clang_libs = os.path.join(self.package_folder, 'sources', 'cxx-stl', 'llvm-libc++', 'libs', ndk_arch)

        sanitizer_libs = os.path.join(self.package_folder,
                                      'toolchains', 'llvm', 'prebuilt', self.platform_id,
                                      'lib64', 'clang', self.compiler_version, 'lib', 'linux')

        file_filters = [
            '*-{arch}-*.so',
            '*-{arch}.so',
            '*-{arch}-*.a',
            '*-{arch}.a',
        ]

        self.output.info('Copying libraries into: %s' % target_path)
        self.output.info('Copying sanitizer libs from %s' % sanitizer_libs)
        for arch_filter in file_filters:
            mask = arch_filter.format(arch=clang_libs_arch)
            self.copy(mask, src=sanitizer_libs, dst=target_path, keep_path=False)

        self.output.info('Copying standard libraries from %s' % clang_libs)
        self.copy('*.so', src=clang_libs, dst=target_path, keep_path=False)
        self.copy('*.a', src=clang_libs, dst=target_path, keep_path=False)

    def package(self):
        self.copy("android-toolchain-wrapper.cmake")

        self.copy('*', dst='', src='android-ndk-%s' % self.ndk_version, keep_path=True)
        for arch in ['x86', 'x86_64', 'armv7', 'armv8']:
            self.copy_ndk_libs(arch)

    def package_id(self):
        self.info.include_build_settings()
        self.info.settings.arch = 'ANY'
        self.info.settings.runtime = 'ANY'
        self.info.settings.compiler = 'ANY'
        self.info.settings.os.api_level = 'ANY'

    def package_info(self):
        tools_path = os.path.join(self.package_folder, 'build', 'tools')
        cmake_toolchain = os.path.join(self.package_folder, 'build', 'cmake', 'android.toolchain.cmake')
        toolchain_dir = os.path.join(self.package_folder, 'toolchains', 'llvm', 'prebuilt', self.platform_id)

        self.env_info.PATH.append(tools_path)
        self.env_info.ANDROID_NDK = self.package_folder
        self.env_info.ANDROID_NDK_CMAKE_TOOLCHAIN = cmake_toolchain

        self.env_info.CONAN_CMAKE_TOOLCHAIN_FILE = os.path.join(self.package_folder, "android-toolchain-wrapper.cmake")
        self.env_info.CONAN_ANDROID_NATIVE_API_LEVEL = str(self.settings.os.api_level)
        self.env_info.CONAN_ANDROID_STL = str(self.settings.compiler.libcxx)
        self.env_info.CONAN_POSITION_INDEPENDENT_CODE = 'ON' if self.options.fPIC else 'OFF'
        self.env_info.CONAN_ANDROID_PIE = 'ON' if self.options.fPIE else 'OFF'
        self.env_info.CONAN_ANDROID_ABI = self.ndk_arch

        bin_dir = os.path.join(toolchain_dir, 'bin')
        def bin_path(name):
            return os.path.join(bin_dir, '%s-%s' % (self.android_triple, name))

        def get_target_flag():
            return os.path.join('--target=%s-linux-%s%s' % (self.android_triple_prefix, self.android_triple_suffix, str(self.settings.os.api_level)))

        self.env_info.PATH.append(bin_dir)
        self.env_info.CC = os.path.join(bin_dir, 'clang')
        self.env_info.CXX = os.path.join(bin_dir, 'clang++')
        self.env_info.SYSROOT = os.path.join(toolchain_dir , 'sysroot')
        self.env_info.CHOST = self.android_triple
        self.env_info.AR = bin_path('ar')
        self.env_info.AS = bin_path('as')
        self.env_info.LD = bin_path('ld')
        self.env_info.STRIP = bin_path('strip')
        self.env_info.RANLIB = bin_path('ranlib')
        self.env_info.ARFLAGS = bin_path('rcs')

        if self.settings.os_build == 'Windows':
            self.output.info('Setting Unix Makefiles as default generator for Android under Windows')
            self.env_info.CONAN_CMAKE_GENERATOR="Unix Makefiles"

        include_folder = os.path.join(toolchain_dir , 'sysroot', 'usr', 'include')

        cflags = [
            get_target_flag(),
            # '-isystem %s' % os.path.join(include_folder, 'c++', 'v1'),
            # '-isystem %s' % os.path.join(include_folder),
            # '-isystem %s' % os.path.join(include_folder, self.android_triple),
        ]
        exelinkflags = []
        if self.options.fPIE:
            cflags.append('-fPIE')
            exelinkflags.append('-pie')

        if self.options.fPIC:
            cflags.append('-fPIC')

        # https://github.com/android-ndk/ndk/issues/635
        if self.settings.arch == 'x86' and int(str(self.settings.os.api_level)) < 24:
            cflags.append('-mstackrealign')

        self.cpp_info.cflags = cflags
        self.cpp_info.cxxflags = cflags
        self.cpp_info.exelinkflags = exelinkflags
        self.cpp_info.includedirs = [include_folder]

        self.env_info.ASFLAGS = [get_target_flag()]

        # Setup libraries directories
        self.cpp_info.libdirs = [os.path.join('android-lib', str(self.settings.arch))]
