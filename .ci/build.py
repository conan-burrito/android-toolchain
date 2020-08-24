from conan.packager import ConanMultiPackager


def make_settings(arch):
    bitness = {
        'x86': 32,
        'armv7': 32,
        'armv7s': 32,
        'armv7k': 32,
        'armv7hf': 32,
        'x86_64': 64,
        'armv8': 64,
    }.get(arch)

    def get_level():
        return 16 if bitness == 32 else 21

    return {
        'os': 'Android',
        'os.api_level': get_level(),
        'compiler': 'clang',
        'compiler.version': '9',
        'compiler.libcxx': 'c++_static',
        'arch': arch
    }


if __name__ == "__main__":
    builder = ConanMultiPackager()

    builder.add(settings=make_settings('x86'))
    builder.add(settings=make_settings('x86_64'))
    builder.add(settings=make_settings('armv7'))
    builder.add(settings=make_settings('armv8'))

    builder.run()
