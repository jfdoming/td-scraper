#!/bin/bash

filename="/opt/chrome/chrome"
perl -pi -e 's/cdc_/dog_/g' $filename
perl -pi -e 's/wdc_/cat_/g' $filename
perl -pi -e 's/selenium/chocolat/g' $filename
