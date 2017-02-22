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
#
#    Some of this code is derived from IAU SOFA source code and is in no
#    way associated with their work. Proper credit is heretofore given,
#    Correspondence concerning SOFA software should be addressed as follows:
#
#      By email:  sofa@ukho.gov.uk
#      By post:   IAU SOFA Center
#                 HM Nautical Almanac Office
#                 UK Hydrographic Office
#                 Admiralty Way, Taunton
#                 Somerset, TA1 2DN
#                 United Kingdom

"""
Solar geometry functions

This module contains the most important functions for calculation of the position of the sun.

"""
import datetime
# from decimal import *
# getcontext().prec = 16
import math

from . import au_coeffs
from . import constants
from . import time
from . import helio_lat
from . import helio_lon
from . import radiation

def aberration_correction(jct):
    """
    Given the julian century time
    calculates
    a correction for abbereation
    """
    # a possible updated aberration constant 20.49552
    # 3.6. Calculate the aberration correction, Δτ (in degrees):
    sed = astronomical_units(jct)
    # sun-earth distance is in astronomical units
    # return -20.4898 / (3600.0 * sed)
    return -0.0056916111 / sed
    # return -0.0056932 / sed

def apparent_solar_longitude(jct):
    """
    Given the julian century time
    calculates
    Apparent Solar Longitude in degrees
    """
    lon = geocentric_longitude(jct)
    d_psi = delta_psi(jct)
    aberration = aberration_correction(jct)
    return lon + d_psi + aberration

def radius_vector_list(jct):
    """
    Given the julian century time
    calculates
    sun earth distance in astronomical units
    into a list data structure
    """
    # 3.2.8. Calculate the Earth radius vector, R (in Astronomical Units, AU),
    #  by repeating step 3.2.7 and by replacing all Ls by Rs in all equations.
    #  Note that there is no R5, consequently, replace it by zero in steps 3.2.3 and 3.2.4.
    return coefficients(jct, au_coeffs.AU_DISTANCE_COEFFS)

def astronomical_units(jct):
    """
    Given the julian century time
    calculates
    sun earth distance in astronomical units
    """
    # 3.2.8. Calculate the Earth radius vector, R (in Astronomical Units, AU),
    #  by repeating step 3.2.7 and by replacing all Ls by Rs in all equations.
    #  Note that there is no R5, consequently, replace it by zero in steps 3.2.3 and 3.2.4.
    jem = jct / 10.0
    rvl = radius_vector_list(jct)
    return (
        rvl[0] + jem * (
            rvl[1] + jem * (
                rvl[2] + jem * (
                    rvl[3] + jem * rvl[4]))))  / 1e8

def coefficients(jct, coeffs):
    """
    Given the julian century time and the constant name for
    the coefficient set to use
    sums the time-varying coefficients sub arrays and returns an array
    with each.
    """
    jem = jct / 10.0
    result = []

    for group in coeffs:
        count = 0.0
        tsum = 0.0
        for item in group:
            tsum += float(item[0]) * math.cos(float(item[1]) + float(item[2]) * jem) * 1e8
        #end for
        result.append(tsum)
        count += 1
    #end for
    return result
#end coefficients

