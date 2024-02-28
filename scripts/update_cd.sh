#!/bin/bash

filename="${1:-/opt/chrome/chrome}"
export LC_ALL=C
sed -i '' -e 's/cdc_/dog_/g' "$filename"
sed -i '' -e 's/wdc_/cat_/g' "$filename"
sed -i '' -e 's/selenium/chocolat/g' "$filename"
