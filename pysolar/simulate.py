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

"""Support functions for horizon calculation

"""
from . import numeric as math
import datetime
from . import constants
from . import radiation
from . import solar

def datetime_range(start_datetime, end_datetime, step_minutes):
    '''yields a sequence of datetimes evenly spaced apart by step_minutes.'''
    step = step_minutes * 60
    span = end_datetime - start_datetime
    dt = datetime.timedelta(seconds = step)
    for n in range((span.days * constants.seconds_per_day + span.seconds) // step) :
        yield start_datetime + dt * n
    #end for
#end datetime_range

def simulate_span(latitude_deg, longitude_deg, horizon, start_datetime, end_datetime, step_minutes, elevation = 0, temperature = constants.standard_temperature, pressure = constants.standard_pressure):
    '''simulates the motion of the sun over a time span and location of your choosing.

    The start and end points are set by datetime objects, which can be created with
    the standard Python datetime module like this:
    import datetime
    start = datetime.datetime(2008, 12, 23, 23, 14, 0)
    '''
    alt_zero = 380
    for time in datetime_range(start_datetime, end_datetime, step_minutes) :
        alt = solar.get_altitude(latitude_deg, longitude_deg, time, elevation, temperature, pressure)
        azi = solar.get_azimuth(latitude_deg, longitude_deg, time, elevation)
        shade = horizon[round(azi)]
        if shade < alt_zero - round(alt_zero * math.sin(math.radians(alt))) :
            rad = 0
        else :
            rad = radiation.get_radiation_direct(time, alt)
        #end if
        yield time, alt, azi, rad, shade
    #end for
#end simulate_span

#       xs = shade.GetXShade(width, 120, azimuth_deg)
#       ys = shade.GetYShade(height, 120, altitude_deg)
#       shaded_area = xs * ys
#       shaded_percentage = shaded_area/area
# import simulate, datetime; s = datetime.datetime(2008,1,1); e = datetime.datetime(2008,1,5); simulate.simulate_span(42.0, -70.0, s, e, 30)
