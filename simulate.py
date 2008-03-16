#!/usr/bin/python

#    Library for calculating location of the sun

#    Copyright 2007 Brandon Stafford
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

import datetime
import solar

def BuildTimeList(start_utc_datetime, end_utc_datetime, step_minutes):

	step = step_minutes * 60
	time_list = []
	span = end_utc_datetime - start_utc_datetime
	dt = datetime.timedelta(seconds = step)
	print span
	return map(lambda n: start_utc_datetime + dt * n, range((span.days * 86400 + span.seconds) / step))

def SimulateSpan(latitude_deg, longitude_deg, start_utc_datetime, end_utc_datetime, step_minutes):
	
	time_list = buildTimeList(start_utc_datetime, end_utc_datetime, step_minutes)
	
	for time in time_list:
		print 'Altitude: ' + str(solar.GetAltitude(latitude_deg, longitude_deg, time)) + ' Azimuth: ' + str(solar.GetAzimuth(latitude_deg, longitude_deg, time))
