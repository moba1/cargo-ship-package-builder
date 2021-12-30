#!/usr/bin/env bash

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"


. "$SOURCE_DIR/version.bash"

set -e
bash "$SOURCE_DIR/builder/main.bash"
set +e
