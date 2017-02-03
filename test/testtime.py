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
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        # below are ways to make adjustments for delta t. But we are using dt_list[7] for now
        # self.dt_list[5] = math.floor(time.get_delta_t(self.dt_list)) + self.dt_list[5]
        # self.dt_list[6] = round((time.get_delta_t(self.dt_list) % 1) * 1e6) + self.dt_list[6]
        return 'Testing pysolar time functions', int(pytime.time())

    def test_delta_ut1(self):
        """
        testing
        see DUT1 http://asa.usno.navy.mil/SecM/Glossary.html#ut1
        MIDC SPA is set to 0 sec DUT1
        """
        # print(self.test_delta_ut1.__doc__)
        print('testing time.py Delta T method')
        dut1 = datetime.timedelta(0)
        self.assertEqual(dut1, self.dut1)

    def test_julian_astronomical(self):
        """
        MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        Date, Time,
        10/17/2003, 12:30:30
        Julian day, Julian century
        delta t 67
        2452930.312847, 0.037928
        delta t 0
        2452930.312847, 0.037928
        no delta t defaults to current delta t of date
        2452930.313594, 0.037928
        """
        # print(self.test_julian_astronomical.__doc__)
        print('testing time.py Julian Day method')
        jdn = time.jdn(self.dt_list)
        self.assertEqual(2452930, jdn)

        ajd = time.ajd(self.dt_list, self.delta_t)
        self.assertEqual(2452930.313622685, ajd, 6)

        ajd1 = time.ajd(self.dt_list, 0)
        self.assertEqual(2452930.312847222, ajd1, 6)

        ajd2 = time.ajd(self.dt_list)
        self.assertEqual(2452930.3135942305, ajd2, 6)

        jsd = time.julian_day(self.dt_list, self.delta_t)
        self.assertEqual(2452930.313622685, jsd, 6)

        jsd1 = time.julian_day(self.dt_list, 0)
        self.assertEqual(2452930.312847222, jsd1, 6)

        jsd2 = time.julian_day(self.dt_list)
        self.assertEqual(2452930.3135942305, jsd2, 6)

        print('testing time.py Julian Century method')
        jct = time.julian_century(self.dt_list, self.delta_t)
        self.assertEqual(0.037927819922933585, jct, 6)
        self.assertAlmostEqual(0.037928, jct, 6)

        jct1 = time.julian_century(self.dt_list, 0)
        self.assertEqual(0.03792779869191517, jct1, 6)
        self.assertAlmostEqual(0.037928, jct1, 6)

        jct2 = time.julian_century(self.dt_list)
        self.assertEqual(0.0379278191438864, jct2, 6)
        self.assertAlmostEqual(0.037928, jct2, 6)

    def test_julian_ephemeris(self):
        """
        Julian ephemeris day, Julian ephemeris century, Julian ephemeris millennium
        delta t 67
        2452930.313623, 0.037928, 0.003793
        delta t 0
        2452930.312847, 0.037928, 0.003793
        """
        # print(self.test_julian_ephemeris.__doc__)
        print('testing time.py Julian Ephemeris Day method')
        jed = time.julian_ephemeris_day(self.dt_list, self.delta_t)
        self.assertEqual(2452930.313622685, jed, 6)
        self.assertAlmostEqual(2452930.313623, jed, 6)

        jed1 = time.julian_ephemeris_day(self.dt_list, 0)
        self.assertEqual(2452930.312847222, jed1, 6)
        self.assertAlmostEqual(2452930.312847, jed1, 6)

        jed2 = time.julian_ephemeris_day(self.dt_list)
        self.assertEqual(2452930.3135942305, jed2, 6)
        self.assertAlmostEqual(2452930.313594, jed2, 6)

        print('testing time.py Julian Ephemeris Century method')
        jec = time.julian_ephemeris_century(self.dt_list)
        self.assertEqual(0.0379278191438864, jec, 6)
        self.assertAlmostEqual(0.037928, jec, 6)

        jec1 = time.julian_ephemeris_century(self.dt_list, 0)
        self.assertEqual(0.03792779869191517, jec1, 6)
        self.assertAlmostEqual(0.037928, jec1, 6)

        jec2 = time.julian_ephemeris_century(self.dt_list, self.delta_t)
        self.assertEqual(0.037927819922933585, jec2, 6)
        self.assertAlmostEqual(0.037928, jec2, 6)

        print('testing time.py Julian Ephemeris Millennium method')
        jem = time.julian_ephemeris_millennium(self.dt_list, self.delta_t)
        self.assertEqual(0.003792781992293359, jem, 6)
        self.assertAlmostEqual(0.003793, jem, 6)

        jem1 = time.julian_ephemeris_millennium(self.dt_list, 0)
        self.assertEqual(0.003792779869191517, jem1, 6)
        self.assertAlmostEqual(0.003793, jem1, 6)

        jem2 = time.julian_ephemeris_millennium(self.dt_list)
        self.assertEqual(0.0037927819143886397, jem2, 6)
        self.assertAlmostEqual(0.003793, jem2, 6)

        jlon = time.julian_day(self.dt_list, self.delta_t) - self.lon_offset
        self.assertEqual(2452930.605785463, jlon, 6)

        jlon1 = time.julian_day(self.dt_list, 0) - self.lon_offset
        self.assertEqual(2452930.60501, jlon1, 6)

        jlon2 = time.julian_day(self.dt_list) - self.lon_offset
        self.assertEqual(2452930.6057570083, jlon2, 6)

    def test_leap_seconds(self):
        """
        testing Leap seconds
        """
        # print(self.test_leap_seconds.__doc__)
        print('testing time.py Leap Seconds method')
        gls = time.leap_seconds(self.dt_list)
        self.assertEqual(gls, 32)

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

    def test_timestamp(self):
        """
        testing Timestamp
        """
        # print(self.test_timestamp.__doc__)
        # print(int(pytime.time())/86400.0 + 2440587.5)
        print('testing time.py Timestamp method')
        tss = time.timestamp(self.dt_list, self.delta_t)
        self.assertEqual(1066437097.0, tss, 6)

        tss1 = time.timestamp(self.dt_list, 0)
        self.assertEqual(1066437030.0, tss1, 6)

        tss2 = time.timestamp(self.dt_list)
        self.assertEqual(1066437094.5415, tss2, 6)

if __name__ == "__main__":
    TIME = unittest.defaultTestLoader.loadTestsFromTestCase(TestTime)
    unittest.TextTestRunner(verbosity=2).run(TIME)
