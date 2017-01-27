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
import warnings
import math

from . import constants
from . import time
from . import radiation

def altitude(jdn):
    """
    doc
    """
    return jdn

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

def input_location(lat, lon):
    """
    docstring goes here
    """
    lat_lon_list = [lat, lon]
    return lat_lon_list

def equation_of_time(day):
    """
    returns the number of minutes to add to mean solar time to get actual solar time.
    """
    bias = 2 * math.pi / 364.0 * (day - 81)
    return 9.87 * math.sin(2 * bias) - 7.53 * math.cos(bias) - 1.5 * math.sin(bias)

def get_aberration_correction(dt_list):
    """
    docstring goes here
    """
    sun_earth_distance = get_sun_earth_distance(dt_list)
    # param is sun-earth distance is in astronomical units
    return -20.4898/(3600.0 * sun_earth_distance)

def get_altitude(
        lat_lon_list,
        dt_list, elevation=0, temperature=constants.STANDARD_TEMPERATURE,
        pressure=constants.STANDARD_PRESSURE):# too many local variables 27/15
    """
    See also the faster, but less accurate, get_altitude_fast()
    """
    # location-dependent calculations
    projected_radial_distance = get_projected_radial_distance(elevation, lat_lon_list[0])
    projected_axial_distance = get_projected_axial_distance(elevation, lat_lon_list[0])

    # time-dependent calculations
    jde = time.get_julian_ephemeris_day(dti)
    jce = time.get_julian_ephemeris_century(jde)
    jem = time.get_julian_ephemeris_millennium(dt_list)
    geocentric_latitude = get_geocentric_latitude(jem)
    geocentric_longitude = get_geocentric_longitude(jem)
    sun_earth_distance = get_sun_earth_distance(jem)
    aberration_correction = get_aberration_correction(sun_earth_distance)
    max_horizontal_parallax = get_max_horizontal_parallax(sun_earth_distance)
    # nutation = get_nutation(jce)
    gast = get_gast(dt_list)
    true_ecliptic_obliquity = get_true_ecliptic_obliquity(dt_list)

    # calculations dependent on location and time
    apparent_sun_longitude = get_apparent_sun_longitude(
        geocentric_longitude, get_nutation(jce), aberration_correction)
    geocentric_right_ascension = get_geocentric_right_ascension(
        apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude)
    geocentric_declination = get_geocentric_sun_declination(
        apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude)
    local_hour_angle = get_local_hour_angle(
        gast, lat_lon_list[1], geocentric_right_ascension)
    parallax_sun_right_ascension = get_parallax_right_ascension(
        projected_radial_distance, max_horizontal_parallax, local_hour_angle,
        geocentric_declination)
    topocentric_lha = get_topocentric_lha(
        local_hour_angle, parallax_sun_right_ascension)
    topocentric_sun_declination = get_topocentric_sun_declination(
        geocentric_declination, projected_axial_distance, max_horizontal_parallax,
        parallax_sun_right_ascension, local_hour_angle)
    topocentric_elevation_angle = get_topocentric_elevation_angle(
        lat_lon_list[1], topocentric_sun_declination, topocentric_lha)
    refraction_correction = get_refraction_correction(
        pressure, temperature, topocentric_elevation_angle)
    return topocentric_elevation_angle + refraction_correction

def get_altitude_fast(latitude, longitude, when):
    """
    docstring goes here
    """
# expect 19 degrees for solar.get_altitude(
#     42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 13, 1, 130320))
    day = when.utctimetuple().tm_yday
    cos_ha = math.cos(math.radians(get_hour_angle(when, longitude)))
    cos_dec = math.cos(math.radians(get_declination(day)))
    sin_dec = math.sin(math.radians(get_declination(day)))
    cos_lat = math.cos(math.radians(latitude))
    sin_lat = math.sin(math.radians(latitude))
    first_term = cos_lat * cos_dec * cos_ha
    second_term = sin_lat * sin_dec
    return math.degrees(math.asin(first_term + second_term))

def get_apparent_sun_longitude(dt_list):
    """
    docstring goes here
    """
    mgl = get_geocentric_longitude(dt_list)
    dpsi = get_nutation(dt_list)['longitude']
    aberration = get_aberration_correction(dt_list)
    return mgl + dpsi + aberration

