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

    configure_options = [
        "--prefix=/usr",
        "--disable-static",
        "--with-gcc-arch=native",
        "--disable-exec-static-tramp",
    ]
    cmds = [
        [str(args.source_dir / "configure"), *configure_options],
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
