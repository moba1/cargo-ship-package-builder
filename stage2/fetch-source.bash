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
