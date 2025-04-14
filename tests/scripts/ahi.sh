#!/bin/bash

# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

run_procflow $GEOIPS_TESTDATA_DIR/test_data_ahi_day/data/20200405_0000/* \
          --procflow single_source \
          --reader_name ahi_hsd \
          --resampled_read \
          --product_name GeoColor \
          --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/ahi/<product>_image" \
         --output_formatter imagery_clean \
         --filename_formatter tc_clean_fname \
         --trackfile_parser gdeck_parser \
         --trackfiles $GEOIPS_TESTDATA_DIR/test_data_ahi_day/sectors/Gsh252020.dat \
         --feature_annotator tc_visir \
         --gridline_annotator tc_visir

retval=$?
exit $retval
