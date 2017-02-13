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

""" Tests for solar azimuth altitude """
import datetime
import unittest
from pysolar import solar, constants, util
class TestAzAltSolar(unittest.TestCase):
    """
    Tests functions that use when as a time parameter
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    tyn = util.TY_DEFAULT
    amd = util.AM_DEFAULT
    ltf = util.TL_DEFAULT
    spc = util.SC_DEFAULT
    param_list = [elevation, latitude, longitude, surface_slope,
                  surface_azimuth_rotation, temperature, pressure,
                  tyn, amd, ltf, spc]
    def setUp(self):
        self.when0 = datetime.datetime(
            2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)
        self.when1 = datetime.datetime(
            2003, 10, 17, 19, 31, 34, 5415, tzinfo=datetime.timezone.utc)
        self.when2 = datetime.datetime(
            2003, 10, 17, 19, 31, 37, tzinfo=datetime.timezone.utc)

    def test_altitude(self):
        """
        testing Altitude Angle
        """
        # print(self.test_altitude.__doc__)
        # print('testing solar.py Altitude Angle method')
        alt = solar.altitude(self.when0, self.param_list)
        self.assertEqual(63.79703840292356, alt, 12)

        alt1 = solar.altitude(self.when1, self.param_list)
        self.assertEqual(63.76299277821548, alt1, 12)

        alt2 = solar.altitude(self.when2, self.param_list)
        self.assertEqual(63.76142336675205, alt2, 12)

    def test_azimuth(self):
        """
        testing Azimuth
        """
        # print(self.test_azimuth.__doc__)
        # print('testing solar.py Azimuth Angle method')
        azm = solar.azimuth(self.when0, self.param_list)
        self.assertEqual(8.555603593622664, azm, 12)

        azm1 = solar.azimuth(self.when1, self.param_list)
        self.assertEqual(8.314833126248914, azm1, 12)

        azm2 = solar.azimuth(self.when2, self.param_list)
        self.assertEqual(8.303565890510981, azm2, 12)

if __name__ == "__main__":

    AESOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestAzAltSolar)

    unittest.TextTestRunner(verbosity=2).run(AESOLAR)


#end if
