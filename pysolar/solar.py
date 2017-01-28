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

"""
Solar geometry functions

This module contains the most important functions for calculation of the position of the sun.

"""
import datetime
import math

from . import constants
from . import time
from . import radiation

def solar_test():
    """
    docstring goes here
    """
    latitude_deg = 42.364908
    longitude_deg = -71.112828
    dto = datetime.datetime(
        2003, 10, 17, 19, 30, tzinfo=datetime.timezone.utc)
    dt_list = [2003, 10, 17, 19, 30, 0, 0, 0, 0]
    # dto = (dto - time.EPOCH)
    thirty_minutes = datetime.timedelta(hours=0.5)
    lat_lon_list = [latitude_deg, longitude_deg]
    for _idx in range(48):
        timestamp = dto.ctime()
        altitude_deg = get_altitude(lat_lon_list, dt_list)
        azimuth_deg = get_azimuth(lat_lon_list, dt_list)
        power = radiation.get_radiation_direct(dt_list, altitude_deg)
        if altitude_deg > 0:
            print(timestamp, "UTC", altitude_deg, azimuth_deg, power)
        dto = dto + thirty_minutes

def equation_of_time(day):
    """
    returns the number of minutes to add to mean solar time to get actual solar time.
    """
    bias = 2 * math.pi / 364.0 * (day - 81)
    return 9.87 * math.sin(2 * bias) - 7.53 * math.cos(bias) - 1.5 * math.sin(bias)

def get_aberration_correction(dt_list, default=None):
    """
    docstring goes here
    """
    sun_earth_distance = get_sun_earth_distance(dt_list, default)
    # param is sun-earth distance is in astronomical units
    return -20.4898/(3600.0 * sun_earth_distance)

def get_altitude(dt_list, params_list, default=None):
    """
    See also the faster, but less accurate, get_altitude_fast()
    """
    topocentric_elevation_angle = get_topocentric_elevation_angle(dt_list, params_list, default)
    refraction_correction = get_refraction_correction(dt_list, params_list, default)
    return topocentric_elevation_angle + refraction_correction

def get_altitude_fast(when, params_list):
    """
    docstring goes here
    """
# expect 19 degrees for solar.get_altitude(
#     42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 13, 1, 130320))
    day = when.utctimetuple().tm_yday
    latitude = params_list[1]
    longitude = params_list[2]
    cos_ha = math.cos(math.radians(get_hour_angle(when, longitude)))
    cos_dec = math.cos(math.radians(get_declination(day)))
    sin_dec = math.sin(math.radians(get_declination(day)))
    cos_lat = math.cos(math.radians(latitude))
    sin_lat = math.sin(math.radians(latitude))
    first_term = cos_lat * cos_dec * cos_ha
    second_term = sin_lat * sin_dec
    return math.degrees(math.asin(first_term + second_term))

def get_apparent_sun_longitude(dt_list, default=None):
    """
    docstring goes here
    """
    mgl = get_geocentric_longitude(dt_list, default)
    dpsi = get_nutation(dt_list, default)['longitude']
    aberration = get_aberration_correction(dt_list, default)
    return mgl + dpsi + aberration

def get_azimuth(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    return 180 - get_topocentric_azimuth_angle(dt_list, params_list, default)

def get_azimuth_fast(when, dt_list, params_list, default=None):
    """
    docstring goes here
    """
# expect -50 degrees for solar.get_azimuth(
#     42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 18, 0, 0))
    latitude = params_list[1]
    longitude = params_list[2]
    day = when.utctimetuple().tm_yday
    declination_rad = math.radians(get_declination(day))
    latitude_rad = math.radians(latitude)
    hour_angle_rad = math.radians(get_hour_angle(when, longitude))
    altitude_rad = math.radians(get_altitude(dt_list, params_list, default))

    azimuth_rad = math.asin(
        math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))

    if (
            math.cos(
                hour_angle_rad) >= (
                    math.tan(declination_rad) / math.tan(latitude_rad))):
        return math.degrees(azimuth_rad)
    else:
        return 180 - math.degrees(azimuth_rad)

def get_coeff(dt_list, coeffs, default=None):
    """
    computes a polynomial with time-varying coefficients from the given constant
    coefficients array and the current Julian millennium.
    """
    jem = time.get_julian_ephemeris_millennium(dt_list, default)
    result = 0.0
    group = 1.0
    for line in coeffs:
        term = 0.0
        for element in line:
            term += element[0] * math.cos(element[1] + element[2] * jem)
        #end for
        result += term * group
        group *= jem
    #end for
    return result
#end get_coeff

def get_declination(day):
    """
    The declination of the sun is the angle between
    Earth's equatorial plane and a line between the Earth and the sun.
    The declination of the sun varies between 23.45 degrees and -23.45 degrees,
    hitting zero on the equinoxes and peaking on the solstices.
    """
    return constants.EARTH_AXIS_INCLINATION * math.sin((2 * math.pi / 365.0) * (day - 81))

