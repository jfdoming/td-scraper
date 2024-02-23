#!/bin/bash

filename="${1:-/opt/chrome/chrome}"
export LC_ALL=C
sed -ie 's/cdc_/dog_/g' $filename
sed -ie 's/wdc_/cat_/g' $filename
sed -ie 's/selenium/chocolat/g' $filename
