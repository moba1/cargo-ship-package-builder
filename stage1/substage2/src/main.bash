#!/usr/bin/env bash

set -e

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

bash "$SOURCE_DIR/libstdc++.bash" \
  -h "$TARGET" \
  -s "$DIST_DIR/gcc-$GCC_VERSION-for-libstdc++" \
  -p "/usr"

bash "$SOURCE_DIR/gettext.bash" \
  -s "$DIST_DIR/gettext-$GETTEXT_VERSION"

bash "$SOURCE_DIR/bison.bash" \
  -s "$DIST_DIR/bison-$BISON_VERSION" \
  -p "/usr" \
  -d "/usr/share/doc/bison-$BISON_VERSION"

bash "$SOURCE_DIR/bison.bash" \
  -s "$DIST_DIR/bison-$BISON_VERSION" \
  -p "/usr" \
  -d "/usr/share/doc/bison-$BISON_VERSION"

PERL_MAJOR="$(echo "$PERL_VERSION" | cut -f1 -d.)"
PERL_MINOR="$(echo "$PERL_VERSION" | cut -f2 -d.)"
PERL_LIB="/usr/lib/perl$PERL_MAJOR/$PERL_MAJOR.$PERL_MINOR"
bash "$SOURCE_DIR/perl.bash" \
  -s "$DIST_DIR/perl-$PERL_VERSION" \
  -p "/usr" \
  -v "/usr" \
  -r "$PERL_LIB/core_perl" \
  -a "$PERL_LIB/core_perl" \
  -t "$PERL_LIB/site_perl" \
  -i "$PERL_LIB/site_perl" \
  -e "$PERL_LIB/vendor_perl" \
  -c "$PERL_LIB/vendor_perl"

bash "$SOURCE_DIR/python.bash" \
  -s "$DIST_DIR/python-$PYTHON3_VERSION" \
  -p "/usr"

bash "$SOURCE_DIR/texinfo.bash" \
  -s "$DIST_DIR/texinfo-$TEXINFO_VERSION" \
  -p "/usr"

bash "$SOURCE_DIR/util-linux.bash" \
  -s "$DIST_DIR/util-linux-$UTILLINUX_VERSION" \
  -d "/usr/share/doc/util-linux-$UTILLINUX_VERSION" \
  -l "/usr/lib" \
  -a "/var/lib/hwclock/adjtime" \
  -r "/run"
