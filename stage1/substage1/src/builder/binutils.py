import argparse
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
    parser.add_argument(
        "--prefix",
        type=pathlib.Path,
        required=True,
        action='store',
    )
    args = parser.parse_args()

    source_dir = args.dist_dir / f"binutils-{args.version}-stage1"
    fetch_source_code(
        f"https://ftp.gnu.org/gnu/binutils/binutils-{args.version}.tar.xz",
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
        f"--prefix={args.prefix}",
        f"--host={args.target}",
        f"--build={config_guess.stdout.strip()}",
        "--disable-nls",
        "--enable-shared",
        "--disable-werror",
        "--enable-64-bit-bfd",
    ]
    cmds = [
        [source_dir / "configure", *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", f"DESTDIR={args.install_dir}", "install", "-j1"],
        ["install", "-vm755", pathlib.Path("libctf") / ".libs" / "libctf.so.0.0.0", args.install_dir / "usr" / "lib"],
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
