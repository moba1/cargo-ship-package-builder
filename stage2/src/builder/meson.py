import pathlib
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=pathlib.Path,
        action='store',
        required=True,
    )
    args = parser.parse_args()

    cmds = [
        ["python3", "setup.py", "build"],
        ["python3", "setup.py", "install", "--root=dest"],
        ["bash", "-c", "cp -Rv dest/* /"],
        ["install", "-vDm644", "data/shell-completions/bash/meson", "/usr/share/bash-completion/completions/meson"],
        ["install", "-vDm644", "data/shell-completions/zsh/_meson", "/usr/share/zsh/site-functions/_meson"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )


if __name__ == '__main__':
    main()
