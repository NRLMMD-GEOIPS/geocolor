#!/bin/bash

geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_geocolor/data/mtg/20240924.1500/* \
    --reader_name fci_netcdf \
    --reader_kwargs '{"self_register": "LOW"}' \
    --self_register_dataset 'FULL_DISK' \
    --self_register_source fci \
    --output_formatter unprojected_image \
    --output_formatter_kwargs '{"x_size": "11136", "y_size": "11136"}' \
    --filename_formatter geoips_fname \
    --product_name GeoColor \
    --minimum_coverage 0
retval=$?
exit $retval

