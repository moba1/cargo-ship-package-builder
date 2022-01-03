import shutil
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
        "--disable-debuginfod",
        "--enable-libdebuginfod=dummy",
    ]
    cmds = [
        [str(args.source_dir / "configure"), *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "-C", "libelf", "install"],
        ["install", "-vm644", "config/libelf.pc", "/usr/lib/pkgconfig"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )

    shutil.rmtree("/usr/lib/libelf.a", ignore_errors=True)


if __name__ == '__main__':
    main()
