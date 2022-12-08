#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

dl_url="$(python3 get_latest_cd.py)"
if [ -z "$dl_url" ]; then
    read -n 1 -s -r -p "Failed to download, press any key to exit..."
    exit 1
fi

if ! curl "$dl_url" --output "chromedriver.zip"; then
    read -n 1 -s -r -p "Failed to download, press any key to exit..."
    exit 1
fi

if ! unzip -o "chromedriver.zip"; then
    read -n 1 -s -r -p "Failed to extract, press any key to exit..."
    exit 1
fi
rm "chromedriver.zip"
if [ -f chromedriver.exe ]; then
    filename=chromedriver.exe
else
    filename=chromedriver
fi
perl -pi -e 's/cdc_/dog_/g' $filename

# MacOS M1.
if command -v codesign > /dev/null; then
    codesign --remove-signature $filename
    codesign --force --deep -s - $filename
fi

rm -f "$filename.bak"
read -n 1 -s -r -p "Update complete, press any key to exit..."
echo
