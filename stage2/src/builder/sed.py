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

    cmds = [
        [str(args.source_dir / "configure"), "--prefix=/usr"],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "html"],
        ["make", "install"]
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )

    install_cmds = [
        ["install", "-d", "-m755", f"/usr/share/doc/sed-{args.version}"],
        ["install", "-m644", "doc/sed.html", f"/usr/share/doc/sed-{args.version}"],
    ]
    for cmd in install_cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )


if __name__ == '__main__':
    main()
