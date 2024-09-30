#!/bin/bash

# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

run_procflow $GEOIPS_TESTDATA_DIR/test_data_abi_day/data/goes16_20200918_1950/* \
          --procflow single_source \
          --reader_name abi_netcdf \
          --resampled_read \
          --product_name GeoColor \
          --output_formatter imagery_clean \
          --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/abi_goes_east//<product>_image" \
         --sector_list goes_east
retval=$?

exit $retval
