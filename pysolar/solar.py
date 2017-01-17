
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
    when = datetime.datetime.utcnow()
    thirty_minutes = datetime.timedelta(hours=0.5)
    for idx in range(48):
        timestamp = when.ctime()
        altitude_deg = altitude(latitude_deg, longitude_deg, when)
        azimuth_deg = azimuth(latitude_deg, longitude_deg, when)
        power = radiation.radiation_direct(when, altitude_deg)
        if altitude_deg > 0:
            print(timestamp, "UTC", altitude_deg, azimuth_deg, power)
        when = when + thirty_minutes

def my_eot(day):
    """ under dev so first we need the right time entry. Year day needs to be converted to a
      Julian day number with time added as EOT is not just for lunch
      https://equationoftime.herokuapp.com/ """
    jdn = day
    jct = time.julian_century(jdn)
    vma = 357.52772 + \
      35999.050340 * jct + \
      -0.0001603 * jct * jct + \
      -300000.0 * jct * jct * jct
    print(vma % 360)
    # delta angle = mean anomally - true anomally + true longitude - right ascension
    return math.radians(vma % 360)

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
    """ pending docs """
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
    xml = 1.0
    for line in coeffs:
        col = 0.0
        for idx in line:
            col += idx[0] * math.cos(idx[1] + idx[2] * jem)
        #end for
        result += col * xml
        xml *= jem
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


def equatorial_horizontal_parallax(sun_earth):
    """ pending docs """
    return 8.794 / (3600 / sun_earth)

def flattened_latitude(latitude):
    """ pending docs """
    latitude_rad = math.radians(latitude)
    return math.degrees(math.atan(0.99664719 * math.tan(latitude_rad)))

# Geocentric functions calculate angles relative to the center of the earth.

def geocentric_latitude(jme):
    """ pending docs """
    return -1 * heliocentric_latitude(jme)

def geocentric_longitude(jme):
    """ pending docs """
    return (heliocentric_longitude(jme) + 180) % 360

def geocentric_declination(true_longitude,
                           true_obliquity,
                           latitude):
    """ pending docs """
    apparent_longitude_rad = math.radians(true_longitude)
    true_obliquity_rad = math.radians(true_obliquity)
    geocentric_latitude_rad = math.radians(latitude)

    vao = math.sin(geocentric_latitude_rad) * math.cos(true_obliquity_rad)
    vbo = math.cos(geocentric_latitude_rad) * \
      math.sin(true_obliquity_rad) * \
      math.sin(apparent_longitude_rad)
    delta = math.asin(vao + vbo)
    return math.degrees(delta)

def geocentric_right_ascension(true_longitude,
                               true_obliquity,
                               latitude):
    """ http://www.nrel.gov/docs/fy08osti/34302.pdf page. (8)
    3.9. Calculate the geocentric sun right ascension, " (in degrees):
    3.9.1. Calculate the sun right ascension, " (in radians),

    α = Arctan2((sin λ * cos ε − tan β * sin ε) / cos λ), (30)

    where Arctan2 is an arctangent function that is applied to the numerator and the
    denominator (instead of the actual division) to maintain the correct quadrant of the α

    where α is in the range from -π to π.
    3.9.2. Calculate α in degrees using Equation 12, then limit it to the range from 0° to
    360°  using the technique described in step 3.2.6. """
    apparent_sun_longitude_rad = math.radians(true_longitude)
    true_ecliptic_obliquity_rad = math.radians(true_obliquity)
    geocentric_latitude_rad = math.radians(latitude)
    vao = math.sin(apparent_sun_longitude_rad) * math.cos(true_ecliptic_obliquity_rad)
    vbo = math.tan(geocentric_latitude_rad) * math.sin(true_ecliptic_obliquity_rad)
    vco = math.cos(apparent_sun_longitude_rad)
    alpha = math.atan2((vao - vbo), vco)
    return math.degrees(alpha) % 360

