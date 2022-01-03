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

    configure_options = [
        "--prefix=/usr",
        "--with-tcl=/usr/lib",
        "--enable-shared",
        "--mandir=/usr/share/man",
        "--with-tclinclude=/usr/include"
    ]
    cmds = [
        [str(args.source_dir / "configure"), *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "install"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )

    subprocess.run(
        ["ln", "-sfv", f"expect{args.version}/libexpect{args.version}", "/usr/lib"],
        check=True,
    )


if __name__ == '__main__':
    main()
