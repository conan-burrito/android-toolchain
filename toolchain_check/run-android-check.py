#!/usr/bin/env python3
from subprocess import run
import os


SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
PROFILE_DIR = os.path.join(SCRIPT_DIR, 'profiles')
LIBRARY_DIR = os.path.join(SCRIPT_DIR, 'library')
EXECUTABLE_DIR = os.path.join(SCRIPT_DIR, 'executable')


def profile_path(name: str):
    return os.path.join(PROFILE_DIR, name)


def run_with_profile(path: str, is_shared: bool, profile_name: str):
    args = ['conan', 'create', '-pr:h', profile_path(profile_name), '-pr:b', 'default', '--user', 'conan-burrito',
            '--channel', 'test', '-o', f'dummy-conan-library/*:shared={is_shared}', path]

    run(args, env=os.environ, check=True)


def run_full_test(shared: bool):
    run_with_profile(LIBRARY_DIR, shared, 'armv7')
    run_with_profile(LIBRARY_DIR, shared, 'armv8')
    run_with_profile(LIBRARY_DIR, shared, 'x86')
    run_with_profile(LIBRARY_DIR, shared, 'x86_64')

    run_with_profile(EXECUTABLE_DIR, shared, 'armv7')
    run_with_profile(EXECUTABLE_DIR, shared, 'armv8')
    run_with_profile(EXECUTABLE_DIR, shared, 'x86')
    run_with_profile(EXECUTABLE_DIR, shared, 'x86_64')


run_full_test(False)
run_full_test(True)
