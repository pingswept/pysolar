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

def aberration_correction(dt_list, default=None):
    """
    docstring goes here
    """
    sed = sun_earth_distance(dt_list, default)
    # param is sun-earth distance is in astronomical units
    return -20.4898/(3600.0 * sed)

def apparent_sun_longitude(dt_list, default=None):
    """
    docstring goes here
    """
    mgl = geocentric_longitude(dt_list, default)
    dpsi = nutation(dt_list, default)['longitude']
    aberration = aberration_correction(dt_list, default)
    return mgl + dpsi + aberration

def coefficients(dt_list, coeffs, default=None):
    """
    computes a polynomial with time-varying coefficients from the given constant
    coefficients array and the current Julian millennium.
    """
    jem = time.julian_ephemeris_millennium(dt_list, default)
    # jem = (2452930.312847 - 2451545.0) / 365250.0
    result = []
    count = 0.0
    for group in coeffs:
        term = 0.0
        jexp = math.pow(jem, count)
        for item in group:
            term += item[0] * math.cos(item[1] + item[2] * jem)
        #end for
        result.append(term * jexp)
        count += 1
    #end for
    return result
#end coefficients

def equation_of_equinox(dt_list, default=None):
    """
    doc
    """
    delta_psi = nutation(dt_list, default)['longitude']
    epsilon = true_ecliptic_obliquity(dt_list, default)
    cos_eps = math.cos(math.radians(epsilon))
    return delta_psi * cos_eps

def flattened_latitude(latitude):
    """
    docstring goes here
    """
    tan_lat = math.tan(math.radians(latitude))
    return math.degrees(math.atan(0.99664719 * tan_lat))

def gmst(dt_list, default=None):
    """
    docstring goes here
    """
    # print(dt_list)
    # This function doesn't agree with Andreas and Reda as well as it should.
    # Works to ~5 sig figs in current unit test
    jct = time.julian_century(dt_list, default)
    jdn = jct * 36525.0
    day_deg = (360.9856473659 * jdn) # 360.98564736629 is old and this is not SOFA
    mean_st = ((jct / 38710000.0) * jct + 0.000387933) * jct + 280.46061837 + day_deg
    return mean_st % 360

def gast(dt_list, default=None):
    """
    docstring goes here
    """
    mean = gmst(dt_list, default)
    eqeq = equation_of_equinox(dt_list, default)
    return mean + eqeq

def lmst(dt_list, params_list, default=None):
    """
    Loacal Mean Sidereal Time
    """
    mean = gmst(dt_list, default)
    return mean + params_list[3] % 360.0

def last(dt_list, params_list, default=None):
    """
    Loacal Apparent Sidereal Time
    """
    true = gast(dt_list, default)
    return true + params_list[3] % 360.0

# Geocentric functions calculate angles relative to the center of the earth.

def geocentric_latitude(dt_list, default=None):
    """
    docstring goes here
    """
    return -1 * heliocentric_latitude(dt_list, default)

def geocentric_longitude(dt_list, default=None):
    """
    docstring goes here
    """
    return (heliocentric_longitude(dt_list, default) + 180) % 360

def geocentric_declination(dt_list, default=None):
    """
    Geocentric declination of the Sun
    """
    asl = apparent_sun_longitude(dt_list, default)
    teo = true_ecliptic_obliquity(dt_list, default)
    glat = geocentric_latitude(dt_list, default)
    sin_asl = math.sin(math.radians(asl))
    sin_teo = math.sin(math.radians(teo))
    cos_teo = math.cos(math.radians(teo))
    sin_glat = math.sin(math.radians(glat))
    cos_glat = math.cos(math.radians(glat))
    return math.degrees(math.asin(sin_glat * cos_teo + cos_glat * sin_teo * sin_asl))

def geocentric_right_ascension(dt_list, default=None):
    """
    docstring goes here
    """
    asl = apparent_sun_longitude(dt_list, default)
    teo = true_ecliptic_obliquity(dt_list, default)
    glat = geocentric_latitude(dt_list, default)
    sin_asl = math.sin(math.radians(asl))
    cos_asl = math.cos(math.radians(asl))
    sin_teo = math.sin(math.radians(teo))
    cos_teo = math.cos(math.radians(teo))
    tan_glat = math.tan(math.radians(glat))
    return math.degrees(math.atan2((sin_asl * cos_teo - tan_glat * sin_teo), cos_asl)) % 360

# Heliocentric functions calculate angles relative to the center of the sun.

