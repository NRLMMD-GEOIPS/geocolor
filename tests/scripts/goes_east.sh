#!/bin/bash

# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_geocolor/data/goes16/20240920.1500/OR_ABI-L1b-RadF-M6C*.nc \
          --procflow single_source \
          --reader_name abi_netcdf \
          --resampled_read \
          --product_name GeoColor \
          --output_formatter imagery_clean \
          --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/abi_goes_east//<product>_image" \
         --sector_list test_goes16_eqc_10km_terminator_20240920T1500Z
retval=$?

exit $retval
