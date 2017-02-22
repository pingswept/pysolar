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
"""
tests for time.py
"""
import datetime
import time as pytime
import unittest
from pysolar import time, constants
class TestTime(unittest.TestCase):
    """
    Test time methods
    """
    delta_t = 67
    longitude = -105.1786
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    params_list = [elevation, latitude, longitude, surface_slope,
                   surface_azimuth_rotation, temperature, pressure]
    lon_offset = longitude / 360.0
    dut1 = datetime.timedelta(seconds=0.0)
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]

    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        return int(pytime.time())

    def test_delta_ut1(self):
        """
        testing
        see DUT1 http://asa.usno.navy.mil/SecM/Glossary.html#ut1
        MIDC SPA is set to 0 sec DUT1
        """
        # print(self.test_delta_ut1.__doc__)
        dut1 = datetime.timedelta(0)
        self.assertEqual(dut1, self.dut1)

    def test_ephemeris_to_solar(self):
        """
        testing
        A comparison of Julian Ephemeris day to Julian Day
        This shows a little bit of error creeping in
        """
        # print(self.test_ephemeris_to_solar.__doc__)
        jed1 = time.julian_ephemeris_day(self.dt_list)
        jed1 += self.delta_t / 86400.0
        jsd1 = time.julian_day(self.dt_list)
        test = (jed1 - jsd1) * 86400 - self.delta_t
        self.assertEqual(-1.3113021850585938e-06, test)

    def test_julian_astronomical(self):
        """
        MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        testing jdn and ajd
        0       2452930.312847
        64.5415 2452930.313594
        67
        """
        # print(self.test_julian_astronomical.__doc__)
        # print('testing time.py Julian Day method')
        jdn = time.jdn(self.dt_list)
        self.assertEqual(2452930, jdn)

        ajd0 = time.ajd(self.dt_list, 0)
        self.assertEqual(2452930.312847222, ajd0, 6)

        ajd1 = time.ajd(self.dt_list)
        self.assertEqual(2452930.3135942305, ajd1, 6)

        ajd2 = time.ajd(self.dt_list, self.delta_t)
        self.assertEqual(2452930.313622685, ajd2, 6)

        jsd0 = time.julian_day(self.dt_list, 0)
        self.assertEqual(2452930.312847222, jsd0, 6)

        jsd1 = time.julian_day(self.dt_list)
        self.assertEqual(2452930.3135942305, jsd1, 6)

        jsd2 = time.julian_day(self.dt_list, self.delta_t)
        self.assertEqual(2452930.313622685, jsd2, 6)

    def test_julian_century(self):
        """
        MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        testing Julian century
        0       0.037928
        64.5415 0.037928
        67
        """
        jd0 = time.julian_day(self.dt_list, 0)
        jct0 = time.julian_century(jd0)
        self.assertEqual(0.03792779869191517, jct0, 6)
        self.assertAlmostEqual(0.037928, jct0, 6)

        jct1 = time.julian_century(jd0 + 64.5415 / 86400)
        self.assertEqual(0.0379278191438864, jct1, 6)
        self.assertAlmostEqual(0.037928, jct1, 6)

        jct2 = time.julian_century(jd0 + 67 / 86400)
        self.assertEqual(0.037927819922933585, jct2, 6)
        self.assertAlmostEqual(0.037928, jct2, 6)

    def test_julian_ephemeris_day(self):
        """
        testing Julian ephemeris day
        0  2452930.312847
        67 2452930.313623
        """
        # print(self.test_julian_ephemeris.__doc__)
        # print('testing time.py Julian Ephemeris Day method')

        jed0 = time.julian_ephemeris_day(self.dt_list, 0)
        self.assertEqual(2452930.312847222, jed0, 6)
        self.assertAlmostEqual(2452930.312847, jed0, 6)

        jed1 = time.julian_ephemeris_day(self.dt_list)
        self.assertEqual(2452930.3135942305, jed1, 6)
        self.assertAlmostEqual(2452930.313594, jed1, 6)

        jed2 = time.julian_ephemeris_day(self.dt_list, self.delta_t)
        self.assertEqual(2452930.313622685, jed2, 6)
        self.assertAlmostEqual(2452930.313623, jed2, 6)

    def test_julian_ephemeris_century(self):
        """
        testing Julian ephemeris century
        0  0.037928
        67 0.037928
        """
        # print(self.test_julian_ephemeris.__doc__)
        # print('testing time.py Julian Ephemeris Century method')
        jec1 = time.julian_ephemeris_century(self.dt_list, 0)
        self.assertEqual(0.03792779869191517, jec1, 6)
        self.assertAlmostEqual(0.037928, jec1, 6)

        jec = time.julian_ephemeris_century(self.dt_list)
        self.assertEqual(0.0379278191438864, jec, 6)
        self.assertAlmostEqual(0.037928, jec, 6)

        jec2 = time.julian_ephemeris_century(self.dt_list, self.delta_t)
        self.assertEqual(0.037927819922933585, jec2, 6)
        self.assertAlmostEqual(0.037928, jec2, 6)

    def test_julian_ephemeris_millennium(self):
        """
        testing Julian ephemeris millennium
        0   0.003793
        67  0.003793
        """
        # print('testing time.py Julian Ephemeris Millennium method')
        jem0 = time.julian_ephemeris_millennium(self.dt_list, 0)
        self.assertEqual(0.003792779869191517, jem0, 12)
        self.assertAlmostEqual(0.003793, jem0, 6)

        jem1 = time.julian_ephemeris_millennium(self.dt_list)
        self.assertEqual(0.0037927819143886397, jem1, 12)
        self.assertAlmostEqual(0.003793, jem1, 6)

        jem2 = time.julian_ephemeris_millennium(self.dt_list, self.delta_t)
        self.assertEqual(0.0037927819922933584, jem2, 12)
        self.assertAlmostEqual(0.003793, jem2, 6)

    def test_leap_seconds(self):
        """
        testing Leap seconds
        """
        # print(self.test_leap_seconds.__doc__)
        # print('testing time.py Leap Seconds method')
        gls = time.leap_seconds(self.dt_list)
        self.assertEqual(gls, 32)

    def test_timestamp(self):
        """
        testing Timestamp
        """
        # print(self.test_timestamp.__doc__)
        tss1 = time.timestamp(self.dt_list, 0)
        self.assertEqual(1066437030.0, tss1, 12)

        tss2 = time.timestamp(self.dt_list)
        self.assertEqual(1066437094.5415, tss2, 12)

        tss = time.timestamp(self.dt_list, self.delta_t)
        self.assertEqual(1066437097.0, tss, 12)

if __name__ == "__main__":
    TIME = unittest.defaultTestLoader.loadTestsFromTestCase(TestTime)
    unittest.TextTestRunner(verbosity=2).run(TIME)
