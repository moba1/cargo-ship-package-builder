import pathlib
import subprocess
import argparse
import multiprocessing


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
    args = parser.parse_args()

    subprocess.run(
        ["sed", "-i", "/install -m.*STA/d", "libcap/Makefile"],
        check=True,
        cwd=args.source_dir,
    )

    cmds = [
        ["make", "prefix=/usr", "lib=lib", f"-j{multiprocessing.cpu_count()}"],
        ["make", "prefix=/usr", "lib=lib", "install"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )

    subprocess.run(
        ["bash", "-c", f"chmod -v 755 /usr/lib/lib{{cap,psx}}.so.{args.version}"],
        check=True,
    )


if __name__ == '__main__':
    main()
