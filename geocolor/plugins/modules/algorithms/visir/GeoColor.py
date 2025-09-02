# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""GeoColor algorithm."""

# Python Standard Libraries
from math import log10
import logging

# Installed Libraries
import numpy as np


# from .synthetic_green import synthetic_green

log = logging.getLogger(__name__)

interface = "algorithms"
family = "xarray_to_numpy"
name = "GeoColor"

ahi_var_map = {
    "BLU": "B01Rad",
    "GRN": "B02Rad",
    "RED": "B03Rad",
    "NIR": "B04Rad",
    "SWIR": "B07BT",
    "IR": "B13BT",
    "LATS": "latitude",
    "LONS": "longitude",
    "SATZEN": "satellite_zenith_angle",
    "SUNZEN": "solar_zenith_angle",
    "SATAZM": "satellite_azimuth_angle",
    "SUNAZM": "solar_azimuth_angle",
}
fci_var_map = {
    "BLU": "B01Rad",
    "GRN": "B02Rad",
    "RED": "B03Rad",
    "NIR": "B04Rad",
    "SWIR": "B09BT",
    "IR": "B14BT",
    "LATS": "latitude",
    "LONS": "longitude",
    "SATZEN": "satellite_zenith_angle",
    "SUNZEN": "solar_zenith_angle",
    "SATAZM": "satellite_azimuth_angle",
    "SUNAZM": "solar_azimuth_angle",
}
ami_var_map = {
    "BLU": "VI004Rad",
    "GRN": "VI005Rad",
    "RED": "VI006Rad",
    "NIR": "VI008Rad",
    "SWIR": "SW038BT",
    "IR": "IR105BT",
    "LATS": "latitude",
    "LONS": "longitude",
    "SATZEN": "satellite_zenith_angle",
    "SUNZEN": "solar_zenith_angle",
    "SATAZM": "satellite_azimuth_angle",
    "SUNAZM": "solar_azimuth_angle",
}
abi_var_map = {
    "BLU": "B01Rad",
    "RED": "B02Rad",
    "NIR": "B03Rad",
    "SWIR": "B07BT",
    "IR": "B13BT",
    "LATS": "latitude",
    "LONS": "longitude",
    "SATZEN": "satellite_zenith_angle",
    "SUNZEN": "solar_zenith_angle",
    "SATAZM": "satellite_azimuth_angle",
    "SUNAZM": "solar_azimuth_angle",
}

sensor_var_maps = {
    "ahi": ahi_var_map,
    "abi": abi_var_map,
    "ami": ami_var_map,
    "fci": fci_var_map,
}


def normalize(val, minval, maxval):
    """Normalize values."""
    val[val < minval] = minval
    val[val > maxval] = maxval
    val = (val - minval) / (maxval - minval)
    return val


def normalize_ir_by_abslats(ir, lats):
    """Normalize IR by absolute latitudes."""
    abslats = np.ma.abs(lats)
    abslats[abslats < 30.0] = 30.0
    abslats[abslats > 60.0] = 60.0

    minir = 170 + 30.0 * (abslats - 30.0) / (60.0 - 30.0)
    normir = (ir - minir) / (300.0 - minir)

    return normir


def normalize_city_lights(lights):
    """Normalize city lights."""
    lights[lights <= 0] = 0.0223
    lights[lights > 0] = np.log10(lights[lights > 0])
    min_lights = -0.5
    # max lights = 2.0 in IDL GeoColor code
    max_lights = 2.0
    lights = normalize(lights, min_lights, max_lights)
    return lights


def compute_true_color(ref):
    """Compute True Color."""
    min_ref = 0.0223
    max_ref = 1.0
    log_min_ref = log10(min_ref)
    log_max_ref = log10(max_ref)

    # Truncate to avoid underflow
    for ch, dat in ref.items():
        dat[np.ma.where(dat < min_ref)] = min_ref
        ref[ch] = np.ma.log10(dat).filled(log_min_ref)
        ref[ch] = (ref[ch] - log_min_ref) / (log_max_ref - log_min_ref)
        ref[ch][ref[ch] < 0] = 0
        ref[ch][ref[ch] > 1] = 1
        ref[ch] = np.ma.masked_array(ref[ch], mask=dat.mask)
    return ref


def compute_ahi_true_color(ref):
    """Compute AHI True Color."""
    ref = {
        "RED": ref["RED"],
        "GRN": 0.93 * ref["GRN"] + 0.07 * ref["NIR"],
        "BLU": ref["BLU"],
    }
    return compute_true_color(ref)


