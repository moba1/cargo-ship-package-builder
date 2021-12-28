import argparse
import pathlib
import urllib.request
import shutil
import tempfile
import subprocess
import dataclasses
import os
import asyncio
import platform
import multiprocessing


async def fetch_source_code(url: str, extract_path: pathlib.Path):
    print(f'downloading source code from "{url}"...')
    with urllib.request.urlopen(url) as response:
        print(f'download source code from "{url}"')
        with tempfile.NamedTemporaryFile() as tmp_file:
            shutil.copyfileobj(response, tmp_file)

            os.makedirs(extract_path, exist_ok=True)
            print(f'extract source code to "{extract_path}"')
            subprocess.run(
                ['tar', 'xf', tmp_file.name, '--strip-components', '1', '-C', extract_path],
                check=True,
            )
            print(f'extracted source code to "{extract_path}"')


@dataclasses.dataclass
class Source:
    path: str
    extract_path: pathlib.Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gcc-version",
        type=str,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--mpc-version",
        type=str,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--mpfr-version",
        type=str,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--gmp-version",
        type=str,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--dist-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--target",
        type=str,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--sysroot",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--prefix",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    source_dir = args.dist_dir / f"gcc-{args.gcc_version}-cross"
    sources = [
        Source(
            f"https://ftp.gnu.org/gnu/gcc/gcc-{args.gcc_version}/gcc-{args.gcc_version}.tar.gz",
            source_dir,
        ),
        Source(
            f"https://ftp.gnu.org/gnu/mpfr/mpfr-{args.mpfr_version}.tar.xz",
            source_dir / "mpfr"
        ),
        Source(
            f"https://ftp.gnu.org/gnu/gmp/gmp-{args.gmp_version}.tar.xz",
            source_dir / "gmp"
        ),
        Source(
            f"https://ftp.gnu.org/gnu/mpc/mpc-{args.mpc_version}.tar.gz",
            source_dir / "mpc"
        ),
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.wait(
            map(
                lambda source: fetch_source_code(source.path, source.extract_path),
                sources,
            )
        )
    )

    if platform.machine() == 'x86_64':
        subprocess.run(
            ['sed', '-e', '/m64=/s/lib64/lib/', '-i', str(source_dir / 'gcc' / 'config' / 'i386' / 't-linux64')],
            check=True,
        )

    build_dir = source_dir / "build"
    os.makedirs(build_dir, exist_ok=True)

    configure_options = [
        f'--target={args.target}',
        f'--prefix={args.prefix}',
        '--with-glibc-version=2.11',
        f'--with-sysroot={args.sysroot}',
        '--with-newlib',
        '--without-headers',
        '--enable-initfini-array',
        '--disable-nls',
        '--disable-shared',
        '--disable-multilib',
        '--disable-decimal-float',
        '--disable-threads',
        '--disable-libatomic',
        '--disable-libgomp',
        '--disable-libquadmath',
        '--disable-libssp',
        '--disable-libvtv',
        '--disable-libstdcxx',
        '--enable-languages=c,c++',
    ]
    cmds = [
        [source_dir / "configure", *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "install"],
    ]
    for cmd in cmds:
        print(' '.join(map(str, cmd)))
        subprocess.run(
            map(str, cmd),
            check=True,
            cwd=build_dir,
        )

    print_libgcc_file_name = subprocess.run(
        [f'{args.target}-gcc','-print-libgcc-file-name'],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    libgcc_file_path = pathlib.Path(print_libgcc_file_name.stdout)
    with open(libgcc_file_path.parent / 'install-tools' / 'include' / 'limits.h', 'wb') as outfile:
        for original in map(lambda path: source_dir / 'gcc' / path, ['limitx.h', 'glimits.h', 'limity.h']):
            with open(original, 'rb') as infile:
                shutil.copyfileobj(infile, outfile)


if __name__ == '__main__':
    main()
