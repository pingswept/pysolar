'''
Created on Aug 13, 2015

@author: rene
'''
import unittest
import datetime
from pysolar.solar import *
from pysolar.solartime import *


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testHourAngle(self):

        '''
        Example 1.6.1 from Book "Solar Engineering of Thermal Processes by Duffie and Beckman, fourth edition, Wiley 2013"

        hour angle should be -22.5. (-22.5 % 360.0 = 337.5)
        '''

        tz = datetime.timezone(datetime.timedelta(hours=-6))
        when = datetime.datetime(2008, 2, 13, 10, 42, tzinfo=tz)

        latitude_deg = 43.076342
        longitude_deg = -89.384448

        '''
        Hour angle from get_hour_angle
        '''
        ha = get_hour_angle(when, longitude_deg)

        '''Hour angle as in pysolar.solar.get_altitude'''

        # time-dependent calculations
        jd = get_julian_solar_day(when)
        jde = get_julian_ephemeris_day(when)
        jce = get_julian_ephemeris_century(jde)
        jme = get_julian_ephemeris_millennium(jce)
        geocentric_latitude = get_geocentric_latitude(jme)
        geocentric_longitude = get_geocentric_longitude(jme)
        sun_earth_distance = get_sun_earth_distance(jme)
        aberration_correction = get_aberration_correction(sun_earth_distance)
        nutation = get_nutation(jce)
        apparent_sidereal_time = get_apparent_sidereal_time(jd, jme, nutation)
        true_ecliptic_obliquity = get_true_ecliptic_obliquity(jme, nutation)

        # calculations dependent on location and time
        apparent_sun_longitude = get_apparent_sun_longitude(
            geocentric_longitude,
            nutation,
            aberration_correction)
        geocentric_sun_right_ascension = get_geocentric_sun_right_ascension(
            apparent_sun_longitude,
            true_ecliptic_obliquity,
            geocentric_latitude)
        local_hour_angle = get_local_hour_angle(
            apparent_sidereal_time,
            longitude_deg,
            geocentric_sun_right_ascension)

        reference_ha = -22.5 % 360.0

        self.assertAlmostEqual(local_hour_angle % 360.0, ha % 360.0, places=0)
        self.assertAlmostEqual(reference_ha % 360.0, ha % 360.0, places=0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
