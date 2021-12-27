#!/usr/bin/env bash

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

. "$SOURCE_DIR/init.bash"
. "$SOURCE_DIR/version.bash"

export CROSS_TOOLCHAIN_DIR="$WORK_ROOT/tools"

commands=(
  "$SOURCE_DIR/roles/cross-toolchain/main.bash"
  "$SOURCE_DIR/roles/tools/main.bash"
)
for command in "${commands[@]}"
do
  bash "$command"
done
