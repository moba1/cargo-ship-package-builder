#!/usr/bin/env bash

set -e

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

# SSL_DIR=/etc/ssl

python3 \
  "$SOURCE_DIR/man-pages.py" \
  --source-dir "$DIST_DIR/man-pages-$MANPAGES_VERSION" \
  --dist-dir "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/iana-etc.py" \
  --source-dir "$DIST_DIR/iana-etc-$IANAETC_VERSION" \
  --dist-dir "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/glibc.py" \
  --source-dir "$DIST_DIR/glibc-$GLIBC_VERSION" \
  --patch-file "$DIST_DIR/glibc-$GLIBC_VERSION-fhs-1.patch" \
  --dist-dir "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/tzdata.py" \
  --source-dir "$DIST_DIR/tzdata-$TZDATA_VERSION" \
  --dist-dir "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/dynamic-loader.py" \
  --dist-dir "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/zlib.py" \
  --source-dir "$DIST_DIR/zlib-$ZLIB_VERSION" \
  --dist-dir "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/bzip2.py" \
  --source-dir "$DIST_DIR/bzip2-$BZIP2_VERSION" \
  --patch-file "$DIST_DIR/bzip2-$BZIP2_VERSION-install_docs-1.patch" \
  --version "$BZIP2_VERSION" \
  --dist-dir "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/xz.py" \
  --source-dir "$DIST_DIR/xz-$XZ_VERSION" \
  --version "$XZ_VERSION" \
  --dist-dir "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/zstd.py" \
  --source-dir "$DIST_DIR/zstd-$ZSTD_VERSION" \
  --dist-dir "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/file.py" \
  --source-dir "$DIST_DIR/file-$FILE_VERSION" \
  --dist-dir "$WORK_ROOT"

python3 \
  "$SOURCE_DIR/readline.py" \
  --source-dir "$DIST_DIR/readline-$READLINE_VERSION" \
  --version "$READLINE_VERSION" \
  --dist-dir "$WORK_ROOT"

# python3 \
#   "$SOURCE_DIR/m4.py" \
#   --source-dir "$DIST_DIR/m4-$M4_VERSION"

# python3 \
#   "$SOURCE_DIR/bc.py" \
#   --source-dir "$DIST_DIR/bc-$BC_VERSION"

# python3 \
#   "$SOURCE_DIR/flex.py" \
#   --source-dir "$DIST_DIR/flex-$FLEX_VERSION" \
#   --version "$FLEX_VERSION"

# python3 \
#   "$SOURCE_DIR/tcl.py" \
#   --source-dir "$DIST_DIR/tcl-$TCL_VERSION" \
#   --version "$TCL_VERSION" \
#   --arch "$ARCH"

# python3 \
#   "$SOURCE_DIR/expect.py" \
#   --source-dir "$DIST_DIR/expect-$EXPECT_VERSION" \
#   --version "$EXPECT_VERSION"

# python3 \
#   "$SOURCE_DIR/dejagnu.py" \
#   --source-dir "$DIST_DIR/dejagnu-$DEJAGNU_VERSION" \
#   --version "$DEJAGNU_VERSION"

# python3 \
#   "$SOURCE_DIR/binutils.py" \
#   --source-dir "$DIST_DIR/binutils-$BINUTILS_VERSION" \
#   --patch-file "$DIST_DIR/binutils-$BINUTILS_VERSION-upstream_fix-1.patch"

# python3 \
#   "$SOURCE_DIR/gmp.py" \
#   --source-dir "$DIST_DIR/gmp-$GMP_VERSION" \
#   --version "$GMP_VERSION" \
#   --arch "$ARCH"

# python3 \
#   "$SOURCE_DIR/mpfr.py" \
#   --source-dir "$DIST_DIR/mpfr-$MPFR_VERSION" \
#   --version "$MPFR_VERSION"

# python3 \
#   "$SOURCE_DIR/mpc.py" \
#   --source-dir "$DIST_DIR/mpc-$MPC_VERSION" \
#   --version "$MPC_VERSION"

# python3 \
#   "$SOURCE_DIR/attr.py" \
#   --source-dir "$DIST_DIR/attr-$ATTR_VERSION" \
#   --version "$ATTR_VERSION"

# python3 \
#   "$SOURCE_DIR/acl.py" \
#   --source-dir "$DIST_DIR/acl-$ACL_VERSION" \
#   --version "$ACL_VERSION"

# python3 \
#   "$SOURCE_DIR/libcap.py" \
#   --source-dir "$DIST_DIR/libcap-$LIBCAP_VERSION" \
#   --version "$LIBCAP_VERSION"

# python3 \
#   "$SOURCE_DIR/shadow.py" \
#   --source-dir "$DIST_DIR/shadow-$SHADOW_VERSION"

# python3 \
#   "$SOURCE_DIR/gcc.py" \
#   --source-dir "$DIST_DIR/gcc-$GCC_VERSION" \
#   --arch "$ARCH" \
#   --version "$GCC_VERSION"

# python3 \
#   "$SOURCE_DIR/pkg-config.py" \
#   --source-dir "$DIST_DIR/pkg-config-$PKGCONFIG_VERSION" \
#   --version "$PKGCONFIG_VERSION"

