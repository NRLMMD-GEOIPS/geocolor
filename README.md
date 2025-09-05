    # # # This source code is subject to the license referenced at
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
The following are required prior to following the installation instructions below.
We intend to improve this installation process in the near future.

Click each package for installation instructions.

* [GNU make](https://www.gnu.org/software/make/)
* [gfortran](https://fortran-lang.org/learn/os_setup/install_gfortran/)
* [geoips >= 1.15.0](https://github.com/NRLMMD-GEOIPS/geoips#installation)

Install geocolor package
------------------------
The instructions below describe how to install the GeoColor GeoIPS plugin.

GeoColor is dissimilar to other GeoIPS packages. It's dependent on multiple other plugin
packages, most of which contain static datasets or fortran functionality that is
required to produce GeoColor. We apologize for the inconvenience and are working on
making the installation process much easier in the future.

The instructions below will install:
- GeoIPS Plugin Packages:
  - fortran_utils
  - ancildat
  - synth_green
  - rayleigh
  - geocolor
- Ancillary Datasets:
  - city_lights
  - elevation
  - lw_mask
  - rayleigh
  - synth_green

```bash

    # Add the following environment variables to your .bashrc and re-source it afterwards
    export GEOIPS_DEPENDENCIES_DIR=$GEOIPS_PACKAGES_DIR/dependencies
    export GEOIPS_ANCILDAT=$GEOIPS_PACKAGES_DIR/ancildat
    source ~/.bashrc

    # Ensure GeoIPS Python environment is enabled.
    # I.e. something like: conda/mamba activate geoips

    # Clone and install repos GeoColor requires
    git clone https://github.com/NRLMMD-GEOIPS/fortran_utils $GEOIPS_PACKAGES_DIR/fortran_utils
    git clone https://github.com/NRLMMD-GEOIPS/ancildat $GEOIPS_PACKAGES_DIR/ancildat
    git clone https://github.com/NRLMMD-GEOIPS/synth_green $GEOIPS_PACKAGES_DIR/synth_green
    git clone https://github.com/NRLMMD-GEOIPS/rayleigh $GEOIPS_PACKAGES_DIR/rayleigh
    git clone https://github.com/NRLMMD-GEOIPS/geocolor $GEOIPS_PACKAGES_DIR/geocolor

    # NOTE: fortran_utils MUST be installed prior to ancildat and rayleigh.
    # If you install in this order and you should be fine.

    # NOTE: if you are reinstalling these packages from a previous installation,
    # you must first call `make clean` from within each fortran dependency.
    # i.e. fortran_utils, ancildat, synth_green, rayleigh

    # NOTE: currently, fortran dependencies must be installed separately, initially
    # including in pyproject.toml resulted in incorrect installation paths.
    # More work required to get the pip dependencies working properly for fortran
    # installations via pyproject.toml with the poetry backend.
    pip install -e $GEOIPS_PACKAGES_DIR/fortran_utils
    pip install -e $GEOIPS_PACKAGES_DIR/ancildat
    pip install -e $GEOIPS_PACKAGES_DIR/synth_green
    pip install -e $GEOIPS_PACKAGES_DIR/rayleigh
    pip install -e $GEOIPS_PACKAGES_DIR/geocolor

    # Install ancillary datasets needed for GeoColor
    geoips config install city_lights --outdir $GEOIPS_ANCILDAT
    geoips config install elevation --outdir $GEOIPS_ANCILDAT
    geoips config install lw_mask --outdir $GEOIPS_ANCILDAT
    geoips config install rayleigh --outdir $GEOIPS_ANCILDAT
    geoips config install synth_green --outdir $GEOIPS_ANCILDAT

    # Install test_data_geocolor to your default $GEOIPS_TESTDATA_DIR
    # This command defaults to that location, hence the absence of '--outdir'
    geoips config install test_data_geocolor

```

Test geocolor installation
--------------------------
```bash

    # Ensure GeoIPS Python environment is enabled.

    # This will run ALL tests within this package
    pytest -m integration $GEOIPS_PACKAGES_DIR/geocolor

    # Individual direct test calls, for reference
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/abi_global.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/abi.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/ahi.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/ami.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/fci.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/goes_east.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/goes_west.sh
    $GEOIPS_PACKAGES_DIR/geocolor/tests/scripts/abi_clean.sh
```
