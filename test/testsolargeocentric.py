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

""" Tests for solar.py """

import unittest
from pysolar import solar, time, elevation, constants

class TestGeocentricSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67 / 86400
    param_list = [elevation, latitude, longitude, surface_slope,
                  surface_azimuth_rotation, temperature, pressure]
    def setUp(self):
        self.jd1 = 2452929.5

        self.jd2 = (
            self.dt_list[3] / 24.0) + (
                self.dt_list[4] / 1440.0) + (
                    self.dt_list[5] / 86400.0)

        self.default = time.delta_t(self.jd1 + self.jd2) / 86400.0

    def test_geocentric_declination(self):
        """
        testing Geocentric sun declination
        0       -9.314048298076031
        64.5415 -9.3143212526048
        67      -9.314331649840488
        """
        # print(self.test_geo_rad_dec.__doc__)
        # print('testing solar.py Geocentric Declination method')
        gsd0 = solar.geocentric_declination(self.jd1, self.jd2)
        self.assertEqual(-9.314052493720652, gsd0, 12)
        self.assertAlmostEqual(-9.314048298076031, gsd0, 5)

        gsd1 = solar.geocentric_declination(self.jd1, self.default + self.jd2)
        self.assertEqual(-9.314325448278428, gsd1, 12)
        self.assertAlmostEqual(-9.3143212526048, gsd1, 5)

        gsd2 = solar.geocentric_declination(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(-9.314335845515107, gsd2, 12)
        self.assertAlmostEqual(-9.314331649840488, gsd2, 5)

    def test_geocentric_latitude(self):
        """
        testing Geocentric latitude
        0       0.00010110749648050061
        64.5415 0.00010112139544887049
        67      0.00010112192480034693
        """
        # print(self.test_geo_lat_lon.__doc__)
        # print('testing solar.py Geocentric Latitude')
        glat0 = solar.geocentric_latitude(self.jd1, self.jd2)
        self.assertEqual(0.00010111269416498883, glat0, 12)
        self.assertAlmostEqual(0.00010110749648050061, glat0, 7)

        glat1 = solar.geocentric_latitude(self.jd1, self.default + self.jd2)
        self.assertEqual(0.00010112659361522744, glat1, 12)
        self.assertAlmostEqual(0.00010112139544887049, glat1, 7)

        glat2 = solar.geocentric_latitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(0.00010112712298505422, glat2, 12)
        self.assertAlmostEqual(0.00010112192480034693, glat2, 7)


    def test_geocentric_longitude(self):
        """
        testing Geocentric longitude
        0       204.01746718593841
        64.5415 204.01820845556682
        67      204.01823669167976
        """
        # print(self.test_geo_lat_lon.__doc__)
        # print('testing solar.py True Geocentric Longitude method')
        glon0 = solar.geocentric_longitude(self.jd1, self.jd2)
        self.assertEqual(204.01749225027402, glon0, 12)
        self.assertAlmostEqual(204.01746718593841, glon0, 4)

        glon1 = solar.geocentric_longitude(self.jd1, self.default + self.jd2)
        self.assertEqual(204.0182335199886, glon1, 12)
        self.assertAlmostEqual(204.01820845556682, glon1, 4)

        glon2 = solar.geocentric_longitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(204.0182617561045, glon2, 12)
        self.assertAlmostEqual(204.01823669167976, glon2, 4)

    def test_geocentric_right_ascension(self):
        """
        testing Geocentric sun right ascension
        0       202.22665926504152 / 15
        64.5415 202.22735767137598 / 15
        67      202.2273842747809 / 15
        """
        # print(self.test_geo_rad_dec.__doc__)
        # print('testing solar.py Geocentric Right Ascension method')
        gsra0 = solar.geocentric_right_ascension(self.jd1, self.jd2)
        self.assertEqual(13.481779006038968, gsra0, 12)
        self.assertAlmostEqual(202.22665926504152 / 15, gsra0, 4)

        gsra1 = solar.geocentric_right_ascension(self.jd1, self.default + self.jd2)
        self.assertEqual(13.4818255664478, gsra1, 12)
        self.assertAlmostEqual(202.22735767137598 / 15, gsra1, 4)

        gsra2 = solar.geocentric_right_ascension(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(13.481827340007595, gsra2, 12)
        self.assertAlmostEqual(202.2273842747809 / 15, gsra2, 4)

    def test_mean_geocentric_longitude(self):
        """
        test Mean Geocentric Longitude
        """
        # print('testing solar.py Mean Geocentric Longitude')
        mgl0 = solar.mean_solar_longitude(self.jd1, self.jd2)
        self.assertEqual(205.89640791951274, mgl0, 12)

        mgl1 = solar.mean_solar_longitude(self.jd1, self.default + self.jd2)
        self.assertEqual(205.8971442062218, mgl1, 12)

        mgl2 = solar.mean_solar_longitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(205.89717225252048, mgl2, 12)

if __name__ == "__main__":

    GSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestGeocentricSolar)
    unittest.TextTestRunner(verbosity=2).run(GSOLAR)

#end if
