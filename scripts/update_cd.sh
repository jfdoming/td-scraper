#!/bin/bash

filename="/opt/chrome/chrome"
sed -ie 's/cdc_/dog_/g' $filename
sed -ie 's/wdc_/cat_/g' $filename
sed -ie 's/selenium/chocolat/g' $filename
