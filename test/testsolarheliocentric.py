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

""" Tests helio_lat.py """

import unittest

from pysolar import constants
from pysolar import helio_lat
from pysolar import helio_lon
from pysolar import solar
from pysolar import time


class TestHeliocentricSolar(unittest.TestCase):
    """
    Test heliocentric methods
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

    def test_heliocentric_latitude(self):
        """
        testing Heliocentric latitude
        0       -0.00010110749648050061
        64.5415 -0.00010112139544887049
        67      -0.00010112192480034693
        """
        # print(self.heliocentric_latitude.__doc__)
        # print('testing solar.py Heliocentric Latitude method')
        hlat0 = helio_lat.heliocentric_latitude(self.jct0)
        self.assertEqual(-0.00011640012691222886, hlat0, 12)
        self.assertAlmostEqual(-0.00010110749648050061, hlat0, 4)

        hlat1 = helio_lat.heliocentric_latitude(self.jct1)
        self.assertEqual(-0.00011641495011238601, hlat1, 12)
        self.assertAlmostEqual(-0.00010112139544887049, hlat1, 4)

        hlat2 = helio_lat.heliocentric_latitude(self.jct2)
        self.assertEqual(-0.00011641551467699968, hlat2, 12)
        self.assertAlmostEqual(-0.00010112192480034693, hlat2, 4)

    def test_heliocentric_longitude(self):
        """
        testing Heliocentric longitude
        0       24.01749218593841
        64.5415 24.018233455566815
        67      24.018261691679754
        """
        # print(self.test_heliocentric_longitude.__doc__)
        # print('testing solar.py Heliocentric longitude method')
        hlon0 = solar.heliocentric_longitude(self.jct0)
        self.assertEqual(24.01754778491386, hlon0, 12)
        self.assertAlmostEqual(24.01749218593841, hlon0, 3)

        hlon1 = solar.heliocentric_longitude(self.jct1)
        self.assertEqual(24.018289053363787, hlon1, 12)
        self.assertAlmostEqual(24.018233455566815, hlon1, 3)

        hlon2 = solar.heliocentric_longitude(self.jct2)
        self.assertEqual(24.01831728943148, hlon2, 12)
        self.assertAlmostEqual(24.018261691679754, hlon2, 3)

    def test_lb0_to_lb4(self):
        """
        test each latitude term Element
        should be
        [-176.502688, 3.067582]
        """
        # print('testing solar.py Heliocentric Longitude Terms method')
        lb0 = helio_lat.heliocentric_lat_elements(self.jct0)[0]
        lb1 = helio_lat.heliocentric_lat_elements(self.jct0)[1]
        lb2 = helio_lat.heliocentric_lat_elements(self.jct0)[2]
        lb3 = helio_lat.heliocentric_lat_elements(self.jct0)[3]
        lb4 = helio_lat.heliocentric_lat_elements(self.jct0)[4]
        self.assertEqual(-203.1686401523526, lb0, 12)
        self.assertEqual(3.1828513503667772, lb1, 12)
        self.assertEqual(1.519754875980019, lb2, 12)
        self.assertEqual(0.002032825197327741, lb3, 12)
        self.assertEqual(0.008798475935879296, lb4, 12)

    def test_lo0_to_lo5(self):
        """
        test each longitude term Element
        should be
        [172067561.526586, 628332010650.051147, 61368.682493,
         -26.902819, -121.279536, -0.999999]
        """
        # print('testing solar.py Heliocentric Longitude Terms method')
        lo0 = solar.heliocentric_lon_elements(self.jct0)[0]
        lo1 = solar.heliocentric_lon_elements(self.jct0)[1]
        lo2 = solar.heliocentric_lon_elements(self.jct0)[2]
        lo3 = solar.heliocentric_lon_elements(self.jct0)[3]
        lo4 = solar.heliocentric_lon_elements(self.jct0)[4]
        lo5 = solar.heliocentric_lon_elements(self.jct0)[5]
        self.assertEqual(172067649.50049174, lo0, 12)
        self.assertAlmostEqual(172067561.526586 / 1000, lo0 / 1000, 0)
        self.assertEqual(628332010659.6948, lo1, 12)
        self.assertAlmostEqual(628332010650.051147 / 100, lo1 / 100, 0)
        self.assertEqual(61369.13452846821, lo2, 12)
        self.assertAlmostEqual(61368.682493 / 10, lo2 / 10, 0)
        self.assertEqual(-26.885912766418144, lo3, 12)
        self.assertAlmostEqual(-26.902819, lo3, 0)
        self.assertEqual(-120.93960852868578, lo4, 12)
        self.assertAlmostEqual(-121.279536, lo4, 0)
        self.assertEqual(-0.8793236989305419, lo5, 12)
        self.assertAlmostEqual(-0.999999, lo5, 0)

if __name__ == "__main__":

    HSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestHeliocentricSolar)
    unittest.TextTestRunner(verbosity=2).run(HSOLAR)

#end if