def get_azimuth(lat_lon_list, when, elevation=0):# too many local variabels 25/15
    """
    docstring goes here
    """
    # location-dependent calculations
    projected_radial_distance = get_projected_radial_distance(elevation, lat_lon_list[1])
    projected_axial_distance = get_projected_axial_distance(elevation, lat_lon_list[0])

    # time-dependent calculations
    jdn = time.get_julian_solar_day(when)# jd to short
    jde = time.get_julian_ephemeris_day(when)
    jce = time.get_julian_ephemeris_century(jde)
    jme = time.get_julian_ephemeris_millennium(jce)
    geocentric_latitude = get_geocentric_latitude(jme)
    geocentric_longitude = get_geocentric_longitude(jme)
    sun_earth_distance = get_sun_earth_distance(jme)
    aberration_correction = get_aberration_correction(sun_earth_distance)
    equatorial_horizontal_parallax = get_max_horizontal_parallax(sun_earth_distance)
    nutation = get_nutation(jce)
    gast = get_gast(jdn)
    true_ecliptic_obliquity = get_true_ecliptic_obliquity(jme)

    # calculations dependent on location and time
    apparent_sun_longitude = get_apparent_sun_longitude(
        geocentric_longitude, nutation, aberration_correction)# all lines too long now wrapped
    geocentric_sun_right_ascension = get_geocentric_right_ascension(
        apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude)
    geocentric_sun_declination = get_geocentric_sun_declination(
        apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude)
    local_hour_angle = get_local_hour_angle(
        gast, lat_lon_list[1], geocentric_sun_right_ascension)
    parallax_sun_right_ascension = get_parallax_right_ascension(
        projected_radial_distance, equatorial_horizontal_parallax, local_hour_angle,
        geocentric_sun_declination)
    topocentric_local_hour_angle = get_topocentric_lha(
        local_hour_angle, parallax_sun_right_ascension)
    topocentric_sun_declination = get_topocentric_sun_declination(
        geocentric_sun_declination, projected_axial_distance, equatorial_horizontal_parallax,
        parallax_sun_right_ascension, local_hour_angle)
    return 180 - get_topocentric_azimuth_angle(
        topocentric_local_hour_angle, lat_lon_list[0], topocentric_sun_declination)

def get_azimuth_fast(latitude_deg, longitude_deg, when):
    """
    docstring goes here
    """
# expect -50 degrees for solar.get_azimuth(
#     42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 18, 0, 0))
    day = when.utctimetuple().tm_yday
    declination_rad = math.radians(get_declination(day))
    latitude_rad = math.radians(latitude_deg)
    hour_angle_rad = math.radians(get_hour_angle(when, longitude_deg))
    altitude_rad = math.radians(get_altitude(latitude_deg, longitude_deg, when))

    azimuth_rad = math.asin(
        math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))

    if (
            math.cos(
                hour_angle_rad) >= (
                    math.tan(declination_rad) / math.tan(latitude_rad))):
        return math.degrees(azimuth_rad)
    else:
        return 180 - math.degrees(azimuth_rad)

def get_coeff(dt_list, coeffs):
    """
    computes a polynomial with time-varying coefficients from the given constant
    coefficients array and the current Julian millennium.
    """
    jem = time.get_julian_ephemeris_millennium(dt_list)
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

def get_equation_of_equinox(dt_list):
    """
    doc
    """
    delta_psi = get_nutation(dt_list)['longitude']
    epsilon = get_true_ecliptic_obliquity(dt_list)
    cos_eps = math.cos(math.radians(epsilon))
    return delta_psi * cos_eps

def get_flattened_latitude(latitude):
    """
    docstring goes here
    """
    latitude_rad = math.radians(latitude)
    return math.degrees(math.atan(0.99664719 * math.tan(latitude_rad)))

def get_gmst(dt_list):
    """
    docstring goes here
    """
    # print(dt_list)
    # This function doesn't agree with Andreas and Reda as well as it should.
    # Works to ~5 sig figs in current unit test
    jct = time.get_julian_century(dt_list)
    jdn = jct * 36525.0
    day_deg = (360.9856473659 * jdn) # 360.98564736629 is old and this is not SOFA
    mean_st = ((jct / 38710000.0) * jct + 0.000387933) * jct + 280.46061837 + day_deg
    return mean_st % 360

def get_gast(dt_list):
    """
    docstring goes here
    """
    gmst = get_gmst(dt_list)
    eqeq = get_equation_of_equinox(dt_list)
    return gmst + eqeq

def get_lmst(dt_list):
    """
    docstring goes here
    """
    return None

def get_last(dt_list):
    """
    docstring goes here
    """
    return None

# Geocentric functions calculate angles relative to the center of the earth.

def get_geocentric_latitude(dt_list):
    """
    docstring goes here
    """
    return -1 * get_heliocentric_latitude(dt_list)

def get_geocentric_longitude(dt_list):
    """
    docstring goes here
    """
    return (get_heliocentric_longitude(dt_list) + 180) % 360

