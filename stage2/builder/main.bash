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

python3 \
  "$SOURCE_DIR/zlib.py" \
  --source-dir "$DIST_DIR/zlib-$ZLIB_VERSION"

python3 \
  "$SOURCE_DIR/bzip2.py" \
  --source-dir "$DIST_DIR/bzip2-$BZIP2_VERSION" \
  --patch-file "$DIST_DIR/bzip2-$BZIP2_VERSION-install_docs-1.patch" \
  --version "$BZIP2_VERSION"

python3 \
  "$SOURCE_DIR/xz.py" \
  --source-dir "$DIST_DIR/xz-$XZ_VERSION" \
  --version "$XZ_VERSION"

python3 \
  "$SOURCE_DIR/zstd.py" \
  --source-dir "$DIST_DIR/zstd-$ZSTD_VERSION"
