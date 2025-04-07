#!/bin/bash

# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_geocolor/data/himawari9/20240924.1500/* \
    --reader_name ahi_hsd \
    --product_name GeoColor \
    --resampled_read \
    --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/ahi/<product>_image" \
    --minimum_coverage 0 \
    --output_formatter imagery_clean \
    --sector_list himawari
retval=$?
exit $retval
