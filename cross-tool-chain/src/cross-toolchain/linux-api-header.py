import argparse
import pathlib
import subprocess
import os
import tempfile


def fetch_source_code(url: str, extract_path: pathlib.Path):
    print(f'downloading source code from "{url}"...')
    ## cannot download valid linux archive by urllib.request.urlopen.
    ## > EOF position is wrong...
    ##
    # with urllib.request.urlopen(url) as response:
    download_kernel_code = subprocess.run(
        ['curl', '-sSL', url],
        stdout=subprocess.PIPE,
        check=True,
    )
    print(f'download source code from "{url}"')
    with tempfile.NamedTemporaryFile(mode='wb') as tmp_file:
        tmp_file.write(download_kernel_code.stdout)

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
        "--install-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    major_version = args.version.split('.')[0]
    source_dir = args.dist_dir / f"linux-api-headers-{args.version}"
    fetch_source_code(
        f"https://www.kernel.org/pub/linux/kernel/v{major_version}.x/linux-{args.version}.tar.xz",
        source_dir,
    )

    header_dir = pathlib.Path("usr") / "include"
    cmds = [
        ["make", "mrproper"],
        ["make", "headers"],
        ["find", header_dir, "-name", "'.*'", "-delete"],
        ["rm", header_dir / "Makefile"],
        ["cp", "-rv", header_dir, args.install_dir]
    ]
    for cmd in cmds:
        subprocess.run(
            map(str, cmd),
            check=True,
            cwd=source_dir,
        )


if __name__ == '__main__':
    main()
