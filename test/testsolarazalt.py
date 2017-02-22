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
from pysolar import azelsolar, constants, util

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
    param_list = [latitude, longitude, elevation, surface_slope,
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
        alt = azelsolar.altitude(self.when0, self.param_list)
        self.assertEqual(39.82844682673359, alt, 12)

        alt1 = azelsolar.altitude(self.when1, self.param_list)
        self.assertEqual(39.775639446793036, alt1, 12)

        alt2 = azelsolar.altitude(self.when2, self.param_list)
        self.assertEqual(39.7731403675628, alt2, 12)

    def test_azimuth(self):
        """
        testing Azimuth
        """
        # print(self.test_azimuth.__doc__)
        # print('testing solar.py Azimuth Angle method')
        azm0 = azelsolar.azimuth(self.when0, self.param_list)
        self.assertEqual(194.68016811582498, azm0, 12)

        azm1 = azelsolar.azimuth(self.when1, self.param_list)
        self.assertEqual(195.01577219120838, azm1, 12)

        azm2 = azelsolar.azimuth(self.when2, self.param_list)
        self.assertEqual(195.0314600048607, azm2, 12)

if __name__ == "__main__":

    AESOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestAzAltSolar)
    unittest.TextTestRunner(verbosity=2).run(AESOLAR)

#end if
