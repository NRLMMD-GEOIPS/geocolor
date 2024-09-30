    # # # This source code is protected under the license referenced at
    # # # https://github.com/NRLMMD-GEOIPS.

# v1.5.3: 2022-11-04, update test YAML metadata output

## GEOIPS#103: 2022-10-20, Remove YAML metadata output
### Test Repo Outputs
#### Remove YAML metadata outputs from test output files
* Avoid unnecessary test output updates with slight modifications to metadata output
* Prompted by addition of "storm_start_datetime" field in sector_info
* Metadata outputs will be tested separately from a consolidated test location
    * Provide a single location to test all metadata output, with only a single repo update required with changes
* Removed files:
```
deleted:    tests/outputs/abi/GeoColor_image/20210718_015031_EP062021_abi_goes-17_GeoColor_120kts_100p00_1p0-clean.png.yaml
deleted:    tests/outputs/ahi/GeoColor_image/20200405_000000_SH252020_ahi_himawari-8_GeoColor_100kts_100p00_1p0-clean.png.yaml
```
#### Remove YAML metadata outputs from test scripts
* YAML metadata tests will be performed from a consolidated testing location
    * Allow for a single update of all YAML metadata outputs when updates required
* Updated scripts:
```
modified:   tests/scripts/abi.sh
modified:   tests/scripts/ahi.sh
```


# v1.5.1: 2022-07-13, geoips2->geoips

### Refactor
* **File modifications**
    * Update all instances of 'geoips2' with 'geoips'
    * Update all instances of 'GEOIPS2' with 'GEOIPS'
* **Setup standardization**
    * Replace 'setup\_geocolor.sh install\_geocolor' with 'setup.sh install'
    * Remove NRL specific environment from setup.sh

### Documentation Updates
* Update \*.md Distro statement headers to use 4 spaces prefix rather than ### (formatting improvement)


# v1.4.5: 2022-03-18, compare_paths->compare_path

### Refactor
* Replace compare_paths with compare_path in geocolor single_source test scripts
    * abi.sh
    * abi_global.sh
    * ahi.sh
    * goes16.sh
    * goes17.sh
    * himawari8.sh


# v1.4.2: 2022-02-05, add --resampled_read argument to test scripts, replaced annotated test outputs with clean

### Test Repo Updates
    * Replaced annotated imagery test outputs with clean imagery
        * Test algorithm only, not plotting parameters

### Refactor
    * Added --resampled_read argument for ABI and AHI geocolor test scripts


# v1.4.0: 2022-01-11, add metadata output requests for TC test products

### Improvements
    * Add metadata output requests for TC test products
        * ABI, AHI


# v1.3.0: 2021-11-24, GeoIPSfinal/tcwww to preprocessed/tcwww

### Refactor
    * Updated metadata YAML outputs to replace paths


# v1.2.5: 2021-11-18, Initial version of geocolor package and simplified test scripts

### Major New Functionality
    * Initial geocolor implementation
    * Simplified test scripts include explicit command line calls with valid return codes
        * abi.sh:  one TC case
        * ahi.sh:  one TC case
        * goes16.sh: one case for GOES-E full coverage
        * goes17.sh: one case for GOES-W full coverage
        * himawari8.sh: one case for Himawari-8 full coverage
        * abi_global.sh: one case for global coverage with GOES-W data
