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
from .constants import \
    standard_pressure, \
    standard_temperature, \
    earth_temperature_lapse_rate, \
    air_gas_constant, \
    earth_gravity, \
    earth_atmosphere_molar_mass

def get_pressure_with_elevation(h, Ps=standard_pressure, Ts=standard_temperature, Tl=earth_temperature_lapse_rate, Hb=0.0, R=air_gas_constant, g=earth_gravity, M=earth_atmosphere_molar_mass):
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

def get_temperature_with_elevation(h, Ts=standard_temperature, Tl=earth_temperature_lapse_rate):
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
    for _ in range(11):
        P = get_pressure_with_elevation(h)
        T = get_temperature_with_elevation(h)
        print("%i %i %i" % (h, P, T))
        h += 1000
    #end for
#end elevation_test
