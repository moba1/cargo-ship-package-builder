import pathlib
import subprocess
import argparse
import multiprocessing
import shutil


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
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
        "--arch",
        type=str,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    copy_files = [
        ("configfsf.guess", "config.guess"),
        ("configfsf.sub", "config.sub"),
    ]
    for source, destination in copy_files:
        shutil.copyfile(args.source_dir / source, args.source_dir / destination)

    configure_options = [
        "--prefix=/usr",
        "--enable-cxx",
        "--disable-static",
        f"--build={args.arch}-pc-linux-gnu",
        f"--docdir=/usr/share/doc/gmp-{args.version}",
    ]
    cmds = [
        [str(args.source_dir / "configure"), *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "html"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )

    install_cmds = [
        ["make", "install"],
        ["make", "install-html"],
    ]
    for install_cmd in install_cmds:
        subprocess.run(
            install_cmd,
            check=True,
            cwd=args.source_dir,
        )


if __name__ == '__main__':
    main()
