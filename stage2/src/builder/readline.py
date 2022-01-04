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

    cmds = [
        ["sed", "-i", "/MV.*old/d", "Makefile.in"],
        ["sed", "-i", "/{OLDSUFF}/c:", "support/shlib-install"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir
        )

    configure_options = [
        f"--prefix={args.dist_dir / 'usr'}",
        "--disable-static",
        "--with-curses",
        f"--docdir={args.dist_dir / 'usr' / 'share' / 'doc' / f'readline-{args.version}'}",
    ]
    cmds = [
        [str(args.source_dir / "configure"), *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}", "SHLIB_LIBS=-lncursesw"],
        ["make", "SHLIB_LIBS=-lncursesw", "install"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )


if __name__ == '__main__':
    main()
