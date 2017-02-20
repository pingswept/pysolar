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
from pysolar import solar, time, constants

class TestGeocentricSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786 # -105:
    longitude_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67 / 86400
    default = 64.5415 / 86400
    param_list = [elevation, latitude, longitude, surface_slope,
                  surface_azimuth_rotation, temperature, pressure]
    hours = dt_list[3] / 24.0
    minutes = dt_list[4] / 1440.0
    seconds = dt_list[5] / 86400.0
    jd1 = time.jdn(dt_list) - 0.5 # julian day midnight
    jd2 = hours + minutes + seconds # fractional day
    print(jd1 + jd2)
    # need to take the timezone offset out because all
    # whole julian day numbers begin at noon.
    jd3 = 0.5 + minutes + seconds - 7 / 24.0
    jd4 = jd3 - longitude_offset
    jct0 = time.julian_century(jd1 + jd2)
    jct1 = time.julian_century(jd1 + default + jd2)
    jct2 = time.julian_century(jd1 + delta_t + jd2)
    jct3 = time.julian_century(jd1 + jd4)
    jct4 = time.julian_century(jd1 + default + jd4)
    jct5 = time.julian_century(jd1 + delta_t + jd4)
    def setUp(self):
        """
        set up
        """
        return None

    def test_geocentric_declination(self):
        """
        testing Geocentric sun declination
        0       -9.314048298076031
        64.5415 -9.3143212526048
        67      -9.314331649840488
        """
        # print(self.test_geo_rad_dec.__doc__)
        # print('testing solar.py Geocentric Declination method')
        gsd0 = solar.geocentric_declination(self.jct0)
        self.assertEqual(-9.314054716355045, gsd0, 12)
        self.assertAlmostEqual(-9.314048298076031, gsd0, 4)

        gsd1 = solar.geocentric_declination(self.jct1)
        self.assertEqual(-9.314327669350611, gsd1, 12)
        self.assertAlmostEqual(-9.3143212526048, gsd1, 4)

        gsd2 = solar.geocentric_declination(self.jct2)
        self.assertEqual(-9.31433806652776, gsd2, 12)
        self.assertAlmostEqual(-9.314331649840488, gsd2, 4)

    def test_geocentric_latitude(self):
        """
        testing Geocentric latitude
        0       0.00010110749648050061
        64.5415 0.00010112139544887049
        67      0.00010112192480034693
        """
        # print(self.test_geo_lat_lon.__doc__)
        # print('testing solar.py Geocentric Latitude')
        glat0 = solar.geocentric_latitude(self.jct0)
        self.assertEqual(0.00011640012691222886, glat0, 12)
        self.assertAlmostEqual(0.00010110749648050061, glat0, 4)

        glat1 = solar.geocentric_latitude(self.jct1)
        self.assertEqual(0.00011641495011238601, glat1, 12)
        self.assertAlmostEqual(0.00010112139544887049, glat1, 4)

        glat2 = solar.geocentric_latitude(self.jct2)
        self.assertEqual(0.00011641551467699968, glat2, 12)
        self.assertAlmostEqual(0.00010112192480034693, glat2, 4)


    def test_geocentric_longitude(self):
        """
        testing Geocentric longitude
        0       204.01746718593841
        64.5415 204.01820845556682
        67      204.01823669167976
        """
        # print(self.test_geo_lat_lon.__doc__)
        # print('testing solar.py True Geocentric Longitude method')
        glon0 = solar.geocentric_longitude(self.jct0)
        self.assertEqual(204.01754778491386, glon0, 12)
        self.assertAlmostEqual(204.01746718593841, glon0, 3)

        glon1 = solar.geocentric_longitude(self.jct1)
        self.assertEqual(204.0182890533638, glon1, 12)
        self.assertAlmostEqual(204.01820845556682, glon1, 3)

        glon2 = solar.geocentric_longitude(self.jct2)
        self.assertEqual(204.01831728943148, glon2, 12)
        self.assertAlmostEqual(204.01823669167976, glon2, 3)

    def test_geocentric_right_ascension(self):
        """
        testing Geocentric sun right ascension
        0       202.22665926504152 / 15
        64.5415 202.22735767137598 / 15
        67      202.2273842747809 / 15
        """
        # print(self.test_geo_rad_dec.__doc__)
        # print('testing solar.py Geocentric Right Ascension method')
        gsra0 = solar.geocentric_right_ascension(self.jct0)
        self.assertEqual(13.48178116538139, gsra0, 12)
        self.assertAlmostEqual(202.22665926504152 / 15, gsra0, 5)

        gsra1 = solar.geocentric_right_ascension(self.jct1)
        self.assertEqual(13.48182772574043, gsra1, 12)
        self.assertAlmostEqual(202.22735767137598 / 15, gsra1, 5)

        gsra2 = solar.geocentric_right_ascension(self.jct2)
        self.assertEqual(13.481829499298325, gsra2, 12)
        self.assertAlmostEqual(202.2273842747809 / 15, gsra2, 5)

if __name__ == "__main__":

    GSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestGeocentricSolar)
    unittest.TextTestRunner(verbosity=2).run(GSOLAR)

#end if
