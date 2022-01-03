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

  sed -e 's/__attribute_nonnull__/__nonnull/' \
    -i gnulib/lib/malloc/dynarray-skeleton.c

  ./configure \
    --prefix="$prefix"
  make -j"${PROCESS_NUMBER}"
  make install
}

main "$@"
