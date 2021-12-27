#!/usr/bin/env bash

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

python3 \
  "$SOURCE_DIR/m4.py" \
  --dist-dir "$DIST_DIR" \
  --version "$M4_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET"