def heliocentric_latitude(dt_list, default=None):
    """
    That based on the Sun as a center.
    The Nautical Almanac gives the Heliocentric positions of all celestial bodies.
    """
    return math.degrees(
        coefficients(dt_list, constants.HELIOCENTRIC_LATITUDE_COEFFS, default) / 1e8)

def heliocentric_longitude(dt_list, default=None):
    """
    That based on the Sun as a center.
    The Nautical Almanac gives the Heliocentric positions of all celestial bodies.
    """
    # return math.degrees(
    #     coefficients(dt_list, constants.HELIOCENTRIC_LONGITUDE_COEFFS, default) / 1e8) % 360
    # jem = time.julian_ephemeris_millennium(dt_list, default)
    # jem = (2452930.312847 - 2451545.0) / 365250.0
    hlc = coefficients(dt_list, constants.HELIOCENTRIC_LONGITUDE_COEFFS, default)
    hlv = hlc[0] + hlc[1] + hlc[2] + hlc[3] + hlc[4] + hlc[5]
    return (hlv / 1.0e8) % 360.0

def incidence_angle(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    slope = params_list[3]
    slope_orientation = params_list[4]
    taa = topocentric_azimuth_angle(dt_list, params_list, default)
    taa_rad = (math.radians(taa))
    tza = topocentric_zenith_angle(dt_list, params_list, default)
    sin_tza = math.sin(math.radians(tza))
    cos_tza = math.cos(math.radians(tza))
    sin_slope = math.sin(math.radians(slope))
    cos_slope = math.cos(math.radians(slope))
    so_rad = math.radians(slope_orientation)

    return math.degrees(
        math.acos(
            cos_tza * cos_slope + sin_slope * sin_tza * math.cos(taa_rad - math.pi - so_rad)))

def local_hour_angle(dt_list, params_list, default=None):
    """
    Local hour angle
    """
    longitude = params_list[2]
    true = gast(dt_list, default)
    gra = geocentric_right_ascension(dt_list, default)
    return (true + longitude - gra) % 360

def max_horizontal_parallax(dt_list, default=None):
    """
    docstring goes here
    """
    sed = sun_earth_distance(dt_list, default)
    return 8.794 / (3600 / sed)

def mean_ecliptic_obliquity(dt_list, default=None):
    """
    docstring goes here
    """
    tmu = time.julian_ephemeris_century(dt_list, default)
    mean_eps1 = ((((((((((
        2.45 * tmu + 5.79) * tmu + 27.87) * tmu + 7.12) * tmu -
                       39.05) * tmu - 249.67) * tmu - 51.38) * tmu +
                    1999.25) * tmu - 1.55) * tmu - 4680.93) * tmu +
                 84381.448)
    return mean_eps1

def nutation(dt_list, default=None):
    """
    docstring goes here
    """
    jec = time.julian_ephemeris_century(dt_list, default)
    abcd = constants.NUTATION_COEFFICIENTS
    nutation_long = []
    nutation_oblique = []
    coef = constants.aberration_coeffs()
    xdx = list \
      (
          coef[k](jec)
          for k in
          ( # order is important
              'MeanAnomalyOfMoon',
              'MeanAnomalyOfSun',
              'ArgumentOfLatitudeOfMoon',
              'MeanElongationOfMoon',
              'LongitudeOfAscendingNode',
          )
      )
    sin_terms = constants.FAM
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
    deltas = {'longitude' : sum(
        nutation_long) / 36000000.0, 'obliquity' : sum(nutation_oblique) / 36000000.0}

    return deltas
#end nutation

def projected_axial_distance(params_list):
    """
    docstring goes here
    """
    elevation = params_list[0]
    latitude = params_list[1]
    flat = flattened_latitude(latitude)
    sin_flat = math.sin(math.radians(flat))
    sin_lat = math.sin(math.radians(latitude))
    return 0.99664719 * sin_flat + (elevation * sin_lat / constants.EARTH_RADIUS)

def projected_radial_distance(params_list):
    """
    docstring goes here
    """
    elevation = params_list[0]
    latitude = params_list[1]
    flattened_latitude_rad = math.radians(flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return math.cos(
        flattened_latitude_rad) + (elevation * math.cos(latitude_rad) / constants.EARTH_RADIUS)

def refraction_correction(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    #function and default values according to original NREL SPA C code
    #http://www.nrel.gov/midc/spa/

    sun_radius = 0.26667
    atmos_refract = 0.5667
    del_e = 0.0
    tea = topocentric_elevation_angle(dt_list, params_list, default)

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

def right_ascension_parallax(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    gsd = geocentric_declination(dt_list, default)
    ehp = max_horizontal_parallax(dt_list, default)
    lha = local_hour_angle(dt_list, params_list, default)

    prd = projected_radial_distance(params_list)
    sin_ehp = math.sin(math.radians(ehp))
    sin_lha = math.sin(math.radians(lha))

    cos_gsd = math.cos(math.radians(gsd))
    cos_lha = math.cos(math.radians(lha))

    return math.degrees(
        math.atan2(-1 * prd * sin_ehp * sin_lha,
                   cos_gsd - prd * sin_ehp * cos_lha))



def sun_earth_distance(dt_list, default=None):
    """
    docstring goes here
    """
    return coefficients(dt_list, constants.AU_DISTANCE_COEFFS, default) / 1e8

# Topocentric functions calculate angles relative to a location on the surface of the earth.

def topocentric_azimuth_angle(dt_list, params_list, default=None):
    """
    Measured eastward from north
    """
    latitude = params_list[1]
    tdec = topocentric_sun_declination(dt_list, params_list, default)
    tlha = topocentric_lha(dt_list, params_list, default)
    cos_tlha = math.cos(math.radians(tlha))
    sin_tlha = math.sin(math.radians(tlha))
    sin_lat = math.sin(math.radians(latitude))
    cos_lat = math.cos(math.radians(latitude))
    sin_lat = math.cos(math.radians(latitude))
    tan_tdec = math.tan(math.radians(tdec))
    ayt = sin_tlha
    bxt = cos_tlha * sin_lat - tan_tdec * cos_lat
    return 180.0 + math.degrees(math.atan2(ayt, bxt)) % 360

def topocentric_elevation_angle(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    latitude = params_list[1]
    sin_latitude = math.sin(math.radians(latitude))
    cos_latitude = math.cos(math.radians(latitude))
    tsd = topocentric_sun_declination(dt_list, params_list, default)
    sin_tsd = math.sin(math.radians(tsd))
    cos_tsd = math.sin(math.radians(tsd))
    tlha = topocentric_lha(dt_list, params_list, default)
    cos_tlha = math.cos(math.radians(tlha))
    return math.degrees(
        math.asin(
            (sin_latitude * sin_tsd) + cos_latitude * cos_tsd * cos_tlha))

def topocentric_lha(dt_list, params_list, default=None):
    """
    Date,Time,Topocentric local hour angle
    """
    lha = local_hour_angle(dt_list, params_list, default)
    rap = right_ascension_parallax(dt_list, params_list, default)
    return lha - rap

def topocentric_sun_declination(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    gsd = geocentric_declination(dt_list, default)
    pad = projected_axial_distance(params_list)
    ehp = max_horizontal_parallax(dt_list, default)
    psra = right_ascension_parallax(dt_list, params_list, default)
    lha = local_hour_angle(dt_list, params_list, default)
    sin_ehp = math.sin(math.radians(ehp))
    sin_gsd = math.sin(math.radians(gsd))
    cos_gsd = math.cos(math.radians(gsd))
    pad = projected_axial_distance(params_list)
    cos_psra = math.cos(math.radians(psra))
    cos_lha = math.cos(math.radians(lha))
    ayt = sin_gsd - pad * sin_ehp * cos_psra
    bxt = cos_gsd - (pad * sin_ehp * cos_lha)
    return math.degrees(math.atan2(ayt, bxt))

def topocentric_right_ascension(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    psra = right_ascension_parallax(dt_list, params_list, default)
    gsra = geocentric_right_ascension(dt_list, default)
    return psra + gsra

def topocentric_zenith_angle(dt_list, params_list, default=None):
    """
    docstring goes here
    """
    tea = topocentric_elevation_angle(dt_list, params_list, default)
    return 90 - tea - refraction_correction(dt_list, params_list, default)

def true_ecliptic_obliquity(dt_list, default=None):
    """
    docstring goes here
    """
    tmu = time.julian_ephemeris_century(dt_list, default)
    mean_eps = 84381.448 - (4680.93 * tmu) - (1.55 * tmu ** 2) + (1999.25 * tmu ** 3) \
    - (51.38 * tmu ** 4) -(249.67 * tmu ** 5) - (39.05 * tmu ** 6) + (7.12 * tmu ** 7) \
    + (27.87 * tmu ** 8) + (5.79 * tmu ** 9) + (2.45 * tmu)

    mean_eps = ((((-0.0000000434 * tmu - 0.000000576) * tmu +
                  0.00200340) * tmu - 0.0001831) * tmu -
                46.836769) * tmu + 84381.406

    mean_eps = mean_ecliptic_obliquity(dt_list, default)
    delta_eps = nutation(dt_list, default)['obliquity']

    return (mean_eps / 3600.0) + delta_eps


def altitude(when, params_list, default=None):
    """
    See also the faster, but less accurate, altitude_fast()
    """
    dt_list = [when.year, when.month, when.day,
               when.hour, when.minute, when.second,
               when.microsecond, 0, 0]
    tea = topocentric_elevation_angle(dt_list, params_list, default)
    rca = refraction_correction(dt_list, params_list, default)
    return tea + rca

def altitude_fast(when, params_list):
    """
    docstring goes here
    """
# expect 19 degrees for solar.altitude(
#     42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 13, 1, 130320))
    day = when.utctimetuple().tm_yday
    latitude = params_list[1]
    longitude = params_list[2]
    cos_ha = math.cos(math.radians(hour_angle(when, longitude)))
    cos_dec = math.cos(math.radians(declination(day)))
    sin_dec = math.sin(math.radians(declination(day)))
    cos_lat = math.cos(math.radians(latitude))
    sin_lat = math.sin(math.radians(latitude))
    return math.degrees(math.asin(cos_lat * cos_dec * cos_ha + sin_lat * sin_dec))

def azimuth(when, params_list, default=None):
    """
    docstring goes here
    """
    dt_list = [when.year, when.month, when.day,
               when.hour, when.minute, when.second,
               when.microsecond, 0, 0]
    return 180 - topocentric_azimuth_angle(dt_list, params_list, default)

def azimuth_fast(when, dt_list, params_list, default=None):
    """
    docstring goes here
    """
    # expect -50 degrees for solar.get_azimuth(
    #     42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 18, 0, 0))
    latitude = params_list[1]
    longitude = params_list[2]
    day = when.utctimetuple().tm_yday
    declination_rad = math.radians(declination(day))
    latitude_rad = math.radians(latitude)
    hour_angle_rad = math.radians(hour_angle(when, longitude))
    altitude_rad = math.radians(altitude(dt_list, params_list, default))

    azimuth_rad = math.asin(
        math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))

    if (
            math.cos(
                hour_angle_rad) >= (
                    math.tan(declination_rad) / math.tan(latitude_rad))):
        return math.degrees(azimuth_rad)
    else:
        return 180 - math.degrees(azimuth_rad)

def declination(day):
    """
    The declination of the sun is the angle between
    Earth's equatorial plane and a line between the Earth and the sun.
    The declination of the sun varies between 23.45 degrees and -23.45 degrees,
    hitting zero on the equinoxes and peaking on the solstices.
    """
    return constants.EARTH_AXIS_INCLINATION * math.sin((2 * math.pi / 365.0) * (day - 81))

def equation_of_time(day):
    """
    returns the number of minutes to add to mean solar time to get actual solar time.
    """
    bias = 2 * math.pi / 364.0 * (day - 81)
    return 9.87 * math.sin(2 * bias) - 7.53 * math.cos(bias) - 1.5 * math.sin(bias)

def hour_angle(when, longitude_deg):
    """
    docstring goes here
    """
    sun_time = solar_time(when, longitude_deg)
    return 15 * (12 - sun_time)

def solar_time(when, longitude_deg):
    """
    returns solar time in hours for the specified longitude and time,
    accurate only to the nearest minute.
    """
    when = when.utctimetuple()
    return (
        (when.tm_hour * 60 + when.tm_min + 4 * longitude_deg + equation_of_time(when.tm_yday))
        /
        60
        )

def solar_test(params_list):
    """
    docstring goes here
    """
    latitude_deg = 42.364908
    longitude_deg = -71.112828
    when = datetime.datetime(
        2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)
    # dto = (dto - time.EPOCH)
    thirty_minutes = datetime.timedelta(hours=0.5)
    params_list[1] = latitude_deg
    params_list[2] = longitude_deg
    for _idx in range(48):
        timestamp = when.ctime()
        altitude_deg = altitude(when, params_list)
        azimuth_deg = azimuth(when, params_list)
        power = radiation.get_radiation_direct(when, altitude_deg)
        if altitude_deg > 0:
            print(timestamp, "UTC", altitude_deg, azimuth_deg, power)
        when = when + thirty_minutes
