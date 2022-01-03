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

python3 \
  "$SOURCE_DIR/file.py" \
  --source-dir "$DIST_DIR/file-$FILE_VERSION"

python3 \
  "$SOURCE_DIR/readline.py" \
  --source-dir "$DIST_DIR/readline-$READLINE_VERSION" \
  --version "$READLINE_VERSION"

python3 \
  "$SOURCE_DIR/m4.py" \
  --source-dir "$DIST_DIR/m4-$M4_VERSION"

python3 \
  "$SOURCE_DIR/bc.py" \
  --source-dir "$DIST_DIR/bc-$BC_VERSION"

python3 \
  "$SOURCE_DIR/flex.py" \
  --source-dir "$DIST_DIR/flex-$FLEX_VERSION" \
  --version "$FLEX_VERSION"

python3 \
  "$SOURCE_DIR/tcl.py" \
  --source-dir "$DIST_DIR/tcl-$TCL_VERSION" \
  --version "$TCL_VERSION"

python3 \
  "$SOURCE_DIR/expect.py" \
  --source-dir "$DIST_DIR/expect-$EXPECT_VERSION" \
  --version "$EXPECT_VERSION"

python3 \
  "$SOURCE_DIR/dejagnu.py" \
  --source-dir "$DIST_DIR/dejagnu-$DEJAGNU_VERSION" \
  --version "$DEJAGNU_VERSION"

python3 \
  "$SOURCE_DIR/binutils.py" \
  --source-dir "$DIST_DIR/binutils-$BINUTILS_VERSION" \
  --patch-file "$DIST_DIR/binutils-$BINUTILS_VERSION-upstream_fix-1.patch"

python3 \
  "$SOURCE_DIR/gmp.py" \
  --source-dir "$DIST_DIR/gmp-$GMP_VERSION" \
  --version "$GMP_VERSION" \
  --arch "$ARCH"

python3 \
  "$SOURCE_DIR/mpfr.py" \
  --source-dir "$DIST_DIR/mpfr-$MPFR_VERSION" \
  --version "$MPFR_VERSION"

python3 \
  "$SOURCE_DIR/mpc.py" \
  --source-dir "$DIST_DIR/mpc-$MPC_VERSION" \
  --version "$MPC_VERSION"

python3 \
  "$SOURCE_DIR/attr.py" \
  --source-dir "$DIST_DIR/attr-$ATTR_VERSION" \
  --version "$ATTR_VERSION"

python3 \
  "$SOURCE_DIR/acl.py" \
  --source-dir "$DIST_DIR/acl-$ACL_VERSION" \
  --version "$ACL_VERSION"

python3 \
  "$SOURCE_DIR/libcap.py" \
  --source-dir "$DIST_DIR/libcap-$LIBCAP_VERSION" \
  --version "$LIBCAP_VERSION"

python3 \
  "$SOURCE_DIR/shadow.py" \
  --source-dir "$DIST_DIR/shadow-$SHADOW_VERSION"
