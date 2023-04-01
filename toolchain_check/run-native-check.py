#!/usr/bin/env python3
from subprocess import run
from os.path import join, exists, isdir, abspath, dirname

import shutil
import sys

SCRIPT_PATH = abspath(__file__)
SCRIPT_DIR = dirname(SCRIPT_PATH)
LIBRARY_DIR = join(SCRIPT_DIR, 'library')
EXECUTABLE_DIR = join(SCRIPT_DIR, 'executable')
BUILD_DIR = join(SCRIPT_DIR, 'build')

if exists(BUILD_DIR) and isdir(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)


class CMake:
    def __init__(self, name: str):
        self.name = name
        self.project_dir = join(SCRIPT_DIR, self.name)
        self.build_dir = join(BUILD_DIR, self.name)
        self.install_dir = join(self.build_dir, 'install-dir')

    def configure(self, extra_args=None):
        args = ['cmake', f'-H{self.project_dir}', f'-B{self.build_dir}', f'-DCMAKE_INSTALL_PREFIX={self.install_dir}']
        if extra_args is not None:
            args.extend(extra_args)

        run(args, check=True)

    def install(self):
        run(['cmake', '--build', self.build_dir, '--target', 'install'], check=True)

    def prefix_arg(self):
        return f'-DCMAKE_PREFIX_PATH={self.install_dir}'


library = CMake('library')
library.configure()
library.install()

executable = CMake('executable')
executable.configure([library.prefix_arg()])
executable.install()


def binary_name():
    binary = 'dummy-conan-executable'
    if sys.platform.startswith('win'):
        binary += '.exe'

    return binary


run([join(executable.install_dir, 'bin', binary_name())])
