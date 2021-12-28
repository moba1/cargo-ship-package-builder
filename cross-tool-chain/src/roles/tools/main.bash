#!/usr/bin/env bash

set -e

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

python3 \
  "$SOURCE_DIR/m4.py" \
  --dist-dir "$DIST_DIR" \
  --version "$M4_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/ncurses.py" \
  --dist-dir "$DIST_DIR" \
  --version "$NCURSES_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr" \
  --man-dir "/usr/share/man"

python3 \
  "$SOURCE_DIR/bash.py" \
  --dist-dir "$DIST_DIR" \
  --version "$BASH_VERSION_" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/coreutils.py" \
  --dist-dir "$DIST_DIR" \
  --version "$COREUTILS_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/diffutils.py" \
  --dist-dir "$DIST_DIR" \
  --version "$DIFFUTILS_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/file.py" \
  --dist-dir "$DIST_DIR" \
  --version "$FILE_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"
