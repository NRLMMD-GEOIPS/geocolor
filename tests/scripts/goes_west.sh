#!/bin/bash

# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_geocolor/data/goes18/20240924.1500/OR_ABI-L1b-RadF-M6C* \
          --procflow single_source \
          --reader_name abi_netcdf \
          --resampled_read \
          --product_name GeoColor \
          --output_formatter imagery_clean \
          --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/abi_goes_west/<product>_image" \
         --sector_list test_goes18_eqc_10km_terminator_20240924T1500Z
retval=$?

exit $retval
