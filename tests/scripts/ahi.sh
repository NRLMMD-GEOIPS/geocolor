#!/bin/bash

# # # Distribution Statement A. Approved for public release. Distribution unlimited.
# # #
# # # Author:
# # # Naval Research Laboratory, Marine Meteorology Division
# # #
# # # This program is free software: you can redistribute it and/or modify it under
# # # the terms of the NRLMMD License included with this program. This program is
# # # distributed WITHOUT ANY WARRANTY; without even the implied warranty of
# # # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the included license
# # # for more details. If you did not receive the license, for more information see:
# # # https://github.com/U-S-NRL-Marine-Meteorology-Division/

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
