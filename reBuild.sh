SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
docker build -t kv-store:2.0 $SCRIPTPATH
