import argparse
import platform
import re
import subprocess
import os
import pathlib
import urllib.request
import tempfile
import shutil
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
        "--dist-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--version",
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
        "--target",
        type=str,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    source_dir = args.dist_dir / f"glibc-{args.version}-cross"
    fetch_source_code(
        f"https://ftp.gnu.org/gnu/glibc/glibc-{args.version}.tar.xz",
        source_dir,
    )

    with tempfile.NamedTemporaryFile() as patch_file:
        subprocess.run(
            ["curl", "-sSL", f"https://www.linuxfromscratch.org/patches/lfs/11.0/glibc-{args.version}-fhs-1.patch", "-o", patch_file.name],
            stdout=subprocess.PIPE,
            check=True,
        )
        subprocess.run(
            ["patch", "-Np1", "-i", patch_file.name],
            cwd=source_dir,
            check=True,
        )

    architecture = platform.machine()
    if re.fullmatch("i.86", architecture):
        subprocess.run(
            ["ln", '-sfv', 'ld-linux.so.2', f"{args.instal_dir / 'lib' / 'ld-lsb.so.3'}"],
            check=True,
        )
    elif architecture == "x86_64":
        cmds = [
            ["ln", '-sfv', pathlib.Path("..") / "lib" / "ld-linux-x86-64.so.2", args.install_dir / "lib64"],
            ["ln", "-sfv", pathlib.Path("..") / "lib" / "ld-linux-x86-64.so.2", args.install_dir / "lib64" / "ld-lsb-x86-64.so.3"]
        ]
        for cmd in cmds:
            subprocess.run(
                map(str, cmd),
                check=True,
            )

    build_dir = source_dir / "build"
    os.makedirs(build_dir, exist_ok=True)

    with open(source_dir / "configparms", 'w') as configparms:
        configparms.write("rootsbindir=/usr/sbin")

    config_guess = subprocess.run(
        [str(source_dir / "scripts" / "config.guess")],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    configure_options = [
        '--prefix=/usr',
        f'--host={args.target}',
        f'--build={config_guess.stdout.strip()}',
        '--enable-kernel=3.2',
        f'--with-headers={args.install_dir / "usr" / "include"}',
        'libc_cv_slibdir=/usr/lib'
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
        ["sed", "/RTLDLIST=/s@/usr@@g", "-i", str(args.install_dir / 'usr' / 'bin' / 'ldd')],
        check=True,
    )


if __name__ == '__main__':
    main()
