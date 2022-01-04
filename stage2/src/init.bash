#!/usr/bin/env bash

export WORK_ROOT=/work

mkdir -pv "$WORK_ROOT"
mkdir -pv "$WORK_ROOT"/{boot,home,mnt,opt,srv}
mkdir -pv "$WORK_ROOT"/etc/{opt,sysconfig}
mkdir -pv "$WORK_ROOT"/lib/firmware
mkdir -pv "$WORK_ROOT"/media/{floppy,cdrom}
mkdir -pv "$WORK_ROOT"/usr/{,local/}{include,src}
mkdir -pv "$WORK_ROOT"/usr/local/{bin,lib,sbin}
mkdir -pv "$WORK_ROOT"/usr/{,local/}share/{color,dict,doc,info,locale,man}
mkdir -pv "$WORK_ROOT"/usr/{,local/}share/{misc,terminfo,zoneinfo}
mkdir -pv "$WORK_ROOT"/usr/{,local/}share/man/man{1..8}
mkdir -pv "$WORK_ROOT"/var/{cache,local,log,mail,opt,spool}
mkdir -pv "$WORK_ROOT"/var/lib/{color,misc,locate}

ln -sfv /run "$WORK_ROOT"/var/run
ln -sfv /run/lock "$WORK_ROOT"/var/lock

install -dv -m 0750 "$WORK_ROOT"/root
install -dv -m 1777 "$WORK_ROOT"/tmp "$WORK_ROOT"/var/tmp
