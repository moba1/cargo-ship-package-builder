set -e pipefail

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

function fetch_and_unarchive_source() {
  local OPTIND OPT tar_option strip_components=1
  while getopts "Jjzs:" OPT
  do
    case "$OPT" in
      J|j|z) tar_option="$OPT" ;;
      s) strip_components="$OPTARG" ;;
      *) exit 1 ;;
    esac
  done
  shift $((OPTIND-1))

  local -r url="$1" dest="$2"
  echo "$url"

  mkdir -pv "$dest"
  curl -sSL "$1" | tar "${tar_option}xf" - --strip-components "$strip_components" -C "$dest"
}

. "$SOURCE_DIR/version.bash"

fetch_and_unarchive_source -J \
  "https://www.kernel.org/pub/linux/docs/man-pages/man-pages-$MANPAGES_VERSION.tar.xz" \
  "$DIST_DIR/man-pages-$MANPAGES_VERSION"
fetch_and_unarchive_source -z \
  "https://github.com/Mic92/iana-etc/releases/download/$IANAETC_VERSION/iana-etc-$IANAETC_VERSION.tar.gz" \
  "$DIST_DIR/iana-etc-$IANAETC_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/glibc/glibc-$GLIBC_VERSION.tar.xz" \
  "$DIST_DIR/glibc-$GLIBC_VERSION"
curl \
  -sSL \
  -o "$DIST_DIR/glibc-$GLIBC_VERSION-fhs-1.patch" \
  "https://www.linuxfromscratch.org/patches/lfs/11.0/glibc-$GLIBC_VERSION-fhs-1.patch"
fetch_and_unarchive_source -z -s 0 \
  "https://www.iana.org/time-zones/repository/releases/tzdata$TZDATA_VERSION.tar.gz" \
  "$DIST_DIR/tzdata-$TZDATA_VERSION"
fetch_and_unarchive_source -J \
  "https://zlib.net/zlib-$ZLIB_VERSION.tar.xz" \
  "$DIST_DIR/zlib-$ZLIB_VERSION"
fetch_and_unarchive_source -z \
  "https://www.sourceware.org/pub/bzip2/bzip2-$BZIP2_VERSION.tar.gz" \
  "$DIST_DIR/bzip2-$BZIP2_VERSION"
curl \
  -sSL \
  -o "$DIST_DIR/bzip2-$BZIP2_VERSION-install_docs-1.patch" \
  "https://www.linuxfromscratch.org/patches/lfs/11.0/bzip2-$BZIP2_VERSION-install_docs-1.patch"
fetch_and_unarchive_source -J \
  "https://tukaani.org/xz/xz-$XZ_VERSION.tar.xz" \
  "$DIST_DIR/xz-$XZ_VERSION"
fetch_and_unarchive_source -z \
  "https://github.com/facebook/zstd/releases/download/v$ZSTD_VERSION/zstd-$ZSTD_VERSION.tar.gz" \
  "$DIST_DIR/zstd-$ZSTD_VERSION"
fetch_and_unarchive_source -z \
  "https://astron.com/pub/file/file-$FILE_VERSION.tar.gz" \
  "$DIST_DIR/file-$FILE_VERSION"
fetch_and_unarchive_source -z \
  "https://ftp.gnu.org/gnu/readline/readline-$READLINE_VERSION.tar.gz" \
  "$DIST_DIR/readline-$READLINE_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/m4/m4-$M4_VERSION.tar.xz" \
  "$DIST_DIR/m4-$M4_VERSION"
fetch_and_unarchive_source -J \
  "https://github.com/gavinhoward/bc/releases/download/$BC_VERSION/bc-$BC_VERSION.tar.xz" \
  "$DIST_DIR/bc-$BC_VERSION"
fetch_and_unarchive_source -z \
  "https://github.com/westes/flex/releases/download/v$FLEX_VERSION/flex-$FLEX_VERSION.tar.gz" \
  "$DIST_DIR/flex-$FLEX_VERSION"
fetch_and_unarchive_source -z \
  "https://downloads.sourceforge.net/tcl/tcl$TCL_VERSION-src.tar.gz" \
  "$DIST_DIR/tcl-$TCL_VERSION"
fetch_and_unarchive_source -z \
  "https://downloads.sourceforge.net/tcl/tcl$TCL_VERSION-html.tar.gz" \
  "$DIST_DIR/tcl-$TCL_VERSION"
