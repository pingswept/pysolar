
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


import math
import datetime
from . import constants
from . import time
from . import radiation

def solar_test():
    """ test """
    latitude_deg = 42.364908
    longitude_deg = -71.112828
    DTNOW = datetime.datetime.utcnow()
    thirty_minutes = datetime.timedelta(hours=0.5)
    for i in range(48):
        timestamp = DTNOW.ctime()
        altitude_deg = altitude(latitude_deg, longitude_deg, DTNOW)
        azimuth_deg = azimuth(latitude_deg, longitude_deg, DTNOW)
        power = radiation.get_radiation_direct(DTNOW, altitude_deg)
        if altitude_deg > 0:
            print(timestamp, "UTC", altitude_deg, azimuth_deg, power)
        DTNOW = DTNOW + thirty_minutes

def equation_of_time(day):
    "returns the number of minutes to add to mean solar time to get actual solar time."
    return 9.87 * \
      math.sin(2 * 2 * math.pi / 364.0 * (day - 81)) - \
      7.53 * math.cos(2 * math.pi / 364.0 * (day - 81)) - \
      1.5 * math.sin(2 * math.pi / 364.0 * (day - 81))

def aberration_correction(distance):
    """ sun-earth distance is in astronomical units """
    return -20.4898 / (3600.0 * distance)

def apparent_sidereal_time(ajd, jme, nut):
    """ true sidereal time """
    return mean_sidereal_time(ajd) + \
      nut['longitude'] * \
      math.cos(true_ecliptic_obliquity(jme, nut))

def apparent_longitude(geocentric_lon, nut, ab_correction):
    """ ____ """
    return geocentric_lon + nut['longitude'] + ab_correction

def get_azimuth_fast(latitude_deg, longitude_deg, when):
    """ expect -50 degrees for
    solar.azimuth(42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 18, 0, 0)) """
    day = when.utctimetuple().tm_yday
    declination_rad = math.radians(declination(day))
    latitude_rad = math.radians(latitude_deg)
    hour_angle_rad = math.radians(hour_angle(when, longitude_deg))
    altitude_rad = math.radians(altitude(latitude_deg, longitude_deg, when))

    azimuth_rad = \
      math.asin(math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))

    if math.cos(hour_angle_rad) >= (math.tan(declination_rad) / math.tan(latitude_rad)):
        return math.degrees(azimuth_rad)
    else:
        return 180 - math.degrees(azimuth_rad)

def coeff(jem, coeffs):
    "computes a polynomial with time-varying coefficients from the given constant" \
    " coefficients array and the current Julian millennium."
    result = 0.0
    x = 1.0
    for line in coeffs:
        c = 0.0
        for l in line:
            c += l[0] * math.cos(l[1] + l[2] * jem)
        #end for
        result += c * x
        x *= jem
    #end for
    return result
#end coeff

def declination(day):
    '''The declination of the sun is the angle between
    Earth's equatorial plane and a line between the Earth and the sun.
    The declination of the sun varies between 23.45 degrees and -23.45 degrees,
    hitting zero on the equinoxes and peaking on the solstices.
    '''
    return constants.EARTH_AXIS_INCLINATION * math.sin((2 * math.pi / 365.0) * (day - 81))

def equatorial_horizontal_parallax(sun_earth_distance):
    return 8.794 / (3600 / sun_earth_distance)

def flattened_latitude(latitude):
    latitude_rad = math.radians(latitude)
    return math.degrees(math.atan(0.99664719 * math.tan(latitude_rad)))

# Geocentric functions calculate angles relative to the center of the earth.

def geocentric_latitude(jme):
    return -1 * heliocentric_latitude(jme)

def geocentric_longitude(jme):
    return (heliocentric_longitude(jme) + 180) % 360

def geocentric_declination(apparent_sun_longitude,
                           true_ecliptic_obliquity,
                           geocentric_latitude):
    apparent_sun_longitude_rad = math.radians(apparent_sun_longitude)
    true_ecliptic_obliquity_rad = math.radians(true_ecliptic_obliquity)
    geocentric_latitude_rad = math.radians(geocentric_latitude)

    a = \
      math.sin(geocentric_latitude_rad) * math.cos(true_ecliptic_obliquity_rad)
    b = \
      math.cos(geocentric_latitude_rad) * \
      math.sin(true_ecliptic_obliquity_rad) * \
      math.sin(apparent_sun_longitude_rad)
    delta = math.asin(a + b)
    return math.degrees(delta)

