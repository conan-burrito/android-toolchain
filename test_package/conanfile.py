from conans import ConanFile, CMake
import os


class AndroidNDKTestConan(ConanFile):
    settings = 'os', 'compiler', 'arch', 'build_type', 'os_build'
    generators = 'cmake'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    @staticmethod
    def expect_arch(arch, elf_arch):
        if arch != elf_arch:
            raise Exception("Invalid binary architecture. Expected '%s', found '%s'" % (arch, elf_arch))

    @staticmethod
    def ensure_arch(conan_arch, elf_arch):
        archs = {
            'armv7': 'ARM',
            'armv8': 'AArch64',
            'x86': 'x86',
            'x86_64': 'x64'
        }
        AndroidNDKTestConan.expect_arch(archs[str(conan_arch)], elf_arch)

    def check_arch(self):
        from elftools.elf.elffile import ELFFile
        self.output.info('Loading ELFFile')
        with open(os.path.join('bin', 'example'), 'rb') as f:
            elf = ELFFile(f)

        elf_arch = elf.get_machine_arch()
        conan_arch = str(self.settings.arch)

        self.output.info('Checking binary architecture: %s vs %s' % (conan_arch, elf_arch))
        self.ensure_arch(conan_arch, elf_arch)

    def test(self):
        try:
            from elftools.elf.elffile import ELFFile
        except ImportError:
            # Not present on all platforms
            return

        self.check_arch()
