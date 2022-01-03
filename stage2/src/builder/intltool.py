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

    subprocess.run(
        ["sed", "-i", "s:\\${:\\$\\{:", "intltool-update.in"],
        check=True,
        cwd=args.source_dir,
    )

    cmds = [
        [str(args.source_dir / "configure"), "--prefix=/usr"],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "install"],
        ["install", "-v", "-Dm644", "doc/I18N-HOWTO", f"/usr/share/doc/intltool-{args.version}/I18N-HOWTO"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )


if __name__ == '__main__':
    main()
