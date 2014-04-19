#!/usr/bin/env python

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
from datetime import datetime as dt
from datetime import timedelta
import math
import pytz
from pytz import all_timezones
from . import solar

# Some default constants

AM_default = 2.0             # Default air mass is 2.0
TL_default = 1.0             # Default Linke turbidity factor is 1.0 
SC_default = 1367.0          # Solar constant in W/m^2 is 1367.0. Note that this value could vary by +/-4 W/m^2 
TY_default = 365             # Total year number from 1 to 365 days
elevation_default = 0.0      # Default elevation is 0.0

# Useful equations for analysis

def GetSunriseSunset(latitude_deg, longitude_deg, utc_datetime, timezone):
    """This function calculates the astronomical sunrise and sunset times in local time.
    
    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting 
        the north/south angular location of a place on a sphere.            
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location 
        in an east-west direction,relative to the Greenwich meridian.        
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 )        
    timezone : float
        timezone as numerical value: GMT offset in hours. A time zone is a region of 
        the earth that has uniform standard time, usually referred to as the local time.
               
    Returns
    -------
    sunrise_time_dt : datetime.datetime
        Sunrise time in local time as datetime_obj.
    sunset_time_dt : datetime.datetime
        Sunset time in local time as datetime_obj.
            
    References
    ----------
    .. [1] http://www.skypowerinternational.com/pdf/Radiation/7.1415.01.121_cm121_bed-anleitung_engl.pdf
    .. [2] http://pysolar.org/
        
    Examples
    --------
    >>> gmt_offset = 1
    >>> lat = 50.111512
    >>> lon = 8.680506
    >>> timezone_local = 'Europe/Berlin'
    >>> utct = dt.datetime.utcnow()
    >>> sr, ss = sb.GetSunriseSunset(lat, lon, utct, gmt_offset)
    >>> print 'sunrise: ', sr
    >>> print 'sunset:', ss
   
    """

    # Day of the year
    day = solar.GetDayOfYear(utc_datetime)

    # Solar hour angle
    SHA = ((timezone)* 15.0 - longitude_deg)

    # Time adjustment
    TT = (279.134+0.985647*day)*math.pi/180

    # Time adjustment in hours
    time_adst = ((5.0323 - 100.976*math.sin(TT)+595.275*math.sin(2*TT)+
                  3.6858*math.sin(3*TT) - 12.47*math.sin(4*TT) - 430.847*math.cos(TT)+
                  12.5024*math.cos(2*TT) + 18.25*math.cos(3*TT))/3600)
 
    # Time of noon
    TON = (12 + (SHA/15.0) - time_adst)
    
    sunn = (math.pi/2-(23.45*math.pi/180)*math.tan(latitude_deg*math.pi/180)*
            math.cos(2*math.pi*day/365.25))*(180/(math.pi*15))

    # Sunrise_time in hours
    sunrise_time = (TON - sunn + time_adst)
 
    # Sunset_time in hours
    sunset_time = (TON + sunn - time_adst) 

    sunrise_time_dt = date_with_decimal_hour(utc_datetime, sunrise_time)    
    sunset_time_dt = date_with_decimal_hour(utc_datetime, sunset_time)    

    return sunrise_time_dt, sunset_time_dt

def GetSunriseTime(latitude_deg, longitude_deg, utc_datetime, timezone):
    "Wrapper for GetSunriseSunset that returns just the sunrise time" 
    sr, ss = GetSunriseSunset(latitude_deg, longitude_deg, utc_datetime, timezone)
    
    return sr

def GetSunsetTime(latitude_deg, longitude_deg, utc_datetime, timezone):
    "Wrapper for GetSunriseSunset that returns just the sunset time" 
    sr, ss = GetSunriseSunset(latitude_deg, longitude_deg, utc_datetime, timezone)    
    return ss

