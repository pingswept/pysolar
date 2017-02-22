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
from pysolar import solar, time, constants

class TestNutation(unittest.TestCase):
    """
    Test nutation methods plus terms effected by nutation or are
    actually part of nutation
    large should be numbers were derived from a modified copy of
    http://www.celnav.de/longterm.htm
    """
    longitude = -105.1786
    longitude_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dut1 = datetime.timedelta(seconds=0.0)
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67 / 86400.0
    default = 64.5415 / 86400
    param_list = [latitude, longitude, elevation, surface_slope,
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
        return None

    def test_apparent_solar_longitude(self):
        """
        0        204.00775769284664
        64.5415  204.0084989745065
        67       204.0085272110777
        """
        # print(self.test_apparent_sun_longitude.__doc__)
        # print('testing solar.py Apparent Sun Longitude method')
        asl0 = solar.apparent_solar_longitude(self.jct0)
        self.assertEqual(204.00783846758483, asl0, 12)
        self.assertAlmostEqual(204.00775769284664, asl0, 3)

        asl1 = solar.apparent_solar_longitude(self.jct1)
        self.assertEqual(204.00857974779782, asl1, 12)
        self.assertAlmostEqual(204.0084989745065, asl1, 3)

        asl2 = solar.apparent_solar_longitude(self.jct2)
        self.assertEqual(204.00860798431356, asl2, 12)
        self.assertAlmostEqual(204.0085272110777, asl2, 3)

    def test_delta_epsilon(self):
        """
        testing Nutation obliquity delta epsilon
        0         0.0016665452253917616
        64.5415   0.0016665472500373482
        67        0.001666547327214764
        """
        # print(self.test_delta_epsilon.__doc__)
        # print('testing solar.py Delta Epsilon method')
        deps0 = solar.nutation(self.jct0)['obliquity']
        self.assertEqual(0.0016668041903600411, deps0, 12)
        self.assertAlmostEqual(0.0016665452253917616, deps0, 6)

        deps1 = solar.nutation(self.jct1)['obliquity']
        self.assertEqual(0.0016668061340751688, deps1, 12)
        self.assertAlmostEqual(0.0016665472500373482, deps1, 6)

        deps2 = solar.nutation(self.jct2)['obliquity']
        self.assertEqual(0.001666806208170689, deps2, 12)
        self.assertAlmostEqual(0.001666547327214764, deps2, 6)

    def test_delta_psi(self):
        """
        testing Nutation longitude delta psi
        0         -0.003998135135636136
        64.5415   -0.0039981219235174165
        67        -0.003998121420285507
        """
        # print(self.test_delta_psi.__doc__)
        # print('testing solar.py Delta Psi method')
        dpsi0 = solar.nutation(self.jct0)['longitude']
        self.assertEqual(-0.003997960095151495, dpsi0, 12)
        self.assertAlmostEqual(-0.003998135135636136, dpsi0, 6)

        dpsi1 = solar.nutation(self.jct1)['longitude']
        self.assertEqual(-0.003997947151572717, dpsi1, 12)
        self.assertAlmostEqual(-0.0039981219235174165, dpsi1, 6)

        dpsi2 = solar.nutation(self.jct2)['longitude']
        self.assertEqual(-0.0039979466585653494, dpsi2, 12)
        self.assertAlmostEqual(-0.003998121420285507, dpsi2, 6)

    def test_equation_of_eqinox(self):
        """
        testing Equation of equinox = delta psi * cosine epsilon
        0          -0.003668185029955833
        64.5415    -0.0036681729081316267
        67         -0.0036681724464275732
        """
        # print(self.test_equation_of_eqinox.__doc__)
        # print('testing solar.py Equation of Equinox method')
        eqeq0 = solar.equation_of_equinox(self.jct0)
        self.assertEqual(-0.0036680244276743198, eqeq0, 15)
        self.assertAlmostEqual(-0.003668185029955833, eqeq0, 6)

        eqeq1 = solar.equation_of_equinox(self.jct1)
        self.assertEqual(-0.0036680125522307984, eqeq1, 15)
        self.assertAlmostEqual(-0.0036681729081316267, eqeq1, 6)

        eqeq2 = solar.equation_of_equinox(self.jct2)
        self.assertEqual(-0.0036680120999075835, eqeq2, 15)
        self.assertAlmostEqual(-0.0036681724464275732, eqeq2, 6)

    def test_mean_epsilon(self):
        """
        testing  Mean Obliquity epsilon
        0        23.43878599563886
        64.5415  23.43878599537278
        67       23.43878599536264
        """
        # print(self.test_mean_epsilon.__doc__)
        # print('testing solar.py Mean Epsilon method')
        meps0 = solar.mean_ecliptic_obliquity(self.jct0)
        self.assertEqual(23.43878599563886, meps0, 12)
        self.assertAlmostEqual(23.43878599563886, meps0, 12)

        meps1 = solar.mean_ecliptic_obliquity(self.jct1)
        self.assertEqual(23.43878599537278, meps1, 12)
        self.assertAlmostEqual(23.43878599537278, meps1, 12)

        meps2 = solar.mean_ecliptic_obliquity(self.jct2)
        self.assertEqual(23.43878599536264, meps2, 12)
        self.assertAlmostEqual(23.43878599536264, meps2, 12)

    def test_true_ecliptic_obliquity(self):
        """
        0       23.44045254086425
        64.5415 23.440452542622815
        67      23.440452542689854
        """
        teo0 = solar.true_ecliptic_obliquity(self.jct0)
        self.assertEqual(23.44045279982922, teo0, 12)
        self.assertAlmostEqual(23.44045254086425, teo0, 6)

        teo1 = solar.true_ecliptic_obliquity(self.jct1)
        self.assertEqual(23.440452801506854, teo1, 12)
        self.assertAlmostEqual(23.440452542622815, teo1, 6)

        teo2 = solar.true_ecliptic_obliquity(self.jct2)
        self.assertEqual(23.440452801506854, teo1, 12)
        self.assertAlmostEqual(23.440452542689854, teo2, 6)

if __name__ == "__main__":
    NUTATION = unittest.defaultTestLoader.loadTestsFromTestCase(TestNutation)

    unittest.TextTestRunner(verbosity=2).run(NUTATION)
#end if
