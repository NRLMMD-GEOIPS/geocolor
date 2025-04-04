#!/bin/bash

# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_geocolor/data/goes18/20240924.1500/* \
    --reader_name abi_netcdf \
    --product_name GeoColor \
    --output_formatter imagery_clean \
    --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/abi_goes_west/<product>_image" \
    --minimum_coverage 0 \
    --sector_list goes_west
retval=$?

exit $retval
