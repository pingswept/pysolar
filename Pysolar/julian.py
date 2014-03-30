#!/usr/bin/python

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

"""This file contains all the functions related to the Julian calendar, which
are used in calculating the position of the sun relative to the earth

"""
import math

def GetJulianCentury(julian_day):
    return (julian_day - 2451545.0) / 36525.0

def GetJulianDay(utc_datetime):
    """This function is based on NREL/TP-560-34302 by Andreas and Reda

    This function does not accept years before 0 because of the bounds check
    on Python's datetime.year field.

    """
    year = utc_datetime.year
    month = utc_datetime.month
    if(month <= 2.0):        # shift to accomodate leap years?
        year = year - 1.0
        month = month + 12.0
    day = utc_datetime.day + (((utc_datetime.hour * 3600.0) + (utc_datetime.minute * 60.0) + utc_datetime.second + (utc_datetime.microsecond / 1000000.0)) / 86400.0)
    gregorian_offset = 2.0 - (year // 100.0) + ((year // 100.0) // 4.0)
    julian_day = math.floor(365.25 * (year + 4716.0)) + math.floor(30.6001 * (month + 1.0)) + day - 1524.5
    if (julian_day <= 2299160.0):
        return julian_day # before October 5, 1852
    else:
        return julian_day + gregorian_offset # after October 5, 1852

def GetJulianEphemerisCentury(julian_ephemeris_day):
    return (julian_ephemeris_day - 2451545.0) / 36525.0

def GetJulianEphemerisDay(julian_day, delta_seconds = 66.0):
    """delta_seconds is the value referred to by astronomers as Delta-T, defined as the difference between
    Dynamical Time (TD) and Universal Time (UT). In 2007, it's around 65 seconds.
    A list of values for Delta-T can be found here: ftp://maia.usno.navy.mil/ser7/deltat.data

    More details: http://en.wikipedia.org/wiki/DeltaT

    """
    return julian_day + (delta_seconds / 86400.0)

def GetJulianEphemerisMillenium(julian_ephemeris_century):
    return (julian_ephemeris_century / 10.0)