# Heliocentric functions calculate angles relative to the center of the sun.

def heliocentric_latitude(jme):
    """ pending docs """
    return math.degrees(coeff(jme, constants.HELIOCENTRIC_LATITUDE_COEFFS) / 1e8)

def heliocentric_longitude(jme):
    """ pending docs """
    return math.degrees(coeff(jme, constants.HELIOCENTRIC_LONGITUDE_COEFFS) / 1e8) % 360

def angle_of_incidence(zenith_angle,
                       slope,
                       slope_orientation,
                       azimuth_angle):
    """ The angle of incidence (θi) of the Sun on a surface tilted at an angle from the
    horizontal (β) and with any surface azimuth angle (AZS) can be calculated from
    (when AZS is measured clockwise from north):

    cosine(θi) =
    sine(δ)sine(φ)sine(β)
    +
    sine(δ)cosine(φ)sine(β)cosine(AZS)
    +
    cosine(δ)cosine(φ)cosine(β)cosine(ω)
    -
    cosine(δ)sine(φ)sine(β)cosine(AZS)cosine(ω)
    -
    cosine(δ)sine(β)sine(AZS)sine(ω)

    Where:
    ω = the hour angle;
    α = the altitude angle;
    AZ = the solar azimuth angle;
    δ = the declination angle;
    φ = observer’s latitude.

    This horrible equation can be simplified in a number of instances.
    When the surface is flat (i.e. horizontal) β=0, cosine(β) = 1, sine(β) = 0.
    Therefore the equation becomes:

    cosine(θi) =
    cosine(δ)cosine(φ)cosine(ω)
    +
    sine(δ)sine(φ)

    When the surface is tilted towards the equator
    (facing south in the northern hemisphere):

    cosine(θi) =
    cosine(δ)cosine(φ-β)cosine(ω)
    +
    sine(δ)sine(φ-β)

    Note that if θi > 90° at any point the Sun is behind the surface and
    the surface will be shading itself. """

    cos_tza = math.cos(math.radians(zenith_angle))
    cos_slope = math.cos(math.radians(slope))
    sin_tza = math.sin(math.radians(zenith_angle))
    sin_slope = math.sin(math.radians(slope))
    vaa_rad = math.radians(azimuth_angle)
    vso_rad = math.radians(slope_orientation)
    return math.degrees(math.acos( \
      cos_tza * cos_slope + \
      sin_slope * sin_tza * math.cos(vaa_rad - math.pi - vso_rad)))

def altitude_fast(lat_deg, lon_deg, when):
    """ expect 19 degrees for
    solar.altitude(42.364908, -71.112828, datetime.datetime(2007, 2, 18, 20, 13, 1, 130320)) """
    day = when.utctimetuple().tm_yday
    cos_dec = math.cos(math.radians(declination(day)))
    cos_lat = math.cos(math.radians(lat_deg))
    cos_hra = math.cos(math.radians(hour_angle(when, lon_deg)))
    first_term = cos_dec * cos_hra * cos_lat
    sin_dec = math.sin(math.radians(declination(day)))
    sin_lat = math.sin(math.radians(lat_deg))
    second_term = sin_dec * sin_lat
    return math.degrees(math.asin(first_term + second_term))

def local_hour_angle(sidereal_time, longitude, right_ascension):
    """ pending docs """
    return (sidereal_time + longitude - right_ascension) % 360

def mean_sidereal_time(jsd):
    """ This function doesn't agree with Andreas and Reda as well as it should.
        Works to ~5 sig figs in current unit test """

    jec = time.julian_century(jsd)
    return (280.46061837 + \
      (360.98564736629 * (jsd - 2451545.0)) + \
      0.000387933 * jec * jec * (1 - jec / 38710000)) % 360