def geocentric_right_ascension(apparent_sun_longitude,
                               true_ecliptic_obliquity,
                               geocentric_latitude):
    apparent_sun_longitude_rad = math.radians(apparent_sun_longitude)
    true_ecliptic_obliquity_rad = math.radians(true_ecliptic_obliquity)
    geocentric_latitude_rad = math.radians(geocentric_latitude)

    a = math.sin(apparent_sun_longitude_rad) * math.cos(true_ecliptic_obliquity_rad)
    b = math.tan(geocentric_latitude_rad) * math.sin(true_ecliptic_obliquity_rad)
    c = math.cos(apparent_sun_longitude_rad)
    alpha = math.atan2((a - b), c)
    return math.degrees(alpha) % 360

# Heliocentric functions calculate angles relative to the center of the sun.

def heliocentric_latitude(jme):
    return math.degrees(coeff(jme, constants.heliocentric_latitude_coeffs) / 1e8)

def heliocentric_longitude(jme):
    return math.degrees(coeff(jme, constants.heliocentric_longitude_coeffs) / 1e8) % 360

def incidence_angle(topocentric_zenith_angle,
                    slope,
                    slope_orientation,
                    topocentric_azimuth_angle):
    tza_rad = math.radians(topocentric_zenith_angle)
    slope_rad = math.radians(slope)
    so_rad = math.radians(slope_orientation)
    taa_rad = math.radians(topocentric_azimuth_angle)
    return math.degrees(math.acos(math.cos(tza_rad) * math.cos(slope_rad) +
                                  math.sin(slope_rad) * math.sin(tza_rad) *
                                  math.cos(taa_rad - math.pi - so_rad)))

def altitude_fast(latitude_deg, longitude_deg, when):
    """ expect 19 degrees for
    solar.altitude(42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 13, 1, 130320)) """
    day = when.utctimetuple().tm_yday
    declination_rad = math.radians(declination(day))
    latitude_rad = math.radians(latitude_deg)
    hour_angle = hour_angle(when, longitude_deg)
    first_term = \
      math.cos(latitude_rad) * \
      math.cos(declination_rad) * \
      math.cos(math.radians(hour_angle))
    second_term = math.sin(latitude_rad) * math.sin(declination_rad)
    return math.degrees(math.asin(first_term + second_term))

def local_hour_angle(apparent_sidereal_time, longitude, geocentric_right_ascension):
    return (apparent_sidereal_time + longitude - geocentric_right_ascension) % 360

def mean_sidereal_time(jd):
    """ This function doesn't agree with Andreas and Reda as well as it should. """
    """ Works to ~5 sig figs in current unit test """

    jc = time.julian_century(jd)
    GMST0 = 280.46061837 + \
        (360.98564736629 * (jd - 2451545.0)) + 0.000387933 * jc * jc * (1 - jc / 38710000)
    return GMST0 % 360

