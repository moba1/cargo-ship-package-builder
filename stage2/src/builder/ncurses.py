import os
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
    args = parser.parse_args()

    configure_options = [
        "--prefix=/usr",
        "--mandir=/usr/share/man",
        "--with-shared",
        "--without-debug",
        "--without-normal",
        "--enable-pc-files",
        "--enable-widec",
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

    libs = [
        "ncurses",
        "form",
        "panel",
        "menu"
    ]
    for lib_name in libs:
        shutil.rmtree(f"/usr/lib/lib{lib_name}.so", ignore_errors=True)
        with open(f"/usr/lib/lib{lib_name}.so", 'w') as lib:
            lib.write(f"INPUT(-l{lib_name}w)")
        subprocess.run(
            ["ln", "-sfnv", f"{lib_name}w.pc", f"/usr/lib/pkgconfig/{lib_name}.pc"],
            check=True,
        )

    shutil.rmtree("/usr/lib/libcursesw.so", ignore_errors=True)
    with open("/usr/lib/libcursesw.so", 'w') as lib:
        lib.write("INPUT(-lncursesw)")
    subprocess.run(
        ["ln", "-sfnv", "libncurses.so", "/usr/lib/curses.so"],
        check=True
    )

    shutil.rmtree("/usr/lib/libncurses++w.a", ignore_errors=True)

    os.makedirs(f"/usr/share/doc/ncurses-{args.version}", exist_ok=True)
    subprocess.run(
        ["bash", "-c", f"cp -v -R doc/* /usr/share/doc/ncurses-{args.version}"],
        check=True,
        cwd=args.source_dir,
    )


if __name__ == '__main__':
    main()
