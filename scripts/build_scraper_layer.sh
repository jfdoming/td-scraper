#!/bin/bash
set -euo pipefail

tempdir="$(mktemp -d)"
cleanup () {
    CODE=$?
    rm -rd "$tempdir"
    exit $CODE
}
trap cleanup EXIT

cp -r scrape "$tempdir"/scrape
cp lambda_function.py main.py "$tempdir"/
find "$tempdir" -name '*__pycache__*' | xargs rm -rd || true

pushd "$tempdir" > /dev/null
zip -r scraper_layer.zip .
popd > /dev/null

mkdir -p layers/
cp "$tempdir"/scraper_layer.zip layers/
