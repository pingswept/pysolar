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

import unittest
from pysolar import solar, time, elevation, constants

class TestSolar(unittest.TestCase):
    """
    Non Az El Geocentric or Topocentric
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
    jd1 = time.jdn(dt_list) - 0.5
    jd2 = hours + minutes + seconds
    jd3 = 0.5 + minutes + seconds
    # need to take the timezone offset out because all
    # whole julian day numbers begin at noon.
    jd4 = jd3 - longitude_offset - 7 / 24.0
    jct0 = time.julian_century(jd1 + jd4)
    jct1 = time.julian_century(jd1 + default + jd4)
    jct2 = time.julian_century(jd1 + delta_t + jd4)
    def setUp(self):
        return None

    def test_aberration_correction(self):
        """
        testing Aberration correction
        0       -0.005711
        67      -0.005711
        """
        # print(self.test_aberration_correction.__doc__)
        # print('testing solar.py Aberration Correction method')
        ac0 = solar.aberration_correction(self.jd1, self.jd2)
        self.assertEqual(-0.005711358068106298, ac0, 12)
        self.assertAlmostEqual(-0.005711, ac0, 6)

        ac1 = solar.aberration_correction(self.jd1, self.default + self.jd2)
        self.assertEqual(-0.005711359248748542, ac1, 12)

        ac2 = solar.aberration_correction(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(-0.005711359293720966, ac2, 12)
        self.assertAlmostEqual(-0.005711, ac1, 6)

    def test_astronomical_units(self):
        """
        testing Earth radius vector
        0       0.996543
        67      0.996542
        """
        # print(self.test_sun_earth_distance.__doc__)
        # print('testing solar.py Sun Earth Distance method')
        sed = solar.astronomical_units(self.jd1, self.jd2)
        self.assertEqual(0.9965425091771832, sed, 12)
        self.assertAlmostEqual(0.996542, sed, 5)

        sed1 = solar.astronomical_units(self.jd1, self.default + self.jd2)
        self.assertEqual(0.99654230317365, sed1, 12)

        sed2 = solar.astronomical_units(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(0.9965422953266698, sed2, 12)
        self.assertAlmostEqual(0.996543, sed1, 5)

    def test_equation_of_center(self):
        """
        doc
        """
        eoc0 = solar.equation_of_center(self.jct0)
        self.assertEqual(-0.004641904251279983, eoc0, 12)

        eoc1 = solar.equation_of_center(self.jct1)
        self.assertEqual(-0.004617026169606156, eoc1, 12)

        eoc2 = solar.equation_of_center(self.jct2)
        self.assertEqual(-0.0046160784722622675, eoc2, 12)

    def test_greenwich_hour_angle(self):
        """
        testing Greenwich hour angle

        0       116.28525082273921
        default 116.55421168491452
        67      116.56445681978897
        """
        # print(self.test_local_hour_angle.__doc__)
        # print('testing solar.py Greewich Hour Angle method')
        gha = solar.greenwich_hour_angle(self.jd1, self.jd2)
        self.assertEqual(116.28522515556216, gha, 12)
        self.assertAlmostEqual(116.28525082273921, gha, 4)

        gha1 = solar.greenwich_hour_angle(self.jd1, self.default + self.jd2)
        self.assertEqual(116.554186017718, gha1, 12)
        self.assertAlmostEqual(116.55421168491452, gha1, 4)

        gha2 = solar.greenwich_hour_angle(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(116.56443115257608, gha2, 12)
        self.assertAlmostEqual(116.56445681978897, gha2, 4)

    def test_local_hour_angle(self):
        """
        testing Observer hour angle

        0       11.448972808852602
        64.5415 11.717934223859459
        67      11.728179379790333
        """
        # print(self.test_local_hour_angle.__doc__)
        # print('testing solar.py Local Hour Angle method')
        lha0 = solar.local_hour_angle(self.jd1, self.jd4)
        self.assertEqual(11.448947158715015, lha0, 12)
        self.assertAlmostEqual(11.448972808852602, lha0, 4)

        lha1 = solar.local_hour_angle(self.jd1, self.default + self.jd4)
        self.assertEqual(11.717908573645815, lha1, 12)
        self.assertAlmostEqual(11.717934223859459, lha1, 4)

        lha2 = solar.local_hour_angle(self.jd1, self.delta_t + self.jd4)
        self.assertEqual(11.728153729559693, lha2, 12)
        self.assertAlmostEqual(11.728179379790333, lha2, 4)

    def max_horizontal_parallax(self):
        """
        testing equatorial horizontal parallax
        67      0.002451
        0       0.002451
        """
        # print(self.test_max_horizontal_parallax.__doc__)
        # print('testing solar.py Equitorial Horizontal Parallax method')
        ehp = solar.max_horizontal_parallax(self.jd1, self.jd2)
        self.assertEqual(0.0024343318960289304, ehp, 12)
        self.assertAlmostEqual(0.002451, ehp, 4)

        ehp1 = solar.max_horizontal_parallax(self.jd1, self.default + self.jd2)
        self.assertEqual(0.0024343313928080774, ehp1, 12)
        self.assertAlmostEqual(0.002451, ehp1, 4)

        ehp2 = solar.max_horizontal_parallax(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(0.0024343313736396484, ehp2, 12)

    def test_mean_anomaly(self):
        """
        test mean anomaly
        """
        mas0 = solar.mean_anomaly(self.jct0)
        self.assertEqual(282.60686638293305, mas0, 12)

        mas1 = solar.mean_anomaly(self.jct1)
        self.assertEqual(282.60760263447446, mas1, 12)

        mas2 = solar.mean_anomaly(self.jct2)
        self.assertEqual(282.60763067943367, mas2, 12)

    def test_orbital_eccentricity(self):
        """
        test earths eliptic orbit
        """
        eoe0 = solar.orbital_eccentricity(self.jct0)
        self.assertEqual(0.0167070227866553, eoe0, 12)

        eoe1 = solar.orbital_eccentricity(self.jct1)
        self.assertEqual(0.016707022785795368, eoe1, 12)

        eoe2 = solar.orbital_eccentricity(self.jct2)
        self.assertEqual(0.016707022785762613, eoe2, 12)

    def test_pressure_with_elevation(self):
        """
        testing Pressure with elevation
        MIDC SPA is not at 12:30
        """
        # print(self.test_pressure_with_elevation.__doc__)
        # print('testing solar.py Pressure with Elevation method')
        pwe = elevation.pressure_with_elevation(1567.7)
        self.assertEqual(83855.90227687225, pwe, 12)

    def test_projected_axial_distance(self):
        """
        testing Projected axial distance
        MIDC SPA is not at 12:30
        """
        # print(self.test_projected_axial_distance.__doc__)
        # print('testing solar.py Projected Axial Distance method')
        pad = solar.projected_axial_distance(self.param_list)
        self.assertEqual(0.6361121708785658, pad, 12)

    def test_projected_radial_distance(self):
        """
        testing Projected radial distance
        MIDC SPA is not at 12:30
        """
        # print(self.test_projected_radial_distance.__doc__)
        # print('testing solar.py Projected Radial Distance method')
        prd = solar.projected_radial_distance(self.elevation, self.latitude)
        self.assertEqual(0.7702006191191089, prd, 12)

    def test_temperature_with_elevation(self):
        """
        testing
        Temperature with elevation
        MIDC SPA is not at 12:30
        """
        # print(self.test_temperature_with_elevation.__doc__)
        # print('testing solar.py Temperature with Elevation method')
        twe = elevation.temperature_with_elevation(1567.7)
        self.assertEqual(277.95995, twe, 12)

    def test_true_anomaly(self):
        """
        test mean anomaly
        """
        tas0 = solar.true_anomaly(self.jct0)
        self.assertEqual(282.60222447868176, tas0, 12)

        tas1 = solar.true_anomaly(self.jct1)
        self.assertEqual(282.60298560830483, tas1, 12)

        tas2 = solar.true_anomaly(self.jct2)
        self.assertEqual(282.6030146009614, tas2, 12)

if __name__ == "__main__":

    SOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)

    unittest.TextTestRunner(verbosity=2).run(SOLAR)
#end if