def get_geocentric_sun_declination(dt_list):
    """
    docstring goes here
    """
    apparent_sun_longitude = get_apparent_sun_longitude(dt_list)
    true_ecliptic_obliquity = get_true_ecliptic_obliquity(dt_list)
    geocentric_latitude = get_geocentric_latitude(dt_list)
    sin_apparent_sun_longitude = math.sin(math.radians(apparent_sun_longitude))
    sin_true_ecliptic_obliquity = math.sin(math.radians(true_ecliptic_obliquity))
    cos_true_ecliptic_obliquity = math.cos(math.radians(true_ecliptic_obliquity))
    sin_geocentric_latitude = math.sin(math.radians(geocentric_latitude))
    cos_geocentric_latitude = math.cos(math.radians(geocentric_latitude))
    adec = sin_geocentric_latitude * cos_true_ecliptic_obliquity
    bdec = cos_geocentric_latitude * sin_true_ecliptic_obliquity * sin_apparent_sun_longitude
    delta = math.asin(adec + bdec)
    return math.degrees(delta)

def get_geocentric_right_ascension(dt_list):
    """
    docstring goes here
    """
    apparent_sun_longitude = get_apparent_sun_longitude(dt_list)
    true_ecliptic_obliquity = get_true_ecliptic_obliquity(dt_list)
    geocentric_latitude = get_geocentric_latitude(dt_list)
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

def get_heliocentric_latitude(dt_list):
    """
    docstring goes here
    """
    return math.degrees(get_coeff(dt_list, constants.HELIOCENTRIC_LATITUDE_COEFFS) / 1e8)

def get_heliocentric_longitude(dt_list):
    """
    docstring goes here
    """
    return math.degrees(get_coeff(dt_list, constants.HELIOCENTRIC_LONGITUDE_COEFFS) / 1e8) % 360

def get_hour_angle(when, longitude_deg):
    """
    docstring goes here
    """

    solar_time = get_solar_time(longitude_deg, when)
    return 15 * (12 - solar_time)

def get_incidence_angle(
        topocentric_zenith_angle, slope, slope_orientation, topocentric_azimuth_angle):
    """
    docstring goes here
    """
    tza_rad = math.radians(topocentric_zenith_angle)
    slope_rad = math.radians(slope)
    so_rad = math.radians(slope_orientation)
    taa_rad = math.radians(topocentric_azimuth_angle)
    return math.degrees(
        math.acos(
            math.cos(
                tza_rad) * math.cos(
                    slope_rad) + math.sin(
                        slope_rad) * math.sin(tza_rad) * math.cos(taa_rad - math.pi - so_rad)))

def get_local_hour_angle(dt_list, local_longitude):
    """
    Local hour angle
    """
    gast = get_gast(dt_list)
    gra = get_geocentric_right_ascension(dt_list)
    return (gast + local_longitude - gra) % 360

def get_max_horizontal_parallax(dt_list):
    """
    docstring goes here
    """
    sun_earth_distance = get_sun_earth_distance(dt_list)
    return 8.794 / (3600 / sun_earth_distance)

def get_nutation(dt_list):
    """
    docstring goes here
    """
    jec = time.get_julian_ephemeris_century(dt_list)
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

def get_parallax_right_ascension(
        projected_radial_distance, equatorial_horizontal_parallax,
        local_hour_angle, geocentric_sun_declination):
    """
    docstring goes here
    """
    prd = projected_radial_distance
    ehp_rad = math.radians(equatorial_horizontal_parallax)
    lha_rad = math.radians(local_hour_angle)
    gsd_rad = math.radians(geocentric_sun_declination)
    ara = -1 * prd * math.sin(ehp_rad) * math.sin(lha_rad)
    bra = math.cos(gsd_rad) - prd * math.sin(ehp_rad) * math.cos(lha_rad)
    parallax = math.atan2(ara, bra)
    return math.degrees(parallax)

