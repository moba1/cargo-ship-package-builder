#!/usr/bin/env bash

set -e

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

python3 \
  "$SOURCE_DIR/binutils.py" \
  --version "$BINUTILS_VERSION" \
  --dist-dir "$DIST_DIR" \
  --target "$TARGET" \
  --prefix "$CROSS_TOOLCHAIN_DIR" \
  --sysroot "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/gcc.py" \
  --gcc-version "$GCC_VERSION" \
  --mpc-version "$MPC_VERSION" \
  --mpfr-version "$MPFR_VERSION" \
  --gmp-version "$GMP_VERSION" \
  --dist-dir "$DIST_DIR" \
  --target "$TARGET" \
  --prefix "$CROSS_TOOLCHAIN_DIR" \
  --sysroot "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/linux-api-header.py" \
  --version "$LINUX_VERSION" \
  --dist-dir "$DIST_DIR" \
  --install-dir "$WORK_ROOT/usr"

python3 \
  "$SOURCE_DIR/glibc.py" \
  --version "$GLIBC_VERSION" \
  --dist-dir "$DIST_DIR" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET"

(
  set -e

  echo 'int main(){}' > /tmp/dummy.c
  trap 'rm -vf /tmp/a.out /tmp/dummy.c' 1 2 3 15
  "$TARGET-gcc" /tmp/dummy.c -o /tmp/a.out
  readelf -l /tmp/a.out | grep '/ld-linux'
)

"$WORK_ROOT/tools/libexec/gcc/$TARGET/$GCC_VERSION/install-tools/mkheaders"

python3 \
  "$SOURCE_DIR/libstdc++.py" \
  --dist-dir "$DIST_DIR" \
  --gcc-version "$GCC_VERSION" \
  --install-dir "$WORK_ROOT" \
  --target "$TARGET"
