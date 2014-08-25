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
import datetime
from .constants import seconds_per_day

def GetJulianCentury(julian_day):
    return (julian_day - 2451545.0) / 36525.0

def GetJulianDay(when):
    """This function is based on NREL/TP-560-34302 by Andreas and Reda

    This function does not accept years before 0 because of the bounds check
    on Python's datetime.year field.

    """
    if when.tzinfo != None and when.tzinfo != datetime.timezone.utc :
        when = when.astimezone(datetime.timezone.utc)
    #end if
    year = when.year
    month = when.month
    if(month <= 2.0):        # shift to accomodate leap years?
        year = year - 1.0
        month = month + 12.0
    day = when.day + (((when.hour * 3600.0) + (when.minute * 60.0) + when.second + (when.microsecond / 1000000.0)) / seconds_per_day)
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
    return julian_day + (delta_seconds / seconds_per_day)

def GetJulianEphemerisMillenium(julian_ephemeris_century):
    return (julian_ephemeris_century / 10.0)
