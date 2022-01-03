set -e

function main() {
  local prefix vendor_prefix source_dir OPTIND OPT \
    priv_lib arch_lib site_lib site_arch vendor_lib vendor_arch
  while getopts s:p:v:r:a:t:i:e:l:c: OPT
  do
    case "$OPT" in
      s) source_dir="$OPTARG" ;;
      p) prefix="$OPTARG" ;;
      v) vendor_prefix="$OPTARG" ;;
      r) priv_lib="$OPTARG" ;;
      a) arch_lib="$OPTARG" ;;
      t) site_lib="$OPTARG" ;;
      i) site_arch="$OPTARG" ;;
      e) vendor_lib="$OPTARG" ;;
      c) vendor_arch="$OPTARG" ;;
      *) exit 1 ;;
    esac
  done
  shift $((OPTIND-1))

  [ -n "$source_dir" ] || exit 2
  [ -n "$prefix" ] || exit 3
  [ -n "$vendor_prefix" ] || exit 4
  [ -n "$priv_lib" ] || exit 5
  [ -n "$arch_lib" ] || exit 6
  [ -n "$site_lib" ] || exit 7
  [ -n "$site_arch" ] || exit 8
  [ -n "$vendor_lib" ] || exit 9
  [ -n "$vendor_arch" ] || exit 10

  cd "$source_dir"
  sh Configure \
    -des \
    -Dprefix="$prefix" \
    -Dvendorprefix="$vendor_prefix" \
    -Dprivlib="$priv_lib" \
    -Darchlib="$arch_lib" \
    -Dsitelib="$site_lib" \
    -Dsitearch="$site_arch" \
    -Dvendorlib="$vendor_lib" \
    -Dvendorarch="$vendor_arch"
  make -j"${PROCESS_NUMBER}"
  make install
}

main "$@"
