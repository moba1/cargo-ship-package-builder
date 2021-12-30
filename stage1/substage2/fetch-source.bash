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

  mkdir -pv "$dest"
  curl "$1" | tar "${tar_option}xf" - --strip-components 1 -C "$dest"
}

. "$SOURCE_DIR/version.bash"

fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/gcc/gcc-$GCC_VERSION/gcc-$GCC_VERSION.tar.xz" \
  "$DIST_DIR/gcc-$GCC_VERSION-for-libstdc++"
fetch_and_unarchive_source -J \
  "https://ftp.gnu.org/gnu/gettext/gettext-$GETTEXT_VERSION.tar.xz" \
  "$DIST_DIR/gettext-$GETTEXT_VERSION"
