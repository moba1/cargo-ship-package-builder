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
    parser.add_argument(
        "--ssl-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    configure_options = [
        "--prefix=/usr",
        f"--openssldir={args.ssl_dir}",
        "--libdir=lib",
        "shared",
        "zlib-dynamic",
    ]
    cmds = [
        [str(args.source_dir / "config"), *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["sed", "-i", "/INSTALL_LIBS/s/libcrypto.a libssl.a//", "Makefile"],
        ["make", "install"]
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )

    shutil.move("/usr/share/doc/openssl", f"/usr/share/doc/openssl-{args.version}")
    subprocess.run(
        ["bash", "-c", f"cp -vfr doc/* /usr/share/doc/openssl-{args.version}"],
        check=True,
        cwd=args.source_dir,
    )


if __name__ == '__main__':
    main()
