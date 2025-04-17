#!/bin/bash

# # # This source code is protected under the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

geoips run single_source /home/evan/geoips/geoips_packages/test_data/temp_g18_data/* \
    --reader_name abi_netcdf \
    --product_name GeoColor \
    --resampled_read \
    --minimum_coverage 0 \
    --output_formatter imagery_clean \
    --sector_list goes_west
retval=$?

exit $retval
