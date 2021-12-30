#!/usr/bin/env bash

cd "$DIST_DIR/gcc-$GCC_VERSION-for-libstdc++"

ln -snfv gthr-posix.h libgcc/gthr-default.h

mkdir -pv build
cd build

# ../libstdc++-v3/configure \
#   CXXFLAGS="-g -O2 -DGNU_SOURCE" \
#   --prefix=/usr \
#   --disable-multilib \
#   --disable-nls \
#   --host=$(uname -m)
