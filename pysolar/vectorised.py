#    Copyright Brandon Stafford
#
#    This file is part of Pysolar.
#
#    Pysolar is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Pysolar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with Pysolar. If not, see <http://www.gnu.org/licenses/>.

"""Vectorised solar position and radiation calculations

This module provides high-performance NumPy-based implementations of solar
position and radiation calculations, optimized for processing large arrays
of timestamps and locations simultaneously.

Key functions:
- get_solar_angles_vector(): Calculate solar azimuth and zenith angles
- get_radiation_direct_vector(): Calculate direct solar radiation

Performance: Typically 500-2000x faster than scalar implementations while
maintaining accuracy within 0.1° for angles and 0.5 W/m² for radiation.
"""

import numpy as np

from .numeric import to_utc_datetime64


def get_solar_angles_vector(latitudes_deg, longitudes_deg, whens):
    """
    Calculate solar azimuth and zenith angles using vectorised operations.

    Parameters
    ----------
    latitudes_deg : float or array of float
        Latitude(s) in degrees (positive for North)
    longitudes_deg : float or array of float
        Longitude(s) in degrees (positive for East)
    whens : datetime64 or array of datetime64
        UTC timestamp(s) - should be timezone-aware datetime objects

    Returns
    -------
    azimuths_deg : float or array of float
        Solar azimuth angle(s) in degrees (0-360, North=0, East=90)
    zeniths_deg : float or array of float
        Solar zenith angle(s) in degrees (0=overhead, 90=horizon)

    Notes
    -----
    This is a vectorised implementation optimized for NumPy arrays.
    Results should closely match the original solar.get_azimuth() and
    solar.get_altitude() functions (where zenith = 90 - altitude).

    For consistency with existing pysolar API:
    - Parameter order matches get_azimuth(latitude_deg, longitude_deg, when)
    - Returns (azimuth, zenith) similar to get_position() returning (azimuth, altitude)
    - Parameter names are pluralized to indicate vectorised operation

    Accuracy: Typical error ~0.01°, max error ~0.6° compared to full NREL SPA
    Speed: ~2000x faster than full NREL SPA, ~500x faster than get_*_fast()
    """
    whens = to_utc_datetime64(whens)
    latitudes_deg = np.asarray(latitudes_deg)
    longitudes_deg = np.asarray(longitudes_deg)

    # Convert datetime64 to Julian Day
    jds = (whens - np.datetime64("1970-01-01T00:00:00")) / np.timedelta64(1, "s") / 86400.0 + 2440587.5
    jcs = (jds - 2451545.0) / 36525.0  # Julian centuries since J2000.0

    # Mean elements
    L0s = (280.46646 + jcs * (36000.76983 + 0.0003032 * jcs)) % 360
    Ms = (357.52911 + jcs * (35999.05029 - 0.0001537 * jcs)) % 360

    # Equation of center
    Cs = (1.914602 - jcs * (0.004817 + 0.000014 * jcs)) * np.sin(np.deg2rad(Ms))
    Cs += 0.019993 * np.sin(np.deg2rad(2 * Ms)) + 0.000289 * np.sin(np.deg2rad(3 * Ms))

    # True and apparent longitude
    true_longs = L0s + Cs
    omegas = 125.04 - 1934.136 * jcs
    lams = true_longs - 0.00569 - 0.00478 * np.sin(np.deg2rad(omegas))

    # Obliquity
    epss = 23.439292 - 0.0000130111 * jcs
    epss_rad = np.deg2rad(epss)

    # Right ascension & declination
    lams_rad = np.deg2rad(lams)
    sin_lams, cos_lams = np.sin(lams_rad), np.cos(lams_rad)
    sin_epss, cos_epss = np.sin(epss_rad), np.cos(epss_rad)
    decls = np.arcsin(sin_epss * sin_lams)
    ras = np.arctan2(cos_epss * sin_lams, cos_lams)

    # Local Sidereal Time
    thetas = (280.46061837 + 360.98564736629 * (jds - 2451545) + longitudes_deg) % 360
    Hs = np.deg2rad(thetas) - ras  # Hour angle (radians)
    Hs = (Hs + np.pi) % (2 * np.pi) - np.pi  # Wrap [-π, π]

    # Convert to horizontal coordinates
    lats_rad = np.deg2rad(latitudes_deg)
    sin_lats, cos_lats = np.sin(lats_rad), np.cos(lats_rad)
    sin_decls, cos_decls = np.sin(decls), np.cos(decls)
    elevations = np.arcsin(sin_lats * sin_decls + cos_lats * cos_decls * np.cos(Hs))
    azimuths = np.arctan2(-np.sin(Hs), np.tan(decls) * cos_lats - sin_lats * np.cos(Hs))

    # Convert to degrees
    elevations_deg = np.rad2deg(elevations)
    azimuths_deg = (np.rad2deg(azimuths) + 360) % 360
    zeniths_deg = 90.0 - elevations_deg

    # Optional atmospheric refraction correction (applied to elevation)
    refractions = np.where(
        elevations_deg > -0.575,
        1.02 / np.tan(np.deg2rad(elevations_deg + 10.3 / (elevations_deg + 5.11))) / 60.0,
        0.0,
    )
    zeniths_deg -= refractions  # decrease zenith since elevation increased slightly

    return azimuths_deg, zeniths_deg


def get_radiation_direct_vector(altitudes_deg, whens):
    """
    Calculate direct solar radiation using vectorised operations.

    Parameters
    ----------
    altitudes_deg : float or array of float
        Solar altitude angle(s) in degrees (0=horizon, 90=overhead)
    whens : datetime64 or array of datetime64
        UTC timestamp(s) for day-of-year calculation

    Returns
    -------
    radiation : float or array of float
        Direct solar radiation in W/m² (0 when sun below horizon)

    Notes
    -----
    Uses the simple atmospheric model from Masters, p. 412.
    Suitable for clear-sky conditions. Does not account for clouds,
    humidity, or other atmospheric conditions.

    For typical use, get altitude from:
        azimuths, zeniths = get_solar_angles_vector(lats, lons, whens)
        altitudes = 90.0 - zeniths
        radiation = get_radiation_direct_vector(altitudes, whens)
    """
    altitudes_deg = np.asarray(altitudes_deg)
    whens = to_utc_datetime64(whens)

    # Get day of year from datetime64
    # Extract year-start and current date to compute day-of-year
    year_start = whens.astype('datetime64[Y]')
    days_from_year_start = (whens - year_start) / np.timedelta64(1, 'D')
    day_of_year = days_from_year_start + 1  # 1-indexed

    # Apparent extraterrestrial flux (W/m²)
    flux = 1160 + (75 * np.sin(2 * np.pi / 365 * (day_of_year - 275)))

    # Optical depth (atmospheric clarity parameter)
    optical_depth = 0.174 + (0.035 * np.sin(2 * np.pi / 365 * (day_of_year - 100)))

    # Air mass ratio (path length through atmosphere)
    # Use where to avoid division by zero
    air_mass_ratio = np.where(
        altitudes_deg > 0,
        1.0 / np.sin(np.deg2rad(altitudes_deg)),
        np.inf
    )

    # Direct radiation (only when sun is above horizon)
    is_daytime = altitudes_deg > 0
    radiation = flux * np.exp(-optical_depth * air_mass_ratio) * is_daytime

    return radiation
