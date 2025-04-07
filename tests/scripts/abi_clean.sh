#!/bin/bash

# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_geocolor/data/goes16/20240924.1500/* \
    --reader_name abi_netcdf \
    --product_name GeoColor \
    --compare_path "$GEOIPS_PACKAGES_DIR/geocolor/tests/outputs/abi/<product>_image" \
    --reader_kwargs '{"self_register": "LOW"}' \
    --self_register_dataset 'Full-Disk' \
    --self_register_source abi \
    --output_formatter unprojected_image \
    --output_formatter_kwargs '{"x_size": "10848", "y_size": "10848"}' \
    --minimum_coverage 0
retval=$?

exit $retval
