import argparse
from re import sub
import urllib.request
import pathlib
import tempfile
import subprocess
import shutil
import os
import multiprocessing


def fetch_source_code(url: str, extract_path: pathlib.Path):
    print(f'downloading source code from "{url}"...')
    with urllib.request.urlopen(url) as response:
        print(f'download source code from "{url}"')
        with tempfile.NamedTemporaryFile() as tmp_file:
            shutil.copyfileobj(response, tmp_file)

            os.makedirs(extract_path, exist_ok=True)

            print(f'validate source code downloaded from "{url}" in "{extract_path}"...')
            validate_tar = subprocess.run(
                ['tar', 'df', tmp_file.name, '--strip-components', '1', '--no-same-owner', '--no-same-permissions'],
                stdout=subprocess.DEVNULL,
                cwd=extract_path,
            )
            if validate_tar.returncode == 0:
                print(f'already valid source code downloaded from "{url}"')
                return
            print('invalidate source code')

            print(f'extract source code to "{extract_path}"')
            subprocess.run(
                ['tar', 'xf', tmp_file.name, '--strip-components', '1', '-C', extract_path],
                check=True,
            )
            print(f'extracted source code to "{extract_path}"')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gcc-version",
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
        "--install-dir",
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
    parser.add_argument(
        "--cxx-include-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    source_dir = args.dist_dir / f"gcc-{args.gcc_version}-for-libc++-cross"
    fetch_source_code(
        f"https://ftp.gnu.org/gnu/gcc/gcc-{args.gcc_version}/gcc-{args.gcc_version}.tar.gz",
        source_dir,
    )

    build_dir = source_dir / "build"
    os.makedirs(build_dir, exist_ok=True)

    config_guess = subprocess.run(
        [str(source_dir / "config.guess")],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    configure_options = [
        f"--host={args.target}",
        f"--build={config_guess.stdout.strip()}",
        f"--prefix={args.prefix}",
        "--disable-multilib",
        "--disable-nls",
        "--disable-libstdcxx-pch",
        f"--with-gxx-include-dir={args.cxx_include_dir}"
    ]
    cmds = [
        [source_dir / "libstdc++-v3" / "configure", *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", f"DESTDIR={args.install_dir}", "install"]
    ]
    for cmd in cmds:
        print(' '.join(map(str, cmd)))
        subprocess.run(
            map(str, cmd),
            check=True,
            cwd=build_dir,
        )


if __name__ == '__main__':
    main()
