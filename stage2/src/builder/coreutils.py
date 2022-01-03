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

    configure_cmd = "FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=/usr --enable-no-install-program=kill,uptime"
    cmds = [
        ["autoreconf", "-fiv"],
        ["bash", "-c", configure_cmd]
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "install"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )

    shutil.move("/usr/bin/chroot", "/usr/sbin")
    shutil.move("/usr/share/man/man1/chroot.1", "/usr/share/man/man8/chroot.8")
    subprocess.run(
        ["sed", "-i", 's/"1"/"8"/', '/usr/share/man//man8/chroot.8'],
        check=True,
    )


if __name__ == '__main__':
    main()
