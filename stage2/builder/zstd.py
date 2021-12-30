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
    args = parser.parse_args()

    cmds = [
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "check"],
        ["make", "prefix=/usr", "install"]
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            cwd=args.source_dir,
            check=True,
        )

    subprocess.run(
        ["rm", "-fv", "/usr/lib/libzstd.a"],
        check=True,
    )


if __name__ == '__main__':
    main()
