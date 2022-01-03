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
        "--bindir=/usr/bin",
        "--localstatedir=/var",
        "--disable-logger",
        "--disable-whois",
        "--disable-rcp",
        "--disable-rexec",
        "--disable-rlogin",
        "--disable-rsh",
        "--disable-servers",
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

    subprocess.run(
        ["bash", "-c", "mv -v /usr/{,s}bin/ifconfig"],
        check=True,
    )


if __name__ == '__main__':
    main()
