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
import math

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

def get_diffuse_skyfactor(day):
     # from Masters, p. 416
     return 0.095 + 0.04 *  math.sin(math.radians((360 / 365) * (day - 100)))
#end get_diffuse_skyfactor

def get_direct_radiation(when, altitude_deg):
    # from Masters, p. 412
    if altitude_deg < 0:
        return 0.0
    day = when.utctimetuple().tm_yday
    flux = get_apparent_extraterrestrial_flux(day)
    optical_depth = get_optical_depth(day)
    air_mass_ratio = get_air_mass_ratio(altitude_deg)
    return flux * math.exp(-1 * optical_depth * air_mass_ratio)
#end get_direct_radiation

def get_diffuse_radiation(when, altitude_deg):
    # from Masters, p. 416
    return get_diffuse_radiation_on_collector(when, altitude_deg, 0)
#end get_diffuse_radiation

def get_direct_radiation_collector(when, altitude_deg, azimuth_deg, \
    collector_azimuth_deg, tilt_angle):
    # from Masters, p. 414
    cos_incidence_angle = (math.cos(math.radians(altitude_deg))
        * math.cos(math.radians(azimuth_deg - collector_azimuth_deg))
        * math.sin(math.radians(tilt_angle))
        + math.sin(math.radians(altitude_deg))
        * math.cos(math.radians(tilt_angle)))
    direct_radiation = get_direct_radiation(when, altitude_deg)
    return direct_radiation * cos_incidence_angle
#end get_direct_radiation_collector

def get_diffuse_radiation_on_collector(when, altitude_deg, tilt_angle):
    # from Masters, p. 416
    day = when.utctimetuple().tm_yday
    diffuse_sky_factor = get_diffuse_skyfactor(day)
    direct_radiation = get_direct_radiation(when, altitude_deg)
    return (diffuse_sky_factor * direct_radiation
       * ((1 + math.cos(math.radians(tilt_angle)))/2))
#end get_diffuse_radiation_on_collector

def get_radiation_reflected_collector(when, altitude_deg, tilt_angle, \
    reflectance):
    # from Masters, p. 418
    day = when.utctimetuple().tm_yday
    diffuse_sky_factor = get_diffuse_skyfactor(day)
    direct_radiation = get_direct_radiation(when, altitude_deg)
    return (reflectance * direct_radiation
        * (math.sin(math.radians(altitude_deg)) + diffuse_sky_factor)
        * ((1 - math.cos(math.radians(tilt_angle)))/2))
#end get_radiation_reflected_collector

def get_radiation_total_collector(when, altitude_deg, azimuth_deg, \
    collector_azimuth_deg, tilt_angle, reflectance):
    # from Masters, p. 419
    return (get_direct_radiation_collector(when, altitude_deg, azimuth_deg,
        collector_azimuth_deg, tilt_angle)
        + get_diffuse_radiation_on_collector(when, altitude_deg, tilt_angle)
        + get_radiation_reflected_collector(when, altitude_deg, tilt_angle,
        reflectance))
#end get_radiation_total_collector

def get_radiation_total(when,  altitude_deg):
    return (get_direct_radiation(when, altitude_deg)
        + get_diffuse_radiation(when, altitude_deg))
#end get_radiation_total
