#!/bin/bash

# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_geocolor/data/geokompsat/20240924.1500/*.nc \
    --reader_name ami_netcdf \
    --product_name GeoColor \
    --resampled_read \
    --output_formatter imagery_clean \
    --minimum_coverage 0 \
    --sector_list geokompsat \
    --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/ami/<product>_image" \
    --logging_level info
retval=$?
exit $retval

