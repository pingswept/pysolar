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

"""Solar geometry functions

This module contains the most important functions for calculation of the position of the sun.

"""
from . import numeric as math
import datetime
from . import constants
from . import solartime as stime
from . import radiation
from .tzinfo_check import check_aware_dt


def solar_test():
    latitude_deg = 42.364908
    longitude_deg = -71.112828
    d = datetime.datetime.now(tz=datetime.timezone.utc)
    thirty_minutes = datetime.timedelta(hours = 0.5)
    for _ in range(48):
        timestamp = d.ctime()
        altitude_deg = get_altitude(latitude_deg, longitude_deg, d)
        azimuth_deg = get_azimuth(latitude_deg, longitude_deg, d)
        power = radiation.get_radiation_direct(d, altitude_deg)
        if (altitude_deg > 0):
            print(timestamp, "UTC", altitude_deg, azimuth_deg, power)
        d = d + thirty_minutes


def equation_of_time(day):
    "returns the number of minutes to add to mean solar time to get actual solar time."
    b = 2 * math.pi / 364.0 * (day - 81)
    return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)


def get_aberration_correction(sun_earth_distance):     # sun-earth distance is in astronomical units
    return -20.4898/(3600.0 * sun_earth_distance)


@check_aware_dt('when')
def get_topocentric_position(latitude_deg, longitude_deg, when, elevation = 0):
    '''Common calculations for altitude and azimuth'''
    # location-dependent calculations
    projected_radial_distance = get_projected_radial_distance(elevation, latitude_deg)
    projected_axial_distance = get_projected_axial_distance(elevation, latitude_deg)

    # time-dependent calculations
    jd = stime.get_julian_solar_day(when)
    jde = stime.get_julian_ephemeris_day(when)
    jce = stime.get_julian_ephemeris_century(jde)
    jme = stime.get_julian_ephemeris_millennium(jce)
    geocentric_latitude = get_geocentric_latitude(jme)
    geocentric_longitude = get_geocentric_longitude(jme)
    sun_earth_distance = get_sun_earth_distance(jme)
    aberration_correction = get_aberration_correction(sun_earth_distance)
    equatorial_horizontal_parallax = get_equatorial_horizontal_parallax(sun_earth_distance)
    nutation = get_nutation(jce)
    apparent_sidereal_time = get_apparent_sidereal_time(jd, jme, nutation)
    true_ecliptic_obliquity = get_true_ecliptic_obliquity(jme, nutation)

    # calculations dependent on location and time
    apparent_sun_longitude = get_apparent_sun_longitude(geocentric_longitude, nutation, aberration_correction)
    geocentric_sun_right_ascension = get_geocentric_sun_right_ascension(apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude)
    geocentric_sun_declination = get_geocentric_sun_declination(apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude)
    local_hour_angle = get_local_hour_angle(apparent_sidereal_time, longitude_deg, geocentric_sun_right_ascension)
    parallax_sun_right_ascension = get_parallax_sun_right_ascension(projected_radial_distance, equatorial_horizontal_parallax, local_hour_angle, geocentric_sun_declination)
    topocentric_local_hour_angle = get_topocentric_local_hour_angle(local_hour_angle, parallax_sun_right_ascension)
    topocentric_sun_declination = get_topocentric_sun_declination(geocentric_sun_declination, projected_axial_distance, equatorial_horizontal_parallax, parallax_sun_right_ascension, local_hour_angle)

    return topocentric_sun_declination, topocentric_local_hour_angle


@check_aware_dt('when')
def get_position(latitude_deg, longitude_deg, when, elevation=0,
                 temperature = constants.standard_temperature,
                 pressure = constants.standard_pressure):
    ''' Given location, time and atmospheric conditions
    returns (azimuth, altitude) of sun in degrees.

    Same as a combination of get_azimuth and get_altitude
    '''

    topocentric_sun_declination, topocentric_local_hour_angle = \
        get_topocentric_position(latitude_deg, longitude_deg, when, elevation)

    topocentric_elevation_angle = \
        get_topocentric_elevation_angle(latitude_deg, topocentric_sun_declination,
                                        topocentric_local_hour_angle)

    refraction_correction = get_refraction_correction(pressure, temperature,
                                                      topocentric_elevation_angle)

    altitude_deg = topocentric_elevation_angle + refraction_correction

    azimuth_deg = get_topocentric_azimuth_angle(topocentric_local_hour_angle,
                                      latitude_deg, topocentric_sun_declination)

    return azimuth_deg, altitude_deg


