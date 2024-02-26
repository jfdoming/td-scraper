#!/bin/bash
set -euo pipefail

tempdir="$(mktemp -d)"
cleanup() {
    CODE=$?
    rm -rd "$tempdir"
    exit $CODE
}
trap cleanup EXIT

mkdir -p "$tempdir"/lib
cp -r lib/ "$tempdir/lib"

pushd "$tempdir" > /dev/null
zip -r chromedriver_local_libs_layer.zip lib/
popd > /dev/null

mkdir -p layers/
cp "$tempdir"/chromedriver_local_libs_layer.zip layers/
