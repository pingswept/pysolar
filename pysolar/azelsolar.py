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

from . import constants
from . import radiation
from . import solar
from . import time

def altitude(when, param_list):
    """
    See also the faster, but less accurate, altitude_fast()
    """
    dt_list = [when.year, when.month, when.day,
               when.hour, when.minute, when.second,
               when.microsecond, 0, 0]
    jdt = time.julian_day(dt_list)
    jct = time.julian_century(jdt)# - param_list[1] / 360)

    tea = solar.topocentric_elevation_angle(jct, param_list)
    rca = solar.refraction_correction(jct, param_list)
    return tea + rca

def altitude_fast(when, param_list):
    """
    docstring goes here
    """
# expect 19 degrees for solar.altitude(
#     42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 13, 1, 130320))
    day = when.utctimetuple().tm_yday
    latitude = param_list[0]
    cos_lat = math.cos(math.radians(latitude))
    cos_dec = math.cos(math.radians(declination(day)))
    longitude = param_list[1]
    cos_ha = math.cos(math.radians(hour_angle(when, longitude)))
    term1 = cos_lat * cos_dec * cos_ha

    sin_lat = math.sin(math.radians(latitude))
    sin_dec = math.sin(math.radians(declination(day)))
    term2 = sin_lat * sin_dec

    return math.degrees(math.asin(term1 + term2))

def azimuth(when, param_list):
    """
    docstring goes here
    """
    dt_list = [when.year, when.month, when.day,
               when.hour, when.minute, when.second,
               when.microsecond, 0, 0]
    jdt = time.julian_day(dt_list)
    jct = time.julian_century(jdt)# - param_list[1] / 360)

    return solar.topocentric_azimuth_angle(jct, param_list)

def azimuth_fast(when, param_list):
    """
    docstring goes here
    """
    # expect -50 degrees for solar.get_azimuth(
    #     42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 18, 0, 0))
    latitude = param_list[0]
    longitude = param_list[1]
    day = when.utctimetuple().tm_yday
    declination_rad = math.radians(declination(day))
    latitude_rad = math.radians(latitude)
    hour_angle_rad = math.radians(hour_angle(when, longitude))
    altitude_rad = math.radians(altitude(when, param_list))

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

def solar_test(param_list):
    """
    docstring goes here
    """
    latitude_deg = 42.364908
    longitude_deg = -71.112828
    when = datetime.datetime(
        2003, 10, 17, 0, 0, 0, tzinfo=None)
    # when = datetime.datetime.utcnow()
    thirty_minutes = datetime.timedelta(hours=0.5)
    param_list[0] = latitude_deg
    param_list[1] = longitude_deg
    for _idx in range(48):
        timestamp = when.ctime()
        altitude_deg = altitude(when, param_list) - 180
        azimuth_deg = azimuth(when, param_list)
        power = radiation.radiation_direct(when, altitude_deg)
        if altitude_deg > 0:
            print(timestamp, altitude_deg, azimuth_deg, power)
        when = when + thirty_minutes
