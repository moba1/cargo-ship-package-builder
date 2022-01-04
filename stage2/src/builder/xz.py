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
    parser.add_argument(
        "--dist-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    configure_options = [
        f"--prefix={args.dist_dir / 'usr'}",
        "--disable-static",
        f"--docdir={args.dist_dir / 'usr' / 'share' / 'doc' / f'xz-{args.version}'}",
    ]
    cmds = [
        [str(args.source_dir / "configure"), *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "install"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            cwd=args.source_dir,
            check=True,
        )


if __name__ == '__main__':
    main()