@check_aware_dt('when')
def get_altitude(latitude_deg, longitude_deg, when, elevation = 0,
                 temperature = constants.standard_temperature, pressure = constants.standard_pressure):
    '''See also the faster, but less accurate, get_altitude_fast()'''
    topocentric_sun_declination, topocentric_local_hour_angle = \
        get_topocentric_position(latitude_deg, longitude_deg, when)

    topocentric_elevation_angle = get_topocentric_elevation_angle(latitude_deg, topocentric_sun_declination, topocentric_local_hour_angle)
    refraction_correction = get_refraction_correction(pressure, temperature, topocentric_elevation_angle)
    return topocentric_elevation_angle + refraction_correction


@check_aware_dt('when')
def get_altitude_fast(latitude_deg, longitude_deg, when):
# expect 19 degrees for solar.get_altitude(42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 13, 1, 130320))
    day = math.tm_yday(when)
    declination_rad = math.radians(get_declination(day))
    latitude_rad = math.radians(latitude_deg)
    hour_angle = get_hour_angle(when, longitude_deg)
    first_term = math.cos(latitude_rad) * math.cos(declination_rad) * math.cos(math.radians(hour_angle))
    second_term = math.sin(latitude_rad) * math.sin(declination_rad)
    return math.degrees(math.asin(first_term + second_term))


def get_apparent_sidereal_time(jd, jme, nutation):
    return get_mean_sidereal_time(jd) + nutation['longitude'] * math.cos(get_true_ecliptic_obliquity(jme, nutation))


def get_apparent_sun_longitude(geocentric_longitude, nutation, ab_correction):
    return geocentric_longitude + nutation['longitude'] + ab_correction


@check_aware_dt('when')
def get_azimuth(latitude_deg, longitude_deg, when, elevation = 0):

    topocentric_sun_declination, topocentric_local_hour_angle = \
        get_topocentric_position(latitude_deg, longitude_deg, when, elevation)

    azimuth = get_topocentric_azimuth_angle(topocentric_local_hour_angle,
            latitude_deg, topocentric_sun_declination)

    return azimuth


def get_azimuth_fast(latitude_deg, longitude_deg, when):
# expect 230 degrees for solar.get_azimuth(42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 18, 0, 0))
    day = math.tm_yday(when)
    declination_rad = math.radians(get_declination(day))
    latitude_rad = math.radians(latitude_deg)
    hour_angle_rad = math.radians(get_hour_angle(when, longitude_deg))
    altitude_rad = math.radians(get_altitude_fast(latitude_deg, longitude_deg, when))

    azimuth_rad = math.asin(-math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))

    return math.where(math.cos(hour_angle_rad) * math.tan(latitude_rad) >= math.tan(declination_rad),
                      (180 - math.degrees(azimuth_rad)),
                      math.degrees(azimuth_rad) + 360 * (azimuth_rad < 0)
                     )

def get_coeff(jme, coeffs):
    "computes a polynomial with time-varying coefficients from the given constant" \
    " coefficients array and the current Julian millennium."
    result = 0.0
    x = 1.0
    for line in coeffs :
        c = 0.0
        for l in line :
            c += l[0] * math.cos(l[1] + l[2] * jme)
        #end for
        result += c * x
        x *= jme
    #end for
    return \
        result
#end get_coeff

def get_declination(day):
    '''The declination of the sun is the angle between
    Earth's equatorial plane and a line between the Earth and the sun.
    The declination of the sun varies between 23.45 degrees and -23.45 degrees,
    hitting zero on the equinoxes and peaking on the solstices.
    '''
    return constants.earth_axis_inclination * math.sin((2 * math.pi / 365.0) * (day - 81))

def get_equatorial_horizontal_parallax(sun_earth_distance):
    return 8.794 / (3600 / sun_earth_distance)

def get_flattened_latitude(latitude):
    latitude_rad = math.radians(latitude)
    return math.degrees(math.atan(0.99664719 * math.tan(latitude_rad)))

# Geocentric functions calculate angles relative to the center of the earth.

def get_geocentric_latitude(jme):
    return -1 * get_heliocentric_latitude(jme)

def get_geocentric_longitude(jme):
    return (get_heliocentric_longitude(jme) + 180) % 360

def get_geocentric_sun_declination(apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude):
    apparent_sun_longitude_rad = math.radians(apparent_sun_longitude)
    true_ecliptic_obliquity_rad = math.radians(true_ecliptic_obliquity)
    geocentric_latitude_rad = math.radians(geocentric_latitude)

    a = math.sin(geocentric_latitude_rad) * math.cos(true_ecliptic_obliquity_rad)
    b = math.cos(geocentric_latitude_rad) * math.sin(true_ecliptic_obliquity_rad) * math.sin(apparent_sun_longitude_rad)
    delta = math.asin(a + b)
    return math.degrees(delta)

