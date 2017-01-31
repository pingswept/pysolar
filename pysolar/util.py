# -*- coding: utf-8 -*-
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

"""Additional support functions for solar geometry, astronomy, radiation correlation

:Original author: Simeon Nwaogaidu
:Contact: SimeonObinna.Nwaogaidu AT lahmeyer DOT de

:Additional author: Holger Zebner
:Contact: holger.zebner AT lahmeyer DOT de

:Additional author: Brandon Stafford

"""
from datetime import \
    datetime, \
    timedelta
import math
from . import solar, constants

# Some default constants

AM_DEFAULT = 2.0             # Default air mass is 2.0
TL_DEFAULT = 1.0             # Default Linke turbidity factor is 1.0
SC_DEFAULT = 1367.0          # Solar constant in W/m^2 is 1367.0.
                             # Note that this value could vary by +/-4 W/m^2
TY_DEFAULT = 365             # Total year number from 1 to 365 days
ELEVATION_DEFAULT = 0.0      # Default elevation is 0.0

# Useful equations for analysis

def sunrise_sunset(when, params_list):
    """This function calculates the astronomical sunrise and sunset times in local time.

    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting
        the north/south angular location of a place on a sphere.
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location
        in an east-west direction,relative to the Greenwich meridian.
    when : datetime.datetime
        date and time in any valid timezone, answers will be for same day in same timezone.

    Returns
    -------
    sunrise_time_dt : datetime.datetime
        Sunrise time in local time.
    sunset_time_dt : datetime.datetime
        Sunset time in local time.

    References
    ----------
    .. [1]
           http://www.skypowerinternational.com/
           manuals/7.1415.01.121_cm121_bed-anleitung_engl.pdf
    .. [2] http://pysolar.org/

    Examples
    --------
    >>> lat = 50.111512
    >>> lon = 8.680506
    >>> timezone_local = pytz.timezone('Europe/Berlin')
    >>> now = datetime.now(timezone_local)
    >>> sr, ss = sb.get_sunrise_sunset(lat, lon, now)
    >>> print('sunrise: ', sr)
    >>> print('sunset:', ss)

    """

    utc_offset = when.utcoffset()
    if utc_offset != None:
        utc_offset = utc_offset.total_seconds()
    else:
        utc_offset = 0
    #end if
    day = when.utctimetuple().tm_yday # Day of the year
    sha = utc_offset / 3600 * 15.0 - params_list[2] # Solar hour angle
    tta = math.radians(279.134 + 0.985647 * day) # Time adjustment angle
    time_adst = \
        (
            (
                5.0323
                -
                100.976 * math.sin(tta)
                +
                595.275 * math.sin(2 * tta)
                +
                3.6858 * math.sin(3 * tta)
                -
                12.47 * math.sin(4 * tta)
                -
                430.847 * math.cos(tta)
                +
                12.5024 * math.cos(2 * tta)
                +
                18.25 * math.cos(3 * tta)
            )
            /
            3600
        ) # Time adjustment in hours
    ton = 12 + sha / 15.0 - time_adst # Time of noon
    sunn = \
        (
            (
                math.pi / 2
                -
                math.radians(constants.EARTH_AXIS_INCLINATION)
                *
                math.tan(math.radians(params_list[1]))
                *
                math.cos(2 * math.pi * day / 365.25)
            )
            *
            (12 / math.pi)
        )
    same_day = datetime(year=when.year, month=when.month, day=when.day, tzinfo=when.tzinfo)
    sunrise_time = same_day + timedelta(hours=ton - sunn + time_adst)
    sunset_time = same_day + timedelta(hours=ton + sunn - time_adst)
    return sunrise_time, sunset_time

def get_sunrise_time(when, params_list):
    "Wrapper for get_sunrise_sunset that returns just the sunrise time."
    return sunrise_sunset(when, params_list)[0]

def get_sunset_time(when, params_list):
    "Wrapper for get_sunrise_sunset that returns just the sunset time."
    return sunrise_sunset(when, params_list)[1]

