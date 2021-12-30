#!/usr/bin/env bash

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"
. "$SOURCE_DIR/init.bash"
. "$SOURCE_DIR/version.bash"

set -e
bash "$SOURCE_DIR/src/main.bash"
set +e

cp -Rf "$WORK_ROOT/"* "$1"