def get_geocentric_sun_right_ascension(apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude):
    apparent_sun_longitude_rad = math.radians(apparent_sun_longitude)
    true_ecliptic_obliquity_rad = math.radians(true_ecliptic_obliquity)
    geocentric_latitude_rad = math.radians(geocentric_latitude)

    a = math.sin(apparent_sun_longitude_rad) * math.cos(true_ecliptic_obliquity_rad)
    b = math.tan(geocentric_latitude_rad) * math.sin(true_ecliptic_obliquity_rad)
    c = math.cos(apparent_sun_longitude_rad)
    alpha = math.atan2((a - b),  c)
    return math.degrees(alpha) % 360

# Heliocentric functions calculate angles relative to the center of the sun.

def get_heliocentric_latitude(jme):
    return math.degrees(get_coeff(jme, constants.heliocentric_latitude_coeffs) / 1e8)

def get_heliocentric_longitude(jme):
    return math.degrees(get_coeff(jme, constants.heliocentric_longitude_coeffs) / 1e8) % 360

@check_aware_dt('when')
def get_hour_angle(when, longitude_deg):
    solar_time = get_solar_time(longitude_deg, when)
    return 15.0 * (solar_time - 12.0)

def get_incidence_angle(topocentric_zenith_angle, slope, slope_orientation, topocentric_azimuth_angle):
    tza_rad = math.radians(topocentric_zenith_angle)
    slope_rad = math.radians(slope)
    so_rad = math.radians(slope_orientation)
    taa_rad = math.radians(topocentric_azimuth_angle)
    return math.degrees(math.acos(math.cos(tza_rad) * math.cos(slope_rad) + math.sin(slope_rad) * math.sin(tza_rad) * math.cos(taa_rad - math.pi - so_rad)))

def get_local_hour_angle(apparent_sidereal_time, longitude, geocentric_sun_right_ascension):
    return (apparent_sidereal_time + longitude - geocentric_sun_right_ascension) % 360

def get_mean_sidereal_time(jd):
    # This function doesn't agree with Andreas and Reda as well as it should. Works to ~5 sig figs in current unit test
    jc = stime.get_julian_century(jd)
    sidereal_time =  280.46061837 + (360.98564736629 * (jd - 2451545.0)) + 0.000387933 * jc * jc * (1 - jc / 38710000)
    return sidereal_time % 360

def get_nutation(jce):
    abcd = constants.nutation_coefficients
    nutation_long = []
    nutation_oblique = []
    p = constants.get_aberration_coeffs()
    x = list \
      (
        p[k](jce)
        for k in
            ( # order is important
                'MeanElongationOfMoon',
                'MeanAnomalyOfSun',
                'MeanAnomalyOfMoon',
                'ArgumentOfLatitudeOfMoon',
                'LongitudeOfAscendingNode',
            )
      )
    y = constants.aberration_sin_terms
    for i in range(len(abcd)):
        sigmaxy = 0.0
        for j in range(len(x)):
            sigmaxy += x[j] * y[i][j]
        #end for
        nutation_long.append((abcd[i][0] + (abcd[i][1] * jce)) * math.sin(math.radians(sigmaxy)))
        nutation_oblique.append((abcd[i][2] + (abcd[i][3] * jce)) * math.cos(math.radians(sigmaxy)))

    # 36000000 scales from 0.0001 arcseconds to degrees
    nutation = {'longitude' : sum(nutation_long)/36000000.0, 'obliquity' : sum(nutation_oblique)/36000000.0}

    return nutation
#end get_nutation

def get_parallax_sun_right_ascension(projected_radial_distance, equatorial_horizontal_parallax, local_hour_angle, geocentric_sun_declination):
    prd = projected_radial_distance
    ehp_rad = math.radians(equatorial_horizontal_parallax)
    lha_rad = math.radians(local_hour_angle)
    gsd_rad = math.radians(geocentric_sun_declination)
    a = -1 * prd * math.sin(ehp_rad) * math.sin(lha_rad)
    b =  math.cos(gsd_rad) - prd * math.sin(ehp_rad) * math.cos(lha_rad)
    parallax = math.atan2(a, b)
    return math.degrees(parallax)

