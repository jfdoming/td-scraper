#!/bin/bash
set -euo pipefail

tempdir="$(mktemp -d)"
cleanup() {
    CODE=$?
    rm -rd "$tempdir"
    exit $CODE
}
trap cleanup EXIT

download_url="$(curl -sSL https://api.github.com/repos/Sparticuz/chromium/releases/latest | jq -r '.assets[].browser_download_url' | grep pack)"
curl -SL "$download_url" --output "$tempdir"/chrome_pack.tar

version="$(echo "$download_url" | rev | cut -f 2 -d '/' | rev)"
chromedriver_json="$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json)"
chromedriver_url="$(echo "$chromedriver_json" | jq -r 'last(.versions | sort_by(.version)[] | select(.version | startswith("'"${version:1:3}"'"))).downloads.chromedriver[] | select(.platform == "linux64").url')"
curl -SL "$chromedriver_url" --output "$tempdir"/chromedriver.zip

mkdir -p "$tempdir"/bin
tar -xf "$tempdir"/chrome_pack.tar -C "$tempdir"
brotli -d "$tempdir"/chromium.br -o "$tempdir"/bin/chromium
scripts/update_cd.sh "$tempdir"/bin/chromium
unzip -q "$tempdir"/chromedriver.zip -d "$tempdir"/bin
mv "$tempdir"/bin/chromedriver-linux64/chromedriver "$tempdir"/bin/

mkdir -p "$tempdir"/lib
brotli -d "$tempdir"/al2023.tar.br -o "$tempdir"/aws.tar
tar -xf "$tempdir"/aws.tar -C "$tempdir"/  # aws.tar contains a lib/ directory

pushd "$tempdir" > /dev/null
zip -r chrome_layer.zip bin/{chromium,chromedriver} lib/
popd > /dev/null

mkdir -p layers/
cp "$tempdir"/chrome_layer.zip layers/
