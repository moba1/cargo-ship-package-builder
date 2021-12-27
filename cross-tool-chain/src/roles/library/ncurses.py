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
        "--version",
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
    args = parser.parse_args()

    source_dir = args.dist_dir / f"ncurses-{args.version}-library"
    fetch_source_code(
        f"https://ftp.gnu.org/gnu/ncurses/ncurses-{args.version}.tar.gz",
        source_dir,
    )

    subprocess.run(
        ['sed', '-i', 's/mawk//', 'configure'],
        check=True,
        cwd=source_dir,
    )

    build_dir = source_dir / 'build'
    os.makedirs(build_dir, exist_ok=True)
    cmds = [
        [source_dir / 'configure'],
        ['make', '-C', 'include'],
        ['make', '-C', 'progs', 'tic']
    ]
    for cmd in cmds:
        print(' '.join(map(str, cmd)))
        subprocess.run(
            map(str, cmd),
            check=True,
            cwd=build_dir,
        )

    config_guess = subprocess.run(
        [str(source_dir / "config.guess")],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    configure_options = [
        # TODO: remove hard code unix path
        "--prefix=/usr",
        f"--host={args.target}",
        f"--build={config_guess.stdout.strip()}",
        '--mandir=/usr/share/man',
        '--with-manpage-format=normal',
        '--with-shared',
        '--without-debug',
        '--without-ada',
        '--without-normal',
        '--enable-widec'
    ]
    cmds = [
        [source_dir / "configure", *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", f"DESTDIR={args.install_dir}", f"TIC_PATH={source_dir / 'build' / 'progs' / 'tic'}", "install"],
    ]
    for cmd in cmds:
        print(' '.join(map(str, cmd)))
        subprocess.run(
            map(str, cmd),
            check=True,
            cwd=source_dir,
        )
    with open(args.install_dir / "usr" / "lib" / "libncurses.so", 'w') as libncurses:
        libncurses.write("INPUT(-lncursesw)")


if __name__ == '__main__':
    main()
