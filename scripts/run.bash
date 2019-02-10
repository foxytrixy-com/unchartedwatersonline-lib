#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_DIR=$(dirname `readlink -f ${BASH_SOURCE[0]}`)
# FILE_DIR=$(dirname `pwd`)/scripts
SCRIPTS_DIR=$FILE_DIR
BASE_DIR=$(dirname $SCRIPTS_DIR)

PROJECTS_DIR=$(dirname $BASE_DIR)
# UTILS_DIR=$PROJECTS_DIR/uwo_ps_utils

PYTHONPATH=$PROJECTS_DIR/foxylib

PYTHONPATH=$PYTHONPATH python3 $BASE_DIR/main.py
# python3 $BASE_DIR/main.py

