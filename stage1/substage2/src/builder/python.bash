set -e

function main() {
  local prefix source_dir OPTIND OPT
  while getopts s:p: OPT
  do
    case "$OPT" in
      s) source_dir="$OPTARG" ;;
      p) prefix="$OPTARG" ;;
      *) exit 1 ;;
    esac
  done
  shift $((OPTIND-1))

  [ -n "$source_dir" ] || exit 2
  [ -n "$prefix" ] || exit 3

  cd "$source_dir"
  ./configure \
    --prefix="$prefix" \
    --enable-shared \
    --without-ensurepip
  make -j"${PROCESS_NUMBER}"
  make install
}

main "$@"
