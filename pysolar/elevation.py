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
from .constants import \
    standard_pressure, \
    standard_temperature, \
    earth_temperature_lapse_rate, \
    air_gas_constant, \
    earth_gravity, \
    earth_atmosphere_molar_mass

def GetPressureWithElevation(h, Ps=standard_pressure, Ts=standard_temperature, Tl=earth_temperature_lapse_rate, Hb=0.0, R=air_gas_constant, g=earth_gravity, M=earth_atmosphere_molar_mass):
    #This function returns an estimate of the pressure in pascals as a function of elevation above sea level
    #NOTE: This equation is only accurate up to 11,000 meters
    #NOTE: results might be odd for elevations below 0 (sea level), like Dead Sea.
    #h=elevation relative to sea level (m)
    #Ps= static pressure (pascals)
    #Ts= temperature (kelvin)
    #Tl= temperature lapse rate (kelvin/meter)
    #Hb= height at the bottom of the layer
    #R= universal gas constant for air
    #g= gravitational acceleration
    #M= Molar mass of atmosphere
    #P=Ps*(Ts/((Ts+Tl)*(h-Hb)))^((g*M)/(R*Tl))
    #returns pressure in pascals
    if h>11000.0: print("WARNING: Elevation used exceeds the recommended maximum elevation for this function (11,000m)")
    theDenominator = Ts+(Tl*(h-Hb))
    theExponent=(g*M)/(R*Tl)
    return Ps*(Ts/theDenominator)**theExponent

def GetTemperatureWithElevation(h, Ts=standard_temperature, Tl=earth_temperature_lapse_rate):
    #This function returns an estimate of temperature as a function above sea level
    #NOTE: this is only accurate up to 11,000m
    #NOTE: results might be odd for elevations below 0 (sea level), like Dead Sea.
    #Ts= temperature (kelvin)
    #Tl= temperature lapse rate (kelvin/meter)
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
