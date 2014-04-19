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

"""Support functions for horizon calculation 

"""
import datetime
from . import radiation
from . import solar
from math import *

def BuildTimeList(start_utc_datetime, end_utc_datetime, step_minutes):
	'''Create a list of sample points evenly spaced apart by step_minutes.'''
	step = step_minutes * 60
	time_list = []
	span = end_utc_datetime - start_utc_datetime
	dt = datetime.timedelta(seconds = step)
	return [start_utc_datetime + dt * n for n in range((span.days * 86400 + span.seconds) / step)]

def CheckAgainstHorizon(power):
    (time, alt, az, radiation, shade) = power
    alt_zero = 380

    if shade < alt_zero - int(alt_zero * sin(radians(alt))):
        radiation = 0

    return (time, alt, az, radiation, shade)

def SimulateSpan(latitude_deg, longitude_deg, horizon, start_utc_datetime, end_utc_datetime, step_minutes, elevation = 0, temperature_celsius = 25, pressure_millibars = 1013.25):
	'''Simulate the motion of the sun over a time span and location of your choosing.
	
	The start and end points are set by datetime objects, which can be created with
	the standard Python datetime module like this:
	import datetime
	start = datetime.datetime(2008, 12, 23, 23, 14, 0)
	'''
	time_list = BuildTimeList(start_utc_datetime, end_utc_datetime, step_minutes)
	
	angles_list = [(
		time,
		solar.GetAltitude(latitude_deg, longitude_deg, time, elevation, temperature_celsius, pressure_millibars),
		solar.GetAzimuth(latitude_deg, longitude_deg, time, elevation)
		) for time in time_list]	
	power_list = [(time, alt, az, radiation.GetRadiationDirect(time, alt), horizon[int(az)]) for (time, alt, az) in angles_list]
	return list(filter(CheckAgainstHorizon, power_list))
		
#		xs = shade.GetXShade(width, 120, azimuth_deg)
#		ys = shade.GetYShade(height, 120, altitude_deg)
#		shaded_area = xs * ys
#		shaded_percentage = shaded_area/area
# import simulate, datetime; s = datetime.datetime(2008,1,1); e = datetime.datetime(2008,1,5); simulate.SimulateSpan(42.0, -70.0, s, e, 30)
