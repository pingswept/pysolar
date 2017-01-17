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
from . import constants

def pressure_with_elevation(has, vsp=constants.STANDARD_PRESSURE,
                            vtk=constants.STANDARD_TEMPERATURE,
                            tlr=constants.EARTH_TEMPERATURE_LAPSE_RATE,
                            vhb=0.0,
                            agc=constants.AIR_GAS_CONSTANT,
                            veg=constants.EARTH_GRAVITY,
                            mam=constants.EARTH_ATMOSPHERE_MOLAR_MASS):
    "This function returns an estimate of the pressure in pascals as a function of\n" \
    " elevation above sea level.\n" \
    "NOTES:\n" \
    "  * This equation is only accurate up to 11,000 meters\n" \
    "  * results might be odd for elevations below 0 (sea level), like Dead Sea.\n" \
    "has = elevation relative to sea level (m)\n" \
    "vsp = static pressure (pascals)\n" \
    "vtk = temperature (kelvin)\n" \
    "tlr = temperature lapse rate (kelvin / meter)\n" \
    "vhb = height at the bottom of the layer\n" \
    "agc = universal gas constant for air\n" \
    "veg = gravitational acceleration\n" \
    "mam = Molar mass of atmosphere\n" \
    "pip = vsp * (vtk / (vtk + tlr * (has - vhb))) ** ((veg * mam) / (agc * tlr))"\
    "returns pressure in pascals\n"
    if has > 11000.0:
        warnings.warn("Elevation used exceeds the recommended maximum elevation"
                      " for this function (11,000m)\n")
    #end if
    return vsp * (vtk / (vtk + tlr * (has - vhb))) ** ((veg * mam) / (agc * tlr))
#end get_pressure_with_elevation

def temperature_with_elevation(has, vtk=constants.STANDARD_TEMPERATURE,
                               tlr=constants.EARTH_TEMPERATURE_LAPSE_RATE):
    "This function returns an estimate of temperature as a function above sea level.\n" \
    "NOTES:\n" \
    "  * This equation is only accurate up to 11,000 meters\n" \
    "  * results might be odd for elevations below 0 (sea level), like Dead Sea.\n" \
    "vtk = temperature (kelvin)\n" \
    "tlr = temperature lapse rate (kelvin/meter)\n" \
    "returns temp in kelvin\n"
    return vtk + has * tlr
#end get_temperature_with_elevation

def elevation_test():
    """ test """
    print("Elevation(m) Pressure(Pa) Temperature(K)")
    has = 0
    for idx in range(11):
        pwe = pressure_with_elevation(has)
        twe = temperature_with_elevation(has)
        print("%i %i %i" % (has, pwe, twe))
        has += 1000
    #end for
#end elevation_test
