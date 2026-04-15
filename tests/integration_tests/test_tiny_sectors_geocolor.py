# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Pytest file for calling integration bash scripts."""

import os
import pytest

from tests.integration_tests.test_integration import base_setup  # noqa: F401

from tests.integration_tests.test_integration import (
    run_script_with_bash,
    setup_environment as setup_geoips_environment,
)

global_example_integ_test_calls = [
    ##################################################################################
    # ### Scripts to produce global imagery outputs specifically for diagnostic
    # ### purposes, and identifying day/night/spatial contents of a given dataset.
    # ### More information in geoips/tests/integration_tests/test_tiny_sector_geoips.py
    ##################################################################################
    (
        "$geoips_repopath/tests/example_scripts/global_terminator_satzen.sh "
        "abi_netcdf "
        "Test-ABI-B13 "
        "$GEOIPS_TESTDATA_DIR/test_data_geocolor/data/goes18/20240924.1500/OR_ABI-L1b-RadF-M6C13*.nc"  # noqa: E501
    ),
    (
        "$geoips_repopath/tests/example_scripts/global_terminator_satzen.sh "
        "abi_netcdf "
        "Test-ABI-B13 "
        "$GEOIPS_TESTDATA_DIR/test_data_geocolor/data/goes16/20240920.1500/OR_ABI-L1b-RadF-M6C13*.nc"  # noqa: E501
    ),
    (
        "$geoips_repopath/tests/example_scripts/global_terminator_satzen.sh "
        "ahi_hsd "
        "Test-AHI-B13 "
        "$GEOIPS_TESTDATA_DIR/test_data_geocolor/data/himawari9/20240924.1500/*.DAT"  # noqa: E501
    ),
]

tiny_sector_overlay_integ_test_calls = [
    ##################################################################################
    # ### Output geoips test sector overlays on a global map to identify location of
    # ### each defined tiny sector.  Used for diagnostic purposes to evaluate location
    # ### and size of each tiny sector.
    ##################################################################################
    ##################################################################################
    # ### No satellite-specific test sectors in this repo, as those are included in the
    # ### main geoips repo.
    ##################################################################################
    ##################################################################################
    # ### Dataset specific test sectors, reliant on specific time of day and/or
    # ### meteorological features within the dataset.
    ##################################################################################
    # goes18 20240924T1500Z
    "geoips test sector --overlay test_goes18_eqc_10km_terminator_20240924T1500Z -o $GEOIPS_OUTDIRS/example_test_imagery_outputs ",  # noqa: E501
    # goes16 20240920T1500Z
    "geoips test sector --overlay test_goes16_eqc_10km_terminator_20240920T1500Z -o $GEOIPS_OUTDIRS/example_test_imagery_outputs ",  # noqa: E501
    "geoips test sector --overlay test_himawari9_eqc_3km_night_20240924T1500Z -o $GEOIPS_OUTDIRS/example_test_imagery_outputs ",  # noqa: E501
]