def get_equation_of_equinox(dt_list, default=None):
    """
    doc
    """
    delta_psi = get_nutation(dt_list, default)['longitude']
    epsilon = get_true_ecliptic_obliquity(dt_list, default)
    cos_eps = math.cos(math.radians(epsilon))
    return delta_psi * cos_eps

def get_flattened_latitude(latitude):
    """
    docstring goes here
    """
    tan_lat = math.tan(math.radians(latitude))
    return math.degrees(math.atan(0.99664719 * tan_lat))

def get_gmst(dt_list, default=None):
    """
    docstring goes here
    """
    # print(dt_list)
    # This function doesn't agree with Andreas and Reda as well as it should.
    # Works to ~5 sig figs in current unit test
    jct = time.get_julian_century(dt_list, default)
    jdn = jct * 36525.0
    day_deg = (360.9856473659 * jdn) # 360.98564736629 is old and this is not SOFA
    mean_st = ((jct / 38710000.0) * jct + 0.000387933) * jct + 280.46061837 + day_deg
    return mean_st % 360

def get_gast(dt_list, default=None):
    """
    docstring goes here
    """
    gmst = get_gmst(dt_list, default)
    eqeq = get_equation_of_equinox(dt_list, default)
    return gmst + eqeq

def get_lmst(dt_list, default=None):
    """
    docstring goes here
    """
    return None

def get_last(dt_list, default=None):
    """
    docstring goes here
    """
    return None

# Geocentric functions calculate angles relative to the center of the earth.

def get_geocentric_latitude(dt_list, default=None):
    """
    docstring goes here
    """
    return -1 * get_heliocentric_latitude(dt_list, default)

def get_geocentric_longitude(dt_list, default=None):
    """
    docstring goes here
    """
    return (get_heliocentric_longitude(dt_list, default) + 180) % 360

def get_geocentric_sun_declination(dt_list, default=None):
    """
    docstring goes here
    """
    apparent_sun_longitude = get_apparent_sun_longitude(dt_list, default)
    true_ecliptic_obliquity = get_true_ecliptic_obliquity(dt_list, default)
    geocentric_latitude = get_geocentric_latitude(dt_list, default)
    sin_apparent_sun_longitude = math.sin(math.radians(apparent_sun_longitude))
    sin_true_ecliptic_obliquity = math.sin(math.radians(true_ecliptic_obliquity))
    cos_true_ecliptic_obliquity = math.cos(math.radians(true_ecliptic_obliquity))
    sin_geocentric_latitude = math.sin(math.radians(geocentric_latitude))
    cos_geocentric_latitude = math.cos(math.radians(geocentric_latitude))
    adec = sin_geocentric_latitude * cos_true_ecliptic_obliquity
    bdec = cos_geocentric_latitude * sin_true_ecliptic_obliquity * sin_apparent_sun_longitude
    delta = math.asin(adec + bdec)
    return math.degrees(delta)

def get_geocentric_right_ascension(dt_list, default=None):
    """
    docstring goes here
    """
    apparent_sun_longitude = get_apparent_sun_longitude(dt_list, default)
    true_ecliptic_obliquity = get_true_ecliptic_obliquity(dt_list, default)
    geocentric_latitude = get_geocentric_latitude(dt_list, default)
    sin_apparent_sun_longitude = math.sin(math.radians(apparent_sun_longitude))
    cos_apparent_sun_longitude = math.cos(math.radians(apparent_sun_longitude))
    sin_true_ecliptic_obliquity = math.sin(math.radians(true_ecliptic_obliquity))
    cos_true_ecliptic_obliquity = math.cos(math.radians(true_ecliptic_obliquity))
    tan_geocentric_latitude = math.tan(math.radians(geocentric_latitude))
    ara = sin_apparent_sun_longitude * cos_true_ecliptic_obliquity
    bra = tan_geocentric_latitude * sin_true_ecliptic_obliquity
    cra = cos_apparent_sun_longitude
    alpha = math.atan2((ara - bra), cra)
    return math.degrees(alpha) % 360

# Heliocentric functions calculate angles relative to the center of the sun.

def get_heliocentric_latitude(dt_list, default=None):
    """
    docstring goes here
    """
    return math.degrees(get_coeff(dt_list, constants.HELIOCENTRIC_LATITUDE_COEFFS, default) / 1e8)

def get_heliocentric_longitude(dt_list, default=None):
    """
    docstring goes here
    """
    return math.degrees(
        get_coeff(dt_list, constants.HELIOCENTRIC_LONGITUDE_COEFFS, default) / 1e8) % 360

