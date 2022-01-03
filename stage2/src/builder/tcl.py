import pathlib
import subprocess
import argparse
import multiprocessing
import typing


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
        "--arch",
        type=str,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    unix_dir = args.source_dir / "unix"
    configure_cmd = [str(unix_dir / "configure"), "--prefix=/usr", "--mandir=/usr/share/man"]
    if args.arch == "x86_64":
        configure_cmd.append("--enable-64bit")
    cmds = [
        configure_cmd,
        ["make", f"-j{multiprocessing.cpu_count()}"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=unix_dir,
        )

    major, minor, _ = args.version.split('.')
    def sed(target: typing.Union[pathlib.Path, str], *expressions: typing.List[str]) -> typing.List[str]:
        cmd = ["sed", "-i", str(target)]
        for expr in expressions:
            cmd.append("-e")
            cmd.append(expr)
        return cmd
    cmds = [
        sed(
            "tclConfig.sh",
            f"s|{args.source_dir / 'unix'}|/usr/lib|",
            f"s|{args.source_dir}|/usr/include|",
        ),
        sed(
            "pkgs/tdbc1.1.2/tdbcConfig.sh",
            f"s|{args.source_dir / 'unix' / 'pkgs' / 'tdbc1.1.2'}|/usr/lib/tdbc1.1.2|",
            f"s|{args.source_dir / 'pkgs' / 'tdbc1.1.2' / 'generic'}|/usr/include|",
            f"s|{args.source_dir / 'pkgs' / 'tdbc1.1.2' / 'library'}|/usr/lib/tcl{major}.{minor}|",
            f"s|{args.source_dir / 'pkgs' / 'tdbc1.1.2'}|/usr/include|",
        ),
        sed(
            "pkgs/itcl4.2.1/itclConfig.sh",
            f"s|{args.source_dir / 'unix' / 'pkgs' / 'itcl4.2.1'}|/usr/lib/itcl4.2.1|",
            f"s|{args.source_dir / 'pkgs' / 'itcl4.2.1' / 'generic'}|/usr/include|",
            f"s|{args.source_dir / 'pkgs' / 'itcl4.2.1'}|/usr/include|",
        )
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=unix_dir,
        )

    cmds = [
        ["make", "install"],
        ["chmod", "-v", "u+w", f"/usr/lib/libtcl{major}.{minor}.so"],
        ["make", "install-private-headers"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=unix_dir,
        )

    subprocess.run(
        ["ln", "-sfnv", f"tclsh{major}.{minor}", "/usr/bin/tclsh"],
        check=True,
    )

    subprocess.run(
        ["bash", "-c", "mv /usr/share/man/man3/{Thread,Tcl_Thread}.3"],
        check=True,
    )


if __name__ == '__main__':
    main()
