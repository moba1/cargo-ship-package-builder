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

python3 \
  "$SOURCE_DIR/findutils.py" \
  --dist-dir "$DIST_DIR" \
  --version "$FINDUTILS_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr" \
  --localstatedir "/var/lib/locate"

python3 \
  "$SOURCE_DIR/gawk.py" \
  --dist-dir "$DIST_DIR" \
  --version "$GAWK_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/grep.py" \
  --dist-dir "$DIST_DIR" \
  --version "$GREP_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/gzip.py" \
  --dist-dir "$DIST_DIR" \
  --version "$GZIP_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/make.py" \
  --dist-dir "$DIST_DIR" \
  --version "$MAKE_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/patch.py" \
  --dist-dir "$DIST_DIR" \
  --version "$PATCH_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/sed.py" \
  --dist-dir "$DIST_DIR" \
  --version "$SED_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/tar.py" \
  --dist-dir "$DIST_DIR" \
  --version "$TAR_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/xz.py" \
  --dist-dir "$DIST_DIR" \
  --version "$XZ_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr" \
  --docdir "/usr/share/share/doc/xz-$XZ_VERSION"

python3 \
  "$SOURCE_DIR/binutils.py" \
  --dist-dir "$DIST_DIR" \
  --version "$BINUTILS_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr"

python3 \
  "$SOURCE_DIR/gcc.py" \
  --dist-dir "$DIST_DIR" \
  --gcc-version "$GCC_VERSION" \
  --mpc-version "$MPC_VERSION" \
  --mpfr-version "$MPFR_VERSION" \
  --gmp-version "$GMP_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET" \
  --prefix "/usr" \
  --arch "$ARCH"
