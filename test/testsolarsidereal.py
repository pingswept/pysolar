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
import datetime
import unittest
from pysolar import solar, time, elevation, constants

class TestSiderealTime(unittest.TestCase):
    """
    Test sidereal time methods
    """
    delta_t = 67 / 86400.0
    longitude = -105.1786
    longitude_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    param_list = [elevation, latitude, longitude, surface_slope,
                  surface_azimuth_rotation, temperature, pressure]
    lon_offset = longitude / 360.0
    dut1 = datetime.timedelta(seconds=0.0)
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    def setUp(self):
        self.jd1 = 2452929.5

        self.jd2 = (
            self.dt_list[3] / 24.0) + (
                self.dt_list[4] / 1440.0) + (
                    self.dt_list[5] / 86400.0)

        self.default = time.delta_t(self.jd1 + self.jd2) / 86400.0

    def test_gasa(self):
        """
        testing  Greenwich apparent sidereal angle
        0        318.51191008778073
        64.5415  318.7815693562905
        67       318.79184109456986
        """
        # print(self.test_gasa.__doc__)
        # print('testing solar.py Greenwich Apparent Sidereal Angle method')
        gasa = solar.gasa(self.jd1, self.jd2)
        self.assertEqual(318.51191024614667, gasa, 12)
        self.assertAlmostEqual(318.51191008778073, gasa, 6)

        gasa1 = solar.gasa(self.jd1, self.default + self.jd2)
        self.assertEqual(318.781569514435, gasa1, 12)
        self.assertAlmostEqual(318.7815693562905, gasa1, 6)

        gasa2 = solar.gasa(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(318.79184125269, gasa2, 12)
        self.assertAlmostEqual(318.79184109456986, gasa2, 6)

    def test_gast(self):
        """
        testing Greenwich Apparent Sidereal Time
        0       21.23412733918538
        64.5415 21.2521046237527
        67      21.252789406304657
        """
        # print(self.test_gast.__doc__)
        # print('testing solar.py Greenwich Apparent Sideral Time method')
        gast = solar.gast(self.jd1, self.jd2)
        self.assertEqual(21.234127349743112, gast, 12)
        self.assertAlmostEqual(21.23412733918538, gast, 7)

        gast1 = solar.gast(self.jd1, self.default + self.jd2)
        self.assertEqual(21.252104634295666, gast1, 12)
        self.assertAlmostEqual(21.2521046237527, gast1, 7)

        gast2 = solar.gast(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(21.252789416846, gast2, 12)
        self.assertAlmostEqual(21.252789406304657, gast2, 7)

    def test_gmsa(self):
        """
        testing Greenwich mean sidereal angle
        0       318.51557827281067
        64.5415 318.78523752919864
        67      318.7955092670163
        """
        # print(self.test_sidereal_angles.__doc__)
        # print('testing solar.py Greenwich Mean Sideral Angle method')
        gmsa0 = solar.gmsa(self.jd1, self.jd2)
        self.assertEqual(318.51557827057434, gmsa0, 12)
        self.assertAlmostEqual(318.51557827281067, gmsa0, 8)

        gmsa1 = solar.gmsa(self.jd1, self.default + self.jd2)
        self.assertEqual(318.7852375269872, gmsa1, 12)
        self.assertAlmostEqual(318.78523752919864, gmsa1, 8)

        gmsa2 = solar.gmsa(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(318.7955092647899, gmsa2, 12)
        self.assertAlmostEqual(318.7955092670163, gmsa2, 8)

    def test_gmst(self):
        """
        testing Greenwich Mean Sideral Time with these delta t's
        0       21.234371884854045
        64.5415 21.252349168613243
        67      21.25303395113442
        """
        # print(self.test_sidereal_angles.__doc__)
        # print('testing solar.py Greenwich Mean Sideral Time method')
        gmst = solar.gmst(self.jd1, self.jd2)
        self.assertEqual(21.234371884704956, gmst, 12)
        self.assertAlmostEqual(21.234371884854045, gmst, 9)

        gmst1 = solar.gmst(self.jd1, self.default + self.jd2)
        self.assertEqual(21.252349168465813, gmst1, 12)
        self.assertAlmostEqual(21.252349168613243, gmst1, 9)

        gmst2 = solar.gmst(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(21.253033950985994, gmst2, 12)
        self.assertAlmostEqual(21.25303395113442, gmst2, 9)

if __name__ == "__main__":

    SIDEREAL = unittest.defaultTestLoader.loadTestsFromTestCase(TestSiderealTime)
    unittest.TextTestRunner(verbosity=2).run(SIDEREAL)

#end if
