#!/usr/bin/env bash

set -e

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

python3 \
  "$SOURCE_DIR/man-pages.py" \
  --prefix "/usr" \
  --source-dir "$DIST_DIR/man-pages-$MANPAGES_VERSION"

python3 \
  "$SOURCE_DIR/iana-etc.py" \
  --prefix "/etc" \
  --source-dir "$DIST_DIR/iana-etc-$IANAETC_VERSION"
