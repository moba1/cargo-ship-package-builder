import pathlib
import shutil
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
    parser.add_argument(
        "--doc",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    configure_options = [
        "--prefix=/usr",
        "--enable-shared",
        "--with-system-expat",
        "--with-system-ffi",
        "--with-ensurepip=yes",
        "--enable-optimizations",
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

    doc_dir = f"/usr/share/doc/python-{args.version}/html"
    subprocess.run(
        ["install", "-v", "-dm755", doc_dir],
        check=True,
        cwd=args.source_dir,
    )
    subprocess.run(
        ["bash", "-c", f"cp -Rfv '{args.doc}'/* '{doc_dir}'"],
        check=True,
    )


if __name__ == '__main__':
    main()
