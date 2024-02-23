#!/bin/bash
set -euo pipefail

tempdir="$(mktemp -d)"
cleanup () {
    CODE=$?
    rm -rd "$tempdir"
    exit $CODE
}
trap cleanup EXIT

python3 -m venv "$tempdir"/env
. "$tempdir"/env/bin/activate

pip install \
--platform manylinux2014_x86_64 \
--target="$tempdir"/python \
--implementation cp \
--python-version 3.12 \
--only-binary=:all: --upgrade \
-r requirements-scraper.txt

pushd "$tempdir" > /dev/null
zip -r py_deps_layer.zip python/
popd > /dev/null

mkdir -p layers/
cp "$tempdir"/py_deps_layer.zip layers/
