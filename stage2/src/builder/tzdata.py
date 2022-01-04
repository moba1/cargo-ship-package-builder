import pathlib
import subprocess
import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    parser.add_argument(
        "--dist-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    zoneinfo_dir = args.dist_dir / 'usr' / 'share' / 'zoneinfo'
    subprocess.run(
        ["bash", "-c", f"mkdir -pv '{zoneinfo_dir}'/{{posix,right}}"],
        check=True,
    )

    timezones = [
        "etcetera",
        "southamerica",
        "northamerica",
        "europe",
        "africa",
        "antarctica",
        "asia",
        "australasia",
        "backward"
    ]
    for timezone in timezones:
        zic_args = [
            ("/dev/null", zoneinfo_dir),
            ("/dev/null", zoneinfo_dir / "posix"),
            ("leapseconds", zoneinfo_dir / "right"),
        ]
        for zic_arg in zic_args:
            subprocess.run(
                ["zic", "-L", zic_arg[0], "-d", str(zic_arg[1]), timezone],
                check=True,
                cwd=args.source_dir,
            )

    cmds = [
        ["cp", "-v", "zone.tab", "zone1970.tab", "iso3166.tab", str(zoneinfo_dir)],
        ["zic", "-d", str(zoneinfo_dir), "-p", "America/New_York"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )


if __name__ == '__main__':
    main()
