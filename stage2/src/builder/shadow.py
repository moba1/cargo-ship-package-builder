import pathlib
from shutil import chown
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

    subprocess.run(
        ["sed", "-i", "s/groups$(EXEEXT) //", "src/Makefile.in"],
        cwd=args.source_dir,
        check=True,
    )
    sed_expressions = [
        "s/groups\.1 / /",
        "s/getspnam\.3 / /",
        "s/passwd\.5 / /",
    ]
    for expr in sed_expressions:
        subprocess.run(
            ["find", "man", "-name", "Makefile.in", "-exec", "sed", "-i", expr, "{}", ";"],
            check=True,
            cwd=args.source_dir,
        )
    sed_expressions = [
        "s:#ENCRYPT_METHOD DES:ENCRYPT_METHOD SHA512:",
        "s:/var/spool/mail:/var/mail:",
        "/PATH=/{s@/sbin:@@;s@/bin:@@}",
    ]
    sed_cmd = ["sed"]
    for expr in sed_expressions:
        sed_cmd.append("-e")
        sed_cmd.append(expr)
    subprocess.run(
        [*sed_cmd, "-i", "etc/login.defs"],
        check=True,
        cwd=args.source_dir,
    )

    subprocess.run(
        ["sed", "-e", "224s/rounds/min_rounds/", "-i", "libmisc/salt.c"],
        check=True,
        cwd=args.source_dir,
    )

    cmds = [
        ["touch", "/usr/bin/passwd"],
        [str(args.source_dir / "configure"), "--sysconfdir=/etc", "--with-group-name-max-length=32"],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["make", "exec_prefix=/usr", "install"],
        ["make", "-C", "man", "install-man"],
        ["mkdir", "-p", "/etc/default"],
        ["useradd", "-D", "--gid", "999"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )

    cmds = [
        ["pwconv"],
        ["grpconv"],
    ]
    for cmd in cmds:
        subprocess.run(cmd, check=True)
    subprocess.run(
        ["sed", "-i", "s/yes/no/", "/etc/default/useradd"],
        check=True,
    )


if __name__ == '__main__':
    main()
