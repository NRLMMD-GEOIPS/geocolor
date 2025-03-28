#!/bin/bash

# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

run_procflow $GEOIPS_TESTDATA_DIR/test_data_ahi_day/data/20200405_0000/* \
          --procflow single_source \
          --reader_name ahi_hsd \
          --resampled_read \
          --product_name GeoColor \
          --output_formatter imagery_clean \
          --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/ahi_himawari/<product>_image" \
         --sector_list himawari
retval=$?

exit $retval
