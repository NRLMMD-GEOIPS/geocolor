# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""GeoColor algorithm."""

# Python Standard Libraries
from math import log10
from scipy.special import erf
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


def apply_day_tone_curve(true_color):
    """Lift shadows and roll off highlights on TrueColor.

    We preserve hue by operating on luma and scaling RGB by the luma ratio.
    Parameters are intentionally conservative to avoid destabilizing contrast.
    """
    r = np.ma.array(true_color["RED"])
    g = np.ma.array(true_color["GRN"])
    b = np.ma.array(true_color["BLU"])

    # Perceptual luma
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b

    # 1) Shadow lift (gamma < 1 brightens darks slightly)
    shadow_gamma = 0.9
    luma_lifted = luma**shadow_gamma

    # 2) Soft highlight roll-off using a smooth knee
    knee_start = 0.78  # where compression starts
    shoulder_strength = 1.5  # >0 increases compression steepness

    valid = np.logical_not(np.ma.getmaskarray(luma))

    t = np.zeros(luma.shape, dtype=float)
    t[valid] = (luma_lifted[valid] - knee_start) / (1.0 - knee_start)
    t[valid] = np.clip(t[valid], 0.0, 1.0)

    # Smoothstep weight for a gentle transition through the knee
    w = t * t * (3.0 - 2.0 * t)

    # Target curve keeps 1.0 -> 1.0 while compressing just above the knee
    target_vals = knee_start + (1.0 - knee_start) * np.power(
        t[valid], 1.0 + shoulder_strength
    )

    luma_toned = np.ma.array(luma_lifted, copy=True)
    luma_toned[valid] = luma_lifted[valid] + w[valid] * (
        target_vals - luma_lifted[valid]
    )

    # Preserve color by scaling RGB by the luma ratio (with safe denom)
    eps = 1e-6
    denom = luma.filled(0.0)
    scale = np.ones(luma.shape, dtype=float)
    pos = np.logical_and(valid, denom > eps)
    scale[pos] = luma_toned[pos] / denom[pos]

    out = {}
    for ch in ("RED", "GRN", "BLU"):
        arr = np.ma.array(true_color[ch], copy=True)
        arr[pos] = np.clip(arr[pos] * scale[pos], 0.0, 1.0)
        out[ch] = arr

    return out


