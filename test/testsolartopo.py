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
import unittest
from pysolar import solar, time

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

    def test_angle_of_incidence(self):
        """
        testing Surface incidence angle
        experimental see method doc string
        """
        ai0 = solar.angle_of_incidence(self.jct3, self.param_list)
        self.assertEqual(23.15231729891296, ai0, 12)
        hours = (((self.jct3 * 36525.0 + time.DJ00) % 1.0 + 0.5) * 24.0)
        print(hours)
        print(15 * (hours - 12.0))

        ai1 = solar.angle_of_incidence(self.jct4, self.param_list)
        self.assertEqual(23.301592583019893, ai1, 12)
        hours = (((self.jct4 * 36525.0 + time.DJ00) % 1.0 + 0.5) * 24.0)
        print(hours)
        print(15 * (hours - 12.0))

        ai2 = solar.angle_of_incidence(self.jct5, self.param_list)
        self.assertEqual(23.30732056578055, ai2, 12)
        hours = (((self.jct5 * 36525.0 + time.DJ00) % 1.0 + 0.5) * 24.0)
        print(hours)
        print(15 * (hours - 12.0))

    def test_incidence_angle(self):
        """
        testing Surface incidence angle
        0       25.187244
        67      25.187000
        """
        # print(self.test_incidence_angle.__doc__)
        # print('testing solar.py Angle of Incedence method')
        ia0 = solar.incidence_angle(self.jct0, self.param_list)
        self.assertEqual(25.20520131177765, ia0, 12)
        self.assertAlmostEqual(25.187244, ia0, 1)

        ia1 = solar.incidence_angle(self.jct1, self.param_list)
        self.assertEqual(25.37711871797506, ia1, 12)

        ia2 = solar.incidence_angle(self.jct2, self.param_list)
        self.assertEqual(25.383700108185433, ia2, 12)
        self.assertAlmostEqual(25.187000, ia2, 0)

        """
        0
        10/17/2003,12:31:11,90.322542,2452930.021655
        10/17/2003,12:31:12,90.318494,2452930.021667
        10/17/2003,12:31:13,90.314445,2452930.021678
        """
        print(self.jct3 * 36525.0 + time.DJ00)
        ia3 = solar.incidence_angle(self.jct3, self.param_list)
        self.assertEqual(90.31502934323628, ia3, 12)
        self.assertAlmostEqual(90.315, ia3, 3)
        """
        65.5415
        10/17/2003,12:32:17,90.056113,2452930.022419
        10/17/2003,12:32:18,90.052066,2452930.022431
        """
        print(self.jct4 * 36525.0 + time.DJ00)
        ia4 = solar.incidence_angle(self.jct4, self.param_list)
        self.assertEqual(90.05376749550899, ia4, 12)
        self.assertAlmostEqual(90.054, ia4, 3)
        """
        67
        10/17/2003,12:32:19,90.048018,2452930.022442
        10/17/2003,12:32:20,90.043970,2452930.022454
        """
        print(self.jct5 * 36525.0 + time.DJ00)
        ia5 = solar.incidence_angle(self.jct5, self.param_list)
        self.assertEqual(90.04381633115992, ia5, 12)
        self.assertAlmostEqual(90.044, ia5, 3)

    def test_projected_axial_distance(self):
        """
        testing Projected axial distance
        MIDC SPA is not at 12:30
        """
        # print(self.test_projected_axial_distance.__doc__)
        # print('testing solar.py Projected Axial Distance method')
        pad = solar.projected_axial_distance(self.param_list)
        self.assertEqual(0.636112170624418, pad, 12)

    def test_projected_radial_distance(self):
        """
        testing Projected radial distance
        MIDC SPA is not at 12:30
        """
        # print(self.test_projected_radial_distance.__doc__)
        # print('testing solar.py Projected Radial Distance method')
        prd = solar.projected_radial_distance(self.param_list)
        self.assertEqual(0.7702006193304247, prd, 12)

    def test_right_ascension_parallax(self):
        """
        testing right ascension parallax
        0       -0.000369
        67      -0.000369
        """
        # print(self.test_right_ascension_parallax.__doc__)
        # print('testing solar.py Right Ascension Parallax method')
        rap0 = solar.right_ascension_parallax(self.jct0, self.param_list)
        self.assertEqual(-0.0003685571849308375, rap0, 12)
        self.assertAlmostEqual(-0.000369, rap0, 6)

        rap1 = solar.right_ascension_parallax(self.jct1, self.param_list)
        self.assertEqual(-0.0003773664813711657, rap1, 12)

        rap2 = solar.right_ascension_parallax(self.jct2, self.param_list)
        self.assertEqual(-0.0003777018782335917, rap2, 12)
        self.assertAlmostEqual(-0.000369, rap1, 4)

    def test_topocentric_azimuth_angle(self):
        """
        testing Topocentric azimuth angle (eastward from N)
        0       194.341226 NOAA val 194.34
        67      194.340241 or 14.340241
        """
        # print(self.test_topocentric_azimuth_angle.__doc__)
        # print('testing solar.py Topocentric Azimuth Angle method')
        taa0 = solar.topocentric_azimuth_angle(self.jct0, self.param_list)
        self.assertEqual(194.34118376640455, taa0, 12)
        self.assertAlmostEqual(194.341226, taa0, 4)

        taa1 = solar.topocentric_azimuth_angle(self.jct1, self.param_list)
        self.assertEqual(194.68016811582498, taa1, 12)

        taa2 = solar.topocentric_azimuth_angle(self.jct2, self.param_list)
        self.assertEqual(194.69306932021885, taa2, 12)
        self.assertAlmostEqual(194.340241, taa2, 0)

    def test_topocentri_elevation_angle(self):
        """
        0   39.888518 NOAA val 39.89
        67  39.888378
        """
        tea0 = solar.topocentric_elevation_angle(self.jct0, self.param_list)
        self.assertEqual(39.87219436130642, tea0, 12)
        self.assertAlmostEqual(39.888518, tea0, 1)

        tea1 = solar.topocentric_elevation_angle(self.jct1, self.param_list)
        self.assertEqual(39.82010650913622, tea1, 12)

        tea2 = solar.topocentric_elevation_angle(self.jct2, self.param_list)
        self.assertEqual(39.81809900014416, tea2, 12)
        self.assertAlmostEqual(39.888378, tea0, 1)

    def test_topocentric_lha(self):
        """
        testing Topocentric local hour angle
        0       11.106996
        67      11.106271
        """
        # print(self.test_topocentric_lha.__doc__)
        # print('testing solar.py Topocentric Local Hour Angle method')
        tlha = solar.topocentric_lha(self.jct0, self.param_list)
        self.assertEqual(11.10696132484708, tlha, 12)
        self.assertAlmostEqual(11.106996, tlha, 4)

        tlha1 = solar.topocentric_lha(self.jct1, self.param_list)
        self.assertEqual(11.375930997021326, tlha1, 12)

        tlha2 = solar.topocentric_lha(self.jct2, self.param_list)
        self.assertEqual(11.386176467319755, tlha2, 12)
        # self.assertAlmostEqual(11.106271, tlha2, 0)

    def test_topocentric_ra(self):
        """
        testing Topocentric sun right ascension
        0       202.226314 / 15
        67      202.227039 / 15
        """
        # print(self.test_topo_right_ascension.__doc__)
        # print('testing solar.py Topocentric Right Ascension method')
        tsra0 = solar.topocentric_right_ascension(self.jct0, self.param_list)
        self.assertEqual(202.2263489235359, tsra0, 12)
        self.assertAlmostEqual(202.226314, tsra0, 4)

        tsra1 = solar.topocentric_right_ascension(self.jct1, self.param_list)
        self.assertEqual(202.2270385196251, tsra1, 12)

        tsra2 = solar.topocentric_right_ascension(self.jct2, self.param_list)
        self.assertEqual(202.22706478759665, tsra2, 12)
        self.assertAlmostEqual(202.227039, tsra2, 4)

    def test_topocentric_declination(self):
        """
        testing Topocentric sun declination
        0       -9.315895 NOAA val -9.32
        67      -9.316179
        """
        # print(self.test_topo_sun_declination.__doc__)
        # print('testing solar.py Topocentric Sun Declination method')
        # note: using jd4 with location longitude factored in minus time zone.
        tsd = solar.topocentric_solar_declination(self.jct0, self.param_list)
        self.assertEqual(-9.315893316191877, tsd, 12)
        self.assertAlmostEqual(-9.315895, tsd, 5)

        tsd1 = solar.topocentric_solar_declination(self.jct1, self.param_list)
        self.assertEqual(-9.31616599739233, tsd1, 12)

        tsd2 = solar.topocentric_solar_declination(self.jct2, self.param_list)
        self.assertEqual(-9.316176384085475, tsd2, 12)
        self.assertAlmostEqual(-9.316179, tsd2, 5)

    def test_topocentric_zenith_angle(self):
        """
        testing Topocentric zenith angle
        0       50.111482
        67      50.111622
        """
        # print(self.test_topocentric_zenith_angle.__doc__)
        # print('testing solar.py Topocentric Zenith Angle method')
        tza = solar.topocentric_zenith_angle(self.jct0, self.param_list)
        self.assertEqual(50.13202226070725, tza, 12)
        self.assertAlmostEqual(50.111482, tza, 1)

        tza1 = solar.topocentric_zenith_angle(self.jct1, self.param_list)
        self.assertEqual(50.184117861726854, tza1, 12)

        tza2 = solar.topocentric_zenith_angle(self.jct2, self.param_list)
        self.assertEqual(50.18612566969781, tza2, 12)
        self.assertAlmostEqual(50.111622, tza2, 0)

if __name__ == "__main__":

    TSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestTopocentricSolar)

    unittest.TextTestRunner(verbosity=2).run(TSOLAR)
