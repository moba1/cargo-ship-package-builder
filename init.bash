#!/usr/bin/env bash

ARCH="$(uname -m)"

mkdir -pv "$WORK_ROOT"/{etc,var} "$WORK_ROOT"/usr/{bin,lib,sbin}
case "$ARCH" in
  x86_64) mkdir -pv "$WORK_ROOT/lib64" ;;
esac
for dir in bin lib sbin
do
  ln -sv "usr/$dir" "$WORK_ROOT/$dir"
done

mkdir -pv "$WORK_ROOT/tools"

cat > /etc/bashrc << EOF
set +h
umask 022
WORK_ROOT="$WORK_ROOT"
LC_ALL=POSIX
TARGET="$ARCH-lfs-linux-gnu"
PATH=/usr/bin
[ ! -L /bin ] && PATH="/bin:\$PATH"
PATH="\$WORK_ROOT/tools/bin:\$PATH"
CONFIG_SITE=$WORK_ROOT/usr/share/config.site
ANSIBLE_STDOUT_CALLBACK=debug
export WORK_ROOT LC_ALL TARGET PATH CONFIG_SITE ANSIBLE_STDOUT_CALLBACK
EOF

ln -sf /bin/bash /bin/sh

ansible-galaxy collection install community.general
