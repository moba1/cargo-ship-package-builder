#!/usr/bin/env bash

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

. "$SOURCE_DIR/init.bash"
. "$SOURCE_DIR/version.bash"

export CROSS_TOOLCHAIN_DIR="$WORK_ROOT/tools"

set -e
commands=(
  "$SOURCE_DIR/cross-toolchain/main.bash"
  "$SOURCE_DIR/stage1/main.bash"
)
for command in "${commands[@]}"
do
  bash "$command"
done
set +e

