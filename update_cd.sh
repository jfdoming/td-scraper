#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

dl_url="$(python get_latest_cd.py)"
if [ -z "$dl_url" ]; then
    read -n 1 -s -r -p "Failed to download, press any key to exit..."
    exit 1
fi

cd "../../Programs/chromedriver/"
if ! curl "$dl_url" --output "chromedriver.zip"; then
    read -n 1 -s -r -p "Failed to download, press any key to exit..."
    exit 1
fi

if ! unzip -o "chromedriver.zip"; then
    read -n 1 -s -r -p "Failed to extract, press any key to exit..."
    exit 1
fi
rm "chromedriver.zip"
perl -pi -e 's/cdc_/dog_/g' chromedriver.exe
rm "chromedriver.exe.bak"
read -n 1 -s -r -p "Update complete, press any key to exit..."