def mean_earth_sun_distance(utc_datetime):
    """Mean Earth-Sun distance is the arithmetical mean of the maximum and minimum distances
    between a planet (Earth) and the object about which it revolves (Sun). However, 
    the function is used to  calculate the Mean earth sun distance.
    
    Parameters
    ----------
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 ) 
                         
    Returns
    -------
    KD : float
        Mean earth sun distance
    
    References
    ----------
    .. [1] http://sunbird.jrc.it/pvgis/solres/solmod3.htm#clear-sky%20radiation
    .. [2] R. aguiar and et al, "The ESRA user guidebook, vol. 2. database", models and exploitation software-Solar 
            radiation models, p.113
    """   

    return (1 - (0.0335 * math.sin(360 * ((solar.GetDayOfYear(utc_datetime)) - 94)) / (365)))

def extraterrestrial_irrad(utc_datetime, latitude_deg, longitude_deg,SC=SC_default):
    """Equation calculates Extratrestrial radiation. Solar radiation incident outside the earth's
    atmosphere is called extraterrestrial radiation. On average the extraterrestrial irradiance
    is 1367 Watts/meter2 (W/m2). This value varies by + or - 3 percent as the earth orbits the sun. 
    The earth's closest approach to the sun occurs around January 4th and it is furthest
    from the sun around July 5th.
    
    Parameters
    ----------
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 )                   
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting the north/south angular location 
        of a place on a sphere.    
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location in an east-west direction,relative
        to the Greenwich meridian.    
    SC : float
        The solar constant is the amount of incoming solar electromagnetic radiation per unit area, measured 
        on the outer surface of Earth's atmosphere in a plane perpendicular to the rays.It is measured by 
        satellite to be roughly 1366 watts per square meter (W/m^2)
    
    Returns
    -------
    EXTR1 : float
        Extraterrestrial irradiation
    
    References
    ----------
    .. [1] http://solardat.uoregon.edu/SolarRadiationBasics.html
    .. [2] Dr. J. Schumacher and et al,"INSEL LE(Integrated Simulation Environment Language)Block reference",p.68
        
    """
    day = solar.GetDayOfYear(utc_datetime)
    ab = math.cos(2 * math.pi * (solar.GetDayOfYear(utc_datetime) - 1.0)/(365.0))
    bc = math.sin(2 * math.pi * (solar.GetDayOfYear(utc_datetime) - 1.0)/(365.0))
    cd = math.cos(2 * (2 * math.pi * (solar.GetDayOfYear(utc_datetime) - 1.0)/(365.0)))
    df = math.sin(2 * (2 * math.pi * (solar.GetDayOfYear(utc_datetime) - 1.0)/(365.0)))
    decl = solar.GetDeclination(day)
    ha = solar.GetHourAngle(utc_datetime, longitude_deg)
    ZA = math.sin(latitude_deg) * math.sin(decl) + math.cos(latitude_deg) * math.cos(decl) * math.cos(ha)
    
    return SC * ZA * (1.00010 + 0.034221 * ab + 0.001280 * bc + 0.000719 * cd + 0.000077 * df)


