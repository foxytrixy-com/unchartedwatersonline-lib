#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
GITHUB_DIR=$FILE_DIR
SCRIPTS_DIR=$(dirname $GITHUB_DIR)
ROOT_DIR=$(dirname $SCRIPTS_DIR)

version=$(PYTHONPATH=$ROOT_DIR python -c "import version; print(version.__version__)")

json_data=$(jinja2 -D version="$version" $FILE_DIR/release.part.json)
curl --data "$json_data" \
     https://api.github.com/repos/:owner/:repository/releases?access_token=:access_token
