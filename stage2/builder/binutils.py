import os
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
    args = parser.parse_args()

    subprocess.run(
        ["patch", "-Np1", "-i", str(args.patch_file)],
        check=True,
        cwd=args.source_dir,
    )

    cmds = [
        ["sed", "-i", "63d", "etc/texi2pod.pl"],
        ["find", "-name", "\\*.1", "-delete"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )

    build_dir = args.source_dir / "build"
    os.makedirs(build_dir, exist_ok=True)

    configure_options = [
        "--prefix=/usr",
        "--enable-gold",
        "--enable-ld=default",
        "--enable-plugins",
        "--enable-shared",
        "--disable-werror",
        "--enable-64-bit-bfd",
        "--with-system-zlib",
    ]
    cmds = [
        [str(args.source_dir / "configure"), *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}", "tooldir=/usr"],
        ["make", "tooldir=/usr", "install", "-j1"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=build_dir,
        )

    subprocess.run(
        ["bash", "-c", "rm -fv /usr/lib/lib{bfd,ctf,ctf-nobfd,opcodes}.a"],
        check=True,
    )


if __name__ == '__main__':
    main()
