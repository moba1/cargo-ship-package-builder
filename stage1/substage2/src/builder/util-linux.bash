set -e

function main() {
  local source_dir lib_dir doc_dir adjtime_path run_state_dir OPTIND OPT
  while getopts s:p:d:l:a:r: OPT
  do
    case "$OPT" in
      s) source_dir="$OPTARG" ;;
      d) doc_dir="$OPTARG" ;;
      l) lib_dir="$OPTARG" ;;
      a) adjtime_path="$OPTARG" ;;
      r) run_state_dir="$OPTARG" ;;
      *) exit 1 ;;
    esac
  done
  shift $((OPTIND-1))

  [ -n "$source_dir" ] || exit 2
  [ -n "$doc_dir" ] || exit 4
  [ -n "$lib_dir" ] || exit 5
  [ -n "$adjtime_path" ] || exit 6

  mkdir -pv /var/lib/hwclock

  cd "$source_dir"
  ./configure \
    ADJTIME_PATH="$adjtime_path" \
    --libdir="$lib_dir" \
    --docdir="$doc_dir" \
    --disable-chfn-chsh \
    --disable-login \
    --disable-nologin \
    --disable-su \
    --disable-setpriv \
    --disable-runuser \
    --disable-pylibmount \
    --disable-static \
    --disable-static \
    --without-python \
    runstatedir="$run_state_dir"
  make -j"${PROCESS_NUMBER}"
  make install
}

main "$@"
