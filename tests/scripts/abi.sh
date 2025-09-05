#!/bin/bash

# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

run_procflow $GEOIPS_TESTDATA_DIR/test_data_abi/data/goes17_20210718_0150//* \
          --procflow single_source \
          --reader_name abi_netcdf \
          --resampled_read \
          --product_name GeoColor \
          --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/abi/<product>_image" \
         --output_formatter imagery_clean \
         --filename_formatter tc_clean_fname \
         --trackfile_parser bdeck_parser \
         --trackfiles $GEOIPS_PACKAGES_DIR/geoips/tests/sectors/tc_bdecks/bep062021.dat \
         --feature_annotator tc_visir \
         --gridline_annotator tc_visir
retval=$?

exit $retval