def get_hour_angle(when, longitude_deg):
    """
    docstring goes here
    """
    solar_time = get_solar_time(when, longitude_deg)
    return 15 * (12 - solar_time)

def get_incidence_angle(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    slope = params_list[3]
    slope_orientation = params_list[4]
    topocentric_azimuth_angle = get_topocentric_azimuth_angle(dt_list, params_list, default)
    taa_rad = (math.radians(topocentric_azimuth_angle))
    topocentric_zenith_angle = get_topocentric_zenith_angle(dt_list, params_list, default)
    sin_tza = math.sin(math.radians(topocentric_zenith_angle))
    cos_tza = math.cos(math.radians(topocentric_zenith_angle))
    sin_slope = math.sin(math.radians(slope))
    cos_slope = math.cos(math.radians(slope))
    so_rad = math.radians(slope_orientation)

    return math.degrees(
        math.acos(
            cos_tza * cos_slope + sin_slope * sin_tza * math.cos(taa_rad - math.pi - so_rad)))

def get_local_hour_angle(dt_list, params_list, default=None):
    """
    Local hour angle
    """
    longitude = params_list[2]
    gast = get_gast(dt_list, default)
    gra = get_geocentric_right_ascension(dt_list, default)
    return (gast + longitude - gra) % 360

def get_max_horizontal_parallax(dt_list, default=None):
    """
    docstring goes here
    """
    sun_earth_distance = get_sun_earth_distance(dt_list, default)
    return 8.794 / (3600 / sun_earth_distance)

def get_nutation(dt_list, default=None):
    """
    docstring goes here
    """
    jec = time.get_julian_ephemeris_century(dt_list, default)
    abcd = constants.NUTATION_COEFFICIENTS
    nutation_long = []
    nutation_oblique = []
    coef = constants.get_aberration_coeffs()
    xdx = list \
      (
          coef[k](jec)
          for k in
          ( # order is important
              'MeanElongationOfMoon',
              'MeanAnomalyOfSun',
              'MeanAnomalyOfMoon',
              'ArgumentOfLatitudeOfMoon',
              'LongitudeOfAscendingNode',
          )
      )
    sin_terms = constants.ABERRATION_SIN_TERMS
    for idx, _idx in enumerate(abcd):
        sigmaxy = 0.0
        for jdx, _jdx in enumerate(xdx):
            sigmaxy += xdx[jdx] * sin_terms[idx][jdx]
        #end for
        nutation_long.append(
            (abcd[idx][0] + (abcd[idx][1] * jec)) * math.sin(math.radians(sigmaxy)))
        nutation_oblique.append(
            (abcd[idx][2] + (abcd[idx][3] * jec)) * math.cos(math.radians(sigmaxy)))

    # 36000000 scales from 0.0001 arcseconds to degrees
    nutation = {'longitude' : sum(
        nutation_long) / 36000000.0, 'obliquity' : sum(nutation_oblique) / 36000000.0}

    return nutation
#end get_nutation

def get_right_ascension_parallax(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    gsd = get_geocentric_sun_declination(dt_list, default)
    ehp = get_max_horizontal_parallax(dt_list, default)
    prd = get_projected_radial_distance(params_list)
    lha = get_local_hour_angle(dt_list, params_list, default)
    sin_lha = math.sin(math.radians(lha))
    sin_ehp = math.sin(math.radians(ehp))
    cos_lha = math.cos(math.radians(lha))
    cos_gsd = math.cos(math.radians(gsd))
    ara = -1 * prd * sin_ehp * sin_lha
    bra = cos_gsd - prd * sin_ehp * cos_lha
    parallax = math.atan2(ara, bra)
    return math.degrees(parallax)

def get_projected_axial_distance(params_list):
    """
    docstring goes here
    """
    elevation = params_list[0]
    latitude = params_list[1]
    flat = get_flattened_latitude(latitude)
    sin_flat = math.sin(math.radians(flat))
    sin_lat = math.sin(math.radians(latitude))
    return 0.99664719 * sin_flat + (elevation * sin_lat / constants.EARTH_RADIUS)

def get_projected_radial_distance(params_list):
    """
    docstring goes here
    """
    elevation = params_list[0]
    latitude = params_list[1]
    flattened_latitude_rad = math.radians(get_flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return math.cos(
        flattened_latitude_rad) + (elevation * math.cos(latitude_rad) / constants.EARTH_RADIUS)

def get_refraction_correction(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    #function and default values according to original NREL SPA C code
    #http://www.nrel.gov/midc/spa/

    sun_radius = 0.26667
    atmos_refract = 0.5667
    del_e = 0.0
    tea = get_topocentric_elevation_angle(dt_list, params_list, default)

    # Approximation only valid if sun is not well below horizon
    # This approximation could be improved;
    # see history at https://github.com/pingswept/pysolar/pull/23
    # Better method could come from Auer and Standish [2000]:
    # http://iopscience.iop.org/1538-3881/119/5/2472/pdf/1538-3881_119_5_2472.pdf
    pressure = params_list[6]
    temperature = params_list[5]
    if tea >= -1.0*(sun_radius + atmos_refract):
        arc = pressure * 2.830 * 1.02
        brc = 1010.0 * temperature * 60.0 * math.tan(math.radians(tea + (10.3/(tea + 5.11))))
        del_e = arc / brc

    return del_e

def get_solar_time(when, longitude_deg):
    """
    returns solar time in hours for the specified longitude and time,
    accurate only to the nearest minute.
    """
    when = when.utctimetuple()
    return \
        (
            (when.tm_hour * 60 + when.tm_min + 4 * longitude_deg + equation_of_time(when.tm_yday))
            /
            60
        )

def get_sun_earth_distance(dt_list, default=None):
    """
    docstring goes here
    """
    return get_coeff(dt_list, constants.AU_DISTANCE_COEFFS, default) / 1e8

# Topocentric functions calculate angles relative to a location on the surface of the earth.

def get_topocentric_azimuth_angle(dt_list, params_list, default=None):
    """
    Measured eastward from north
    """
    latitude = params_list[1]
    tdec = get_topocentric_sun_declination(dt_list, params_list, default)
    tlha = get_topocentric_lha(dt_list, params_list, default)
    cos_tlha = math.cos(math.radians(tlha))
    sin_tlha = math.sin(math.radians(tlha))
    sin_lat = math.sin(math.radians(latitude))
    cos_lat = math.cos(math.radians(latitude))
    sin_lat = math.cos(math.radians(latitude))
    tan_tdec = math.tan(math.radians(tdec))
    ayt = sin_tlha
    bxt = cos_tlha * sin_lat - tan_tdec * cos_lat
    return 180.0 + math.degrees(math.atan2(ayt, bxt)) % 360

def get_topocentric_elevation_angle(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    latitude = params_list[1]
    sin_latitude = math.sin(math.radians(latitude))
    cos_latitude = math.cos(math.radians(latitude))
    tsd = get_topocentric_sun_declination(dt_list, params_list, default)
    sin_tsd = math.sin(math.radians(tsd))
    cos_tsd = math.sin(math.radians(tsd))
    tlha = get_topocentric_lha(dt_list, params_list, default)
    cos_tlha = math.cos(math.radians(tlha))
    return math.degrees(
        math.asin(
            (sin_latitude * sin_tsd) + cos_latitude * cos_tsd * cos_tlha))

def get_topocentric_lha(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    local_hour_angle = get_local_hour_angle(dt_list, params_list, default)
    parallax_right_ascension = get_right_ascension_parallax(dt_list, params_list, default)
    return local_hour_angle - parallax_right_ascension

def get_topocentric_sun_declination(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    gsd = get_geocentric_sun_declination(dt_list, default)
    pad = get_projected_axial_distance(params_list)
    ehp = get_max_horizontal_parallax(dt_list, default)
    psra = get_right_ascension_parallax(dt_list, params_list, default)
    lha = get_local_hour_angle(dt_list, params_list, default)
    sin_ehp = math.sin(math.radians(ehp))
    sin_gsd = math.sin(math.radians(gsd))
    cos_gsd = math.cos(math.radians(gsd))
    pad = get_projected_axial_distance(params_list)
    cos_psra = math.cos(math.radians(psra))
    cos_lha = math.cos(math.radians(lha))
    ayt = sin_gsd - pad * sin_ehp * cos_psra
    bxt = cos_gsd - (pad * sin_ehp * cos_lha)
    return math.degrees(math.atan2(ayt, bxt))

def get_topocentric_right_ascension(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    psra = get_right_ascension_parallax(dt_list, params_list, default)
    gsra = get_geocentric_right_ascension(dt_list, default)
    return psra + gsra

def get_topocentric_zenith_angle(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    tea = get_topocentric_elevation_angle(dt_list, params_list, default)
    return 90 - tea - get_refraction_correction(dt_list, params_list, default)

def get_true_ecliptic_obliquity(dt_list, default=None):
    """
    docstring goes here
    """
    delta_eps = get_nutation(dt_list, default)['obliquity']
    tmu = time.get_julian_ephemeris_century(dt_list, default)
    mean_eps = 84381.448 - (4680.93 * tmu) - (1.55 * tmu ** 2) + (1999.25 * tmu ** 3) \
    - (51.38 * tmu ** 4) -(249.67 * tmu ** 5) - (39.05 * tmu ** 6) + (7.12 * tmu ** 7) \
    + (27.87 * tmu ** 8) + (5.79 * tmu ** 9) + (2.45 * tmu ** 10)
    return (mean_eps / 3600.0) + delta_eps
