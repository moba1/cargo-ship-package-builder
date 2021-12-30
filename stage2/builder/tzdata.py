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
    args = parser.parse_args()

    zoneinfo_dir = "/usr/share/zoneinfo"
    zoneinfos = ["posix", "right"]
    for zoneinfo in zoneinfos:
        os.makedirs(f"{zoneinfo_dir}/{zoneinfo}", exist_ok=True)

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
            ("/dev/null", f"{zoneinfo_dir}/posix"),
            ("leapseconds", f"{zoneinfo_dir}/right"),
        ]
        for zic_arg in zic_args:
            subprocess.run(
                ["zic", "-L", zic_arg[0], "-d", zic_arg[1], timezone],
                check=True,
                cwd=args.source_dir,
            )

    cmds = [
        ["cp", "-v", "zone.tab", "zone1970.tab", "iso3166.tab", zoneinfo_dir],
        ["zic", "-d", zoneinfo_dir, "-p", "America/New_York"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )


if __name__ == '__main__':
    main()
