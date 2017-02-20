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
import pysolar.constants

STANDARD_PRESSURE = pysolar.constants.STANDARD_PRESSURE
STANDARD_TEMPERATURE = pysolar.constants.STANDARD_TEMPERATURE
EARTH_TEMPERATURE_LAPSE_RATE = pysolar.constants.EARTH_TEMPERATURE_LAPSE_RATE
AIR_GAS_CONSTANT = pysolar.constants.AIR_GAS_CONSTANT
EARTH_GRAVITY = pysolar.constants.EARTH_GRAVITY
EARTH_ATMOSPHERE_MOLAR_MASS = pysolar.constants.EARTH_ATMOSPHERE_MOLAR_MASS

# too many arguments in this method call. Five is recommended maximum
# perhaps pass in a list or tuple.
def pressure_with_elevation(hgt,
                            psi=STANDARD_PRESSURE,
                            stt=STANDARD_TEMPERATURE,
                            tlr=EARTH_TEMPERATURE_LAPSE_RATE,
                            hbl=0.0,
                            air=AIR_GAS_CONSTANT,
                            gfc=EARTH_GRAVITY,
                            amm=EARTH_ATMOSPHERE_MOLAR_MASS):
    """
    This function returns an estimate of the pressure in pascals as a function of
    elevation above sea level.
    NOTES:
      * This equation is only accurate up to 11,000 meters
      * results might be odd for elevations below 0 (sea level), like Dead Sea.
    hgt = elevation relative to sea level (m)
    psi = static pressure (pascals)
    stt= temperature (kelvin)
    tlr = temperature lapse rate (kelvin/meter)
    hbl = height at the bottom of the layer
    air = universal gas constant for air
    gfc = gravitational acceleration
    amm = Molar mass of atmosphere
    P = Ps * (Ts / ((Ts + Tl) * (h - Hb))) ^ ((g * M)/(R * Tl))
    returns pressure in pascals
    """
    if hgt > 11000.0:
        warnings.warn \
          (
              """
              Elevation used exceeds the recommended maximum elevation \n
              for this function (11,000m)\n
              """
          )
    #end if
    return \
        psi * (stt / (stt + tlr * (hgt - hbl))) ** ((gfc * amm) / (air * tlr))
#end get_pressure_with_elevation

def temperature_with_elevation(hgt,
                               stt=STANDARD_TEMPERATURE,
                               tlr=EARTH_TEMPERATURE_LAPSE_RATE):
    """
    This function returns an estimate of temperature as a function above sea level.
    NOTES:
      * This equation is only accurate up to 11,000 meters
      * results might be odd for elevations below 0 (sea level), like Dead Sea.
    stt = temperature (kelvin)
    tlr = temperature lapse rate (kelvin/meter)
    returns temp in kelvin
    """
    return stt + hgt *tlr
#end get_temperature_with_elevation

def elevation_test():
    """
    doc
    """
    print("Elevation(m) Pressure(Pa) Temperature(K)")
    hgt = 0
    for _idx in range(11):
        pwe = pressure_with_elevation(hgt)
        twe = temperature_with_elevation(hgt)
        print("%i %i %i" % (hgt, pwe, twe))
        hgt += 1000
    #end for
#end elevation_test
if __name__ == "__main__":
    elevation_test()
#end if