def nutation(jce):
    abcd = constants.nutation_coefficients
    nutation_long = []
    nutation_oblique = []
    p = constants.get_aberration_coeffs()
    x = list \
      ( \
          p[k](jce)
          # order is important
          for k in ( \
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
    return {'longitude': sum(nutation_long) / 36000000.0,
            'obliquity': sum(nutation_oblique) / 36000000.0}
#end get_nutation

def ra_parallax(projected_radial_distance,
                equatorial_horizontal_parallax,
                local_hour_angle,
                geocentric_declination):
    prd = projected_radial_distance
    ehp_rad = math.radians(equatorial_horizontal_parallax)
    lha_rad = math.radians(local_hour_angle)
    gsd_rad = math.radians(geocentric_declination)
    parallax = math.atan2( \
      -1 * prd * math.sin(ehp_rad) * math.sin(lha_rad), \
    math.cos(gsd_rad) - prd * math.sin(ehp_rad) * math.cos(lha_rad))
    return math.degrees(parallax)

def projected_radial_distance(elevation, latitude):
    flattened_latitude_rad = math.radians(flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return math.cos(flattened_latitude_rad) + \
        (elevation * math.cos(latitude_rad) / constants.EARTH_RADIUS)

def projected_axial_distance(elevation, latitude):
    flattened_latitude_rad = math.radians(flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return 0.99664719 * math.sin(flattened_latitude_rad) + \
        (elevation * math.sin(latitude_rad) / constants.EARTH_RADIUS)

def sun_earth_distance(jme):
    """ ____ """
    return coeff(jme, constants.SUN_EARTH_DISTANCE_COEFFS) / 1e8

def refraction_correction(pressure, temperature, topo_elevation_angle):
    """ ____ """
    #function and default values according to original NREL SPA C code
    #http://www.nrel.gov/midc/spa/

    sun_radius = 0.26667
    atmos_refract = 0.5667
    del_e = 0.0
    tea = topo_elevation_angle

    # Approximation only valid if sun is not well below horizon
    # This approximation could be improved;
    # see history at https://github.com/pingswept/pysolar/pull/23
    # Better method could come from Auer and Standish [2000]:
    # http://iopscience.iop.org/1538-3881/119/5/2472/pdf/1538-3881_119_5_2472.pdf

    if tea >= -1.0 * (sun_radius + atmos_refract):
        del_e = \
          pressure * 2.830 * 1.02 / \
          1010.0 * temperature * 60.0 * math.tan(math.radians(tea + (10.3 / (tea + 5.11))))

    return del_e

def solar_time(longitude_deg, when):
    "returns solar time in hours for the specified longitude and time," \
    " accurate only to the nearest minute."
    when = when.utctimetuple()
    return \
        (
            (when.tm_hour * 60 + when.tm_min + 4 * longitude_deg + equation_of_time(when.tm_yday))
            /
            60
        )
# Topocentric functions calculate angles relative to a location on the surface of the earth.

def hour_angle(when, longitude_deg):
    """ ____ """
    return 15 * (12 - solar_time(longitude_deg, when))


def topocentric_azimuth_angle(topo_local_hour_angle, lat, topo_declination):
    """Measured eastward from north"""
    tlha_rad = math.radians(topo_local_hour_angle)
    lat_rad = math.radians(lat)
    tsd_rad = math.radians(topo_declination)
    return 180.0 + math.degrees(math.atan2( \
      math.sin(tlha_rad), \
      math.cos(tlha_rad) * math.sin(lat_rad) - math.tan(tsd_rad) * math.cos(lat_rad)
                                          ) % 360

def topocentric_elevation_angle(lat, topo_declination, topo_local_hour_angle):
    sin_lat = math.sin(math.radians(lat))
    cos_lat = math.cos(math.radians(lat))
    sin_dec = math.sin(math.radians(topo_declination))
    cos_dec = math.cos(math.radians(topo_declination))
    cos_lha = math.cos(math.radians(topo_local_hour_angle))
    return math.degrees(math.asin(sin_lat * sin_dec + cos_lat * cos_dec * cos_lha))

def topocentric_local_hour_angle(local_hour_angle, parallax_sun_right_ascension):
    return local_hour_angle - parallax_sun_right_ascension

def topocentric_sun_declination(geocentric_declination,
                                projected_axial_distance, equatorial_horizontal_parallax,
                                parallax_sun_right_ascension, local_hour_angle):
    gsd_rad = math.radians(geocentric_sun_declination)
    pad = projected_axial_distance
    ehp_rad = math.radians(equatorial_horizontal_parallax)
    psra_rad = math.radians(parallax_sun_right_ascension)
    lha_rad = math.radians(local_hour_angle)
    a = (math.sin(gsd_rad) - pad * math.sin(ehp_rad)) * math.cos(psra_rad)
    b = math.cos(gsd_rad) - (pad * math.sin(ehp_rad) * math.cos(lha_rad))
    return math.degrees(math.atan2(a, b))

def topocentric_sun_right_ascension(projected_radial_distance,
                                    equatorial_horizontal_parallax, local_hour_angle,
                                    apparent_longitude, true_ecliptic_obliquity,
                                    geocentric_latitude):
    gsd = geocentric_sun_declination(apparent_longitude,
                                     true_ecliptic_obliquity,
                                     geocentric_latitude)
    psra = ra_parallax(projected_radial_distance,
                       equatorial_horizontal_parallax,
                       local_hour_angle, gsd)
    gsra = geocentric_right_ascension(apparent_sun_longitude,
                                      true_ecliptic_obliquity,
                                      geocentric_latitude)
    return psra + gsra

def topocentric_zenith_angle(latitude,
                             topo_declination,
                             topo_local_hour_angle,
                             pressure, temperature):
    tea = topocentric_elevation_angle(latitude,
                                      topo_declination,
                                      topo_local_hour_angle)
    return 90 - tea - refraction_correction(pressure, temperature, tea)

def true_ecliptic_obliquity(jme, nutation):
    u = jme/10.0
    mean_obliquity = 84381.448 - (4680.93 * u) - (1.55 * u ** 2) + (1999.25 * u ** 3) \
    - (51.38 * u ** 4) -(249.67 * u ** 5) - (39.05 * u ** 6) + (7.12 * u ** 7) \
    + (27.87 * u ** 8) + (5.79 * u ** 9) + (2.45 * u ** 10)
    return (mean_obliquity / 3600.0) + nutation['obliquity']

def altitude(latitude_deg, longitude_deg, when,
             elevation=0,
             temperature=constants.STANDARD_TEMPERATURE,
             pressure=constants.STANDARD_PRESSURE):
    '''See also the faster, but less accurate, get_altitude_fast()'''
    # location-dependent calculations
    p_radial_distance = projected_radial_distance(elevation, latitude_deg)
    p_axial_distance = projected_axial_distance(elevation, latitude_deg)

    # time-dependent calculations
    jd = time.julian_solar_day(when)
    jde = time.julian_ephemeris_day(when)
    jce = time.julian_ephemeris_century(jde)
    jme = time.julian_ephemeris_millennium(jce)
    geo_latitude = geocentric_latitude(jme)
    geo_longitude = geocentric_longitude(jme)
    sun_earth = sun_earth_distance(jme)
    ab_correction = aberration_correction(sun_earth_distance)
    equatorial_horizontal = equatorial_horizontal_parallax(sun_earth_distance)
    nut = nutation(jce)
    sidereal_time = apparent_sidereal_time(jd, jme, nut)
    true_obliquity = true_ecliptic_obliquity(jme, nut)

    # calculations dependent on location and time
    longitude = apparent_longitude(geocentric_longitude,
                                            nut,
                                            ab_correction)
    geo_right_ascension = geocentric_right_ascension(longitude,
                                                            true_obliquity,
                                                            geo_latitude)
    geo_declination = geocentric_sun_declination(longitude,
                                                            true_obliquity,
                                                            geo_latitude)
    local_hr_angle = local_hour_angle(sidereal_time,
                                      longitude_deg,
                                      geo_right_ascension)
    right_ascension = ra_parallax(p_radial_distance,
                                  equatorial_horizontal,
                                  local_hr_angle,
                                  geo_declination)
    topo_local_hour_angle = topocentric_local_hour_angle(local_hr_angle,
                                                         right_ascension)
    topo_declination = topocentric_sun_declination(geo_declination,
                                                   p_axial_distance,
                                                   equatorial_horizontal,
                                                   right_ascension,
                                                   local_hr_angle)
    topo_elevation_angle = topocentric_elevation_angle(latitude_deg,
                                                       topo_declination,
                                                       topo_local_hour_angle)
    correction = refraction_correction(pressure,
                                                  temperature,
                                                  topo_elevation_angle)
    return topo_elevation_angle + correction

    def azimuth(latitude_deg, longitude_deg, when, elevation=0):
        """ ____ """
    # location-dependent calculations
    p_radial_distance = projected_radial_distance(elevation, latitude_deg)
    p_axial_distance = projected_axial_distance(elevation, latitude_deg)

    # time-dependent calculations
    jsd = time.julian_solar_day(when)
    jed = time.julian_ephemeris_day(when)
    jec = time.julian_ephemeris_century(jed)
    jem = time.julian_ephemeris_millennium(jec)
    geo_latitude = geocentric_latitude(jem)
    geo_longitude = geocentric_longitude(jem)
    sun_earth = sun_earth_distance(lem)
    ab_correction = aberration_correction(sun_earth)
    equatorial_horizontal = equatorial_horizontal_parallax(sun_earth)
    nut = nutation(jce)
    sidereal_time = apparent_sidereal_time(jsd, jem, nut)
    true_obliquity = true_ecliptic_obliquity(jem, nut)

    # calculations dependent on location and time
    sun_longitude = \
      apparent_longitude(geo_longitude,
                         nut,
                         ab_correction)
    geo_right_ascension = \
      geocentric_right_ascension(sun_longitude,
                                 true_obliquity,
                                 geo_latitude)
    geo_declination = \
      geocentric_declination(sun_longitude,
                             true_obliquity,
                             geo_latitude)
    local_hr_angle = \
      local_hour_angle(sidereal_time,
                       longitude_deg,
                       geo_right_ascension)
    right_ascension = \
      ra_parallax(p_radial_distance,
                  equatorial_horizontal,
                  local_hr_angle,
                  geo_declination)
    topo_local_hour_angle = \
      topocentric_local_hour_angle(local_hr_angle,
                                   geo_right_ascension)
    topo_declination = \
      topocentric_sun_declination(geo_declination,
                                  p_axial_distance,
                                  equatorial_horizontal,
                                  geo_right_ascension,
                                  local_hr_angle)
    return 180 - topocentric_azimuth_angle(topo_local_hour_angle,
                                           latitude_deg,
                                           topo_declination)