def compute_abi_true_color(ref, land_sea_mask):
    """Compute ABI True Color."""
    ref = {"NIR": ref["NIR"], "RED": ref["RED"], "BLU": ref["BLU"]}
    log.info("Calculating synthetic green.")

    # NOTE: until we get the fortran dependencies working in
    # pyproject.toml, do not import the fortran libraries at the
    # top level
    from synth_green.lib.libsynth_green import synth_green

    synth_green = synth_green.get_synth_green

    ref["GRN"], code = synth_green(ref["NIR"], ref["RED"], ref["BLU"], land_sea_mask)
    ref["GRN"] = np.ma.masked_array(
        normalize(ref["GRN"], 0, 1), mask=np.copy(ref["NIR"].mask)
    )
    return compute_true_color(ref)


def call(xobj):
    """Geo Color algorithm."""
    # Get the appropriate variable name map for the input data file based on sensor name
    try:
        var_map = sensor_var_maps[xobj.source_name]
    except KeyError:
        raise ValueError(
            "Unrecognized sensor {}. Accepted sensors include {}".format(
                xobj.source_name, ", ".join(sensor_var_maps.keys())
            )
        )

    # Ensure we have all of the required variables
    missing_channels = []
    for varname in var_map.keys():
        channame = var_map[varname]
        if channame not in list(xobj.keys()):
            missing_channels.append(channame)
    if missing_channels:
        raise ValueError(
            "Required channels not found: {}".format(", ".join(missing_channels))
        )

    # NOTE: until we get the fortran dependencies working in
    # pyproject.toml, do not import the fortran libraries at the
    # top level
    from ancildat.lib.libancildat import ancildat

    city_lights = ancildat.city_lights
    elevation = ancildat.elevation
    land_sea_mask = ancildat.land_sea_mask
    # Gather variables
    log.info("Gathering ancillary datasets")
    lons = xobj[var_map["LONS"].strip()].values
    # NOTE these 3 are normalized, which modifies the original
    # arrays (lats, sunzen, and lwir).  Ensure we copy these
    # values before applying algorithm.
    lats = xobj[var_map["LATS"].strip()].values.copy()
    sunzen = xobj[var_map["SUNZEN"].strip()].values.copy()
    lwir = xobj[var_map["IR"].strip()].values.copy()
    swir = xobj[var_map["SWIR"].strip()].values
    lights = city_lights(lons, lats)[0]
    ls_mask = land_sea_mask(lons, lats)[0]

    # mask invalid values (NaNs or infs)
    bad_data_mask = np.logical_or(
        np.ma.masked_invalid(xobj[var_map["IR"].strip()].values).mask,
        np.ma.masked_invalid(xobj[var_map["SWIR"].strip()].values).mask,
    )

    # Rayleigh correct the visible bands
    log.info("Performing rayleigh correction")

    # NOTE: until we get the fortran dependencies working in
    # pyproject.toml, do not import the fortran libraries at the
    # top level
    from rayleigh.rayleigh import rayleigh

    ref = rayleigh(xobj)

    # Compute True Color for daytime side
    log.info("Computing true color.")
    if xobj.source_name in ["ahi", "fci"]:
        true_color = compute_ahi_true_color(ref)
    elif xobj.source_name == "abi":
        true_color = compute_abi_true_color(ref, ls_mask)
    else:
        true_color = compute_true_color(ref)

    # Compute nighttime side
    log.info("Computing nighttime side.")
    min_sunzen = 75.0
    max_sunzen = 85.0
    min_elev = 0.0
    # Max elevation/bathymetry = 50,000 in IDL GeoColor code
    max_elev = 50_000.0

    # Make ls_mask binary with Land (and Coast) == Ture and Water == False
    # In the original mask: Land == 1, coast == 2
    bin_ls_mask = np.logical_or(ls_mask == 1, ls_mask == 2)

    elev = elevation(lons, lats)[0]
    # Set elevation to 0 over water
    # (correct elevation artifacts over water in elevation database)
    elev[~bin_ls_mask] = (
        0.0  # set elev = 0 where bin_ls_mask = False (i.e., not over land and coast)
    )

    # Normalize
    sunzen = 1.0 - normalize(sunzen, min_sunzen, max_sunzen)
    norm_lwir = 1.0 - normalize_ir_by_abslats(lwir, lats) ** 1.1
    elev = normalize(elev, min_elev, max_elev)
    lights = normalize_city_lights(lights)

    # Start building color guns
    red = np.empty(norm_lwir.shape)
    grn = np.empty(norm_lwir.shape)
    blu = np.empty(norm_lwir.shape)

    # Add in the city lights
    # Lights threshold for IDL GeoColor code = 0.2
    good_lights = lights > 0.2
    gl = good_lights
    red[gl] = (lights[gl] * 0.8) ** 0.75
    grn[gl] = (lights[gl] * 0.8) ** 1.25
    blu[gl] = (lights[gl] * 0.8) ** 2.00

    # Add in the land background
    # Makes terrain purple/blue with black oceans
    red_base = 0.06
    grn_base = 0.03
    blu_base = 0.13
    # Not sure what's wrong here.
    # This should give some color, but it is turning things white
    # The numbers don't seem to work out.  red_base * ls_mask * elev is always small!
    # This is because elev is always very small.  This just seems wrong...
    # See line 883 in Steve's code and note that red is Y8, grn is Y7, and blu is Y6
    # Yang's note:  this issue could be solved because of modification:
    # elev[np.logical_not(bin_ls_mask)] = 0.0
    #       It will be verified by cases over land.  Oct 20, 2021
    red[~gl] = (
        red_base * bin_ls_mask[~gl]
    )  # + (1.0 - red_base * bin_ls_mask[~gl] * elev[~gl])
    grn[~gl] = (
        grn_base * bin_ls_mask[~gl]
    )  # + (1.0 - grn_base * bin_ls_mask[~gl] * elev[~gl])
    blu[~gl] = (
        blu_base * bin_ls_mask[~gl]
    )  # + (1.0 - blu_base * bin_ls_mask[~gl] * elev[~gl])

    # NOTE: This is where false alarm checks would go with CCBG (see steve's code)

    # Calculate BT difference
    min_diff_lnd = 0.0
    max_diff_lnd = 4.0
    min_diff_wat = 0.0
    max_diff_wat = 4.0
    # lwir => long wave infrared
    # swir => short wave infrared
    btd = lwir - swir
    btd[lwir < 230.0] = 0.0
    # NOTE: More ccbg stuff should go here.  Skipping for now.
    btd[bin_ls_mask] = normalize(btd[bin_ls_mask], min_diff_lnd, max_diff_lnd)
    btd[~bin_ls_mask] = normalize(btd[~bin_ls_mask], min_diff_wat, max_diff_wat)

    # Blend with True Color
    log.info("Blend daytime with nighttime across terminator.")
    good_bt = np.logical_or(lwir > 150.0, lwir < 360.0)
    gb = good_bt
    # btd = brightness temperature difference
    red[gb] = (1.0 - sunzen[gb]) ** 1.5 * (
        norm_lwir[gb]
        + (1.0 - norm_lwir[gb]) * (0.55 * btd[gb] + (1.0 - btd[gb]) * red[gb])
    ) + sunzen[gb] * true_color["RED"][gb]
    grn[gb] = (1.0 - sunzen[gb]) ** 1.5 * (
        norm_lwir[gb]
        + (1.0 - norm_lwir[gb]) * (0.75 * btd[gb] + (1.0 - btd[gb]) * grn[gb])
    ) + sunzen[gb] * true_color["GRN"][gb]
    blu[gb] = (1.0 - sunzen[gb]) ** 1.5 * (
        norm_lwir[gb]
        + (1.0 - norm_lwir[gb]) * (0.98 * btd[gb] + (1.0 - btd[gb]) * blu[gb])
    ) + sunzen[gb] * true_color["BLU"][gb]
    red[~gb] = 0.0
    grn[~gb] = 0.0
    blu[~gb] = 0.0
    red[red < 0] = 0.0
    grn[grn < 0] = 0.0
    blu[blu < 0] = 0.0

    img = np.ma.dstack(
        (
            np.ma.array(red, mask=bad_data_mask),
            np.ma.array(grn, mask=bad_data_mask),
            np.ma.array(blu, mask=bad_data_mask),
        )
    )

    # prepare a geocolor product
    red = img[:, :, 0]
    grn = img[:, :, 1]
    blu = img[:, :, 2]

    from geoips.image_utils.mpl_utils import alpha_from_masked_arrays, rgba_from_arrays

    alp = alpha_from_masked_arrays([red, grn, blu])
    rgba = rgba_from_arrays(red, grn, blu, alp)

    return rgba
