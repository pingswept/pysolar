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
from .constants import \
    julian_day_offset, \
    gregorian_day_offset, \
    seconds_per_day, \
    compute_delta_t

def get_julian_century(julian_day):
    return (julian_day - 2451545.0) / 36525.0

def get_julian_day(when):
    "returns the Julian day number (including fraction of a day) corresponding to" \
    " the specified date/time. This version assumes the proleptic Gregorian calender;" \
    " trying to adjust for pre-Gregorian dates/times seems pointless when the changeover" \
    " happened over such wildly varying times in different regions."
    return \
        when.timestamp() / seconds_per_day + gregorian_day_offset + julian_day_offset

def get_julian_ephemeris_day(julian_day):
    """delta_seconds is the value referred to by astronomers as Delta-T, defined as the difference between
    Dynamical Time (TD) and Universal Time (UT).

    More details: http://en.wikipedia.org/wiki/DeltaT

    """
    return \
        julian_day + compute_delta_t(from_julian_day(julian_day)) / seconds_per_day

def from_julian_day(jd, tz = datetime.timezone.utc) :
    "returns a datetime object corresponding to the specified Julian day number," \
    " which can include fractions of a day."
    return \
        datetime.datetime.fromtimestamp \
          (
            timestamp = (jd - julian_day_offset - gregorian_day_offset) * seconds_per_day,
            tz = tz
          )
#end from_julian_day

def get_julian_ephemeris_century(julian_ephemeris_day):
    return (julian_ephemeris_day - 2451545.0) / 36525.0

def get_julian_ephemeris_millennium(julian_ephemeris_century):
    return (julian_ephemeris_century / 10.0)
