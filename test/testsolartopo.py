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
    pressure = 820.0 # millibars
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67 /86400
    param_list = [elevation, latitude, longitude, surface_slope,
                  surface_azimuth_rotation, temperature, pressure]
    jd_hours = dt_list[3] / 24.0
    jd_minutes = dt_list[4] / 1440.0
    jd_seconds = dt_list[5] / 86400.0
    def setUp(self):
        self.jd1 = time.jdn(self.dt_list) - 0.5
        self.jd2 = self.jd_hours + self.jd_minutes + self.jd_seconds
        self.jd3 = 0.5 + self.jd_minutes + self.jd_seconds
        # need to take the timezone offset out because all
        # whole julian day numbers begin at noon.
        self.jd4 = self.jd3 - self.longitude_offset - 7 / 24.0
        self.default = time.delta_t(self.jd1 + self.jd2) / 86400.0

    def test_angle_of_incidence(self):
        """
        testing
        """
        ai0 = solar.angle_of_incidence(self.jd1, self.jd4, self.param_list)
        self.assertEqual(25.339639446123176, ai0, 12)

        ai1 = solar.angle_of_incidence(self.jd1, self.default + self.jd4, self.param_list)
        self.assertEqual(25.51421682517004, ai1, 12)

        ai2 = solar.angle_of_incidence(self.jd1, self.delta_t + self.jd4, self.param_list)
        self.assertEqual(25.5208986423648, ai2, 12)

    def test_incidence_angle(self):
        """
        testing Surface incidence angle
        0       25.187244
        67      25.187000
        """
        # print(self.test_incidence_angle.__doc__)
        # print('testing solar.py Angle of Incedence method')
        ia0 = solar.incidence_angle(self.jd1, self.jd4, self.param_list)
        self.assertEqual(24.583491615267757, ia0, 12)
        # self.assertAlmostEqual(25.187244, aoi0, 6)

        ia1 = solar.incidence_angle(self.jd1, self.default + self.jd4, self.param_list)
        self.assertEqual(24.736637036153752, ia1, 12)

        ia2 = solar.incidence_angle(self.jd1, self.delta_t + self.jd4, self.param_list)
        self.assertEqual(24.742502719827574, ia2, 12)
        # self.assertAlmostEqual(25.187000, aoi2, 3)

        ia3 = solar.incidence_angle(self.jd1, self.jd3, self.param_list)
        self.assertEqual(24.482688726373773, ia3, 12)

        ia4 = solar.incidence_angle(self.jd1, self.default + self.jd3, self.param_list)
        self.assertEqual(24.63474650783982, ia4, 12)

        ia5 = solar.incidence_angle(self.jd1, self.delta_t + self.jd3, self.param_list)
        self.assertEqual(24.640571170249267, ia5, 12)
        # self.assertAlmostEqual(25.187000, aoi2, 3)

    def test_right_ascension_parallax(self):
        """
        testing right ascension parallax
        0       -0.000369
        67      -0.000369
        """
        # print(self.test_right_ascension_parallax.__doc__)
        # print('testing solar.py Right Ascension Parallax method')
        rap = solar.right_ascension_parallax(self.jd1, self.jd4, self.param_list)
        self.assertEqual(-0.00037706297191607074, rap, 12)
        # self.assertAlmostEqual(-0.000369, rap, 5)

        rap1 = solar.right_ascension_parallax(self.jd1, self.default + self.jd4, self.param_list)
        self.assertEqual(-0.0003857988336644988, rap1, 12)

        rap2 = solar.right_ascension_parallax(self.jd1, self.delta_t + self.jd4, self.param_list)
        self.assertEqual(-0.0003861314294521253, rap2, 12)
        # self.assertAlmostEqual(-0.000369, rap1, 5)

    def test_topocentric_azimuth_angle(self):
        """
        testing Topocentric azimuth angle (eastward from N)
        0       194.341226 NOAA val 194.34
        67      194.340241
        """
        # print(self.test_topocentric_azimuth_angle.__doc__)
        # print('testing solar.py Topocentric Azimuth Angle method')
        taa0 = solar.topocentric_azimuth_angle(self.jd1, self.jd4, self.param_list)
        self.assertEqual(192.73534988387541, taa0, 12)
        # self.assertAlmostEqual(194.341226, taa1, 6)

        taa1 = solar.topocentric_azimuth_angle(self.jd1, self.default + self.jd4, self.param_list)
        self.assertEqual(193.03078489862457, taa1, 12)

        taa2 = solar.topocentric_azimuth_angle(self.jd1, self.delta_t + self.jd4, self.param_list)
        self.assertEqual(193.0420335036125, taa2, 12)
        # self.assertAlmostEqual(194.340241, taa0, 6)

    def test_topocentri_elevation_angle(self):
        """
        0   39.888518 NOAA val 39.89
        67  39.888378
        """
        tea0 = solar.topocentric_elevation_angle(self.jd1, self.jd4, self.param_list)
        self.assertEqual(39.9104553565036, tea0, 12)
        # self.assertAlmostEqual(39.888518, tea0, 6)

        tea1 = solar.topocentric_elevation_angle(self.jd1, self.default + self.jd4, self.param_list)
        self.assertEqual(39.856764902582, tea1, 12)
        # self.assertAlmostEqual(39.888518, tea0, 6)

        tea2 = solar.topocentric_elevation_angle(self.jd1, self.delta_t + self.jd4, self.param_list)
        self.assertEqual(39.85469640688999, tea2, 12)
        # self.assertAlmostEqual(39.888378, tea0, 6)

        tea3 = 90 - solar.topocentric_zenith_angle(self.jd1, self.jd4, self.param_list)
        self.assertEqual(39.9102923427883, tea3, 12)

    def test_topocentric_lha(self):
        """
        testing Topocentric local hour angle
        0       11.106996
        67      11.106271
        """
        # print(self.test_topocentric_lha.__doc__)
        # print('testing solar.py Topocentric Local Hour Angle method')
        tlha = solar.topocentric_lha(self.jd1, self.jd4, self.param_list)
        self.assertEqual(11.44932422168693, tlha, 12)
        # self.assertAlmostEqual(11.106996, tlha, 0)

        tlha1 = solar.topocentric_lha(self.jd1, self.default + self.jd4, self.param_list)
        self.assertEqual(11.718294372479479, tlha1, 12)

        tlha2 = solar.topocentric_lha(self.jd1, self.delta_t + self.jd4, self.param_list)
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
        tsra0 = solar.topocentric_right_ascension(self.jd1, self.jd4, self.param_list)
        self.assertEqual(201.95418977477132, tsra0, 12)
        # self.assertAlmostEqual(202.226314, tsra0, 5)

        tsra1 = solar.topocentric_right_ascension(
            self.jd1, self.default + self.jd4, self.param_list)
        self.assertEqual(201.95487889274426, tsra1, 12)

        tsra2 = solar.topocentric_right_ascension(
            self.jd1, self.delta_t + self.jd4, self.param_list)
        self.assertEqual(201.954905142508, tsra2, 12)
        # self.assertAlmostEqual(202.227039, tsra2, 5)

    def test_topocentri_sun_declination(self):
        """
        testing Topocentric sun declination
        0       -9.315895 NOAA val -9.32
        67      -9.316179
        """
        # print(self.test_topo_sun_declination.__doc__)
        # print('testing solar.py Topocentric Sun Declination method')
        # note: using jd4 with location longitude factored in minus time zone.
        tsd = solar.topocentric_solar_declination(self.jd1, self.jd4, self.param_list)
        self.assertEqual(-9.209338423282212, tsd, 12)
        # self.assertAlmostEqual(-9.315895, tsd, 3)

        tsd1 = solar.topocentric_solar_declination(
            self.jd1, self.default + self.jd4, self.param_list)
        self.assertEqual(-9.209611623714624, tsd1, 12)

        tsd2 = solar.topocentric_solar_declination(
            self.jd1, self.delta_t + self.jd4, self.param_list)
        self.assertEqual(-9.209622030211623, tsd2, 12)
        # self.assertAlmostEqual(-9.316179, tsd2, 3)

    def test_topocentric_zenith_angle(self):
        """
        testing Topocentric zenith angle
        0       50.111482
        67      50.111622
        """
        # print(self.test_topocentric_zenith_angle.__doc__)
        # print('testing solar.py Topocentric Zenith Angle method')
        tza = solar.topocentric_zenith_angle(self.jd1, self.jd4, self.param_list)
        self.assertEqual(50.0897076572117, tza, 12)
        # self.assertAlmostEqual(50.111482, tza, 6)

        tza1 = solar.topocentric_zenith_angle(self.jd1, self.default + self.jd4, self.param_list)
        self.assertEqual(50.14339841986092, tza1, 12)

        tza2 = solar.topocentric_zenith_angle(self.jd1, self.delta_t + self.jd4, self.param_list)
        self.assertEqual(50.145466927460674, tza2, 12)
        # self.assertAlmostEqual(50.111622, tza2, 6)

        tza3 = 90 - solar.topocentric_elevation_angle(self.jd1, self.jd4, self.param_list)
        self.assertEqual(50.0895446434964, tza3, 12)

if __name__ == "__main__":

    TSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestTopocentricSolar)

    unittest.TextTestRunner(verbosity=2).run(TSOLAR)
