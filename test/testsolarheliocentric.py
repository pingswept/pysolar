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

class TestHeliocentricSolar(unittest.TestCase):
    """
    Test heliocentric methods
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


    def test_heliocentric_latitude(self):
        """
        testing Heliocentric latitude
        0       -0.00010110749648050061
        64.5415 -0.00010112139544887049
        67      -0.00010112192480034693
        """
        # print(self.heliocentric_latitude.__doc__)
        # print('testing solar.py Heliocentric Latitude method')
        hlat0 = solar.heliocentric_latitude(self.jd1, self.jd2)
        self.assertEqual(-0.00010111269416498883, hlat0, 12)
        self.assertAlmostEqual(-0.00010110749648050061, hlat0, 7)

        hlat1 = solar.heliocentric_latitude(self.jd1, self.default + self.jd2)
        self.assertEqual(-0.00010112659361522744, hlat1, 12)
        self.assertAlmostEqual(-0.00010112139544887049, hlat1, 7)

        hlat2 = solar.heliocentric_latitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(-0.00010112712298505422, hlat2, 12)
        self.assertAlmostEqual(-0.00010112192480034693, hlat2, 7)

    def test_heliocentric_longitude(self):
        """
        testing Heliocentric longitude
        0       24.01749218593841
        64.5415 24.018233455566815
        67      24.018261691679754
        """
        # print(self.test_heliocentric_longitude.__doc__)
        # print('testing solar.py Heliocentric longitude method')
        hlon0 = solar.heliocentric_longitude(self.jd1, self.jd2)
        self.assertEqual(24.017492250274017, hlon0, 12)
        self.assertAlmostEqual(24.01749218593841, hlon0, 6)

        hlon1 = solar.heliocentric_longitude(self.jd1, self.default + self.jd2)
        self.assertEqual(24.0182335199886, hlon1, 12)
        self.assertAlmostEqual(24.018233455566815, hlon1, 6)

        hlon2 = solar.heliocentric_longitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(24.018261756104494, hlon2, 12)
        self.assertAlmostEqual(24.018261691679754, hlon2, 6)

    def test_lb0_to_lb4(self):
        """
        test each latitude term Element
        should be
        [-176.502688, 3.067582]
        """
        # print('testing solar.py Heliocentric Longitude Terms method')
        lb0 = solar.heliocentric_lat_elements(self.jd1, self.jd2)[0]
        lb1 = solar.heliocentric_lat_elements(self.jd1, self.jd2)[1]
        lb2 = solar.heliocentric_lat_elements(self.jd1, self.jd2)[2]
        lb3 = solar.heliocentric_lat_elements(self.jd1, self.jd2)[3]
        lb4 = solar.heliocentric_lat_elements(self.jd1, self.jd2)[4]
        self.assertEqual(-176.48654284285342, lb0, 12)
        self.assertAlmostEqual(-176.502688, lb0, 1)
        self.assertEqual(3.058434483982354, lb1, 12)
        self.assertAlmostEqual(3.067582, lb1, 1)
        self.assertEqual(0.0, lb2, 12)
        self.assertEqual(0.0, lb3, 12)
        self.assertEqual(0.0, lb4, 12)

    def test_lo0_to_lo5(self):
        """
        test each longitude term Element
        should be
        [172067561.526586, 628332010650.051147, 61368.682493,
         -26.902819, -121.279536, -0.999999]
        """
        # print('testing solar.py Heliocentric Longitude Terms method')
        lo0 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[0]
        lo1 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[1]
        lo2 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[2]
        lo3 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[3]
        lo4 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[4]
        lo5 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[5]
        self.assertEqual(172067552.4204392, lo0, 12)
        self.assertAlmostEqual(172067561.526586 / 100, lo0 / 100, 0)
        self.assertEqual(628332010700.2529, lo1, 12)
        self.assertAlmostEqual(628332010650.051147 / 1000, lo1 / 1000, 0)
        self.assertEqual(61368.64926580728, lo2, 12)
        self.assertAlmostEqual(61368.682493, lo2, 1)
        self.assertEqual(-26.897807223158654, lo3, 12)
        self.assertAlmostEqual(-26.902819, lo3, 0)
        self.assertEqual(-121.28930075553654, lo4, 12)
        self.assertAlmostEqual(-121.279536, lo4, 1)
        self.assertEqual(-0.9999987317275395, lo5, 12)
        self.assertAlmostEqual(-0.999999, lo5, 6)

if __name__ == "__main__":

    HSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestHeliocentricSolar)
    unittest.TextTestRunner(verbosity=2).run(HSOLAR)

#end if
