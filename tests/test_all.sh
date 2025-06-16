#!/bin/bash

# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

# Do not rename this script or test directory - automated integration
# tests look for the tests/test_all.sh script for complete testing.

# This should contain test calls to cover ALL required functionality tests
# for the GeoColor repo.

# The $GEOIPS_PACKAGES_DIR/geoips tests modules sourced within this script handle:
   # setting up the appropriate associative arrays for tracking the overall
   #   return value,
   # calling the test scripts appropriately, and
   # setting the final return value.

if [[ ! -d $GEOIPS_PACKAGES_DIR/geoips ]]; then
    echo "Must CLONE geoips repository into \$GEOIPS_PACKAGES_DIR location"
    echo "to use test_all.sh testing utility."
    echo ""
    echo "export GEOIPS_PACKAGES_DIR=<path_to_geoips_cloned_packages>"
    echo "git clone https://github.com/NRLMMD-GEOIPS/geoips $GEOIPS_PACKAGES_DIR/geoips"
    echo ""
    exit 1
fi

# The following script is used to generate all test geocolor products from abi and ahi.
   # abi.sh: one TC case from abi
   # abi.sh: one TC case from ahi
   # abi_global.sh: global coverage with only one full goes17 coverage
   # goes_east.sh: one full goes_east abi coverage (GOES-EAST)
   # goes_west.sh: one full goes_west abi coverage (GOES-WEST)

repopath=`dirname $0`/../
pkgname=geocolor
. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_pre.sh $pkgname

echo ""
# "call" used in test_all_run.sh
for call in \
  "$GEOIPS_PACKAGES_DIR/geoips/tests/utils/check_code.sh all $repopath" \
  "$GEOIPS_PACKAGES_DIR/geoips/docs/build_docs.sh $repopath $pkgname html_only" \
  "$GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/abi.sh" \
  "$GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/ahi.sh" \
  "$GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/ami.sh" \
  "$GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/fci.sh" \
  "$GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/abi_global.sh" \
  "$GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/abi_clean.sh" \
  "$GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/goes_east.sh"
do
  . $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_run.sh
done

. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_post.sh
