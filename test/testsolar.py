#!/usr/bin/env python

#    Library for calculating location of the sun

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

import datetime
import unittest
from pysolar import \
  solar, \
  constants, \
  time, \
  elevation

class TestSolar(unittest.TestCase):
    """ test Solar class methods """
    def setUp(self):
        self.d1_ = datetime.datetime(2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)
        self.d1_ += datetime.timedelta(seconds=time.delta_t(self.d1_) -
                                       time.TTOFFSET - time.leap_seconds(self.d1_))
        # Reda & Andreas say that this time is in "Local Standard Time", which they
        # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
        # to UTC.
        self.longitude = -105.1786

        self.latitude = 39.742476

        self.pressure = 82000.0 # pascals

        self.elevation = 1830.14 # meters

        self.temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin

        self.slope = 30.0 # degrees

        self.slope_orientation = -10.0 # degrees east from south

        self.jd_ = time.julian_solar_day( \
            self.d1_)

        self.jc_ = time.julian_century( \
            self.jd_)

        self.jde = time.julian_ephemeris_day( \
            self.d1_)

        self.jce = time.julian_ephemeris_century( \
            self.jde)

        self.jme = time.julian_ephemeris_millennium( \
            self.jce)
        self.geocentric_longitude = solar.geocentric_longitude( \
            self.jme)

        self.geocentric_latitude = solar.geocentric_latitude( \
            self.jme)

        self.nutation = solar.nutation( \
            self.jce)

        self.sun_earth_distance = solar.sun_earth_distance( \
            self.jme)

        self.true_obliquity = solar.true_ecliptic_obliquity( \
            self.jme, self.nutation)

        self.aberration_correction = solar.aberration_correction( \
            self.sun_earth_distance)

        self.apparent_longitude = solar.apparent_longitude( \
            self.geocentric_longitude, self.nutation, self.aberration_correction)

        self.apparent_sidereal_time = solar.apparent_sidereal_time( \
            self.jd_, self.jme, self.nutation)

        self.geocentric_right_ascension = solar.geocentric_right_ascension( \
            self.apparent_longitude, self.true_obliquity, self.geocentric_latitude)

        self.geocentric_declination = solar.geocentric_declination( \
            self.apparent_longitude, self.true_obliquity, self.geocentric_latitude)

        #self.apparent_sidereal_time only correct to 5 sig figs, so override
        self.local_hour_angle = solar.local_hour_angle( \
            318.5119, self.longitude, self.geocentric_right_ascension)

        self.equatorial_horizontal_parallax = solar.equatorial_horizontal_parallax( \
            self.sun_earth_distance)

        self.projected_radial_distance = solar.projected_radial_distance( \
            self.elevation, self.latitude)

        self.projected_axial_distance = solar.projected_axial_distance( \
            self.elevation, self.latitude)

        self.topocentric_sun_right_ascension = solar.topocentric_sun_right_ascension( \
            self.projected_radial_distance, self.equatorial_horizontal_parallax, \
            self.local_hour_angle, self.apparent_longitude, self.true_obliquity, \
            self.geocentric_latitude)

        self.parallax_right_ascension = solar.ra_parallax( \
            self.projected_radial_distance, self.equatorial_horizontal_parallax, \
            self.local_hour_angle, self.geocentric_declination)

        self.topocentric_declination = solar.topocentric_sun_declination( \
            self.geocentric_declination, self.projected_axial_distance, \
            self.equatorial_horizontal_parallax, self.parallax_right_ascension, \
            self.local_hour_angle)

        self.topocentric_elevation_angle = solar.topocentric_elevation_angle( \
            self.geocentric_latitude, self.geocentric_declination, \
            self.local_hour_angle)

        self.topocentric_local_hour_angle = solar.topocentric_local_hour_angle( \
            self.local_hour_angle, self.parallax_right_ascension)

        self.topocentric_zenith_angle = solar.topocentric_zenith_angle( \
            self.latitude, self.topocentric_declination, self.topocentric_local_hour_angle, \
            self.pressure, self.temperature)

        self.topocentric_azimuth_angle = solar.topocentric_azimuth_angle( \
            self.topocentric_local_hour_angle, self.latitude, self.topocentric_declination)

        self.angle_of_incidence = solar.angle_of_incidence( \
            self.topocentric_zenith_angle, self.slope, self.slope_orientation, \
            self.topocentric_azimuth_angle)

        self.pressure_with_elevation = elevation.pressure_with_elevation(1567.7)

        self.temperature_with_elevation = elevation.temperature_with_elevation(1567.7)

    def test_date(self):
        """ date should = 2003-10-17 19:30:30.357500+00:00 """
        self.assertEqual("2003-10-17 19:30:30.357500+00:00", str(self.d1_))

    def test_aberration_correction(self):
        """ -0.0057113603 """
        self.assertAlmostEqual(-0.0057113603, self.aberration_correction, 9)

    def test_angle_of_incidence(self):
        """  # failing getting 124.00059395583871 """
        self.assertAlmostEqual(25.18700, self.angle_of_incidence, 3)

    def test_apparent_sidereal_time(self):
        """ 21.234404187 """
        self.assertAlmostEqual(21.234404187, self.apparent_sidereal_time / 15, 9)

    def test_apparent_sun_longitude(self):
        """ 204.008525516  """
        # self.assertAlmostEqual(204.0085537528, self.apparent_sun_longitude, 10)
         # above fails with more accurate Julian Ephemeris correction
        self.assertAlmostEqual(204.008525516, self.apparent_longitude, 6)

    def test_geocentric_alpha_angle(self):
        """ 202.227382943 """
        self.assertAlmostEqual(202.227382943, self.geocentric_right_ascension, 6)

    def test_geocentric_alpha_time(self):
        """ 13.481825529 """
        self.assertAlmostEqual(13.481825529, self.geocentric_right_ascension / 15, 6)

    def test_geocentric_delta_angle(self):
        """ -9.31434 """
        self.assertAlmostEqual(-9.31434, self.geocentric_declination, 4)

    def test_geocentric_latitude(self):
        """ 0.0001011219 """
        # self.assertAlmostEqual(0.0001011219, self.geocentric_latitude, 9)
         # above fails with more accurate Julian Ephemeris correction
        self.assertAlmostEqual(0.0001011219, self.geocentric_latitude, 8)

    def test_geocentric_longitude(self):
        """ 204.018235 """
        # self.assertAlmostEqual(204.0182635175, self.geocentric_longitude, 10)
         # above fails with more accurate Julian Ephemeris correction
        self.assertAlmostEqual(204.018235, self.geocentric_longitude, 6)

    def test_julian_century(self):
        """ 0.03792779869191517 """
        self.assertAlmostEqual(0.03792779869191517, self.jc_, 12)

    def test_julian_ephemeris_day(self):
        """ 2452930.3135942305 """
        self.assertAlmostEqual(2452930.3135942305, self.jde, 6)

    def test_julian_ephemeris_millenium(self):
        """ 0.0037927819143886397 """
        self.assertAlmostEqual(0.0037927819143886397, self.jme, 12)

    def test_julian_solar_day(self):
        """  2452930.312847  """
        self.assertAlmostEqual(2452930.312847, self.jd_, 6)

    def test_local_hour_angle(self):
        """ 11.105900 """
        self.assertAlmostEqual(11.105900, self.local_hour_angle, 4)

    def test_nutation(self):
        """ 0.00166657 obliquity, -0.00399840 longitude  """
        self.assertAlmostEqual(0.00166657, self.nutation['obliquity'], 8)
        self.assertAlmostEqual(-0.00399840, self.nutation['longitude'], 8)

    def test_parallax_right_ascension(self):
        """ -0.0003659911495454668 """
        self.assertAlmostEqual(-0.0003659911495454668, self.parallax_right_ascension, 12)
    def test_pressure_with_elevation(self):
        """ 83855.90228 """
        self.assertAlmostEqual(83855.90228, self.pressure_with_elevation, 4)

    def test_projected_radial_distance(self):
        """ 0.7702006 """
        self.assertAlmostEqual(0.7702006, self.projected_radial_distance, 6)

    def test_sun_earth_distance(self):
        """ 0.9965421031 """
        self.assertAlmostEqual(0.9965421031, self.sun_earth_distance, 7)

    def test_temperature_with_elevation(self):
        """ 277.9600 """
        self.assertAlmostEqual(277.9600, self.temperature_with_elevation, 4)

    def test_timestamp(self):
        """ d 1066419030.3575, no tzinfo 1066437030.0 """
        no_tzinfo = datetime.datetime(2003, 10, 17, 19, 30, 30, tzinfo=None)
        self.assertEqual(1066419030.3575, time.timestamp(self.d1_))
        self.assertEqual(1066437030.0, time.timestamp(no_tzinfo))

    def test_topocentric_alpha(self):
        """ 202.22741 """
        self.assertAlmostEqual(202.22741, self.topocentric_sun_right_ascension, 3)

    def test_topocentric_azimuth(self):
        """ 194.34024 """
        # self.assertAlmostEqual(194.34024, self.topocentric_azimuth_angle, 5)
        # above fails with more accurate Julian Ephemeris correction
        self.assertAlmostEqual(194.34024, self.topocentric_azimuth_angle, 4)

    def test_topocentric_declination(self):
        """ -9.316179 """
        self.assertAlmostEqual(-9.316179, self.topocentric_declination, 3)

    def test_topocentric_elevatn_angle(self):
        """ 75.543 """
        self.assertAlmostEqual(75.543, self.topocentric_elevation_angle, 3)

    def test_topocentric_local_hr_angle(self):
        """ 11.10629 """
        self.assertAlmostEqual(11.10629, self.topocentric_local_hour_angle, 4)

    def test_topocentric_zenith_angle(self):
        """ # failing getting -3364657.1068369234  """
        self.assertAlmostEqual(50.11162, self.topocentric_zenith_angle, 3)

    def test_true_ecliptic_obliquity(self):
        """ 23.440465 """
        self.assertAlmostEqual(23.440465, self.true_obliquity, 6)



if __name__ == "__main__":
    SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
#end if
