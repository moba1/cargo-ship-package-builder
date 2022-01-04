import argparse
import pathlib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dist-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    with open(args.dist_dir / 'etc' / 'ld.so.conf', 'w+') as ld_so_conf:
        ld_so_conf.truncate(0)
        lines = [
            "# Begin /etc/ld.so.conf",
            "/usr/local/lib",
            "/opt/lib",
        ]
        for line in lines:
            print(line, file=ld_so_conf)


if __name__ == '__main__':
    main()