# python3 \
#   "$SOURCE_DIR/ncurses.py" \
#   --source-dir "$DIST_DIR/ncurses-$NCURSES_VERSION" \
#   --version "$NCURSES_VERSION"

# python3 \
#   "$SOURCE_DIR/sed.py" \
#   --source-dir "$DIST_DIR/sed-$SED_VERSION" \
#   --version "$SED_VERSION"

# python3 \
#   "$SOURCE_DIR/psmisc.py" \
#   --source-dir "$DIST_DIR/psmisc-$PSMISC_VERSION"

# python3 \
#   "$SOURCE_DIR/gettext_.py" \
#   --source-dir "$DIST_DIR/gettext-$GETTEXT_VERSION" \
#   --version "$GETTEXT_VERSION"

# python3 \
#   "$SOURCE_DIR/bison.py" \
#   --source-dir "$DIST_DIR/bison-$BISON_VERSION" \
#   --version "$BISON_VERSION"

# python3 \
#   "$SOURCE_DIR/grep.py" \
#   --source-dir "$DIST_DIR/grep-$GREP_VERSION"

# python3 \
#   "$SOURCE_DIR/bash.py" \
#   --source-dir "$DIST_DIR/bash-$BASH_VERSION_" \
#   --version "$BASH_VERSION_"

# python3 \
#   "$SOURCE_DIR/libtool.py" \
#   --source-dir "$DIST_DIR/libtool-$LIBTOOL_VERSION"

# python3 \
#   "$SOURCE_DIR/gdbm.py" \
#   --source-dir "$DIST_DIR/gdbm-$GDBM_VERSION"

# python3 \
#   "$SOURCE_DIR/gperf.py" \
#   --source-dir "$DIST_DIR/gperf-$GPERF_VERSION" \
#   --version "$GPERF_VERSION"

# python3 \
#   "$SOURCE_DIR/expat.py" \
#   --source-dir "$DIST_DIR/expat-$EXPAT_VERSION" \
#   --version "$EXPAT_VERSION"

# python3 \
#   "$SOURCE_DIR/inetutils.py" \
#   --source-dir "$DIST_DIR/inetutils-$INETUTILS_VERSION"

# python3 \
#   "$SOURCE_DIR/less.py" \
#   --source-dir "$DIST_DIR/less-$LESS_VERSION"

# python3 \
#   "$SOURCE_DIR/perl.py" \
#   --source-dir "$DIST_DIR/perl-$PERL_VERSION" \
#   --version "$PERL_VERSION" \
#   --patch-file "$DIST_DIR/perl-$PERL_VERSION-upstream-fixes-1.patch"

# python3 \
#   "$SOURCE_DIR/xml-parser.py" \
#   --source-dir "$DIST_DIR/xml-parser-$XMLPARSER_VERSION"

# python3 \
#   "$SOURCE_DIR/intltool.py" \
#   --source-dir "$DIST_DIR/intltool-$INTLTOOL_VERSION" \
#   --version "$INTLTOOL_VERSION"

# python3 \
#   "$SOURCE_DIR/autoconf.py" \
#   --source-dir "$DIST_DIR/autoconf-$AUTOCONF_VERSION"

# python3 \
#   "$SOURCE_DIR/automake.py" \
#   --source-dir "$DIST_DIR/automake-$AUTOMAKE_VERSION" \
#   --version "$AUTOMAKE_VERSION"

# python3 \
#   "$SOURCE_DIR/kmod.py" \
#   --source-dir "$DIST_DIR/kmod-$KMOD_VERSION"

# python3 \
#   "$SOURCE_DIR/libelf.py" \
#   --source-dir "$DIST_DIR/elfutils-$ELFUTILS_VERSION-for-libelf"

# python3 \
#   "$SOURCE_DIR/libffi.py" \
#   --source-dir "$DIST_DIR/libffi-$LIBFFI_VERSION"

# python3 \
#   "$SOURCE_DIR/openssl.py" \
#   --source-dir "$DIST_DIR/openssl-$OPENSSL_VERSION" \
#   --version "$OPENSSL_VERSION" \
#   --ssl-dir "$SSL_DIR"

# python3 \
#   "$SOURCE_DIR/python3.py" \
#   --source-dir "$DIST_DIR/python3-$PYTHON3_VERSION" \
#   --doc "$DIST_DIR/python3-docs-$PYTHON3_VERSION" \
#   --version "$PYTHON3_VERSION"

# python3 \
#   "$SOURCE_DIR/ninja.py" \
#   --source-dir "$DIST_DIR/ninja-$NINJA_VERSION"

# python3 \
#   "$SOURCE_DIR/meson.py" \
#   --source-dir "$DIST_DIR/meson-$MESON_VERSION"

# python3 \
#   "$SOURCE_DIR/coreutils.py" \
#   --source-dir "$DIST_DIR/coreutils-$COREUTILS_VERSION" \
#   --patch-file "$DIST_DIR/coreutils-$COREUTILS_VERSION-i18n-1.patch"