def get_projected_radial_distance(elevation, latitude):
    flattened_latitude_rad = math.radians(get_flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return math.cos(flattened_latitude_rad) + (elevation * math.cos(latitude_rad) / constants.earth_radius)

def get_projected_axial_distance(elevation, latitude):
    flattened_latitude_rad = math.radians(get_flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return 0.99664719 * math.sin(flattened_latitude_rad) + (elevation * math.sin(latitude_rad) / constants.earth_radius)

def get_sun_earth_distance(jme):
    return get_coeff(jme, constants.sun_earth_distance_coeffs) / 1e8

def get_refraction_correction(pressure, temperature, topocentric_elevation_angle):
    #function and default values according to original NREL SPA C code
    #http://www.nrel.gov/midc/spa/

    sun_radius = 0.26667
    atmos_refract = 0.5667
    tea = topocentric_elevation_angle

    # Approximation only valid if sun is not well below horizon
    # This approximation could be improved; see history at https://github.com/pingswept/pysolar/pull/23
    # Better method could come from Auer and Standish [2000]:
    # http://iopscience.iop.org/1538-3881/119/5/2472/pdf/1538-3881_119_5_2472.pdf

    a = pressure * 2.830 * 1.02
    b = 1010.0 * temperature * 60.0 * math.tan(math.radians(tea + (10.3/(tea + 5.11))))

    del_e = math.where(tea >= -1.0*(sun_radius + atmos_refract),
                       a / b, 0.)

    return del_e

@check_aware_dt('when')
def get_solar_time(longitude_deg, when):
    "returns solar time in hours for the specified longitude and time," \
    " accurate only to the nearest minute."
    return \
        (
            (math.tm_hour(when) * 60 + math.tm_min(when) + 4 * longitude_deg + equation_of_time(math.tm_yday(when)))
        /
            60
        )

# Topocentric functions calculate angles relative to a location on the surface of the earth.

def get_topocentric_azimuth_angle(topocentric_local_hour_angle, latitude, topocentric_sun_declination):
    """West is negative, East is positive, Masters p. 395"""
    tlha_rad = math.radians(topocentric_local_hour_angle)
    latitude_rad = math.radians(latitude)
    tsd_rad = math.radians(topocentric_sun_declination)
    a = math.sin(tlha_rad)
    b = math.cos(tlha_rad) * math.sin(latitude_rad) - math.tan(tsd_rad) * math.cos(latitude_rad)
    return (180.0 + math.degrees(math.atan2(a, b))) % 360

def get_topocentric_elevation_angle(latitude, topocentric_sun_declination, topocentric_local_hour_angle):
    latitude_rad = math.radians(latitude)
    tsd_rad = math.radians(topocentric_sun_declination)
    tlha_rad = math.radians(topocentric_local_hour_angle)
    return math.degrees(math.asin((math.sin(latitude_rad) * math.sin(tsd_rad)) + math.cos(latitude_rad) * math.cos(tsd_rad) * math.cos(tlha_rad)))

def get_topocentric_local_hour_angle(local_hour_angle, parallax_sun_right_ascension):
    return local_hour_angle - parallax_sun_right_ascension

def get_topocentric_sun_declination(geocentric_sun_declination, projected_axial_distance, equatorial_horizontal_parallax, parallax_sun_right_ascension, local_hour_angle):
    gsd_rad = math.radians(geocentric_sun_declination)
    pad = projected_axial_distance
    ehp_rad = math.radians(equatorial_horizontal_parallax)
    psra_rad = math.radians(parallax_sun_right_ascension)
    lha_rad = math.radians(local_hour_angle)
    a = (math.sin(gsd_rad) - pad * math.sin(ehp_rad)) * math.cos(psra_rad)
    b = math.cos(gsd_rad) - (pad * math.sin(ehp_rad) * math.cos(lha_rad))
    return math.degrees(math.atan2(a, b))

def get_topocentric_sun_right_ascension(projected_radial_distance, equatorial_horizontal_parallax, local_hour_angle,
        apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude):
    gsd = get_geocentric_sun_declination(apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude)
    psra = get_parallax_sun_right_ascension(projected_radial_distance, equatorial_horizontal_parallax, local_hour_angle, gsd)
    gsra = get_geocentric_sun_right_ascension(apparent_sun_longitude, true_ecliptic_obliquity, geocentric_latitude)
    return psra + gsra

def get_topocentric_zenith_angle(latitude, topocentric_sun_declination, topocentric_local_hour_angle, pressure, temperature):
    tea = get_topocentric_elevation_angle(latitude, topocentric_sun_declination, topocentric_local_hour_angle)
    return 90 - tea - get_refraction_correction(pressure, temperature, tea)

def get_true_ecliptic_obliquity(jme, nutation):
    u = jme/10.0
    mean_obliquity = 84381.448 - (4680.93 * u) - (1.55 * u ** 2) + (1999.25 * u ** 3) \
    - (51.38 * u ** 4) -(249.67 * u ** 5) - (39.05 * u ** 6) + (7.12 * u ** 7) \
    + (27.87 * u ** 8) + (5.79 * u ** 9) + (2.45 * u ** 10)
    return (mean_obliquity / 3600.0) + nutation['obliquity']
