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
    args = parser.parse_args()

    configure_options = [
        "--prefix=/usr",
        "--sysconfdir=/etc",
        "--with-xz",
        "--with-zstd",
        "--with-zlib",
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

    targets = [
        "depmod",
        "insmod",
        "modinfo",
        "modprobe",
        "rmmod",
    ]
    for target in targets:
        subprocess.run(
            ["ln", "-sfnv", "../bin/kmod", f"/usr/sbin/{target}"],
            check=True,
        )
    subprocess.run(
        ["ln", "-sfnv", "kmod", "/usr/bin/lsmod"],
        check=True,
    )

if __name__ == '__main__':
    main()
