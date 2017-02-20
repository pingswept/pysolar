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

""" Tests for solar topocentrics """
import datetime
import unittest
from pysolar import solar, time, elevation, constants, util

class TestTopocentricSolar(unittest.TestCase):
    """
    Test topocentric results
    """
    longitude = -105.1786 # -105:
    longitude_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 820.0 # 1 pascal = 0.01 millibars
    elevation = 1830.14 # meters
    temperature = 11.0 # Celsius
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67 / 86400
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
        """
        set up
        """
        return None

    def angle_of_incidence(self):
        """
        testing
        """
        ai0 = solar.angle_of_incidence(self.jct0, self.param_list)
        self.assertEqual(25.339639446123176, ai0, 12)

        ai1 = solar.angle_of_incidence(self.jct1, self.param_list)
        self.assertEqual(25.51421682517004, ai1, 12)

        ai2 = solar.angle_of_incidence(self.jct2, self.param_list)
        self.assertEqual(25.5208986423648, ai2, 12)

    def incidence_angle(self):
        """
        testing Surface incidence angle
        0       25.187244
        67      25.187000
        """
        # print(self.test_incidence_angle.__doc__)
        # print('testing solar.py Angle of Incedence method')
        ia0 = solar.incidence_angle(self.jct0, self.param_list)
        self.assertEqual(24.583491615267757, ia0, 12)
        # self.assertAlmostEqual(25.187244, aoi0, 6)

        ia1 = solar.incidence_angle(self.jct1, self.param_list)
        self.assertEqual(24.736637036153752, ia1, 12)

        ia2 = solar.incidence_angle(self.jct2, self.param_list)
        self.assertEqual(24.742502719827574, ia2, 12)
        # self.assertAlmostEqual(25.187000, aoi2, 3)

        ia3 = solar.incidence_angle(self.jct3, self.param_list)
        self.assertEqual(24.482688726373773, ia3, 12)

        ia4 = solar.incidence_angle(self.jct4, self.param_list)
        self.assertEqual(24.63474650783982, ia4, 12)

        ia5 = solar.incidence_angle(self.jct5, self.param_list)
        self.assertEqual(24.640571170249267, ia5, 12)
        # self.assertAlmostEqual(25.187000, aoi2, 3)

    def right_ascension_parallax(self):
        """
        testing right ascension parallax
        0       -0.000369
        67      -0.000369
        """
        # print(self.test_right_ascension_parallax.__doc__)
        # print('testing solar.py Right Ascension Parallax method')
        rap = solar.right_ascension_parallax(self.jct0, self.param_list)
        self.assertEqual(-0.00037706297191607074, rap, 12)
        # self.assertAlmostEqual(-0.000369, rap, 5)

        rap1 = solar.right_ascension_parallax(self.jct1, self.param_list)
        self.assertEqual(-0.0003857988336644988, rap1, 12)

        rap2 = solar.right_ascension_parallax(self.jct2, self.param_list)
        self.assertEqual(-0.0003861314294521253, rap2, 12)
        # self.assertAlmostEqual(-0.000369, rap1, 5)

    def topocentric_azimuth_angle(self):
        """
        testing Topocentric azimuth angle (eastward from N)
        0       194.341226 NOAA val 194.34
        67      194.340241
        """
        # print(self.test_topocentric_azimuth_angle.__doc__)
        # print('testing solar.py Topocentric Azimuth Angle method')
        taa0 = solar.topocentric_azimuth_angle(self.jct0, self.param_list)
        self.assertEqual(192.73534988387541, taa0, 12)
        # self.assertAlmostEqual(194.341226, taa1, 6)

        taa1 = solar.topocentric_azimuth_angle(self.jct1, self.param_list)
        self.assertEqual(193.03078489862457, taa1, 12)

        taa2 = solar.topocentric_azimuth_angle(self.jct2, self.param_list)
        self.assertEqual(193.0420335036125, taa2, 12)
        # self.assertAlmostEqual(194.340241, taa0, 6)

    def topocentri_elevation_angle(self):
        """
        0   39.888518 NOAA val 39.89
        67  39.888378
        """
        tea0 = solar.topocentric_elevation_angle(self.jct0, self.param_list)
        self.assertEqual(39.9104553565036, tea0, 12)
        # self.assertAlmostEqual(39.888518, tea0, 6)

        tea1 = solar.topocentric_elevation_angle(self.jct1, self.param_list)
        self.assertEqual(39.856764902582, tea1, 12)
        # self.assertAlmostEqual(39.888518, tea0, 6)

        tea2 = solar.topocentric_elevation_angle(self.jct2, self.param_list)
        self.assertEqual(39.85469640688999, tea2, 12)
        # self.assertAlmostEqual(39.888378, tea0, 6)

        tea3 = 90 - solar.topocentric_zenith_angle(self.jct2, self.param_list)
        self.assertEqual(39.9102923427883, tea3, 12)

    def topocentric_lha(self):
        """
        testing Topocentric local hour angle
        0       11.106996
        67      11.106271
        """
        # print(self.test_topocentric_lha.__doc__)
        # print('testing solar.py Topocentric Local Hour Angle method')
        tlha = solar.topocentric_lha(self.jct0, self.param_list)
        self.assertEqual(11.44932422168693, tlha, 12)
        # self.assertAlmostEqual(11.106996, tlha, 0)

        tlha1 = solar.topocentric_lha(self.jct1, self.param_list)
        self.assertEqual(11.718294372479479, tlha1, 12)

        tlha2 = solar.topocentric_lha(self.jct2, self.param_list)
        self.assertEqual(11.728539860989146, tlha2, 12)
        # self.assertAlmostEqual(11.106271, tlha2, 0)

    def test_topocentri_right_ascension(self):
        """
        testing Topocentric sun right ascension
        0       202.226314 / 15
        67      202.227039 / 15
        """
        # print(self.test_topo_right_ascension.__doc__)
        # print('testing solar.py Topocentric Right Ascension method')
        tsra0 = solar.topocentric_right_ascension(self.jct0, self.param_list)
        self.assertEqual(202.22613656450582, tsra0, 12)
        self.assertAlmostEqual(202.226314, tsra0, 3)

        tsra1 = solar.topocentric_right_ascension(self.jct1, self.param_list)
        self.assertEqual(202.226836322856, tsra1, 12)

        tsra2 = solar.topocentric_right_ascension(self.jct2, self.param_list)
        self.assertEqual(202.22686297801366, tsra2, 12)
        self.assertAlmostEqual(202.227039, tsra2, 3)

    def test_topocentri_sun_declination(self):
        """
        testing Topocentric sun declination
        0       -9.315895 NOAA val -9.32
        67      -9.316179
        """
        # print(self.test_topo_sun_declination.__doc__)
        # print('testing solar.py Topocentric Sun Declination method')
        # note: using jd4 with location longitude factored in minus time zone.
        tsd = solar.topocentric_solar_declination(self.jct0, self.param_list)
        self.assertEqual(-9.315475816336868, tsd, 12)
        self.assertAlmostEqual(-9.315895, tsd, 3)

        tsd1 = solar.topocentric_solar_declination(self.jct1, self.param_list)
        self.assertEqual(-9.315747710974527, tsd1, 12)

        tsd2 = solar.topocentric_solar_declination(self.jct2, self.param_list)
        self.assertEqual(-9.315758067884662, tsd2, 12)
        self.assertAlmostEqual(-9.316179, tsd2, 3)

    def topocentric_zenith_angle(self):
        """
        testing Topocentric zenith angle
        0       50.111482
        67      50.111622
        """
        # print(self.test_topocentric_zenith_angle.__doc__)
        # print('testing solar.py Topocentric Zenith Angle method')
        tza = solar.topocentric_zenith_angle(self.jct0, self.param_list)
        self.assertEqual(50.0897076572117, tza, 12)
        # self.assertAlmostEqual(50.111482, tza, 6)

        tza1 = solar.topocentric_zenith_angle(self.jct1, self.param_list)
        self.assertEqual(50.14339841986092, tza1, 12)

        tza2 = solar.topocentric_zenith_angle(self.jct1, self.param_list)
        self.assertEqual(50.145466927460674, tza2, 12)
        # self.assertAlmostEqual(50.111622, tza2, 6)

        tza3 = 90 - solar.topocentric_elevation_angle(self.jct2, self.param_list)
        self.assertEqual(50.0895446434964, tza3, 12)

if __name__ == "__main__":

    TSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestTopocentricSolar)

    unittest.TextTestRunner(verbosity=2).run(TSOLAR)