tiny_sector_integ_test_calls = [
    ##################################################################################
    # ### Test the actual output of each specified tiny sector defined within this repo.
    # ### tiny_sectors_geostationary.sh is a wrapper test script to produce the
    # ### specified tiny sector output, and compare it with the stored comparison
    # ### output imagery.
    # ### More information in geoips/tests/integration_tests/test_tiny_sector_geoips.py
    ##################################################################################
    ##################################################################################
    # ### No satellite-specific test sectors in this repo, as those are included in the
    # ### main geoips repo.
    ##################################################################################
    ##################################################################################
    # ### Dataset specific test sectors, reliant on specific time of day and/or
    # ### meteorological features within the dataset.
    ##################################################################################
    # Tiny sector for GOES-16 terminator 10km, regular B14 Infrared channel not in this
    # dataset (only Ch1, 2, 3, 7, 13)
    (
        "$GEOIPS_PACKAGES_DIR/geoips/tests/integration_tests/tiny_sectors/"
        "tiny_sectors_geostationary.sh "
        "test_goes18_eqc_10km_terminator_20240924T1500Z "
        "abi_netcdf "
        "Test-ABI-B13-Day-Only "
        "geocolor "
        "$GEOIPS_TESTDATA_DIR/test_data_geocolor/data/goes18/20240924.1500/OR_ABI-L1b-RadF-M6C13*.nc"  # noqa: E501
    ),
    # Tiny sector for GOES-16 terminator 10km, regular B14 Infrared channel not in this
    # dataset (only Ch1, 2, 3, 7, 13)
    (
        "$GEOIPS_PACKAGES_DIR/geoips/tests/integration_tests/tiny_sectors/"
        "tiny_sectors_geostationary.sh "
        "test_goes16_eqc_10km_terminator_20240920T1500Z "
        "abi_netcdf "
        "Test-ABI-B13-Day-Only "
        "geocolor "
        "$GEOIPS_TESTDATA_DIR/test_data_geocolor/data/goes16/20240920.1500/OR_ABI-L1b-RadF-M6C13*.nc"  # noqa: E501
    ),
    # Tiny sectors for himawari-9 3km night only
    (
        "$GEOIPS_PACKAGES_DIR/geoips/tests/integration_tests/tiny_sectors/"
        "tiny_sectors_geostationary.sh "
        "test_himawari9_eqc_3km_night_20240924T1500Z "
        "ahi_hsd "
        "Test-AHI-B13-Night-Only "
        "geocolor "
        "$GEOIPS_TESTDATA_DIR/test_data_geocolor/data/himawari9/20240924.1500/*.DAT"  # noqa: E501
    ),
]


def setup_environment():
    """
    Set up necessary environment variables for integration tests.

    Configures paths and package names for the GeoIPS core and its plugins by
    setting environment variables required for the integration tests. Assumes
    that 'GEOIPS_PACKAGES_DIR' is already set in the environment.

    Notes
    -----
    The following environment variables are set:
    - geoips_repopath
    - geoips_pkgname
    - repopath
    - pkgname
    """
    # Setup base geoips environment
    setup_geoips_environment()
    # Setup current repo's environment
    os.environ["repopath"] = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    os.environ["pkgname"] = "geocolor"


@pytest.mark.optional
@pytest.mark.sample_output
@pytest.mark.tiny_sector_evaluation
@pytest.mark.tiny_sector_global_example
@pytest.mark.parametrize("script", global_example_integ_test_calls)
def test_integ_global_example_script(base_setup: None, script: str):  # noqa: F811
    """
    Run integration test scripts by executing specified shell commands.

    Parameters
    ----------
    script : str
        Shell command to execute as part of the integration test. The command may
        contain environment variables which will be expanded before execution.

    Raises
    ------
    subprocess.CalledProcessError
        If the shell command returns a non-zero exit status.
    """
    setup_environment()
    run_script_with_bash(script)


@pytest.mark.optional
@pytest.mark.sample_output
@pytest.mark.tiny_sector_evaluation
@pytest.mark.tiny_sector_overlay
@pytest.mark.parametrize("script", tiny_sector_overlay_integ_test_calls)
def test_integ_tiny_sector_overlay_script(base_setup: None, script: str):  # noqa: F811
    """
    Run integration test scripts by executing specified shell commands.

    Parameters
    ----------
    script : str
        Shell command to execute as part of the integration test. The command may
        contain environment variables which will be expanded before execution.

    Raises
    ------
    subprocess.CalledProcessError
        If the shell command returns a non-zero exit status.
    """
    setup_environment()
    run_script_with_bash(script)


@pytest.mark.integration
@pytest.mark.tiny_sector_evaluation
@pytest.mark.tiny_sector
@pytest.mark.parametrize("script", tiny_sector_integ_test_calls)
def test_integ_tiny_sector_script(base_setup: None, script: str):  # noqa: F811
    """
    Run integration test scripts by executing specified shell commands.

    Parameters
    ----------
    script : str
        Shell command to execute as part of the integration test. The command may
        contain environment variables which will be expanded before execution.

    Raises
    ------
    subprocess.CalledProcessError
        If the shell command returns a non-zero exit status.
    """
    setup_environment()
    run_script_with_bash(script)
