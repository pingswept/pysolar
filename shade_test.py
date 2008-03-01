#!/usr/bin/python

#    Test of solar panel shading calculations

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

import solar
import shade
import datetime
from pylab import *
#from itertools import izip

def ShadeTest():
	latitude_deg = 42.364908
	longitude_deg = -71.112828
	width = 100
	height = 200
	area = width * height
	d = datetime.datetime.utcnow()
	thirty_minutes = datetime.timedelta(hours = 0.5)
	times = []
	powers = []
	shade_x = []
	shade_y = []
	shaded_powers = []
	for i in range(48):
		timestamp = d.ctime()
		altitude_deg = solar.GetAltitude(latitude_deg, longitude_deg, d)
		azimuth_deg = solar.GetAzimuth(latitude_deg, longitude_deg, d)
		power = solar.GetRadiationDirect(d, altitude_deg)
		xs = shade.GetXShade(width, 120, azimuth_deg)
		ys = shade.GetYShade(height, 120, altitude_deg)
		shaded_area = xs * ys
		shaded_percentage = shaded_area/area
		if (altitude_deg > 0):
			times.append(float(d.hour) + (float(d.minute)/60) - 5) # - 5 to adjust to EST
			powers.append(power)
			shade_x.append(xs)
			shade_y.append(ys)
			shaded_powers.append(power * (1 - shaded_percentage))
			#print timestamp, "UTC", altitude_deg, azimuth_deg, power
		d = d + thirty_minutes
	print times
	print powers
	print shade_x
	
	plot(times, shaded_powers, times, powers)   # plot ends up with a line across it because x values wrap around
	show()                                      # could fix that with sort function below

#def sort(list_to_sort, order): # based on a function by Ron Adam on some Python mailing list
#    d = dict(izip(order, list_to_sort))
#    assert len(d) == len(list_to_sort)
#    list_to_sort[:] = list(d[v] for v in sorted(d))
#    return list_to_sort