def nutation(jec):
    """ pending docs """
    abcd = constants.NUTATION_COEFFICIENTS
    nutation_long = []
    nutation_oblique = []
    abc = constants.aberration_coeffs()
    xed = \
      list \
        (abc[k](jec)
         # order is important
         for k in ( \
                       'MeanElongationOfMoon',
                       'MeanAnomalyOfSun',
                       'MeanAnomalyOfMoon',
                       'ArgumentOfLatitudeOfMoon',
                       'LongitudeOfAscendingNode',
                  )
        )
    yed = constants.ABERRATION_SIN_TERMS
    for idx in range(len(abcd)):
        sigmaxy = 0.0
        for jdx in range(len(xed)):
            sigmaxy += xed[jdx] * yed[idx][jdx]
        #end for

        nutation_long.append((abcd[idx][0] + \
                              (abcd[idx][1] * jec)) * \
                              math.sin(math.radians(sigmaxy)))
        nutation_oblique.append((abcd[idx][2] + \
                                 (abcd[idx][3] * jec)) * \
                                  math.cos(math.radians(sigmaxy)))
    #end for
    # 36000000 scales from 0.0001 arcseconds to degrees
    return {'longitude': sum(nutation_long) / 36000000.0,
            'obliquity': sum(nutation_oblique) / 36000000.0}
#end get_nutation

def ra_parallax(p_radial_distance,
                equatorial_horizontal,
                local_hr_angle,
                geo_declination):
    """ pending docs """
    prd = p_radial_distance
    ehp_rad = math.radians(equatorial_horizontal)
    lha_rad = math.radians(local_hr_angle)
    gsd_rad = math.radians(geo_declination)
    parallax = math.atan2( \
      -1 * prd * math.sin(ehp_rad) * math.sin(lha_rad), \
    math.cos(gsd_rad) - prd * math.sin(ehp_rad) * math.cos(lha_rad))
    return math.degrees(parallax)