def get_projected_radial_distance(elevation, latitude):
    """
    docstring goes here
    """
    flattened_latitude_rad = math.radians(get_flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return math.cos(
        flattened_latitude_rad) + (elevation * math.cos(latitude_rad) / constants.EARTH_RADIUS)

def get_projected_axial_distance(elevation, latitude):
    """
    docstring goes here
    """
    flattened_latitude_rad = math.radians(get_flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return 0.99664719 * math.sin(
        flattened_latitude_rad) + (elevation * math.sin(latitude_rad) / constants.EARTH_RADIUS)

def get_refraction_correction(pressure, temperature, topocentric_elevation_angle):
    """
    docstring goes here
    """
    #function and default values according to original NREL SPA C code
    #http://www.nrel.gov/midc/spa/

    sun_radius = 0.26667
    atmos_refract = 0.5667
    del_e = 0.0
    tea = topocentric_elevation_angle

    # Approximation only valid if sun is not well below horizon
    # This approximation could be improved;
    # see history at https://github.com/pingswept/pysolar/pull/23
    # Better method could come from Auer and Standish [2000]:
    # http://iopscience.iop.org/1538-3881/119/5/2472/pdf/1538-3881_119_5_2472.pdf

    if tea >= -1.0*(sun_radius + atmos_refract):
        arc = pressure * 2.830 * 1.02
        brc = 1010.0 * temperature * 60.0 * math.tan(math.radians(tea + (10.3/(tea + 5.11))))
        del_e = arc / brc

    return del_e

def get_solar_time(longitude_deg, when):
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

def get_sun_earth_distance(dt_list):
    """
    docstring goes here
    """
    return get_coeff(dt_list, constants.AU_DISTANCE_COEFFS) / 1e8

# Topocentric functions calculate angles relative to a location on the surface of the earth.

def get_topocentric_azimuth_angle(
        topocentric_lha, latitude, topocentric_declination):
    """
    Measured eastward from north
    """
    cos_tlha = math.cos(math.radians(topocentric_lha))
    sin_tlha = math.sin(math.radians(topocentric_lha))
    latitude_rad = math.radians(latitude)
    tsd_rad = math.radians(topocentric_declination)
    ayt = sin_tlha
    bxt = cos_tlha * math.sin(latitude_rad) - math.tan(tsd_rad) * math.cos(latitude_rad)
    return 180.0 + math.degrees(math.atan2(ayt, bxt)) % 360

def get_topocentric_elevation_angle(
        latitude, topocentric_sun_declination, topocentric_local_hour_angle):
    """
    docstring goes here
    """
    latitude_rad = math.radians(latitude)
    tsd_rad = math.radians(topocentric_sun_declination)
    tlha_rad = math.radians(topocentric_local_hour_angle)
    return math.degrees(
        math.asin(
            (math.sin(
                latitude_rad) * math.sin(
                    tsd_rad)) + math.cos(
                        latitude_rad) * math.cos(tsd_rad) * math.cos(tlha_rad)))# too long

def get_topocentric_lha(local_hour_angle, parallax_sun_right_ascension):
    """
    docstring goes here
    """
    return local_hour_angle - parallax_sun_right_ascension

def get_topocentric_sun_declination(
        geocentric_sun_declination, projected_axial_distance, equatorial_horizontal_parallax,
        parallax_sun_right_ascension, local_hour_angle):
    """
    docstring goes here
    """
    gsd_rad = math.radians(geocentric_sun_declination)
    pad = projected_axial_distance
    ehp_rad = math.radians(equatorial_horizontal_parallax)
    psra_rad = math.radians(parallax_sun_right_ascension)
    lha_rad = math.radians(local_hour_angle)
    ayt = (math.sin(gsd_rad) - pad * math.sin(ehp_rad)) * math.cos(psra_rad)
    bxt = math.cos(gsd_rad) - (pad * math.sin(ehp_rad) * math.cos(lha_rad))
    return math.degrees(math.atan2(ayt, bxt))

def get_topocentric_right_ascension(
        projected_radial_distance, max_horizontal_parallax, lha,
        apparent_longitude, ecliptic_obliquity, geocentric_latitude): # to many arguments 6/5
    """
    docstring goes here
    """
    gsd = get_geocentric_sun_declination(
        apparent_longitude, ecliptic_obliquity, geocentric_latitude)
    psra = get_parallax_right_ascension(
        projected_radial_distance, max_horizontal_parallax, lha, gsd)
    gsra = get_geocentric_right_ascension(
        apparent_longitude, ecliptic_obliquity, geocentric_latitude)
    return psra + gsra

def get_topocentric_zenith_angle(
        latitude, topocentric_sun_declination, topocentric_local_hour_angle, pressure, temperature):
    """
    docstring goes here
    """
    tea = get_topocentric_elevation_angle(
        latitude, topocentric_sun_declination, topocentric_local_hour_angle)
    return 90 - tea - get_refraction_correction(pressure, temperature, tea)

def get_true_ecliptic_obliquity(dt_list):
    """
    docstring goes here
    """
    delta_eps = get_nutation(dt_list)['obliquity']
    tmu = time.get_julian_ephemeris_century(dt_list)
    mean_eps = 84381.448 - (4680.93 * tmu) - (1.55 * tmu ** 2) + (1999.25 * tmu ** 3) \
    - (51.38 * tmu ** 4) -(249.67 * tmu ** 5) - (39.05 * tmu ** 6) + (7.12 * tmu ** 7) \
    + (27.87 * tmu ** 8) + (5.79 * tmu ** 9) + (2.45 * tmu ** 10)
    return (mean_eps / 3600.0) + delta_eps
