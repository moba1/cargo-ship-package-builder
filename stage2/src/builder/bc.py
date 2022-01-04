import pathlib
import subprocess
import argparse
import multiprocessing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=pathlib.PosixPath,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--dist-dir",
        type=pathlib.PosixPath,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    cmds = [
        ["bash", "-c", f"CC=gcc {args.source_dir / 'configure'} --prefix='{args.dist_dir / 'usr'}' -G -O3"],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "install"]
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )


if __name__ == '__main__':
    main()
