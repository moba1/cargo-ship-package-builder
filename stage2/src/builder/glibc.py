import pathlib
import subprocess
import argparse
import os
import multiprocessing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=pathlib.PosixPath,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--patch-file",
        type=pathlib.PosixPath,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--dist-dir",
        type=pathlib.PosixPath,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    subprocess.run(
        ["sed", "-e", "/NOTIFY_REMOVED)/s/)/ \\&\\& data.attr != NULL)/", "-i", "sysdeps/unix/sysv/linux/mq_notify.c"],
        check=True,
        cwd=args.source_dir
    )

    subprocess.run(
        ["patch", "-Np1", "-i", str(args.patch_file)],
        cwd=args.source_dir,
        check=True,
    )

    build_dir = args.source_dir / "build"
    os.makedirs(build_dir, exist_ok=True)
    with open(build_dir / "configparms", 'w') as configparms:
        print(f"rootsbindir=/usr/sbin", file=configparms)

    configure_options = [
        "--prefix=/usr",
        "--disable-werror",
        "--enable-kernel=3.2",
        "--enable-stack-protector=strong",
        "--with-headers=/usr/include",
        f"libc_cv_slibdir=/usr/lib",
    ]
    cmds = [
        [args.source_dir / "configure", *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["touch", str(args.dist_dir / 'etc' / 'ld.so.conf')],
        ["sed", "/test-installation/s@$(PERL)@echo not running@", "-i", args.source_dir / "Makefile"],
        ["make", f"DESTDIR={args.dist_dir}", "install"],
    ]
    for cmd in cmds:
        cmd = list(map(str, cmd))
        print(' '.join(cmd))
        subprocess.run(
            cmd,
            check=True,
            cwd=build_dir,
        )

    subprocess.run(
        ["sed", "/RTLDLIST=/s@/usr@@g", "-i", str(args.dist_dir / 'usr' / 'bin' / 'ldd')],
        check=True,
    )

    subprocess.run(
        ["cp", "-v", str(args.source_dir / "nscd" / "nscd.conf"), str(args.dist_dir / 'etc' / 'nscd.conf')],
        check=True,
        cwd=build_dir,
    )
    os.makedirs(args.dist_dir / 'var' / 'cache' / 'nscd', exist_ok=True)
    install_args = [
        [str(args.source_dir / "nscd" / "nscd.tmpfiles"), str(args.dist_dir / 'usr' / 'lib' / 'tmpfiles.d' / 'nscd.conf')],
        [str(args.source_dir / "nscd" / "nscd.service"), str(args.dist_dir / 'usr' / 'lib' / 'systemd' / 'system' / 'nscd.service')],
    ]
    for install_arg in install_args:
        subprocess.run(
            ["install", "-v", "-Dm644", *install_arg],
            check=True,
        )

    os.makedirs(args.dist_dir / 'usr' / 'lib' / 'locale', exist_ok=True),
    subprocess.run(
        ["bash", "-c", f"localedef -i POSIX -f UTF-8 --prefix={args.dist_dir} C.UTF-8 2> /dev/null || true"],
        check=True,
    )

    with open(args.dist_dir / 'etc' / 'nsswitch.conf', 'w+') as nsswitch_conf:
        nsswitch_conf.truncate(0)
        lines = [
            "#Begin /etc/nsswitch.conf",
            "",
            "passwd: files",
            "group: files",
            "shadow: files",
            "",
            "hosts: files dns",
            "networks: files",
            "",
            "protocols: files",
            "services: files",
            "ethers: files",
            "rpc: files",
            "",
            "# End /etc/nsswitch.conf"
        ]
        for line in lines:
            print(line, file=nsswitch_conf)


if __name__ == '__main__':
    main()
