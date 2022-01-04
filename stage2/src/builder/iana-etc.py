import pathlib
import subprocess
import argparse


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

    subprocess.run(
        ["cp", "services", "protocols", str(args.dist_dir / "etc")],
        cwd=args.source_dir,
        check=True,
    )


if __name__ == '__main__':
    main()