fetch_and_unarchive_source -z \
  "https://prdownloads.sourceforge.net/expect/expect$EXPECT_VERSION.tar.gz" \
  "$DIST_DIR/expect-$EXPECT_VERSION"
fetch_and_unarchive_source -z \
  "https://ftp.gnu.org/gnu/dejagnu/dejagnu-$DEJAGNU_VERSION.tar.gz" \
  "$DIST_DIR/dejagnu-$DEJAGNU_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/binutils/binutils-$BINUTILS_VERSION.tar.xz" \
  "$DIST_DIR/binutils-$BINUTILS_VERSION"
curl -sSL \
  -o "$DIST_DIR/binutils-$BINUTILS_VERSION-upstream_fix-1.patch" \
  "https://www.linuxfromscratch.org/patches/lfs/11.0/binutils-$BINUTILS_VERSION-upstream_fix-1.patch"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/gmp/gmp-$GMP_VERSION.tar.xz" \
  "$DIST_DIR/gmp-$GMP_VERSION"
fetch_and_unarchive_source -J \
  "https://www.mpfr.org/mpfr-$MPFR_VERSION/mpfr-$MPFR_VERSION.tar.xz" \
  "$DIST_DIR/mpfr-$MPFR_VERSION"
fetch_and_unarchive_source -z \
  "https://ftp.gnu.org/gnu/mpc/mpc-$MPC_VERSION.tar.gz" \
  "$DIST_DIR/mpc-$MPC_VERSION"
fetch_and_unarchive_source -z \
  "https://download.savannah.gnu.org/releases/attr/attr-$ATTR_VERSION.tar.gz" \
  "$DIST_DIR/attr-$ATTR_VERSION"
fetch_and_unarchive_source -J \
  "https://download.savannah.gnu.org/releases/acl/acl-$ACL_VERSION.tar.xz" \
  "$DIST_DIR/acl-$ACL_VERSION"
fetch_and_unarchive_source -J \
  "https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/libcap-$LIBCAP_VERSION.tar.xz" \
  "$DIST_DIR/libcap-$LIBCAP_VERSION"
fetch_and_unarchive_source -J \
  "https://github.com/shadow-maint/shadow/releases/download/v$SHADOW_VERSION/shadow-$SHADOW_VERSION.tar.xz" \
  "$DIST_DIR/shadow-$SHADOW_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/gcc/gcc-$GCC_VERSION/gcc-$GCC_VERSION.tar.xz" \
  "$DIST_DIR/gcc-$GCC_VERSION"
fetch_and_unarchive_source -z \
  "https://pkg-config.freedesktop.org/releases/pkg-config-$PKGCONFIG_VERSION.tar.gz" \
  "$DIST_DIR/pkg-config-$PKGCONFIG_VERSION"
fetch_and_unarchive_source -z \
  "https://ftp.gnu.org/gnu/ncurses/ncurses-$NCURSES_VERSION.tar.gz" \
  "$DIST_DIR/ncurses-$NCURSES_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/sed/sed-$SED_VERSION.tar.xz" \
  "$DIST_DIR/sed-$SED_VERSION"
fetch_and_unarchive_source -J \
  "https://sourceforge.net/projects/psmisc/files/psmisc/psmisc-$PSMISC_VERSION.tar.xz" \
  "$DIST_DIR/psmisc-$PSMISC_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/gettext/gettext-$GETTEXT_VERSION.tar.xz" \
  "$DIST_DIR/gettext-$GETTEXT_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/bison/bison-$BISON_VERSION.tar.xz" \
  "$DIST_DIR/bison-$BISON_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/grep/grep-$GREP_VERSION.tar.xz" \
  "$DIST_DIR/grep-$GREP_VERSION"
fetch_and_unarchive_source -z \
  "https://ftp.gnu.org/gnu/bash/bash-$BASH_VERSION_.tar.gz" \
  "$DIST_DIR/bash-$BASH_VERSION_"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/libtool/libtool-$LIBTOOL_VERSION.tar.xz" \
  "$DIST_DIR/libtool-$LIBTOOL_VERSION"
fetch_and_unarchive_source -z \
  "https://ftp.gnu.org/gnu/gdbm/gdbm-$GDBM_VERSION.tar.gz" \
  "$DIST_DIR/gdbm-$GDBM_VERSION"
fetch_and_unarchive_source -z \
  "https://ftp.gnu.org/gnu/gperf/gperf-$GPERF_VERSION.tar.gz" \
  "$DIST_DIR/gperf-$GPERF_VERSION"
