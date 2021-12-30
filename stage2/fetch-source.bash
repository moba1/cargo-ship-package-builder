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
  "https://www.kernel.org/pub/linux/docs/man-pages/man-pages-$MANPAGES_VERSION.tar.xz" \
  "$DIST_DIR/man-pages-$MANPAGES_VERSION"
fetch_and_unarchive_source -z \
  "https://github.com/Mic92/iana-etc/releases/download/$IANAETC_VERSION/iana-etc-$IANAETC_VERSION.tar.gz" \
  "$DIST_DIR/iana-etc-$IANAETC_VERSION"
