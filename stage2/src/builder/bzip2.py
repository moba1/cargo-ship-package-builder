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
        "--patch-file",
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

    subprocess.run(
        ["patch", "-Np1", "-i", args.patch_file],
        check=True,
        cwd=args.source_dir,
    )

    subprocess.run(
        ["sed", "-i", "s@\\(ln -s -f \\)$(PREFIX)/bin/@\\1@", "Makefile"],
        check=True,
        cwd=args.source_dir,
    )

    subprocess.run(
        ["sed", "-i", "s@(PREFIX)/man@(PREFIX)/share/man@g", "Makefile"],
        check=True,
        cwd=args.source_dir,
    )

    cmds = [
        ["make", "-f", "Makefile-libbz2_so"],
        ["make", "clean"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )

    cmds = [
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", f"PREFIX={args.dist_dir / 'usr'}", "install"],
        ["bash", "-c", f"cp -av libbz2.so.* '{args.dist_dir / 'usr' / 'lib'}'"],
        ["ln", "-sfnv", f"libbz2.so.{args.version}", str(args.dist_dir / 'usr' / 'lib' / 'libbz2.so')],
        ["cp", "-v", "bzip2-shared", str(args.dist_dir / 'usr' / 'bin' / 'bzip2')],
        ["ln", "-sfvn", "bzip2", str(args.dist_dir / 'usr' / 'bin' / 'bzcat')],
        ["ln", "-sfnv", "bzip2", str(args.dist_dir / 'usr' / 'bin' / 'bunzip2')],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            cwd=args.source_dir,
            check=True,
        )

    subprocess.run(
        ["rm", "-fv", str(args.dist_dir / 'usr' / 'lib' / 'libbz2.a')],
        cwd=args.source_dir,
    )


if __name__ == '__main__':
    main()