def delta_epsilon(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    delta obliquity in degrees
    """
    return nutation(jct)['obliquity']

def delta_psi(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    delta longitude in degrees
    """
    return nutation(jct)['longitude']

def orbital_eccentricity(jct):
    """
    earths eliptic orbit
    """
    return 0.016708617 + jct * (-0.000042037 + jct * -0.0000001235)

def mean_anomaly(jct):
    """
    Mean Anomaly of the Sun
    """
    coef = constants.aberration_coeffs()
    xdx = list \
      (
          coef[k](jct)
          for k in
          ( # order is important
              'MeanAnomalyOfMoon',
              'MeanAnomalyOfSun',
              'ArgumentOfLatitudeOfMoon',
              'MeanElongationOfMoon',
              'LongitudeOfAscendingNode',
          )
      )
    return xdx[1] % 360

def equation_of_center(jct):
    """
    equation of center
    """
    eoe = orbital_eccentricity(jct)
    mas = mean_anomaly(jct)
    sin1 = math.sin(1.0 * mas) * 2.0
    sin2 = math.sin(2.0 * mas) * 5.0 / 4.0
    sin3 = math.sin(3.0 * mas)
    sin4 = math.sin(4.0 * mas)
    sin5 = math.sin(5.0 * mas) * 1097.0 / 960.0
    ad3 = sin3 * 13.0 / 12.0 - sin1 / 2.0 * 1.0 / 4.0
    ad4 = sin4 * 103.0 / 96.0 - sin2 / 5.0 / 4.0  * 11.0 / 24.0
    ad5 = sin5 + sin1 / 2.0 * 5.0 / 96.0 - sin3 * 43.0 / 64.0
    return eoe * (sin1 + eoe * (sin2 + eoe * (ad3 + eoe * (ad4 + eoe * ad5))))

def true_anomaly(jct):
    """
    True Anomaly of the Sun
    """
    mas = mean_anomaly(jct)
    eoc = equation_of_center(jct)
    return (mas + eoc) % 360

def equation_of_equinox(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    Equation of Equinox in degrees
    """
    d_psi = delta_psi(jct)
    epsilon = true_ecliptic_obliquity(jct)
    cos_eps = math.cos(math.radians(epsilon))
    return d_psi * cos_eps

def gasa(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    Greenwich Apparent Sidereal Angle in degress
    """
    mean = gmsa(jct)
    eqeq = equation_of_equinox(jct)
    return (mean + eqeq) % 360.0

def gast(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    Greenwich Apparent Sidereal Time in hours
    """
    return gasa(jct) / 15

def gmsa(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    Greenwich Mean Sidereal Angle in degrees
    see: http://aa.usno.navy.mil/publications/docs/Circular_179.pdf
         Resolution B1.8 note 3.
    theta_ut1 = (1.00273781191135448 * hours + 0.7790572732640) * 360
    """
    """
    pending further investigation
    if jd0 < jd1:
        dj1 = jd0
        dj2 = jd1
    else:
        dj1 = jd1
        dj2 = jd0

    jdt = (dj1 - 2451545.0) + dj2

    frac = dj1  % 1.0 + dj2 % 1.0
    s_days = (0.00273781191135448 * jdt + 0.7790572732640 + frac) * 2 * math.pi
    delta_t = time.delta_t(jd0 + jd1)
    print(delta_t)
    jct = jdt / 36525
    angle = 0.014506 + (
        4612.156534 + (
            1.3915817 + (
                -0.00000044 + (
                    -0.000029956 + (
                        -0.0000000368 * jct) * jct) * jct) * jct) * jct) / 3600
    # print(frac)
    # print(math.degrees(s_days) % 360.0)
    # print(math.degrees(angle) % 360.0)
    return (math.degrees(s_days) % 360.0 + angle) / 15
    """
    return gmst(jct) * 15

def gmst(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    Greenwich Mean Sidereal Time in hours
    see: http://aa.usno.navy.mil/faq/docs/GAST.php

    # Let JD1 be the Julian date of the time of interest.
    # Let JD0 be the Julian date of the previous midnight (0h) UT
    # (the value of JD0 will end in .5 exactly),
    # and let H be the hours of UT elapsed since that time.
    # Thus we have JD1 = JD0 + Hours / 24.0
    # For both of these Julian dates, compute the number of days and fraction (+ or -) from
    # 2000 January 1, 12h UT, Julian date 2451545.0:
    # D2K = JD1 - 2451545.0 the J2000 Julian value
    # D02K = JD0 - 2451545.0 the J2000 Julian value
    # Then the Greenwich mean sidereal time in hours is
    # GMST = 6.697374558 + 0.06570982441908 D02K + 1.00273790935 Hours + 0.000026 T2
    # where T = D/36525 is the number of centuries since the year 2000;
    # thus the last term can be omitted in most applications.
    # It will be necessary to reduce GMST to the range 0h to 24h.
    # Setting H = 0 in the above formula yields the Greenwich mean sidereal time at 0h UT,
    # which is tabulated in The Astronomical Almanac.
    """

    jd1 = jct * 36525.0 + 2451545.0
    # d2k = jd1 - 2451545.0 not used because we already have jct
    jd0 = math.floor(jd1) - 0.5 # Midnight
    d02k = jd0 - 2451545.0
    d_frac = jd1 % 1.0 + 0.5 # day fraction from midnight on
    gma = 6.697374558
    s_days = 0.06570982441908 * d02k # days
    # number of sidereal hours in one solar hour
    s_hours = 1.0027379093508055 * d_frac * 24.0 # hours from midnight on
    coeff = 0.000026 * jct * jct
    mean_st = gma + s_days + s_hours + coeff
    return mean_st % 24.0

# Geocentric functions calculate angles relative to the center of the earth.

def geocentric_beta(jct):
    """
    Given the julian century time
    calculates
    Geocentric Beta of the Sun in degress
    """
    l_sun_prime = geocentric_prime(jct)
    cos_lsp = math.cos(math.radians(l_sun_prime))
    sin_lsp = math.sin(math.radians(l_sun_prime))
    beta = -1 * helio_lat.heliocentric_latitude(jct)
    beta = beta + 0.000011 * (cos_lsp - sin_lsp)
    return beta

def geocentric_declination(jct):
    """
    Given the julian century time
    calculates
    Geocentric declination of the Sun in degress
    """
    slam = geocentric_lambda(jct)
    eps = true_ecliptic_obliquity(jct)
    beta = geocentric_beta(jct)

    sin_beta = math.sin(math.radians(beta))
    cos_eps = math.cos(math.radians(eps))
    cos_beta = math.cos(math.radians(beta))
    sin_eps = math.sin(math.radians(eps))
    sin_slam = math.sin(math.radians(slam))

    return math.degrees(math.asin(sin_beta * cos_eps + cos_beta * sin_eps * sin_slam))

def geocentric_lambda(jct):
    """
    Given the julian century time
    calculates
    Geocentric Lambda of the Sun in degress
    """
    true_sun = true_solar_longitude(jct)
    dpsi = delta_psi(jct)
    radius = astronomical_units(jct)
    sunlambda = (true_sun + dpsi - 0.005691611 / radius) % 360.0
    return sunlambda

def geocentric_latitude(jct):
    """
    Given the julian century time
    calculates
    Geocentric Latitude of the Sun in degress
    """
    return -1 * helio_lat.heliocentric_latitude(jct)

def geocentric_longitude(jct):
    """
    Given the julian century time
    calculates
    true Geocentric Longitude of the Sun in degress
    """
    return (heliocentric_longitude(jct) + 180) % 360

def geocentric_prime(jct):
    """
    Given the julian century time
    calculates
    Geocentric Prime of the Sun in degress
    """
    hln = heliocentric_longitude(jct)
    prime = hln + 180 - 1.397 * jct - 0.00031 * jct * jct
    return prime % 360.0

def geocentric_right_ascension(jct):
    """
    Given the julian century time
    calculates Geocentric Right Ascension in degrees
    """
    lam = geocentric_lambda(jct)
    eps = true_ecliptic_obliquity(jct)
    beta = geocentric_beta(jct)

    sin_lam = math.sin(math.radians(lam))
    cos_eps = math.cos(math.radians(eps))
    tan_beta = math.tan(math.radians(beta))
    sin_eps = math.sin(math.radians(eps))

    cos_lam = math.cos(math.radians(lam))

    return (math.degrees(
        math.atan2((sin_lam * cos_eps - tan_beta * sin_eps), cos_lam)) % 360)

def greenwich_hour_angle(jct):
    """
    Given the julian century time
    calculates
    Greenwich Hour Angle in degrees
    """
    ghaa = true_gha_aries(jct)
    gra = geocentric_right_ascension(jct)
    # return (gasa(jct) - gra) % 360.0
    return (ghaa - gra) % 360.0

def heliocentric_longitude(jct):
    """
    Given the julian century time
    calculates Heliocentric Longitude in degrees
    That based on the Sun as a center.
    The Nautical Almanac gives the Heliocentric positions of all celestial bodies.
    """
    # return math.degrees(
    #     coefficients(dt_list, constants.HELIOCENTRIC_LONGITUDE_COEFFS, default) / 1e8) % 360
    jem = jct / 10.0
    # jem = (2452930.312847 - 2451545.0) / 365250.0
    hlc = heliocentric_lon_elements(jct)
    return math.degrees(
        (hlc[0] + jem * (
            hlc[1] + jem * (
                hlc[2] + jem * (
                    hlc[3] + jem * (
                        hlc[4] + jem * hlc[5]))))) / 1e8) % 360.0

def heliocentric_lon_elements(jct):
    """
    Given date/time list and optional delta T
    gets Coefficient terms for Heliocentric Longitude in radians

    That based on the Sun as a center.
    The Nautical Almanac gives the Heliocentric positions of all celestial bodies.
    """
    hlc = coefficients(jct, helio_lon.HELIOCENTRIC_LONGITUDE_COEFFS)
    return hlc

def lasa(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    Loacal Apparent Sidereal Angle in degrees
    """
    return gasa(jct)

def last(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    Loacal Apparent Sidereal Time in hours
    """
    laa = lasa(jct)
    return laa / 15.0

def lmsa(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    Loacal Mean Sidereal Angle in degrees
    by adding a longitude offset on to the jd1
    hence this is defined only for convinience
    of naming functions otherwise it is the same
    as gmsa(jct)
    """
    return gmsa(jct)

def lmst(jct):
    """
    Given UT1 as a 2-part Julian Date
    calculates
    Loacal Mean Sidereal Time in hours
    """
    return gmst(jct)

def local_hour_angle(jct, longitude):
    """
    Given the julian century time
    parameter list
    calculates
    Local Hour Angle
    """

    return (greenwich_hour_angle(jct) + longitude) % 360.0

def mean_ecliptic_obliquity(jct):
    """
    Given the julian century time
    calculates
    Mean Ecliptic Obliquity in degrees
    """
    return (84381.406 + jct * (
        -46.836769 + jct * (
            -0.0001831 + jct * (
                0.00200340 + jct * (
                    -0.000000576 + jct * -0.0000000434))))) / 3600

def true_ecliptic_obliquity(jct):
    """
    Given the julian century time
    calculates
    True Ecliptic Oblquity in degrees
    """
    mean_eps = mean_ecliptic_obliquity(jct)
    delta_eps = delta_epsilon(jct)

    return mean_eps + delta_eps

def mean_gha_aries(jct):
    """
    Given the julian century time
    calculates
    mean longitude of the first point of aries
    """
    jd2000 = jct * 36525.0
    degd = 360.98564736629 * jd2000
    mla = 280.46061837 + degd + jct * (jct * 0.000387933  + jct * (jct * -1 / 38710000))
    return mla % 360.0

def true_gha_aries(jct):
    """
    Given the julian century time
    calculates
    apparent longitude of the first point of aries
    """
    mla = mean_gha_aries(jct)
    return (mla + equation_of_equinox(jct)) % 360.0

def mean_solar_longitude(jct):
    """
    Given the julian century time
    calculates
    Mean Geocentric Longitude in degrees
    """
    mgl = 280.4664567 + jct * (
        36000.76982779 + jct * (
            0.0003032028 + jct * (
                1.0 / 49931.0 + jct * (
                    -1.0 / 15299.0 + jct * (-1.0 / 1988000.0)))))
    return mgl % 360.0

def true_solar_longitude(jct):

    """
    Given the julian century time
    calculates
    True Solar Longitude in degrees
    """
    return (heliocentric_longitude(jct) + 180 - 0.000025) % 360.0

def nutation(jct):
    """
    Given the julian century time
    calculates
    Delta Epsilon and Delta Psi in degrees
    """
    abcd = constants.NUTATION_COEFFICIENTS
    nutation_long = []
    nutation_oblique = []
    coef = constants.aberration_coeffs()
    xdx = list \
      (
          coef[k](jct)
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
            (abcd[idx][0] + (abcd[idx][1] * jct)) * math.sin(math.radians(sigmaxy)))
        nutation_oblique.append(
            (abcd[idx][2] + (abcd[idx][3] * jct)) * math.cos(math.radians(sigmaxy)))

    # 36000000 scales from 0.0001 arcseconds to degrees
    deltas = {'longitude' : sum(
        nutation_long) / 36000000.0, 'obliquity' : sum(nutation_oblique) / 36000000.0}

    return deltas
#end nutation

def flattened_latitude(latitude):
    """
    Given latitude
    calculates
    """
    e_flat = 1 - constants.EARTHS_FLATTENING
    tan_lat = math.tan(math.radians(latitude))
    return math.atan(e_flat * tan_lat) # radians

def projected_axial_distance(param_list):
    """
    Given parameter list with elevation and latitude
    3.12.4. Calculate the term y
    """
    erad = constants.EARTH_RADIUS
    elevation = param_list[2]
    latitude = param_list[0]
    sin_lat = math.sin(math.radians(latitude))
    uval = flattened_latitude(latitude)
    return 0.99664719 * math.sin(uval) + elevation / erad * sin_lat

def projected_radial_distance(param_list):
    """
    Given parameter list having elevation and latitude
    calculates
    a distance correction for
    """
    erad = constants.EARTH_RADIUS
    elevation = param_list[2]
    latitude = param_list[0]
    cos_lat = math.cos(math.radians(latitude))
    uval = flattened_latitude(latitude)
    return math.cos(uval) + elevation / erad * cos_lat

def refraction_correction(jct, param_list):
    """
    Given the julian century time and parameter list with
    pressure and temperature
    calculates
    a correction or offset of view caused by refraction of Earth
    atmosphere and view angle.
    """
    #function and default values according to original NREL SPA C code
    #http://www.nrel.gov/midc/spa/

    sun_radius = 0.26667
    atmos_refract = 0.5667
    del_e = 0.0
    tea = topocentric_elevation_angle(jct, param_list)

    # Approximation only valid if sun is not well below horizon
    # This approximation could be improved;
    # see history at https://github.com/pingswept/pysolar/pull/23
    # Better method could come from Auer and Standish [2000]:
    # http://iopscience.iop.org/1538-3881/119/5/2472/pdf/1538-3881_119_5_2472.pdf
    pressure = param_list[6] / 1010.0
    temperature = param_list[5] + 273
    if tea >= -1.0 * (sun_radius + atmos_refract):
        arc = pressure * 283 / temperature
        brc = 1.02 / (60.0 * math.tan(math.radians(tea + (10.3 / (tea + 5.11)))))
        del_e = arc * brc

    return del_e

def max_horizontal_parallax(jct):
    """
    Given the julian century time
    calculates
    equitorial horizontal parallax
    see: http://star-www.st-and.ac.uk/~fv/webnotes/chapter7.htm
    this function was used but now is depricated so it will make
    a nice place to put some further information.
    Taking a look at the above site we see...
    To convert between the horizontal and equatorial coordinates for an object X,
    we use a spherical triangle often called "The" Astronomical Triangle: XPZ,
    where Z is the zenith, P is the North Celestial Pole, and X is the object.

    The sides of the triangle:
    PZ is the observer's co-latitude = 90°-φ.
    ZX is the zenith distance of X = 90°-a.
    PX is the North Polar Distance of X = 90°-δ.

    The angles of the triangle:
    The angle at P is H, the local Hour Angle of X.
    The angle at Z is 360°-A, where A is the azimuth of X.
    The angle at X is q, the parallactic angle.

    We assume we know the observer’s latitude φ and the Local Sidereal Time LST.
    (LST may be obtained, if necessary, from Greenwich Sidereal Time and observer’s longitude.)
    """
    sed = astronomical_units(jct)
    return 8.794 / (3600 / sed)

def right_ascension_parallax(jct, param_list):
    """
    Given the julian century time and parameter list
    to pass
    calculates
    A delta of Right Ascension caused by parallax in degrees
    """
    xval = projected_radial_distance(param_list)
    ehp = 8.794 / (3600 * astronomical_units(jct))
    lha = local_hour_angle(jct, param_list[1])
    gsd = geocentric_declination(jct)

    sin_ehp = math.sin(math.radians(ehp))
    sin_lha = math.sin(math.radians(lha))

    cos_gsd = math.cos(math.radians(gsd))
    cos_lha = math.cos(math.radians(lha))

    return math.degrees(
        math.atan2(-xval * sin_ehp * sin_lha,
                   cos_gsd - xval * sin_ehp * cos_lha))

# Topocentric functions calculate angles relative to a location on the surface of the earth.

def topocentric_azimuth_angle(jct, param_list):
    """
    Given the julian century time and parameter list
    to pass and with latitude,
    calculates
    Topocentric Azimuth Angle in degrees
    Measured eastward from north
    """
    phi = param_list[0]
    tlha = topocentric_lha(jct, param_list)
    sin_tlha = math.sin(math.radians(tlha))

    tdelta = topocentric_solar_declination(jct, param_list)
    cos_tlha = math.cos(math.radians(tlha))
    sin_phi = math.sin(math.radians(phi))
    tan_tdelta = math.tan(math.radians(tdelta))
    cos_phi = math.cos(math.radians(phi))

    ayt = sin_tlha
    bxt = cos_tlha * sin_phi - tan_tdelta * cos_phi
    return (180.0 + math.degrees(math.atan2(ayt, bxt))) % 360

def topocentric_lha(jct, param_list):
    """
    Given the julian century time and
    parameter list to pass
    calculates
    Topocentric Local Hour Angle in degrees
    """

    lha = local_hour_angle(jct, param_list[1])
    rap = right_ascension_parallax(jct, param_list)
    return lha - rap

def cosine_omega(surface_slope):
    """
    used with the two incidence angle calculations
    """
    return math.cos(math.radians(surface_slope))

def sine_omega(surface_slope):
    """
    used with the two incidence angle calculations
    """
    return math.sin(math.radians(surface_slope))

def incidence_angle(jct, param_list):
    """
    Given date/time list, parameter list, and optional delta T
    calculates
    Angle of Incedence in degrees
    """
    theta = topocentric_zenith_angle(jct, param_list)
    cos_theta = math.cos(math.radians(theta))
    omega = param_list[3]
    cos_omega = cosine_omega(omega)
    term1 = cos_theta * cos_omega

    sin_omega = sine_omega(omega)
    sin_theta = math.sin(math.radians(theta))
    ugamma = topocentric_azimuth_angle(jct, param_list) - 180
    ugamma_rad = math.radians(ugamma)
    lgamma = param_list[4]
    lgamma_rad = math.radians(lgamma)
    term2 = sin_omega * sin_theta * math.cos(ugamma_rad - lgamma_rad)

    return math.degrees(math.acos(term1 + term2))

def angle_of_incidence(jct, param_list):
    """
    from web page at http://article.sapub.org/10.5923.j.ep.20160602.01.html
    """
    delta = topocentric_solar_declination(jct, param_list)
    sin_delta = math.sin(math.radians(delta))
    sin_phi = math.sin(math.radians(param_list[0]))
    cos_omega = cosine_omega(param_list[3])
    term1 = sin_delta * sin_phi * cos_omega

    cos_phi = math.cos(math.radians(param_list[0]))
    sin_omega = sine_omega(param_list[3])
    cos_lgamma = math.cos(math.radians(param_list[4]))
    term2 = sin_delta * cos_phi * sin_omega * cos_lgamma

    hours = (((jct * 36525.0 + time.DJ00) % 1.0 + 0.5) * 24.0)
    tlha = 15 * (hours - 12.0)
    # tlha = topocentric_lha(jct, param_list)

    cos_delta = math.cos(math.radians(delta))
    cos_h = math.cos(math.radians(tlha))
    term3 = cos_delta * cos_phi * cos_omega * cos_h
    term4 = cos_delta * sin_phi * sin_omega * cos_lgamma * cos_h

    sin_lgamma = math.sin(math.radians(param_list[4]))
    sin_h = math.sin(math.radians(tlha))
    term5 = cos_delta * sin_omega * sin_lgamma * sin_h

    cos_theta = term1 - term2 + term3 + term4 + term5

    return math.degrees(math.acos(cos_theta))

def topocentric_solar_declination(jct, param_list):
    """
    Given the julian century time and
    parameter list to pass
    calculates
    Topocentric Solar Declination in degerees
    using sun earth distance in AU,
    geocentric solar declination,
    local hour angle,
    projected axial distance,
    right ascension parallax
    3.12.7. Calculate the topocentric sun declination δ ' (in degrees),
    Arc tan2((sinδ− y * sin ξ ) * cos Δα / cos δ− x * sin ξ * cos H)
    """
    ehp = 8.794 / (3600 * astronomical_units(jct)) # equitorial horizontal parallax
    gsd = geocentric_declination(jct)
    lha = local_hour_angle(jct, param_list[1])

    rap = right_ascension_parallax(jct, param_list)

    sin_gsd = math.sin(math.radians(gsd))
    yval = projected_axial_distance(param_list)
    sin_ehp = math.sin(math.radians(ehp))
    cos_rap = math.cos(math.radians(rap))

    cos_gsd = math.cos(math.radians(gsd))
    xval = projected_radial_distance(param_list)
    cos_lha = math.cos(math.radians(lha))

    ayt = sin_gsd - yval * sin_ehp * cos_rap
    bxt = cos_gsd - xval * sin_ehp * cos_lha
    return math.degrees(math.atan2(ayt, bxt))

def topocentric_right_ascension(jct, param_list):
    """
    Given the julian century time and
    parameter list to pass
    calculates
    Topocentric Right Ascension in degrees
    """
    rap = right_ascension_parallax(jct, param_list)
    gra = geocentric_right_ascension(jct) * 15
    return gra + rap

def topocentric_zenith_angle(jct, param_list):
    """
    Given the julian century time and
    parameter list to pass
    calculates
    Topocentric Zenith Angle in degrees
    """
    # 3.14.3. Calculate the topocentric elevation angle, e (in degrees),
    tea = topocentric_elevation_angle(jct, param_list)
    rc1 = refraction_correction(jct, param_list)
    # 3.14.4. Calculate the topocentric zenith angle, 2 (in degrees),
    return 90 - tea + rc1
    """
    tsd = topocentric_solar_declination(jct, param_list)
    tsd_cos = math.cos(math.radians(tsd))
    tsd_sin = math.sin(math.radians(tsd))

    latitude = param_list[1]
    lat_cos = math.cos(math.radians(latitude))
    lat_sin = math.sin(math.radians(latitude))

    lha = topocentric_lha(jct, param_list)
    lha_cos = math.cos(math.radians(lha))

    term_1 = tsd_cos * lat_cos * lha_cos
    term_2 = tsd_sin * lat_sin

    # return math.degrees(math.acos(term_1 + term_2))
    """

def topocentric_elevation_angle(jct, param_list):
    """
    Given the julian century time and parameter list
    to pass and with latitude
    calculates
    Topocentric Elevation Angle in degrees
    """
    phi = param_list[0]
    delta = topocentric_solar_declination(jct, param_list)
    lha = topocentric_lha(jct, param_list)

    sin_phi = math.sin(math.radians(phi))
    sin_delta = math.sin(math.radians(delta))
    term_1 = sin_phi * sin_delta

    cos_phi = math.cos(math.radians(phi))
    cos_delta = math.cos(math.radians(delta))
    cos_h = math.cos(math.radians(lha))
    term_2 = cos_phi * cos_delta * cos_h

    # just the opposite of zenith angle
    return math.degrees(math.asin(term_1 + term_2))
