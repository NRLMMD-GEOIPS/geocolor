#!/bin/bash

# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_geocolor/data/geokompsat/20240920.1500/*.nc \
    --reader_name ami_netcdf \
    --product_name GeoColor \
    --output_formatter imagery_annotated \
    --minimum_coverage 0 \
    --sector_list geokompsat \
    --logging_level info
retval=$?
exit $retval


# geoips run single_source /mnt/GK2A/AMI/L1B/FD/202501/08/22/*2200* \
