import pathlib
import subprocess
import argparse
import os
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
        print("rootsbindir=/usr/sbin", file=configparms)

    configure_options = [
        f"--prefix=/usr",
        "--disable-werror",
        "--enable-kernel=3.2",
        "--enable-stack-protector=strong",
        f"--with-headers=/usr/include",
        f"libc_cv_slibdir=/usr/lib",
    ]
    cmds = [
        [args.source_dir / "configure", *configure_options],
        ["make", f"-j{multiprocessing.cpu_count()}"],
        ["touch", "/etc/ld.so.conf"],
        ["sed", "/test-installation/s@$(PERL)@echo not running@", "-i", args.source_dir / "Makefile"],
        ["make", "install"],
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
        ["sed", "/RTLDLIST=/s@/usr@@g", "-i", "/usr/bin/ldd"],
        check=True,
    )

    subprocess.run(
        ["cp", "-v", str(args.source_dir / "nscd" / "nscd.conf"), "/etc/nsdc.conf"],
        check=True,
        cwd=build_dir,
    )
    os.makedirs("/var/cache/nscd", exist_ok=True)
    install_args = [
        [str(args.source_dir / "nscd" / "nscd.tmpfiles"), "/usr/lib/tmpfiles.d/nscd.conf"],
        [str(args.source_dir / "nscd" / "nscd.service"), "/usr/lib/systemd/system/nscd.service"],
    ]
    for args in install_args:
        subprocess.run(
            ["install", "-v", "-Dm644", *args],
            check=True,
        )

    os.makedirs("/usr/lib/locale", exist_ok=True),
    subprocess.run(
        ["bash", "-c", "localedef -i POSIX -f UTF-8 C.UTF-8 2> /dev/null || true"],
        check=True,
    )
    subprocess.run(
        ["make", "localedata/install-locales"],
        check=True,
        cwd=build_dir,
    )

    with open("/etc/nsswitch.conf", 'w+') as nsswitch_conf:
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
