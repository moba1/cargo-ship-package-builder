import pathlib
import shutil
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    subprocess.run(
        ["cp", "services", "protocols", "/etc"],
        cwd=args.source_dir,
        check=True,
    )


if __name__ == '__main__':
    main()
