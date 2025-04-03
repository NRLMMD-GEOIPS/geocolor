    # # # This source code is protected under the license referenced at
    # # # https://github.com/NRLMMD-GEOIPS.

| ⚠️ **Warning** |
| -------------- |
| This package is an early release and should be expected to change in the future. We don’t expect the functionality to change in significant ways. We intend to improve the installation process, consolidate packages and, potentially, convert Fortran routines to Python to avoid complexity in installation. |

GeoColor GeoIPS Plugin
======================

The GeoColor package is a GeoIPS-compatible plugin, intended to be used within
the GeoIPS ecosystem.  Please see the
[GeoIPS Documentation](https://github.com/NRLMMD-GEOIPS/geoips#readme) for
more information on the GeoIPS plugin architecture and base infrastructure.

Package Overview
-----------------

The GeoColor plugin provides a product containing True Color imagery during
the day, and enhanced infrared imagery at night.

System Requirements
---------------------

* geoips >= 1.12.0
* Test data repos contained in $GEOIPS_TESTDATA_DIR for tests to pass.
* fortran_utils
* ancildat
* true_color >= 1.12.0

IF REQUIRED: Install base geoips package
------------------------------------------------------------
SKIP IF YOU HAVE ALREADY INSTALLED BASE GEOIPS ENVIRONMENT

If GeoIPS Base is not yet installed, follow the
[installation instructions](https://github.com/NRLMMD-GEOIPS/geoips#installation)
within the geoips source repo documentation:

Install geocolor package
------------------------
```bash

    # Ensure GeoIPS Python environment is enabled.

    # Clone and install geocolor
    git clone https://github.com/NRLMMD-GEOIPS/ancildat $GEOIPS_PACKAGES_DIR/ancildat
    git clone https://github.com/NRLMMD-GEOIPS/rayleigh $GEOIPS_PACKAGES_DIR/rayleigh
    git clone https://github.com/NRLMMD-GEOIPS/geocolor $GEOIPS_PACKAGES_DIR/geocolor

    # NOTE: currently, fortran dependencies must be installed separately, initially
    # including in pyproject.toml resulted in incorrect installation paths.
    # More work required to get the pip dependencies working properly for fortran
    # installations via pyproject.toml with the poetry backend.
    pip install -e $GEOIPS_PACKAGES_DIR/ancildat
    pip install -e $GEOIPS_PACKAGES_DIR/rayleigh
    pip install -e $GEOIPS_PACKAGES_DIR/geocolor

```

Test geocolor installation
--------------------------
```bash

    # Ensure GeoIPS Python environment is enabled.

    # This script will run ALL tests within this package
    $GEOIPS_PACKAGES_DIR/geocolor/tests/test_all.sh

    # Individual direct test calls, for reference
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/abi.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/ahi.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/goes16.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/goes17.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/himawari8.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/abi_global.sh
```
