#!/bin/bash

# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_geocolor/data/mtg/20240924.1500/*.nc \
    --reader_name fci_netcdf \
    --self_register_dataset LOW \
    --self_register_source fci \
    --output_formatter unprojected_image \
    --output_formatter_kwargs '{"x_size": "5568", "y_size": "5568"}' \
    --filename_formatter geoips_fname \
    --product_name GeoColor \
    --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/fci/<product>_image" \
    --minimum_coverage 0
retval=$?
exit $retval
