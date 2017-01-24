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
import warnings
import math
from .constants import \
    STANDARD_PRESSURE, \
    STANDARD_TEMPERATURE, \
    EARTH_TEMPERATURE_LAPSE_RATE, \
    AIR_GAS_CONSTANT, \
    EARTH_GRAVITY, \
    EARTH_ATMOSPHERE_MOLAR_MASS

def get_pressure_with_elevation(h, Ps=STANDARD_PRESSURE, Ts=STANDARD_TEMPERATURE, Tl=EARTH_TEMPERATURE_LAPSE_RATE, Hb=0.0, R=AIR_GAS_CONSTANT, g=EARTH_GRAVITY, M=EARTH_ATMOSPHERE_MOLAR_MASS):
    "This function returns an estimate of the pressure in pascals as a function of\n" \
    " elevation above sea level.\n" \
    "NOTES:\n" \
    "  * This equation is only accurate up to 11,000 meters\n" \
    "  * results might be odd for elevations below 0 (sea level), like Dead Sea.\n" \
    "h=elevation relative to sea level (m)\n" \
    "Ps= static pressure (pascals)\n" \
    "Ts= temperature (kelvin)\n" \
    "Tl= temperature lapse rate (kelvin/meter)\n" \
    "Hb= height at the bottom of the layer\n" \
    "R= universal gas constant for air\n" \
    "g= gravitational acceleration\n" \
    "M= Molar mass of atmosphere\n" \
    "P = Ps * (Ts / ((Ts + Tl) * (h - Hb))) ^ ((g * M)/(R * Tl))\n" \
    "returns pressure in pascals\n"
    if h > 11000.0 :
        warnings.warn \
          (
            "Elevation used exceeds the recommended maximum elevation for this function (11,000m)\n"
          )
    #end if
    return \
        Ps * (Ts / (Ts + Tl * (h - Hb))) ** ((g * M) / (R * Tl))
#end get_pressure_with_elevation

def get_temperature_with_elevation(h, Ts=STANDARD_TEMPERATURE, Tl=EARTH_TEMPERATURE_LAPSE_RATE):
    "This function returns an estimate of temperature as a function above sea level.\n" \
    "NOTES:\n" \
    "  * This equation is only accurate up to 11,000 meters\n" \
    "  * results might be odd for elevations below 0 (sea level), like Dead Sea.\n" \
    "Ts= temperature (kelvin)\n" \
    "Tl= temperature lapse rate (kelvin/meter)\n" \
    "returns temp in kelvin\n"
    return \
        Ts + h *Tl
#end get_temperature_with_elevation

def elevation_test():
    print("Elevation(m) Pressure(Pa) Temperature(K)")
    h = 0
    for i in range(11):
        P = get_pressure_with_elevation(h)
        T = get_temperature_with_elevation(h)
        print("%i %i %i" % (h, P, T))
        h += 1000
    #end for
#end elevation_test
