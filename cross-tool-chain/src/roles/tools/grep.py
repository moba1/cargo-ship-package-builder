import argparse
import pathlib
import tempfile
import subprocess
import os
import multiprocessing


def fetch_source_code(url: str, extract_path: pathlib.Path):
    print(f'downloading source code from "{url}"...')
    ## cannot download valid greo archive by urllib.request.urlopen.
    ## > EOF position is wrong...
    ##
    # with urllib.request.urlopen(url) as response:
    download_grep_code = subprocess.run(
        ['curl', '-sSL', url],
        stdout=subprocess.PIPE,
        check=True,
    )
    print(f'download source code from "{url}"')
    with tempfile.NamedTemporaryFile('wb') as tmp_file:
        tmp_file.write(download_grep_code.stdout)

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
    parser.add_argument(
        "--prefix",
        type=pathlib.Path,
        required=True,
        action='store',
    )
    args = parser.parse_args()

    source_dir = args.dist_dir / f"grep-{args.version}-tools"
    fetch_source_code(
        f"https://ftp.gnu.org/gnu/grep/grep-{args.version}.tar.xz",
        source_dir,
    )

    configure_options = [
        f"--prefix={args.prefix}",
        f"--host={args.target}",
    ]
    cmds = [
        [source_dir / "configure", *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
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