def declination_degree(utc_datetime, TY = TY_default ):
    """The declination of the sun is the angle between Earth's equatorial plane and a line 
    between the Earth and the sun. It varies between 23.45 degrees and -23.45 degrees,
    hitting zero on the equinoxes and peaking on the solstices.
    
    Parameters
    ----------
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 )        
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
    return 23.45 * math.sin((2 * math.pi / (TY)) * ((solar.GetDayOfYear(utc_datetime)) - 81))


def solarelevation_function_clear(latitude_deg, longitude_deg, utc_datetime,temperature_celsius = 25,
                                  pressure_millibars = 1013.25,  elevation = elevation_default):
    """Equation calculates Solar elevation function for clear sky type.
    
    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting 
        the north/south angular location of a place on a sphere.            
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location 
        in an east-west direction,relative to the Greenwich meridian.        
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 )         
    temperature_celsius : float
        Temperature is a physical property of a system that underlies the common notions of hot and cold.    
    pressure_millibars : float
        pressure_millibars    
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point, often the mean
        sea level.
    
    Returns
    -------
    SOLALTC : float
        Solar elevation function clear sky 
        
    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data: present status 
            and proposed new approaches", energy 30 (2005), pp 1533 - 1549.
    
    """
    altitude = solar.GetAltitude(latitude_deg, longitude_deg,utc_datetime, elevation, temperature_celsius,pressure_millibars)        
    return (0.038175 + (1.5458 * (math.sin(altitude))) + ((-0.59980) * (0.5 * (1 - math.cos(2 * (altitude))))))

def solarelevation_function_overcast(latitude_deg, longitude_deg, utc_datetime,
                                     elevation = elevation_default, temperature_celsius = 25,
                                     pressure_millibars = 1013.25):
    """ The function calculates solar elevation function for overcast sky type. 
    This associated hourly overcast radiation model is based on the estimation of the 
    overcast sky transmittance with the sun directly overhead combined with the application 
    of an over sky elavation function to estimate the overcast day global irradiation 
    value at any solar elevation.
    
    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting the north/south angular location of a place on a 
        sphere.            
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location in an east-west direction,relative to the 
        Greenwich meridian.        
    utc_datetime : date_object 
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 ) 
    elevation : float 
        The elevation of a geographic location is its height above a fixed reference point, often the mean sea level.        
    temperature_celsius : float 
        Temperature is a physical property of a system that underlies the common notions of hot and cold.    
    pressure_millibars : float
        pressure_millibars  
                               
    Returns
    -------
    SOLALTO : float
        Solar elevation function overcast
    
    References
    ----------
    .. [1] Prof. Peter Tregenza,"Solar radiation and daylight models", p.89.
    
    .. [2] Also accessible through Google Books: http://tinyurl.com/5kdbwu
        Tariq Muneer, "Solar Radiation and Daylight Models, Second Edition: For the Energy Efficient 
        Design of Buildings"  
            
    """
    altitude = solar.GetAltitude(latitude_deg, longitude_deg,utc_datetime, elevation, temperature_celsius,pressure_millibars)
    return ((-0.0067133) + (0.78600 * (math.sin(altitude)))) + (0.22401 * (0.5 * (1 - math.cos(2 * altitude))))


def diffuse_transmittance(TL = TL_default):
    """Equation calculates the Diffuse_transmittance and the is the Theoretical Diffuse Irradiance on a horizontal 
    surface when the sun is at the zenith.
    
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
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data: present status and proposed 
            new approaches", energy 30 (2005), pp 1533 - 1549.
    
    """
    return ((-21.657) + (41.752 * (TL)) + (0.51905 * (TL) * (TL)))


def diffuse_underclear(latitude_deg, longitude_deg, utc_datetime, elevation = elevation_default, 
                       temperature_celsius = 25, pressure_millibars = 1013.25, TL=TL_default):    
    """Equation calculates diffuse radiation under clear sky conditions.
    
    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting the north/south angular location of a place on 
        a sphere.            
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location in an east-west direction,relative to the 
        Greenwich meridian.        
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 )
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point, often the mean sea level.         
    temperature_celsius : float
        Temperature is a physical property of a system that underlies the common notions of hot and cold.    
    pressure_millibars : float
        pressure_millibars
    TL : float
        Linke turbidity factor     
    
    Returns
    -------
    DIFFC : float
        Diffuse Irradiation under clear sky
    
    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data: present status and proposed 
            new approaches", energy 30 (2005), pp 1533 - 1549.
    
    """    
    DT = ((-21.657) + (41.752 * (TL)) + (0.51905 * (TL) * (TL)))
    altitude = solar.GetAltitude(latitude_deg, longitude_deg,utc_datetime, elevation, temperature_celsius,pressure_millibars)

    return mean_earth_sun_distance(utc_datetime) * DT * altitude

def diffuse_underovercast(latitude_deg, longitude_deg, utc_datetime, elevation = elevation_default,
                          temperature_celsius = 25, pressure_millibars = 1013.25,TL=TL_default):    
    """Function calculates the diffuse radiation under overcast conditions.
    
    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting the north/south angular location of a place on a 
        sphere.            
    longitude_deg : float 
        longitude in decimal degree. Longitude shows your location in an east-west direction,relative to the 
        Greenwich meridian.        
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 )
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point, often the mean sea level.         
    temperature_celsius : float
        Temperature is a physical property of a system that underlies the common notions of hot and cold.    
    pressure_millibars : float
        pressure_millibars
    TL : float
        Linke turbidity factor       
    
    Returns
    -------
    DIFOC : float
        Diffuse Irradiation under overcast
    
    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data: present status and proposed 
            new approaches", energy 30 (2005), pp 1533 - 1549.
    
    """    
    DT = ((-21.657) + (41.752 * (TL)) + (0.51905 * (TL) * (TL)))
        
    DIFOC = ((mean_earth_sun_distance(utc_datetime)
              )*(DT)*(solar.GetAltitude(latitude_deg,longitude_deg, utc_datetime, elevation, 
                                        temperature_celsius, pressure_millibars)))    
    return DIFOC

def direct_underclear(latitude_deg, longitude_deg, utc_datetime, 
                      temperature_celsius = 25, pressure_millibars = 1013.25, TY = TY_default, 
                      AM = AM_default, TL = TL_default,elevation = elevation_default):    
    """Equation calculates direct radiation under clear sky conditions.
    
    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting the north/south angular location of a 
        place on a sphere.            
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location in an east-west direction,relative to the 
        Greenwich meridian.        
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 )           
    temperature_celsius : float
        Temperature is a physical property of a system that underlies the common notions of hot and cold.    
    pressure_millibars : float
        pressure_millibars
    TY : float
        Total number of days in a year. eg. 365 days per year,(no leap days)
    AM : float
        Air mass. An Air Mass is a measure of how far light travels through the Earth's atmosphere. One air mass,
        or AM1, is the thickness of the Earth's atmosphere. Air mass zero (AM0) describes solar irradiance in space,
        where it is unaffected by the atmosphere. The power density of AM1 light is about 1,000 W/m^2
    TL : float
        Linke turbidity factor 
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point, often the mean 
        sea level.        
    
    Returns
    -------
    DIRC : float
        Direct Irradiation under clear
        
    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data: present status and proposed 
           new approaches", energy 30 (2005), pp 1533 - 1549.
    
    """
    KD = mean_earth_sun_distance(utc_datetime)
    
    DEC = declination_degree(utc_datetime,TY)
    
    DIRC = (1367 * KD * math.exp(-0.8662 * (AM) * (TL) * (DEC)
                             ) * math.sin(solar.GetAltitude(latitude_deg,longitude_deg, 
                                                          utc_datetime,elevation , 
                                                          temperature_celsius , pressure_millibars )))
    
    return DIRC

def global_irradiance_clear(DIRC, DIFFC, latitude_deg, longitude_deg, utc_datetime, 
                            temperature_celsius = 25, pressure_millibars = 1013.25, TY = TY_default, 
                            AM = AM_default, TL = TL_default, elevation = elevation_default):
    
    """Equation calculates global irradiance under clear sky conditions.
    
    Parameters
    ----------
    DIRC : float
        Direct Irradiation under clear        
    DIFFC : float
        Diffuse Irradiation under clear sky
    
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting the north/south angular location of a place
        on a sphere.            
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location in an east-west direction,relative to 
        the Greenwich meridian.        
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 )
    temperature_celsius : float
        Temperature is a physical property of a system that underlies the common notions of hot and cold. 
    pressure_millibars : float
        pressure_millibars
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point, often the 
        mean sea level.
    TY : float
        Total number of days in a year. eg. 365 days per year,(no leap days)
    AM : float
        Air mass. An Air Mass is a measure of how far light travels through the Earth's atmosphere. One air mass, 
        or AM1, is the thickness of the Earth's atmosphere. Air mass zero (AM0) describes solar irradiance in 
        space, where it is unaffected by the atmosphere. The power density of AM1 light is about 1,000 W/m.
        
    TL : float
        Linke turbidity factor 
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point, often the mean sea 
        level.     
    
    Returns
    -------
    ghic : float
        Global Irradiation under clear sky
    
    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data: present status and proposed 
            new approaches", energy 30 (2005), pp 1533 - 1549.
            
    """
    DIRC =  direct_underclear(latitude_deg, longitude_deg, utc_datetime, 
                              TY, AM, TL, elevation, temperature_celsius = 25, 
                              pressure_millibars = 1013.25)
    
    DIFFC = diffuse_underclear(latitude_deg, longitude_deg, utc_datetime, 
                               elevation, temperature_celsius = 25, pressure_millibars= 1013.25)
    
    ghic = (DIRC + DIFFC)
    
    return ghic
    

def global_irradiance_overcast(latitude_deg, longitude_deg, utc_datetime, 
                               elevation = elevation_default, temperature_celsius = 25, 
                               pressure_millibars = 1013.25):
    """Calculated Global is used to compare to the Diffuse under overcast conditions.
    Under overcast skies, global and diffuse are expected to be equal due to the absence of the beam 
    component.
    
    Parameters
    ----------
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting the north/south angular location of a 
        place on a sphere.            
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location in an east-west direction,relative 
        to the Greenwich meridian.        
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 )
    elevation : float
        The elevation of a geographic location is its height above a fixed reference point, often the 
        mean sea level.         
    temperature_celsius : float
        Temperature is a physical property of a system that underlies the common notions of hot and 
        cold.    
    pressure_millibars : float
        pressure_millibars    
    
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
    ghioc = (572 * (solar.GetAltitude(latitude_deg, longitude_deg, utc_datetime, 
                                    elevation , temperature_celsius , pressure_millibars )))
    
    return ghioc
    

