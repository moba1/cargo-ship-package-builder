import argparse
import pathlib
import urllib.request
import shutil
import tempfile
import subprocess
import dataclasses
import os
import asyncio
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
        "--prefix",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--install-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--arch",
        type=str,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    source_dir = args.dist_dir / f"gcc-{args.gcc_version}-stage1"
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

    if args.arch == 'x86_64':
        subprocess.run(
            ['sed', '-e', '/m64=/s/lib64/lib/', '-i', str(source_dir / 'gcc' / 'config' / 'i386' / 't-linux64')],
            check=True,
        )

    build_dir = source_dir / "build"
    os.makedirs(build_dir, exist_ok=True)

    libgcc_dir = build_dir / args.target / "libgcc"
    os.makedirs(libgcc_dir, exist_ok=True)
    subprocess.run(
        ["ln", "-sfvn", "../../../libgcc/gthr-posix.h", libgcc_dir / "gthr-default.h"]
    )

    config_guess = subprocess.run(
        [source_dir / "config.guess"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    configure_options = [
        f"--build={config_guess.stdout.strip()}",
        f"--host={args.target}",
        f'--prefix={args.prefix}',
        f"CC_FOR_TARGET={args.target}-gcc",
        f'--with-build-sysroot={args.install_dir}',
        '--enable-initfini-array',
        '--disable-nls',
        '--disable-multilib',
        '--disable-decimal-float',
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
        ["make", f"DESTDIR={args.install_dir}", "install"],
    ]
    for cmd in cmds:
        print(' '.join(map(str, cmd)))
        subprocess.run(
            map(str, cmd),
            check=True,
            cwd=build_dir,
        )

    subprocess.run(
        ["ln", "-sfvn", "gcc", str(args.install_dir / "usr" / "bin" / "cc")],
        check=True,
    )


if __name__ == '__main__':
    main()
