set -e

function main() {
  local host source_dir prefix OPTIND OPT
  while getopts h:s:p: OPT
  do
    case "$OPT" in
      h) host="$OPTARG" ;;
      s) source_dir="$OPTARG" ;;
      p) prefix="$OPTARG" ;;
      *) exit 1 ;;
    esac
  done
  shift $((OPTIND-1))

  [ -n "$host" ] || exit 2
  [ -n "$prefix" ] || exit 3

  cd "$source_dir"

  ln -snfv gthr-posix.h libgcc/gthr-default.h

  mkdir -pv build
  cd build
  ../libstdc++-v3/configure \
    CXXFLAGS="-g -O2 -DGNU_SOURCE" \
    --prefix="$prefix" \
    --disable-multilib \
    --disable-nls \
    --host="$host" \
    --disable-libstdcxx-pch
  make -j"${PROCESS_NUMBER}"
  make install
}

main "$@"
