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

    source_dir = args.dist_dir / f"file-{args.version}-stage1"
    fetch_source_code(
        f"https://astron.com/pub/file/file-{args.version}.tar.gz",
        source_dir,
    )

    build_dir = source_dir / "build"
    os.makedirs(build_dir, exist_ok=True)
    configure_options = [
        "--disable-bzlib",
        "--disable-libseccomp",
        "--disable-xzlib",
        "--disable-zlib",
    ]
    cmds = [
        [source_dir / "configure", *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
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
        f"--prefix={args.prefix}",
        f"--host={args.target}",
        f"--build={config_guess.stdout.strip()}",
    ]
    cmds = [
        [source_dir / "configure", *configure_options],
        ["make", f'FILE_COMPILE={source_dir / "build" / "src" / "file"}', f"-j{multiprocessing.cpu_count()}"],
        ["make", f"DESTDIR={args.install_dir}", "install"]
    ]
    for cmd in cmds:
        print(' '.join(map(str, cmd)))
        subprocess.run(
            map(str, cmd),
            check=True,
            cwd=source_dir,
        )


if __name__ == '__main__':
    main()