def mean_earth_sun_distance(when):
    """Mean Earth-Sun distance is the arithmetical mean of the maximum and minimum distances
    between a planet (Earth) and the object about which it revolves (Sun). However,
    the function is used to  calculate the Mean earth sun distance.

    Parameters
    ----------
    when : datetime.datetime
        date/time for which to do the calculation

    Returns
    -------
    KD : float
        Mean earth sun distance

    References
    ----------
    .. [1] http://sunbird.jrc.it/pvgis/solres/solmod3.htm#clear-sky%20radiation
    .. [2] R. aguiar and et al, "The ESRA user guidebook, vol. 2. database",
           models and exploitation software-Solar radiation models, p.113
    """

    return 1 - 0.0335 * math.sin(2 * math.pi * (when.utctimetuple().tm_yday - 94)) / 365

def extraterrestrial_irrad(when, params_list, spc=SC_DEFAULT):
    """
    Equation calculates Extratrestrial radiation. Solar radiation incident outside the earth's
    atmosphere is called extraterrestrial radiation. On average the extraterrestrial irradiance
    is 1367 Watts/meter2 (W/m2). This value varies by + or - 3 percent as the earth orbits the sun.
    The earth's closest approach to the sun occurs around January 4th and it is furthest
    from the sun around July 5th.

    Parameters
    ----------
    when : datetime.datetime
        date/time for which to do the calculation
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting the north/south angular location
        of a place on a sphere.
    longitude_deg : float
        longitude in decimal degree.
        Longitude shows your location in an east-west direction,
        relative to the Greenwich meridian.
    SC : float
        The solar constant is the amount of incoming solar electromagnetic radiation per unit area,
        measured on the outer surface of Earth's atmosphere in a plane perpendicular to the rays.
        It is measured by satellite to be roughly 1366 watts per square meter (W/m^2)

    Returns
    -------
    EXTR1 : float
        Extraterrestrial irradiation

    References
    ----------
    .. [1] http://solardat.uoregon.edu/SolarRadiationBasics.html
    .. [2] Dr. J. Schumacher and et al,"INSEL LE(Integrated Simulation Environment Language)
           Block reference",p.68

    """
    day = when.utctimetuple().tm_yday
    cos_ab = math.cos(2 * math.pi * (day - 1.0) / (365.0))
    sin_bc = math.sin(2 * math.pi * (day - 1.0) / (365.0))
    cos_cd = math.cos(2 * (2 * math.pi * (day - 1.0) / (365.0)))
    sin_df = math.sin(2 * (2 * math.pi * (day - 1.0) / (365.0)))
    decl = solar.declination(day)
    lha = solar.hour_angle(when, params_list[2])
    zap = math.sin(
        params_list[1]) * math.sin(decl) + math.cos(params_list[1]) * math.cos(decl) * math.cos(lha)

    return spc * zap * (
        1.00010 + 0.034221 * cos_ab + 0.001280 * sin_bc + 0.000719 * cos_cd + 0.000077 * sin_df)


def declination_degree(when, params_list):
    """
    The declination of the sun is the angle between Earth's equatorial plane and a line
    between the Earth and the sun. It varies between 23.45 degrees and -23.45 degrees,
    hitting zero on the equinoxes and peaking on the solstices.

    Parameters
    ----------
    when : datetime.datetime
        date/time for which to do the calculation
    TY : float
        Total number of days in a year. eg. 365 days per year,(no leap days)

    Returns
    -------
    DEC : float
        The declination of the Sun

    References
    ----------
    .. [1] http://pysolar.org/

    """
    return constants.EARTH_AXIS_INCLINATION * math.sin(
        2 * math.pi / params_list[7] * (when.utctimetuple().tm_yday - 81))


def solar_elevation_func_clear(when, params_list):
    """Equation calculates Solar elevation function for clear sky type.

    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting
        the north/south angular location of a place on a sphere.
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location
        in an east-west direction,relative to the Greenwich meridian.
    when : datetime.datetime
        date/time for which to do the calculation
    temperature : float
        atmospheric temperature
   pressure : float
        pressure in pascals
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point,
        often the mean sea level.

    Returns
    -------
    SOLALTC : float
        Solar elevation function clear sky

    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data: present status
            and proposed new approaches", energy 30 (2005), pp 1533 - 1549.

    """

    default = None
    altitude = solar.altitude(when, params_list, default)
    return (
        0.038175 + (
            1.5458 * (math.sin(altitude))) + ((-0.59980) * (0.5 * (1 - math.cos(2 * (altitude))))))

