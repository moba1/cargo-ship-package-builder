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
        ["python3", "configure.py", "--bootstrap"],
        ["install", "-vm755", "ninja", "/usr/bin/"],
        ["install", "-vDm644", "misc/bash-completion", "/usr/share/bash-completion/completions/ninja"],
        ["install", "-vDm644", "misc/zsh-completion", "/usr/share/zsh/site-functions/_ninja"],
    ]
    for cmd in cmds:
        subprocess.run(
            cmd,
            check=True,
            cwd=args.source_dir,
        )


if __name__ == '__main__':
    main()
