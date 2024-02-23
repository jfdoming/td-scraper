#!/bin/bash
set -euo pipefail

tempdir="$(mktemp -d)"
cleanup() {
    CODE=$?
    rm -rd "$tempdir"
    exit $CODE
}
trap cleanup EXIT

download_url="$(curl -SL https://api.github.com/repos/Sparticuz/chromium/releases/latest | jq -r '.assets[].browser_download_url' | grep pack)"
curl -SL "$download_url" --output "$tempdir"/chrome_pack.tar

tar -xf "$tempdir"/chrome_pack.tar -C "$tempdir"
mkdir -p "$tempdir"/bin
brotli -d "$tempdir"/chromium.br -o "$tempdir"/bin/chromium
scripts/update_cd.sh "$tempdir"/bin/chromium

pushd "$tempdir" > /dev/null
zip chrome_layer.zip bin/chromium
popd > /dev/null

mkdir -p layers/
cp "$tempdir"/chrome_layer.zip layers/
