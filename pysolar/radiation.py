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

"""Calculate different kinds of radiation components via default values

"""
from . import numeric as math

def get_air_mass_ratio(altitude_deg):
    # from Masters, p. 412
    try :
        result = 1 / math.sin(math.radians(altitude_deg))
    except ZeroDivisionError :
        result = float("inf")
    #end try
    return result
#end get_air_mass_ratio

def get_apparent_extraterrestrial_flux(day):
    # from Masters, p. 412
    return 1160 + (75 * math.sin(2 * math.pi / 365 * (day - 275)))
#end get_apparent_extraterrestrial

def get_optical_depth(day):
    # from Masters, p. 412
    return 0.174 + (0.035 * math.sin(2 * math.pi / 365 * (day - 100)))
#end get_optical_depth

def get_radiation_direct(when, altitude_deg):
    # from Masters, p. 412
    is_daytime = (altitude_deg > 0)
    day = math.tm_yday(when)
    flux = get_apparent_extraterrestrial_flux(day)
    optical_depth = get_optical_depth(day)
    air_mass_ratio = get_air_mass_ratio(altitude_deg)
    return flux * math.exp(-1 * optical_depth * air_mass_ratio) * is_daytime
#end get_radiation_direct
