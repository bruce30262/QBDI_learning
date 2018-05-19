#!/usr/bin/env sh
script=$1
binary=$2
LD_PRELOAD=/home/docker/qbdi/build/tools/pyqbdi/libpyqbdi.so PYQBDI_TOOL=$script $binary