def projected_radial_distance(elevation, latitude):
    """ pending docs """
    flattened_latitude_rad = math.radians(flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return math.cos(flattened_latitude_rad) + \
        (elevation * math.cos(latitude_rad) / constants.EARTH_RADIUS)

def projected_axial_distance(elevation, latitude):
    """ pending docs """
    flattened_latitude_rad = math.radians(flattened_latitude(latitude))
    latitude_rad = math.radians(latitude)
    return 0.99664719 * math.sin(flattened_latitude_rad) + \
        (elevation * math.sin(latitude_rad) / constants.EARTH_RADIUS)

def sun_earth_distance(jem):
    """ pending docs """
    return coeff(jem, constants.SUN_EARTH_DISTANCE_COEFFS) / 1e8

def refraction_correction(pressure, temperature, topo_elevation_angle):
    """ pending docs """
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
          pressure * 2.830 * 1.02 \
          / 1010.0 * temperature * 60.0 * math.tan(math.radians(tea + (10.3 / (tea + 5.11))))

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
    sin_lha = math.sin(math.radians(topo_local_hour_angle))
    cos_lha = math.cos(math.radians(topo_local_hour_angle))
    sin_lat = math.sin(math.radians(lat))
    cos_lat = math.cos(math.radians(lat))
    tan_dec = math.tan(math.radians(topo_declination))
    return 180.0 + math.degrees(math.atan2(sin_lha, cos_lha * sin_lat - tan_dec * cos_lat)) % 360

def topocentric_elevation_angle(lat, dec, local_hr_angle):
    """ 3.14.3. Calculate the topocentric elevation angle, e (in degrees),
    e = e0 + ∆e .	 (43)  """
    cos_dec = math.cos(math.radians(dec))
    cos_lat = math.cos(math.radians(lat))
    cos_lha = math.cos(math.radians(local_hr_angle))
    sin_dec = math.sin(math.radians(dec))
    sin_lat = math.sin(math.radians(lat))

    return math.degrees(math.asin(sin_lat * sin_dec + cos_lat * cos_dec * cos_lha))

def topocentric_local_hour_angle(local_hr_angle, solar_ra_parallax):
    """ pending docs """
    return local_hr_angle - solar_ra_parallax

def topocentric_sun_declination(geo_declination,
                                p_axial_distance,
                                equatorial_horizontal,
                                right_ascension,
                                local_hr_angle):
    """ pending """
    sin_gsd = math.sin(math.radians(geo_declination))
    cos_gsd = math.cos(math.radians(geo_declination))
    pad = p_axial_distance
    sin_ehp = math.sin(math.radians(equatorial_horizontal))
    cos_psra = math.cos(math.radians(right_ascension))
    cos_lha = math.cos(math.radians(local_hr_angle))
    return math.degrees(math.atan2((sin_gsd - pad * sin_ehp) * \
      cos_psra, cos_gsd - (pad * sin_ehp * cos_lha)))

def topocentric_sun_right_ascension(p_radial_distance,
                                    equatorial_horizontal,
                                    local_hr_angle,
                                    solar_longitude,
                                    true_obliquity,
                                    geo_latitude):
    """ 3.12. Calculate the topocentric sun right ascension α' = α + ∆α (in degrees): """
    gsd = geocentric_declination(solar_longitude,
                                 true_obliquity,
                                 geo_latitude)
    psra = ra_parallax(p_radial_distance,
                       equatorial_horizontal,
                       local_hr_angle, gsd)
    gsra = geocentric_right_ascension(solar_longitude,
                                      true_obliquity,
                                      geo_latitude)
    return psra + gsra

def topocentric_zenith_angle(lat, dec,
                             local_hr_angle,
                             pressure, temperature):
    """ pending docs """
    tea = topocentric_elevation_angle(lat, dec,
                                      local_hr_angle)
    return 90 - tea - refraction_correction(pressure, temperature, tea)

def true_ecliptic_obliquity(jem, nut):
    """ pending docs """
    jmt = jem / 10.0
    mean_obliquity = 84381.448 - (4680.93 * jmt) - (1.55 * jmt ** 2) + (1999.25 * jmt ** 3) \
    - (51.38 * jmt ** 4) - (249.67 * jmt ** 5) - (39.05 * jmt ** 6) + (7.12 * jmt ** 7) \
    + (27.87 * jmt ** 8) + (5.79 * jmt ** 9) + (2.45 * jmt ** 10)
    return (mean_obliquity / 3600.0) + nut['obliquity']

def altitude(latitude_deg, longitude_deg, when,
             elevation=0,
             temperature=constants.STANDARD_TEMPERATURE,
             pressure=constants.STANDARD_PRESSURE):
    '''See also the faster, but less accurate, get_altitude_fast()'''
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
    sun_earth = sun_earth_distance(jem)
    ab_correction = aberration_correction(sun_earth)
    equatorial_horizontal = equatorial_horizontal_parallax(sun_earth)
    nut = nutation(jec)
    sidereal_time = apparent_sidereal_time(jsd, jem, nut)
    true_obliquity = true_ecliptic_obliquity(jem, nut)

    # calculations dependent on location and time
    lon = apparent_longitude(geo_longitude,
                             nut,
                             ab_correction)
    geo_right_ascension = geocentric_right_ascension(lon,
                                                     true_obliquity,
                                                     geo_latitude)
    geo_declination = geocentric_declination(lon,
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
    """ pending docs """
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
    sun_earth = sun_earth_distance(jem)
    ab_correction = aberration_correction(sun_earth)
    equatorial_horizontal = equatorial_horizontal_parallax(sun_earth)
    nut = nutation(jec)
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
                                   right_ascension)
    topo_declination = \
      topocentric_sun_declination(geo_declination,
                                  p_axial_distance,
                                  equatorial_horizontal,
                                  geo_right_ascension,
                                  local_hr_angle)
    return 180 - topocentric_azimuth_angle(topo_local_hour_angle,
                                           latitude_deg,
                                           topo_declination)
