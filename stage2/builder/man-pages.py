import pathlib
import shutil
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prefix",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--source-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    subprocess.run(
        ["make", f"prefix={args.prefix}", "install"],
        cwd=args.source_dir
    )

    shutil.rmtree(args.source_dir)


if __name__ == '__main__':
    main()
