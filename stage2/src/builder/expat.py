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
        f"--docdir=/usr/share/doc/expat-{args.version}",
        "--disable-static",
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

    subprocess.run(
        ["bash", "-c", f"install -v -m644 doc/*.{{html,png,css}} /usr/share/doc/expat-{args.version}"],
        check=True,
        cwd=args.source_dir,
    )


if __name__ == '__main__':
    main()
