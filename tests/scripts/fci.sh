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

# geoips run single_source $GEOIPS_TESTDATA_DIR/fci_test/20250211.0010/*.nc \
geoips run single_source $GEOIPS_TESTDATA_DIR/test_data_geocolor/data/mtg/20240924.1500/*.nc \
    --reader_name fci_netcdf \
    --reader_kwargs '{"self_register": "LOW"}' \
    --self_register_dataset 'FULL_DISK' \
    --self_register_source fci \
    --output_formatter unprojected_image \
    --output_formatter_kwargs '{"x_size": "11136", "y_size": "11136"}' \
    --filename_formatter geoips_fname \
    --product_name GeoColor \
    --minimum_coverage 0 \
    --logging_level info
    # --sector_list mtg_i1
retval=$?
exit $retval


# geoips run single_source /mnt/sat/meteosat/meteosat-12/20250108/MTG-FCI-L1C/*FCI-1C-RRAD-FDHSI-FD--CHK-BODY*OPE_20250108220[0-9]*.nc \
#     /mnt/sat/meteosat/meteosat-12/20250108/MTG-FCI-L1C/*FCI-1C-RRAD-FDHSI-FD--CHK-TRAIL*OPE_20250108220[0-9]*.nc \
