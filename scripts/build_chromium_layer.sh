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

# Executable files.
mkdir -p "$tempdir"/bin
tar -xvf "$tempdir"/chrome_pack.tar -C "$tempdir"
brotli -d "$tempdir"/chromium.br -o "$tempdir"/bin/chromium
scripts/update_cd.sh "$tempdir"/bin/chromium
chmod +x "$tempdir"/bin/chromium
unzip -q "$tempdir"/chromedriver.zip -d "$tempdir"/bin
mv "$tempdir"/bin/chromedriver-linux64/chromedriver "$tempdir"/bin/
chmod +x "$tempdir"/bin/chromedriver

# These are shared libraries that need to be co-located with the executable.
brotli -d "$tempdir"/swiftshader.tar.br -o "$tempdir"/swiftshader.tar
tar -xf "$tempdir"/swiftshader.tar -C "$tempdir"/bin/

# These are shared libraries that can be placed anywhere.
mkdir -p "$tempdir"/lib
brotli -d "$tempdir"/al2023.tar.br -o "$tempdir"/aws.tar
tar -xf "$tempdir"/aws.tar -C "$tempdir"/  # aws.tar contains a lib/ directory

# These are fonts that need to live in .fonts.
mkdir -p "$tempdir/.fonts"
brotli -d "$tempdir"/fonts.tar.br -o "$tempdir"/fonts.tar
tar -xf "$tempdir"/fonts.tar --strip-components 1 -C "$tempdir"/.fonts
cp fonts.conf "$tempdir/.fonts"

pushd "$tempdir" > /dev/null
zip -r chrome_layer.zip bin/ lib/ .fonts/
popd > /dev/null

mkdir -p layers/
cp "$tempdir"/chrome_layer.zip layers/
