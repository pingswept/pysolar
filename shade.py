#!/usr/bin/python

#    Library for solar panel shading calculations

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

import math

def GetSideByLawOfCosines(side_a, side_b, included_angle_deg):
    return math.sqrt(pow((side_a), 2) + pow(side_b, 2) - (2 * side_a * side_b * math.cos(math.radians(included_angle_deg))))

def GetXShade(width, x_spacing, azimuth_deg):
    n = GetSideByLawOfCosines(width/2, x_spacing, azimuth_deg)
    p = (width/2) * math.sin(math.radians(azimuth_deg))
    theta_deg = math.degrees(math.asin(p/n))
    alpha_deg = azimuth_deg + theta_deg
    d = GetSideByLawOfCosines(width/2, n, alpha_deg)
    gamma_deg = math.degrees(math.asin((n * math.sin(math.radians(alpha_deg)))/d))
    shaded_width = d * math.cos(math.radians(gamma_deg))
    if(pow(d, 2) + pow(width/2, 2) < pow(n, 2)): # check for obtuse triangle
        shaded_width = 0
    #print "theta in deg:", theta_deg, "gamma in deg:", gamma_deg, "shaded width:", shaded_width
    return min(shaded_width, width)

def GetYShade(height, y_spacing, altitude_deg):
    return GetXShade(height, y_spacing, 90 - altitude_deg)