def solar_el_function_overcast(when, params_list):
    """ The function calculates solar elevation function for overcast sky type.
    This associated hourly overcast radiation model is based on the estimation of the
    overcast sky transmittance with the sun directly overhead combined with the application
    of an over sky elavation function to estimate the overcast day global irradiation
    value at any solar elevation.

    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree.
        A geographical term denoting the north/south angular location of a place on a sphere.
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location in an east-west direction,
        relative to the Greenwich meridian.
    when : datetime.datetime
        date/time for which to do the calculation
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point,
        often the mean sea level.
    temperature : float
        atmospheric temperature
    pressure : float
        pressure in pascals

    Returns
    -------
    SOLALTO : float
        Solar elevation function overcast

    References
    ----------
    .. [1] Prof. Peter Tregenza,"Solar radiation and daylight models", p.89.

    .. [2] Also accessible through Google Books: http://tinyurl.com/5kdbwu
        Tariq Muneer, "Solar Radiation and Daylight Models, Second Edition:
        For the Energy Efficient Design of Buildings"

    """
    altitude = solar.altitude(when, params_list)
    return (
        -0.0067133 + (
            0.78600 * (math.sin(altitude)))) + (0.22401 * (0.5 * (1 - math.cos(2 * altitude))))


def diffuse_transmittance(params_list):
    """
    Equation calculates the Diffuse_transmittance and the is the Theoretical Diffuse Irradiance
    on a horizontal surface when the sun is at the zenith.

    Parameters
    ----------
    TL : float
        Linke turbidity factor

    Returns
    -------
    DT : float
        diffuse_transmittance

    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data:
           present status and proposed new approaches", energy 30 (2005), pp 1533 - 1549.

    """
    return -21.657 + 41.752 * params_list[9] + 0.51905 * params_list[9] * params_list[9]


def diffuse_underclear(when, params_list):
    """Equation calculates diffuse radiation under clear sky conditions.

    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree.
        A geographical term denoting the north/south angular location of a place on a sphere.
    longitude_deg : float
        longitude in decimal degree.
        Longitude shows your location in an east-west direction,relative to the
        Greenwich meridian.
    when : datetime.datetime
        date/time for which to do the calculation
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point,
        often the mean sea level.
    temperature : float
        atmospheric temperature
    pressure : float
        pressure in pascals
    TL : float
        Linke turbidity factor

    Returns
    -------
    DIFFC : float
        Diffuse Irradiation under clear sky

    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data:
           present status and proposed new approaches", energy 30 (2005), pp 1533 - 1549.

    """
    dtl = -21.657 + 41.752 * params_list[9] + 0.51905 * params_list[9] * params_list[9]
    altitude = solar.altitude(when, params_list)

    return mean_earth_sun_distance(when) * dtl * altitude

def diffuse_underovercast(when, params_list):
    """Function calculates the diffuse radiation under overcast conditions.

    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree.
        A geographical term denoting the north/south angular location of a place on a
        sphere.
    longitude_deg : float
        longitude in decimal degree.
        Longitude shows your location in an east-west direction,relative to the
        Greenwich meridian.
    when : datetime.datetime
        date/time for which to do the calculation
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point,
        often the mean sea level.
    temperature : float
        atmospheric temperature
    pressure : float
        pressure in pascals
    TL : float
        Linke turbidity factor

    Returns
    -------
    DIFOC : float
        Diffuse Irradiation under overcast

    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data:
           present status and proposed new approaches", energy 30 (2005), pp 1533 - 1549.

    """
    dtl = -21.657 + 41.752 * params_list[9] + 0.51905 * params_list[9] * params_list[9]

    difoc = (
        (mean_earth_sun_distance(when)) * dtl * (
            solar.altitude(when, params_list)))
    return difoc

def direct_underclear(when, params_list):
    """Equation calculates direct radiation under clear sky conditions.

    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree.
        A geographical term denoting the north/south angular location of a
        place on a sphere.
    longitude_deg : float
        longitude in decimal degree.
        Longitude shows your location in an east-west direction,relative to the
        Greenwich meridian.
    when : datetime.datetime
        date/time for which to do the calculation
    temperature : float
        atmospheric temperature
    pressure : float
        pressure in pascals
    TY : float
        Total number of days in a year. eg. 365 days per year,(no leap days)
    AM : float
        Air mass.
        An Air Mass is a measure of how far light travels through the Earth's atmosphere.
        One air mass, or AM1, is the thickness of the Earth's atmosphere.
        Air mass zero (AM0) describes solar irradiance in space,
        where it is unaffected by the atmosphere.
        The power density of AM1 light is about 1,000 W/m^2
    TL : float
        Linke turbidity factor
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point,
        often the mean sea level.

    Returns
    -------
    DIRC : float
        Direct Irradiation under clear

    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data: \
           present status and proposed new approaches", energy 30 (2005), pp 1533 - 1549.

    """
    aud = mean_earth_sun_distance(when)

    dec = declination_degree(when, params_list[7])

    dirc = (
        1367 * aud * math.exp(-0.8662 * params_list[8] * params_list[9] * dec * math.sin(
            solar.altitude(when, params_list))))

    return dirc

