import pathlib
import subprocess
import argparse
import multiprocessing
import os


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

    build_dir = args.source_dir / "build"
    os.makedirs(build_dir, exist_ok=True)

    cmds = [
        [str(args.source_dir / "configure"), "--prefix=/usr"],
        ["makeinfo", "--html", "--no-split", "-o", "doc/dejagnu.html", "../doc/dejagnu.texi"],
        ["makeinfo", "--plaintext", "-o", "doc/dejagnu.txt", "../doc/dejagnu.texi"],
        ["make", "install"],
        ["install", "-v", "-dm755", f"/usr/share/doc/dejagnu-{args.version}"],
        ["bash", "-c", f"install -v -m644 doc/dejagnu.{{html,txt}} /usr/share/doc/dejagnu-{args.version}"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=build_dir,
        )

    subprocess.run(
        ["ln", "-sfv", f"expect{args.version}/libexpect{args.version}", "/usr/lib"],
        check=True,
    )


if __name__ == '__main__':
    main()
