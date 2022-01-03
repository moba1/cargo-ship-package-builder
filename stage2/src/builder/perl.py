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
        "--version",
        type=str,
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

    major, minor, _ = args.version.split('.')
    env = os.environ.copy()
    env['BUILD_ZLIB'] = 'False'
    env['BUILD_BZIP2'] = '0'
    perl_dir = f"/usr/lib/perl{major}/{major}.{minor}"
    configure_options = [
        "-des",
        "Dprefix=/usr",
        "-Dvendorprefix=/usr",
        f"-Dprivlib={perl_dir}/core_perl",
        f"-Darchlib={perl_dir}/core_perl",
        f"-Dsitelib={perl_dir}/site_perl",
        f"-Dsitearch={perl_dir}/site_perl",
        f"-Dvendorlib={perl_dir}/vendor_perl",
        f"-Dvendorarch={perl_dir}/vendor_perl",
        "-Dman1dir=/usr/share/man/man1",
        "-Dman3dir=/usr/share/man/man3",
        "-Dpager=/usr/sbin/less -isR",
        "-Duseshrplib",
        "-Dusethreads",
    ]
    cmds = [
        ["sh", str(args.source_dir / "Configure"), *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "install"]
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
            env=env,
        )


if __name__ == '__main__':
    main()
