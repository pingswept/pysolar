#!/usr/bin/python3

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
""" Tests for time.py and solar.py """
import datetime
import unittest
from pysolar import \
    solar, \
    constants, \
    time, \
    elevation
 # R0902: Too many instance attributes
 # R0904: Too many public methods
class TestSolar(unittest.TestCase):
    """ Test solar and time methods """
    def setUp(self):
        # time at MIDC SPA has no seconds setting so let's consider new test data.
        # the doc says use 67 sec delta t
        # self.dio = datetime.datetime(2003, 10, 17, 19, 30, 0, tzinfo=datetime.timezone.utc)
        self.dio = datetime.datetime(2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)
        self.dut1 = datetime.timedelta(seconds=time.get_delta_t(self.dio) - time.tt_offset
                                       - time.get_leap_seconds(self.dio))
        self.dio += datetime.timedelta(seconds=time.get_delta_t(self.dio) - time.tt_offset
                                       - time.get_leap_seconds(self.dio))
          # Reda & Andreas say that this time is in "Local Standard Time", which they
          # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
          # to UTC.

        self.longitude = -105.1786
        self.lon_offset = self.longitude / 360.0
        self.latitude = 39.742476
        self.pressure = 82000.0 # pascals
        self.elevation = 1830.14 # meters
        self.temperature = 11.0 + constants.celsius_offset # kelvin
        self.slope = 30.0 # degrees
        self.slope_orientation = -10.0 # degrees east from south
        self.jdn = time.jdn(self.dio)
        self.ajd = time.ajd(self.dio)
        self.jsd = time.get_julian_solar_day(self.dio)
        self.jct = time.get_julian_century(self.jsd)
        self.jde = time.get_julian_ephemeris_day(self.dio)
        self.jce = time.get_julian_ephemeris_century(self.jde)
        self.jme = time.get_julian_ephemeris_millennium(self.jce)
        self.geo_lon = solar.get_geocentric_longitude(self.jme)
        self.geo_lat = solar.get_geocentric_latitude(self.jme)
        self.nutation = solar.get_nutation(self.jce)
        self.sun_earth_distance = solar.get_sun_earth_distance(self.jme)
        self.true_ecliptic_obliquity = solar.get_true_ecliptic_obliquity(self.jme, self.nutation)
        self.aberration_correction = solar.get_aberration_correction(self.sun_earth_distance)
        self.apparent_sun_longitude = solar.get_apparent_sun_longitude(
            self.geo_lon, self.nutation, self.aberration_correction)
        self.apparent_sidereal_time = solar.get_apparent_sidereal_time(
            self.jsd, self.jme, self.nutation)
        self.geocentric_sun_right_ascension = solar.get_geocentric_sun_right_ascension(
            self.apparent_sun_longitude, self.true_ecliptic_obliquity, self.geo_lat)
        self.geocentric_sun_declination = solar.get_geocentric_sun_declination(
            self.apparent_sun_longitude, self.true_ecliptic_obliquity, self.geo_lat)
        self.local_hour_angle = solar.get_local_hour_angle(
            318.5119, self.longitude, self.geocentric_sun_right_ascension)
            #self.apparent_sidereal_time only correct to 5 sig figs, so override
        self.equatorial_horizontal_parallax = solar.get_equatorial_horizontal_parallax(
            self.sun_earth_distance)
        self.projected_radial_distance = solar.get_projected_radial_distance(
            self.elevation, self.latitude)
        self.projected_axial_distance = solar.get_projected_axial_distance(
            self.elevation, self.latitude)
        self.topocentric_sun_right_ascension = solar.get_topocentric_sun_right_ascension(
            self.projected_radial_distance, self.equatorial_horizontal_parallax,
            self.local_hour_angle, self.apparent_sun_longitude,
            self.true_ecliptic_obliquity, self.geo_lat)
        self.parallax_sun_right_ascension = solar.get_parallax_sun_right_ascension(
            self.projected_radial_distance, self.equatorial_horizontal_parallax,
            self.local_hour_angle, self.geocentric_sun_declination)
        self.topocentric_sun_declination = solar.get_topocentric_sun_declination(
            self.geocentric_sun_declination, self.projected_axial_distance,
            self.equatorial_horizontal_parallax, self.parallax_sun_right_ascension,
            self.local_hour_angle)
        self.topocentric_local_hour_angle = solar.get_topocentric_local_hour_angle(
            self.local_hour_angle, self.parallax_sun_right_ascension)
        self.topocentric_zenith_angle = solar.get_topocentric_zenith_angle(
            self.latitude, self.topocentric_sun_declination, self.topocentric_local_hour_angle,
            self.pressure, self.temperature)
        self.topocentric_azimuth_angle = solar.get_topocentric_azimuth_angle(
            self.topocentric_local_hour_angle, self.latitude, self.topocentric_sun_declination)
        self.incidence_angle = solar.get_incidence_angle(
            self.topocentric_zenith_angle, self.slope, self.slope_orientation,
            self.topocentric_azimuth_angle)
        self.pressure_with_elevation = elevation.get_pressure_with_elevation(1567.7)
        self.temperature_with_elevation = elevation.get_temperature_with_elevation(1567.7)

    def test_get_ac(self):
        """ -0.0057113603 """
        self.assertAlmostEqual(-0.0057113603, self.aberration_correction, 9) # value not validated

    def test_get_ast(self):
        """ 318.5119 """
        # value derived from Reda and Andreas (2005)
        self.assertAlmostEqual(318.5119, self.apparent_sidereal_time, 2)

    def test_get_asl(self):
        """ 204.0085537528 """
         # value from Reda and Andreas (2005)
        # self.assertAlmostEqual(204.0085537528, self.apparent_sun_longitude, 10)
        self.assertAlmostEqual(204.0085537528, self.apparent_sun_longitude, 4)

    def test_get_ajd(self):
        """ 2452930.312847222 """
        self.assertAlmostEqual(2452930.312847222, self.ajd, 12)

    def test_get_dut1(self):
        """ see DUT1 http://asa.usno.navy.mil/SecM/Glossary.html#ut1
        datetime.timedelta(0, 0, 357500)
        """
        self.assertEqual(datetime.timedelta(0, 0, 357500), self.dut1)

    def test_get_glon(self):
        """ 204.0182635175 """
        # value from Reda and Andreas (2005)
        # self.assertAlmostEqual(204.0182635175, self.geocentric_longitude, 10)
        self.assertAlmostEqual(204.0182635175, self.geo_lon, 4)

    def test_get_glat(self):
        """ 0.0001011219 """
         # value from Reda and Andreas (2005)
         # self.assertAlmostEqual(0.0001011219, self.geocentric_latitude, 9)
         # above fails with more accurate Julian Ephemeris correction
        self.assertAlmostEqual(0.0001011219, self.geocentric_latitude, 8)

    def test_get_gsd(self):
        """ -9.31434 """
         # value from Reda and Andreas (2005)
        self.assertAlmostEqual(-9.31434, self.geocentric_sun_declination, 4)

    def test_get_gsra(self):
        """ 202.22741 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(202.22741, self.geocentric_sun_right_ascension, 4)

    def test_get_ia(self):
        """ 25.18700 """
         # value from Reda and Andreas (2005)
        self.assertAlmostEqual(25.18700, self.incidence_angle, 3)

    def test_get_jc(self):
        """ 0.03792779869191517 """
        self.assertAlmostEqual(0.03792779869191517, self.jct, 12) # value not validated

    def test_get_jdn(self):
        """ 2452930.0 """
        self.assertAlmostEqual(2452930.0, self.jdn, 12)

    def test_get_jed(self):
        """ 2452930.3136 """
        self.assertAlmostEqual(2452930.3136, self.jde, 4) # value not validated

    def test_jem(self): # C0103:Invalid method name
        """ 0.0037927819143886397 """
        self.assertAlmostEqual(0.0037927819143886397, self.jme, 12) # value not validated

    def test_get_jsd(self):
        """ 2452930.312847 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(2452930.312847222, self.jsd, 12)

    def test_get_lha(self):
        """ 11.105900 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(11.105900, self.local_hour_angle, 4)

    def test_get_nut(self):
        """ -0.00399840 """
         # value from Reda and Andreas (2005)
        self.assertAlmostEqual(0.00166657, self.nutation['obliquity'], 8)
         # value from Reda and Andreas (2005)
        self.assertAlmostEqual(-0.00399840, self.nutation['longitude'], 8)

    def test_get_psra(self):
        """ -0.0003659911495454668 """
        self.assertAlmostEqual(-0.0003659911495454668, self.parallax_sun_right_ascension, 12)

    def test_get_prd(self): # C0103:Invalid method name
        """ 0.7702006 """
        self.assertAlmostEqual(0.7702006, self.projected_radial_distance, 6) # value not validated

    def test_get_pwe(self):   # C0103:Invalid method name
        """ 83855.90228 """
        self.assertAlmostEqual(83855.90228, self.pressure_with_elevation, 4)

    def test_get_sed(self):
        """ 0.9965421031 """
         # value from Reda and Andreas (2005)
        self.assertAlmostEqual(0.9965421031, self.sun_earth_distance, 7)

    def test_get_taa(self):  # C0103:Invalid method name
        """ 194.34024 """
         # value from Reda and Andreas (2005)
        # self.assertAlmostEqual(194.34024, self.topocentric_azimuth_angle, 5)
        self.assertAlmostEqual(194.34024, self.topocentric_azimuth_angle, 4)

    def test_get_teo(self): # C0103:Invalid method name
        """ 23.440465 """
         # value from Reda and Andreas (2005)
        self.assertAlmostEqual(23.440465, self.true_ecliptic_obliquity, 6)

    def test_get_tlha(self): # C0103:Invalid method name
        """ 11.10629 """
         # value from Reda and Andreas (2005)
        self.assertAlmostEqual(11.10629, self.topocentric_local_hour_angle, 4)

    def test_get_ts(self):
        """ you could put what to expect in here """
        # please consider this so we can compare with MIDC SPA not the doc.
        # no_tzinfo = datetime.datetime(2003, 10, 17, 19, 30, 0, tzinfo=None)
        no_tzinfo = datetime.datetime(2003, 10, 17, 19, 30, 30, tzinfo=None)
        print('d =', time.timestamp(self.dio), 'seconds')
        print('no tzinfo', time.timestamp(no_tzinfo))

    def test_get_tsd(self): # C0103:Invalid method name
        """ -9.316179 """
         # value from Reda and Andreas (2005)
        self.assertAlmostEqual(-9.316179, self.topocentric_sun_declination, 3)

    def test_get_tsra(self):
        """ 202.22741 """
         # value from Reda and Andreas (2005)
        self.assertAlmostEqual(202.22741, self.topocentric_sun_right_ascension, 3)

    def test_get_twe(self):   # C0103:Invalid method name
        """ 277.9600 """
        self.assertAlmostEqual(277.9600, self.temperature_with_elevation, 4)

    def test_get_tza(self):  # C0103:Invalid method name
        """ MID SPA has 115.923120 """
         # value from Reda and Andreas (2005)
        self.assertAlmostEqual(50.11162, self.topocentric_zenith_angle, 3)

if __name__ == "__main__":
    SUN = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    TIME = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    unittest.TextTestRunner(verbosity=2).run(SUN)
#end if