def diffuse_ratio(DIFF_data,ghi_data):
    """Function calculates the Diffuse ratio.
    
    Parameters
    ----------
    DIFF_data : array_like
        Diffuse horizontal irradiation data 
    ghi_data : array_like
        global horizontal irradiation data array    
    
    Returns
    -------
    K : float
        diffuse_ratio
    
    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data: present status and proposed 
            new approaches", energy 30 (2005), pp 1533 - 1549.
           
    """    
    K = DIFF_data/ghi_data
    
    return K 
    

def clear_index(ghi_data, utc_datetime, latitude_deg, longitude_deg):
   
    """This calculates the clear index ratio.
    
    Parameters
    ----------
    ghi_data : array_like
        global horizontal irradiation data array    
    utc_datetime : date_object
        utc_datetime. UTC DateTime is for Universal Time ( i.e. like a GMT+0 )        
    latitude_deg : float
        latitude in decimal degree. A geographical term denoting the north/south angular location of a place 
        on a sphere.            
    longitude_deg : float
        longitude in decimal degree. Longitude shows your location in an east-west direction,relative to the 
        Greenwich meridian.        
        
    Returns
    -------
    KT : float
        Clear index ratio
    
    References
    ----------
    .. [1] S. Younes, R.Claywell and el al,"Quality control of solar radiation data: present status and proposed 
            new approaches", energy 30 (2005), pp 1533 - 1549.
            
    """    
    EXTR1 = extraterrestrial_irrad(utc_datetime, latitude_deg, longitude_deg)
    
    KT = (ghi_data/EXTR1)
    
    return KT
  
def date_with_decimal_hour(date_utc, hour_decimal):    
    """This converts dates with decimal hour to datetime_hour.
    An improved version :mod:`conversions_time`
    
    Parameters
    ----------
    datetime : datetime.datetime
        A datetime object is a single object containing all the information from a 
        date object and a time object.              
    hour_decimal : datetime.datetime
        An hour is a unit of time 60 minutes, or 3,600 seconds in length.
    
    Returns
    -------.
    datetime_hour : datetime.datetime
        datetime_hour
    
    """
    # Backwards compatibility: round down to nearest round minute
    offset_seconds = int(hour_decimal * 60) * 60
    datetime_utc = dt(date_utc.year, date_utc.month, date_utc.day)
    
    return datetime_utc + timedelta(seconds=offset_seconds)