def extend_day_into_twilight(
    true_color,
    sunzen_deg,
    zen_lthr=80.0,
    zen_uthr=88.0,
    preband_deg=4.0,
    center_frac=0.60,
    softness_frac=0.20,
    max_gain=0.25,
):
    """Boost TrueColor near the terminator so it reads a little farther into twilight.

    ERF weighting runs from [zen_lthr - preband_deg, zen_uthr].
    Darker midtones get more lift.
    """
    band_min = max(0.0, float(zen_lthr) - preband_deg)
    band_max = float(zen_uthr)
    band_width = max(1e-6, band_max - band_min)

    t = (sunzen_deg - band_min) / band_width
    t = np.clip(t, 0.0, 1.0)

    z = (t - center_frac) / (np.sqrt(2.0) * softness_frac)
    boost_weight = 0.5 * (1.0 + erf(z))
    boost_weight = np.clip(boost_weight, 0.0, 1.0)

    day_or_twilight = sunzen_deg <= zen_uthr
    boost_weight = np.where(day_or_twilight, boost_weight, 0.0)

    r = np.ma.array(true_color["RED"])
    g = np.ma.array(true_color["GRN"])
    b = np.ma.array(true_color["BLU"])
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b

    scale = 1.0 + max_gain * boost_weight * (1.0 - luma.filled(0.0))

    out = {}
    for ch in ("RED", "GRN", "BLU"):
        arr = np.ma.array(true_color[ch], copy=True)
        arr[day_or_twilight] = np.clip(
            arr[day_or_twilight] * scale[day_or_twilight], 0.0, 1.0
        )
        out[ch] = arr

    return out


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

    # Daytime True Color
    log.info("Computing true color.")
    if xobj.source_name in ["ahi", "fci"]:
        true_color = compute_ahi_true_color(ref)
    elif xobj.source_name == "abi":
        true_color = compute_abi_true_color(ref, ls_mask)
    else:
        true_color = compute_true_color(ref)

    true_color = apply_day_tone_curve(true_color)
    true_color = extend_day_into_twilight(true_color, sunzen)

    # Nighttime side
    log.info("Computing nighttime side.")
    # min_sunzen = 75.0
    # max_sunzen = 85.0
    min_elev = 0.0
    max_elev = 50_000.0  # elevation/bathymetry cap from IDL

    # Make ls_mask binary with Land (and Coast) == Ture and Water == False
    # In the original mask: Land == 1, coast == 2
    bin_ls_mask = np.logical_or(ls_mask == 1, ls_mask == 2)

    elev = elevation(lons, lats)[0]
    # Set elevation to 0 over water
    # (correct elevation artifacts over water in elevation database)
    elev[~bin_ls_mask] = (
        0.0  # set elev = 0 where bin_ls_mask = False (i.e., not over land and coast)
    )

    # Normalizations
    norm_lwir = 1.0 - normalize_ir_by_abslats(lwir, lats) ** 1.1
    elev = normalize(elev, min_elev, max_elev)
    lights = normalize_city_lights(lights)

    # RGB buffers
    # Start building color guns
    red = np.empty(norm_lwir.shape)
    grn = np.empty(norm_lwir.shape)
    blu = np.empty(norm_lwir.shape)

    # City lights
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

    # Day/night/twilight masks
    zen_lthr = 80
    zen_uthr = 88
    day_mask = sunzen <= zen_lthr
    night_mask = sunzen >= zen_uthr
    twilight_mask = np.logical_and(sunzen > zen_lthr, sunzen < zen_uthr)

    # Blend with True Color
    log.info("Blend daytime with nighttime across terminator.")
    good_bt = np.logical_or(lwir > 150.0, lwir < 360.0)

    # Day-only write
    valid_day = np.logical_and(day_mask, good_bt)
    red[valid_day] = true_color["RED"][valid_day]
    grn[valid_day] = true_color["GRN"][valid_day]
    blu[valid_day] = true_color["BLU"][valid_day]

    # Night-only write
    valid_night = np.logical_and(night_mask, good_bt)
    red[valid_night] = norm_lwir[valid_night] + (1.0 - norm_lwir[valid_night]) * (
        0.55 * btd[valid_night] + (1.0 - btd[valid_night]) * red[valid_night]
    )
    grn[valid_night] = norm_lwir[valid_night] + (1.0 - norm_lwir[valid_night]) * (
        0.75 * btd[valid_night] + (1.0 - btd[valid_night]) * grn[valid_night]
    )
    blu[valid_night] = norm_lwir[valid_night] + (1.0 - norm_lwir[valid_night]) * (
        0.98 * btd[valid_night] + (1.0 - btd[valid_night]) * blu[valid_night]
    )

    # Blended twilight output (ERF-weighted within [zen_lthr, zen_uthr])
    valid_twilight = np.logical_and(twilight_mask, good_bt)
    vt = valid_twilight

    tw_min_deg = float(zen_lthr)
    tw_max_deg = float(zen_uthr)
    tw_width_deg = max(1e-6, tw_max_deg - tw_min_deg)

    # Normalized 0..1 coordinate across the twilight span
    t = (sunzen[vt] - tw_min_deg) / tw_width_deg
    t = np.clip(t, 0.0, 1.0)

    # center_frac > 0.5 pushes day a bit deeper into night
    center_frac = 0.55
    sigma_frac = 0.18

    z = (t - center_frac) / (np.sqrt(2.0) * sigma_frac)

    day_weight = 0.5 * (1.0 - erf(z))
    day_weight = np.clip(day_weight, 0.0, 1.0)
    night_weight = 1.0 - day_weight

    # Night RGB for the twilight pixels
    night_r = norm_lwir[vt] + (1.0 - norm_lwir[vt]) * (
        0.55 * btd[vt] + (1.0 - btd[vt]) * red[vt]
    )
    night_g = norm_lwir[vt] + (1.0 - norm_lwir[vt]) * (
        0.75 * btd[vt] + (1.0 - btd[vt]) * grn[vt]
    )
    night_b = norm_lwir[vt] + (1.0 - norm_lwir[vt]) * (
        0.98 * btd[vt] + (1.0 - btd[vt]) * blu[vt]
    )

    # Continuous at tw_min/tw_max
    red[vt] = day_weight * true_color["RED"][vt] + night_weight * night_r
    grn[vt] = day_weight * true_color["GRN"][vt] + night_weight * night_g
    blu[vt] = day_weight * true_color["BLU"][vt] + night_weight * night_b

    red[~good_bt] = 0.0
    grn[~good_bt] = 0.0
    blu[~good_bt] = 0.0

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