fetch_and_unarchive_source -J \
  "https://prdownloads.sourceforge.net/expat/expat-$EXPAT_VERSION.tar.xz" \
  "$DIST_DIR/expat-$EXPAT_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/inetutils/inetutils-$INETUTILS_VERSION.tar.xz" \
  "$DIST_DIR/inetutils-$INETUTILS_VERSION"
fetch_and_unarchive_source -z \
  "https://www.greenwoodsoftware.com/less/less-$LESS_VERSION.tar.gz" \
  "$DIST_DIR/less-$LESS_VERSION"
fetch_and_unarchive_source -J \
  "https://www.cpan.org/src/$(echo "$PERL_VERSION" | cut -f1 -d.).0/perl-$PERL_VERSION.tar.xz" \
  "$DIST_DIR/perl-$PERL_VERSION"
curl -sSL \
  -o "$DIST_DIR/perl-$PERL_VERSION-upstream-fixes-1.patch" \
  "https://www.linuxfromscratch.org/patches/lfs/11.0/perl-$PERL_VERSION-upstream_fixes-1.patch"
fetch_and_unarchive_source -z \
  "https://cpan.metacpan.org/authors/id/T/TO/TODDR/XML-Parser-$XMLPARSER_VERSION.tar.gz" \
  "$DIST_DIR/xml-parser-$XMLPARSER_VERSION"
fetch_and_unarchive_source -z \
  "https://launchpad.net/intltool/trunk/$INTLTOOL_VERSION/+download/intltool-$INTLTOOL_VERSION.tar.gz" \
  "$DIST_DIR/intltool-$INTLTOOL_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/autoconf/autoconf-$AUTOCONF_VERSION.tar.xz" \
  "$DIST_DIR/autoconf-$AUTOCONF_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/automake/automake-$AUTOMAKE_VERSION.tar.xz" \
  "$DIST_DIR/automake-$AUTOMAKE_VERSION"
fetch_and_unarchive_source -J \
  "https://www.kernel.org/pub/linux/utils/kernel/kmod/kmod-$KMOD_VERSION.tar.xz" \
  "$DIST_DIR/kmod-$KMOD_VERSION"
fetch_and_unarchive_source -j \
  "https://sourceware.org/ftp/elfutils/$ELFUTILS_VERSION/elfutils-$ELFUTILS_VERSION.tar.bz2" \
  "$DIST_DIR/elfutils-$ELFUTILS_VERSION-for-libelf"
fetch_and_unarchive_source -z \
  "https://github.com/libffi/libffi/releases/download/v$LIBFFI_VERSION/libffi-$LIBFFI_VERSION.tar.gz" \
  "$DIST_DIR/libffi-$LIBFFI_VERSION"
fetch_and_unarchive_source -z \
  "https://www.openssl.org/source/openssl-$OPENSSL_VERSION.tar.gz" \
  "$DIST_DIR/openssl-$OPENSSL_VERSION"
fetch_and_unarchive_source -J \
  "https://www.python.org/ftp/python/$PYTHON3_VERSION/Python-$PYTHON3_VERSION.tar.xz" \
  "$DIST_DIR/python3-$PYTHON3_VERSION"
fetch_and_unarchive_source -j \
  "https://www.python.org/ftp/python/doc/$PYTHON3_VERSION/python-$PYTHON3_VERSION-docs-html.tar.bz2" \
  "$DIST_DIR/python3-docs-$PYTHON3_VERSION"
fetch_and_unarchive_source -z \
  "https://github.com/ninja-build/ninja/archive/v$NINJA_VERSION/ninja-$NINJA_VERSION.tar.gz" \
  "$DIST_DIR/ninja-$NINJA_VERSION"
fetch_and_unarchive_source -z \
  "https://github.com/mesonbuild/meson/releases/download/$MESON_VERSION/meson-$MESON_VERSION.tar.gz" \
  "$DIST_DIR/meson-$MESON_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/coreutils/coreutils-$COREUTILS_VERSION.tar.xz" \
  "$DIST_DIR/coreutils-$COREUTILS_VERSION"
curl -sSL \
  -o "$DIST_DIR/coreutils-$COREUTILS_VERSION-i18n-1.patch" \
  "https://www.linuxfromscratch.org/patches/lfs/11.0/coreutils-$COREUTILS_VERSION-i18n-1.patch"
