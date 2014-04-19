#!/usr/bin/python

#    Copyright Sean T. Hammond
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

"""Various elevation-related calculations

"""
import math

def GetPressureWithElevation(h, Ps=101325.00, Ts=288.15, Tl=-0.0065, Hb=0.0, R=8.31432, g=9.80665, M=0.0289644):
	#This function returns an estimate of the pressure in pascals as a function of elevation above sea level
	#NOTE: This equation is only accurate up to 11,000 meters
	#NOTE: results might be odd for elevations below 0 (sea level), like Dead Sea.
	#h=elevation relative to sea level (m)
	#Ps= static pressure (pascals) = 101325.00 P
	#Ts= standard temperature (kelvin) = 288.15 K
	#Tl= temperature lapse rate (kelvin/meter) = -0.0065 K/m
	#Hb= height at the bottom of the layer = 0
	#R= universal gas constant for air = 8.31432 N*m/s^2
	#g= gravitational acceleration for earth = 9.80665 m/s^2
	#M= Molar mass of Earth's atmosphere = 0.0289644 kg/mol
	#P=Ps*(Ts/((Ts+Tl)*(h-Hb)))^((g*M)/(R*Tl))
	#returns pressure in pascals
	if h>11000.0: print("WARNING: Elevation used exceeds the recommended maximum elevation for this function (11,000m)")
	theDenominator = Ts+(Tl*(h-Hb))
	theExponent=(g*M)/(R*Tl)
	return Ps*(Ts/theDenominator)**theExponent

def GetTemperatureWithElevation(h, Ts=288.15, Tl=-0.0065):
	#This function returns an estimate of temperature as a function above sea level
	#NOTE: this is only accurate up to 11,000m
	#NOTE: results might be odd for elevations below 0 (sea level), like Dead Sea.
	#Ts= standard temperature (kelvin) = 288.15 K
	#Tl= temperature lapse rate (kelvin/meter) = -0.0065 K/m
	#returns temp in kelvin
	return Ts+(h*Tl)

def ElevationTest():
	print("Elevation(m) Pressure(Pa) Temperature(K)")
	h=0
	for i in range(11):
		P=GetPressureWithElevation(h)
		T=GetTemperatureWithElevation(h)
		print("%i %i %i" % (h, P, T))
		h=h+1000


