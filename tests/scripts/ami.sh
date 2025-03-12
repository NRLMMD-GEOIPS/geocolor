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
