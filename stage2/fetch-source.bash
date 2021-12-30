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
