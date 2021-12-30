set -e

function main() {
  local prefix doc_dir source_dir OPTIND OPT
  while getopts s:d:p: OPT
  do
    case "$OPT" in
      s) source_dir="$OPTARG" ;;
      d) doc_dir="$OPTARG" ;;
      p) prefix="$OPTARG" ;;
      *) exit 1 ;;
    esac
  done
  shift $((OPTIND-1))

  [ -n "$source_dir" ] || exit 2
  [ -n "$doc_dir" ] || exit 3
  [ -n "$prefix" ] || exit 4

  cd "$source_dir"
  ./configure \
    --prefix="$prefix" \
    --docdir="$doc_dir"
  make -j"${PROCESS_NUMBER}"
  make install
}

main "$@"
