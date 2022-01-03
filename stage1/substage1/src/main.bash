#!/usr/bin/env bash

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"
. "$SOURCE_DIR/init.bash"
. "$SOURCE_DIR/version.bash"

set -e
bash "$SOURCE_DIR/builder/main.bash"
set +e

cp -Rf "$WORK_ROOT/"* "$1"

mkdir -pv "$1"/{boot,home,mnt,opt,srv}

mkdir -pv "$1"/etc/{opt,sysconfig}
mkdir -pv "$1"/lib/firmware
mkdir -pv "$1"/media/{floppy,cdrom}
mkdir -pv "$1"/usr/{,local/}{include,src}
mkdir -pv "$1"/usr/local/{bin,lib,sbin}
mkdir -pv "$1"/usr/{,local/}share/{color,dict,doc,info,locale,man}
mkdir -pv "$1"/usr/{,local/}share/{misc,terminfo,zoneinfo}
mkdir -pv "$1"/usr/{,local/}share/man/man{1..8}
mkdir -pv "$1"/var/{cache,local,log,mail,opt,spool}
mkdir -pv "$1"/var/lib/{color,misc,locate}

cat > "$1/etc/hosts" << EOF
127.0.0.1  localhost $(hostname)
::1        localhost
EOF

cat > "$1/etc/passwd" << "EOF"
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/dev/null:/bin/false
daemon:x:6:6:Daemon User:/dev/null:/bin/false
messagebus:x:18:18:D-Bus Message Daemon User:/run/dbus:/bin/false
systemd-bus-proxy:x:72:72:systemd Bus Proxy:/:/bin/false
systemd-journal-gateway:x:73:73:systemd Journal Gateway:/:/bin/false
systemd-journal-remote:x:74:74:systemd Journal Remote:/:/bin/false
systemd-journal-upload:x:75:75:systemd Journal Upload:/:/bin/false
systemd-network:x:76:76:systemd Network Management:/:/bin/false
systemd-resolve:x:77:77:systemd Resolver:/:/bin/false
systemd-timesync:x:78:78:systemd Time Synchronization:/:/bin/false
systemd-coredump:x:79:79:systemd Core Dumper:/:/bin/false
uuidd:x:80:80:UUID Generation Daemon User:/dev/null:/bin/false
systemd-oom:x:81:81:systemd Out Of Memory Daemon:/:/bin/false
nobody:x:99:99:Unprivileged User:/dev/null:/bin/false
EOF

cat > "$1/etc/group" << "EOF"
root:x:0:
bin:x:1:daemon
sys:x:2:
kmem:x:3:
tape:x:4:
tty:x:5:
daemon:x:6:
floppy:x:7:
disk:x:8:
lp:x:9:
dialout:x:10:
audio:x:11:
video:x:12:
utmp:x:13:
usb:x:14:
cdrom:x:15:
adm:x:16:
messagebus:x:18:
systemd-journal:x:23:
input:x:24:
mail:x:34:
kvm:x:61:
systemd-bus-proxy:x:72:
systemd-journal-gateway:x:73:
systemd-journal-remote:x:74:
systemd-journal-upload:x:75:
systemd-network:x:76:
systemd-resolve:x:77:
systemd-timesync:x:78:
systemd-coredump:x:79:
uuidd:x:80:
systemd-oom:x:81:81:
wheel:x:97:
nogroup:x:99:
users:x:999:
EOF
