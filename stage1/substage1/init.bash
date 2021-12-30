#!/usr/bin/env bash

export DIST_DIR=/var/tmp

mkdir -pv "$WORK_ROOT"/{etc,var} "$WORK_ROOT"/usr/{bin,lib,sbin}
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64) mkdir -pv "$WORK_ROOT/lib64" ;;
esac
for dir in bin lib sbin
do
  ln -sfnv "usr/$dir" "$WORK_ROOT/$dir"
done
ls -l "$WORK_ROOT/bin"

mkdir -pv "$DIST_DIR"

. /etc/bashrc
