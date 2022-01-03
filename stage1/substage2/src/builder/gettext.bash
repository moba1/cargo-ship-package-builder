set -ex

function main() {
  local source_dir OPTIND OPT
  while getopts s: OPT
  do
    case "$OPT" in
      s) source_dir="$OPTARG" ;;
      *) exit 1 ;;
    esac
  done
  shift $((OPTIND-1))

  [ -n "$source_dir" ] || exit 2

  cd "$source_dir"
  ./configure \
    --disable-shared
  make -j"${PROCESS_NUMBER}"
  cp -v gettext-tools/src/{msgfmt,msgmerge,xgettext} /usr/bin
}

main "$@"
