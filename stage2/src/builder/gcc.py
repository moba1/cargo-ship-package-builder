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
        "--arch",
        type=str,
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

    exprs = [
        '/static.*SIGSTKSZ/d',
        's/return kAltStackSize/return SIGSTKSZ * 4/',
    ]
    sed_cmd = ['sed']
    for expr in exprs:
        sed_cmd.append('-e')
        sed_cmd.append(expr)
    sed_cmd.append('-i'),
    sed_cmd.append('libsanitizer/sanitizer_common/sanitizer_posix_libcdep.cpp')
    subprocess.run(
        sed_cmd,
        check=True,
        cwd=args.source_dir,
    )

    if args.arch == 'x86_64':
        subprocess.run(
            ['sed', '-e', '/m64=/s/lib64/lib/', 'gcc/config/i386/t-linux64'],
            check=True,
            cwd=args.source_dir,
        )

    build_dir = args.source_dir / "build"
    os.makedirs(build_dir, exist_ok=True)

    configure_options = [
        "--prefix=/usr",
        "LD=ld",
        "--enable-languages=c,c++",
        "--disable-multilib",
        "--disable-bootstrap",
        "--with-system-zlib",
    ]
    cmds = [
        [str(args.source_dir / "configure"), *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "install"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=build_dir,
        )

    gcc_dump = subprocess.run(
        ["gcc", "-dumpmachine"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    shutil.rmtree(f"/usr/lib/gcc/{gcc_dump.stdout.strip()}/{args.version}/include-fixed/bits")

    subprocess.run(
        ["ln", "-svr", "/usr/bin/cpp", "/usr/lib"],
        check=True,
    )

    subprocess.run(
        ["ln", "-sfnv", f"../../libexec/gcc/{gcc_dump.stdout.strip()}/{args.version}/liblto_plugin.so", "/usr/lib/bfd-plugins/"],
        check=True,
    )

    load_dir = "/usr/share/gdb/auto-load/usr/lib"
    os.makedirs(load_dir, exist_ok=True)
    subprocess.run(
        ["bash", "-c", f"mv -v /usr/lib/*gdb.py '{load_dir}'"],
        check=True,
    )


if __name__ == '__main__':
    main()
