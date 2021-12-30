set -e

SOURCE_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"
. "$SOURCE_DIR/init.bash"
. "$SOURCE_DIR/version.bash"

bash "$SOURCE_DIR/src/main.bash"
