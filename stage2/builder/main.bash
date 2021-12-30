#!/usr/bin/env bash

set -e

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

python3 \
  "$SOURCE_DIR/man-pages.py" \
  --source-dir "$DIST_DIR/man-pages-$MANPAGES_VERSION"

python3 \
  "$SOURCE_DIR/iana-etc.py" \
  --source-dir "$DIST_DIR/iana-etc-$IANAETC_VERSION"

python3 \
  "$SOURCE_DIR/glibc.py" \
  --source-dir "$DIST_DIR/glibc-$GLIBC_VERSION" \
  --patch-file "$DIST_DIR/glibc-$GLIBC_VERSION-fhs-1.patch"

python3 \
  "$SOURCE_DIR/tzdata.py" \
  --source-dir "$DIST_DIR/tzdata-$TZDATA_VERSION"

python3 \
  "$SOURCE_DIR/dynamic-loader.py"