# too many argument parameters. who calls this? we need to group those defaults.
# 5 is the recommended limit.
def global_irradiance_clear(dirc, diffc, when, params_list):

    """Equation calculates global irradiance under clear sky conditions.

    Parameters
    ----------
    DIRC : float
        Direct Irradiation under clear
    DIFFC : float
        Diffuse Irradiation under clear sky

    latitude_deg : float
        latitude in decimal degree.
        A geographical term denoting the north/south angular location of a place
        on a sphere.
    longitude_deg : float
        longitude in decimal degree.
        Longitude shows your location in an east-west direction,relative to
        the Greenwich meridian.
    when : datetime.datetime
        date/time for which to do the calculation
    temperature : float
        atmospheric temperature
    pressure : float
        pressure in pascals
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point,
        often the mean sea level.
    TY : float
        Total number of days in a year. eg. 365 days per year,(no leap days)
    AM : float
        Air mass. An Air Mass is a measure of how far light travels through the Earth's atmosphere.
        One air mass, or AM1, is the thickness of the Earth's atmosphere.
        Air mass zero (AM0) describes solar irradiance in space,
        where it is unaffected by the atmosphere.
        The power density of AM1 light is about 1,000 W/m.

    TL : float
        Linke turbidity factor
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point,
        often the mean sea level.

    Returns
    -------
    ghic : float
        Global Irradiation under clear sky

    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data:
              present status and proposed new approaches", energy 30 (2005), pp 1533 - 1549.

    """
    dirc = direct_underclear(when, params_list)

    diffc = diffuse_underclear(when, params_list)

    ghic = (dirc + diffc)

    return ghic


def global_irradiance_overcast(when, params_list):
    """Calculated Global is used to compare to the Diffuse under overcast conditions.
    Under overcast skies, global and diffuse are expected to be equal due to the absence of the beam
    component.

    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree.
        A geographical term denoting the north/south angular location of a place on a sphere.
    longitude_deg : float
        longitude in decimal degree.
        Longitude shows your location in an east-west direction,
        relative to the Greenwich meridian.
    when : datetime.datetime
        date/time for which to do the calculation
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point,
        often the mean sea level.
    temperature : float
        atmospheric temperature
    pressure : float
        pressure in pascals

    Returns
    -------
    ghioc : float
        Global Irradiation under overcast sky

    References
    ----------
    .. [1] S. Younes, R.Claywell and el al, "Quality
            control of solar radiation data: present status
            and proposed new approaches", energy 30
            (2005), pp 1533 - 1549.

    """
    ghioc = (
        572 * (
            solar.altitude(when, params_list)))

    return ghioc


def diffuse_ratio(diff_data, ghi_data):
    """Function calculates the Diffuse ratio.

    Parameters
    ----------
    diff_data : array_like
        Diffuse horizontal irradiation data
    ghi_data : array_like
        global horizontal irradiation data array

    Returns
    -------
    diff_ratio : float
        diffuse_ratio

    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data:
           present status and proposed new approaches", energy 30 (2005), pp 1533 - 1549.

    """
    diff_ratio = diff_data/ghi_data

    return diff_ratio


def clear_index(ghi_data, when, params_list):

    """This calculates the clear index ratio.

    Parameters
    ----------
    ghi_data : array_like
        global horizontal irradiation data array
    when : datetime.datetime
        date/time for which to do the calculation
    latitude_deg : float
        latitude in decimal degree.
        A geographical term denoting the north/south angular location of a place on a sphere.
    longitude_deg : float
        longitude in decimal degree.
        Longitude shows your location in an east-west direction,relative to the Greenwich meridian.

    Returns
    -------
    clr_index_ratio : float
        Clear index ratio

    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data:
           present status and proposed new approaches", energy 30 (2005), pp 1533 - 1549.

    """
    params = extraterrestrial_irrad(when, params_list)

    clr_index_ratio = (ghi_data / params)

    return clr_index_ratio
