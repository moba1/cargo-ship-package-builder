#!/usr/bin/env bash

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

. "$SOURCE_DIR/init.bash"
. "$SOURCE_DIR/version.bash"

export CROSS_TOOLCHAIN_DIR="$WORK_ROOT/tools"

. "$SOURCE_DIR/roles/cross-toolchain/main.bash"
