set -e pipefail

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

function fetch_and_unarchive_source() {
  local OPTIND OPT tar_option
  while getopts "Jjz" OPT
  do
    case "$OPT" in
      J|j|z) tar_option="$OPT" ;;
      *) exit 1 ;;
    esac
  done
  shift $((OPTIND-1))

  local -r url="$1" dest="$2"
  echo "$url"

  mkdir -pv "$dest"
  curl -sSL "$1" | tar "${tar_option}xf" - --strip-components 1 -C "$dest"
}

. "$SOURCE_DIR/version.bash"

fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/gcc/gcc-$GCC_VERSION/gcc-$GCC_VERSION.tar.xz" \
  "$DIST_DIR/gcc-$GCC_VERSION-for-libstdc++"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/gettext/gettext-$GETTEXT_VERSION.tar.xz" \
  "$DIST_DIR/gettext-$GETTEXT_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/bison/bison-$BISON_VERSION.tar.xz" \
  "$DIST_DIR/bison-$BISON_VERSION"
fetch_and_unarchive_source -J \
  "https://www.cpan.org/src/$(echo "$PERL_VERSION" | cut -f1 -d.).0/perl-$PERL_VERSION.tar.xz" \
  "$DIST_DIR/perl-$PERL_VERSION"
fetch_and_unarchive_source -J \
  "https://www.python.org/ftp/python/$PYTHON3_VERSION/Python-$PYTHON3_VERSION.tar.xz" \
  "$DIST_DIR/python-$PYTHON3_VERSION"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/texinfo/texinfo-$TEXINFO_VERSION.tar.xz" \
  "$DIST_DIR/texinfo-$TEXINFO_VERSION"
fetch_and_unarchive_source -J \
  "https://www.kernel.org/pub/linux/utils/util-linux/v$(echo "$UTILLINUX_VERSION" | cut -f1 -d.).$(echo "$UTILLINUX_VERSION" | cut -f2 -d.)/util-linux-$UTILLINUX_VERSION.tar.xz" \
  "$DIST_DIR/util-linux-$UTILLINUX_VERSION"
