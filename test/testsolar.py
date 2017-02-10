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
from pysolar import solar, time, elevation, constants, util

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

class TestNutation(unittest.TestCase):
    """
    Test nutation methods
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

    def test_apparent_solar_longitude(self):
        """
        0        204.00775769284664
        64.5415  204.0084989745065
        67       204.0085272110777
        """
        # print(self.test_apparent_sun_longitude.__doc__)
        # print('testing solar.py Apparent Sun Longitude method')
        asl0 = solar.apparent_solar_longitude(self.jd1, self.jd2)
        self.assertEqual(204.00778293211076, asl0, 12)
        self.assertAlmostEqual(204.00775769284664, asl0, 4)

        asl1 = solar.apparent_solar_longitude(self.jd1, self.default + self.jd2)
        self.assertEqual(204.0085242135883, asl1, 12)
        self.assertAlmostEqual(204.0084989745065, asl1, 4)

        asl2 = solar.apparent_solar_longitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(204.00855245015222, asl2, 12)
        self.assertAlmostEqual(204.0085272110777, asl2, 4)

    def test_delta_epsilon(self):
        """
        testing Nutation obliquity delta epsilon
        0         0.0016665452253917616
        64.5415   0.0016665472500373482
        67        0.001666547327214764
        """
        # print(self.test_delta_epsilon.__doc__)
        # print('testing solar.py Delta Epsilon method')
        deps0 = solar.nutation(self.jd1, self.jd2)['obliquity']
        self.assertEqual(0.0016668041903600411, deps0, 12)
        self.assertAlmostEqual(0.0016665452253917616, deps0, 6)

        deps1 = solar.nutation(self.jd1, self.default + self.jd2)['obliquity']
        self.assertEqual(0.0016668061340751688, deps1, 12)
        self.assertAlmostEqual(0.0016665472500373482, deps1, 6)

        deps2 = solar.nutation(self.jd1, self.delta_t + self.jd2)['obliquity']
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
        dpsi0 = solar.nutation(self.jd1, self.jd2)['longitude']
        self.assertEqual(-0.003997960095151495, dpsi0, 12)
        self.assertAlmostEqual(-0.003998135135636136, dpsi0, 6)

        dpsi1 = solar.nutation(self.jd1, self.jd2)['longitude']
        self.assertEqual(-0.0032509519932996432, self.default + dpsi1, 12)
        self.assertAlmostEqual(-0.0039981219235174165, dpsi1, 6)

        dpsi2 = solar.nutation(self.jd1, self.delta_t + self.jd2)['longitude']
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
        eqeq0 = solar.equation_of_equinox(self.jd1, self.jd2)
        self.assertEqual(-0.0036680244276743198, eqeq0, 15)
        self.assertAlmostEqual(-0.003668185029955833, eqeq0, 6)

        eqeq1 = solar.equation_of_equinox(self.jd1, self.default + self.jd2)
        self.assertEqual(-0.0036680125522307984, eqeq1, 15)
        self.assertAlmostEqual(-0.0036681729081316267, eqeq1, 6)

        eqeq2 = solar.equation_of_equinox(self.jd1, self.delta_t + self.jd2)
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
        meps0 = solar.mean_ecliptic_obliquity(self.jd1, self.jd2)
        self.assertEqual(23.43878599563886, meps0, 12)
        self.assertAlmostEqual(23.43878599563886, meps0, 12)

        meps1 = solar.mean_ecliptic_obliquity(self.jd1, self.default + self.jd2)
        self.assertEqual(23.43878599537278, meps1, 12)
        self.assertAlmostEqual(23.43878599537278, meps1, 12)

        meps2 = solar.mean_ecliptic_obliquity(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(23.43878599536264, meps2, 12)
        self.assertAlmostEqual(23.43878599536264, meps2, 12)

    def test_true_ecliptic_obliquity(self):
        """
        0       23.44045254086425
        64.5415 23.440452542622815
        67      23.440452542689854
        """
        teo0 = solar.true_ecliptic_obliquity(self.jd1, self.jd2)
        self.assertEqual(23.44045279982922, teo0, 12)
        self.assertAlmostEqual(23.44045254086425, teo0, 6)

        teo1 = solar.true_ecliptic_obliquity(self.jd1, self.default + self.jd2)
        self.assertEqual(23.440452801506854, teo1, 12)
        self.assertAlmostEqual(23.440452542622815, teo1, 6)

        teo2 = solar.true_ecliptic_obliquity(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(23.440452801506854, teo1, 12)
        self.assertAlmostEqual(23.440452542689854, teo2, 6)

class TestHeliocentricSolar(unittest.TestCase):
    """
    Test heliocentric methods
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67 / 86400
    param_list = [elevation, latitude, longitude, surface_slope,
                  surface_azimuth_rotation, temperature, pressure]
    def setUp(self):
        self.jd1 = 2452929.5

        self.jd2 = (
            self.dt_list[3] / 24.0) + (
                self.dt_list[4] / 1440.0) + (
                    self.dt_list[5] / 86400.0)

        self.default = time.delta_t(self.jd1 + self.jd2) / 86400.0


    def test_heliocentric_latitude(self):
        """
        testing Heliocentric latitude
        0       -0.00010110749648050061
        64.5415 -0.00010112139544887049
        67      -0.00010112192480034693
        """
        # print(self.heliocentric_latitude.__doc__)
        # print('testing solar.py Heliocentric Latitude method')
        hlat0 = solar.heliocentric_latitude(self.jd1, self.jd2)
        self.assertEqual(-0.00010111269416498883, hlat0, 12)
        self.assertAlmostEqual(-0.00010110749648050061, hlat0, 7)

        hlat1 = solar.heliocentric_latitude(self.jd1, self.default + self.jd2)
        self.assertEqual(-0.00010112659361522744, hlat1, 12)
        self.assertAlmostEqual(-0.00010112139544887049, hlat1, 7)

        hlat2 = solar.heliocentric_latitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(-0.00010112712298505422, hlat2, 12)
        self.assertAlmostEqual(-0.00010112192480034693, hlat2, 7)

    def test_heliocentric_longitude(self):
        """
        testing Heliocentric longitude
        0       24.01749218593841
        64.5415 24.018233455566815
        67      24.018261691679754
        """
        # print(self.test_heliocentric_longitude.__doc__)
        # print('testing solar.py Heliocentric longitude method')
        hlon0 = solar.heliocentric_longitude(self.jd1, self.jd2)
        self.assertEqual(24.017492250274017, hlon0, 12)
        self.assertAlmostEqual(24.01749218593841, hlon0, 6)

        hlon1 = solar.heliocentric_longitude(self.jd1, self.default + self.jd2)
        self.assertEqual(24.0182335199886, hlon1, 12)
        self.assertAlmostEqual(24.018233455566815, hlon1, 6)

        hlon2 = solar.heliocentric_longitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(24.018261756104494, hlon2, 12)
        self.assertAlmostEqual(24.018261691679754, hlon2, 6)

    def test_lb0_to_lb4(self):
        """
        test each latitude term Element
        should be
        [-176.502688, 3.067582]
        """
        # print('testing solar.py Heliocentric Longitude Terms method')
        lb0 = solar.heliocentric_lat_elements(self.jd1, self.jd2)[0]
        lb1 = solar.heliocentric_lat_elements(self.jd1, self.jd2)[1]
        lb2 = solar.heliocentric_lat_elements(self.jd1, self.jd2)[2]
        lb3 = solar.heliocentric_lat_elements(self.jd1, self.jd2)[3]
        lb4 = solar.heliocentric_lat_elements(self.jd1, self.jd2)[4]
        self.assertEqual(-176.48654284285342, lb0, 12)
        self.assertAlmostEqual(-176.502688, lb0, 1)
        self.assertEqual(3.058434483982354, lb1, 12)
        self.assertAlmostEqual(3.067582, lb1, 1)
        self.assertEqual(0.0, lb2, 12)
        self.assertEqual(0.0, lb3, 12)
        self.assertEqual(0.0, lb4, 12)

    def test_lo0_to_lo5(self):
        """
        test each longitude term Element
        should be
        [172067561.526586, 628332010650.051147, 61368.682493,
         -26.902819, -121.279536, -0.999999]
        """
        # print('testing solar.py Heliocentric Longitude Terms method')
        lo0 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[0]
        lo1 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[1]
        lo2 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[2]
        lo3 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[3]
        lo4 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[4]
        lo5 = solar.heliocentric_lon_elements(self.jd1, self.jd2)[5]
        self.assertEqual(172067552.4204392, lo0, 12)
        self.assertAlmostEqual(172067561.526586 / 100, lo0 / 100, 0)
        self.assertEqual(628332010700.2529, lo1, 12)
        self.assertAlmostEqual(628332010650.051147 / 1000, lo1 / 1000, 0)
        self.assertEqual(61368.64926580728, lo2, 12)
        self.assertAlmostEqual(61368.682493, lo2, 1)
        self.assertEqual(-26.897807223158654, lo3, 12)
        self.assertAlmostEqual(-26.902819, lo3, 0)
        self.assertEqual(-121.28930075553654, lo4, 12)
        self.assertAlmostEqual(-121.279536, lo4, 1)
        self.assertEqual(-0.9999987317275395, lo5, 12)
        self.assertAlmostEqual(-0.999999, lo5, 6)

class TestGeocentricSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    surface_slope = 30.0 # Surface slope (measured from the horizontal plane) [degrees]
    surface_azimuth_rotation = -10.0 # Surface azimuth rotation (measured from south to
    # projection of surface normal on horizontal plane, negative east) [degrees]
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67 / 86400
    param_list = [elevation, latitude, longitude, surface_slope,
                  surface_azimuth_rotation, temperature, pressure]
    def setUp(self):
        self.jd1 = 2452929.5

        self.jd2 = (
            self.dt_list[3] / 24.0) + (
                self.dt_list[4] / 1440.0) + (
                    self.dt_list[5] / 86400.0)

        self.default = time.delta_t(self.jd1 + self.jd2) / 86400.0

    def test_geocentric_declination(self):
        """
        testing Geocentric sun declination
        0       -9.314048298076031
        64.5415 -9.3143212526048
        67      -9.314331649840488
        """
        # print(self.test_geo_rad_dec.__doc__)
        # print('testing solar.py Geocentric Declination method')
        gsd0 = solar.geocentric_declination(self.jd1, self.jd2)
        self.assertEqual(-9.314052493720652, gsd0, 12)
        self.assertAlmostEqual(-9.314048298076031, gsd0, 5)

        gsd1 = solar.geocentric_declination(self.jd1, self.default + self.jd2)
        self.assertEqual(-9.314325448278428, gsd1, 12)
        self.assertAlmostEqual(-9.3143212526048, gsd1, 5)

        gsd2 = solar.geocentric_declination(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(-9.314335845515107, gsd2, 12)
        self.assertAlmostEqual(-9.314331649840488, gsd2, 5)

    def test_geocentric_latitude(self):
        """
        testing Geocentric latitude
        0       0.00010110749648050061
        64.5415 0.00010112139544887049
        67      0.00010112192480034693
        """
        # print(self.test_geo_lat_lon.__doc__)
        # print('testing solar.py Geocentric Latitude')
        glat0 = solar.geocentric_latitude(self.jd1, self.jd2)
        self.assertEqual(0.00010111269416498883, glat0, 12)
        self.assertAlmostEqual(0.00010110749648050061, glat0, 7)

        glat1 = solar.geocentric_latitude(self.jd1, self.default + self.jd2)
        self.assertEqual(0.00010112659361522744, glat1, 12)
        self.assertAlmostEqual(0.00010112139544887049, glat1, 7)

        glat2 = solar.geocentric_latitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(0.00010112712298505422, glat2, 12)
        self.assertAlmostEqual(0.00010112192480034693, glat2, 7)


    def test_geocentric_longitude(self):
        """
        testing Geocentric longitude
        0       204.01746718593841
        64.5415 204.01820845556682
        67      204.01823669167976
        """
        # print(self.test_geo_lat_lon.__doc__)
        # print('testing solar.py True Geocentric Longitude method')
        glon0 = solar.geocentric_longitude(self.jd1, self.jd2)
        self.assertEqual(204.01749225027402, glon0, 12)
        self.assertAlmostEqual(204.01746718593841, glon0, 4)

        glon1 = solar.geocentric_longitude(self.jd1, self.default + self.jd2)
        self.assertEqual(204.0182335199886, glon1, 12)
        self.assertAlmostEqual(204.01820845556682, glon1, 4)

        glon2 = solar.geocentric_longitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(204.0182617561045, glon2, 12)
        self.assertAlmostEqual(204.01823669167976, glon2, 4)

    def test_geocentric_right_ascension(self):
        """
        testing Geocentric sun right ascension
        0       202.22665926504152 / 15
        64.5415 202.22735767137598 / 15
        67      202.2273842747809 / 15
        """
        # print(self.test_geo_rad_dec.__doc__)
        # print('testing solar.py Geocentric Right Ascension method')
        gsra0 = solar.geocentric_right_ascension(self.jd1, self.jd2)
        self.assertEqual(13.481779006038968, gsra0, 12)
        self.assertAlmostEqual(202.22665926504152 / 15, gsra0, 4)

        gsra1 = solar.geocentric_right_ascension(self.jd1, self.default + self.jd2)
        self.assertEqual(13.4818255664478, gsra1, 12)
        self.assertAlmostEqual(202.22735767137598 / 15, gsra1, 4)

        gsra2 = solar.geocentric_right_ascension(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(13.481827340007595, gsra2, 12)
        self.assertAlmostEqual(202.2273842747809 / 15, gsra2, 4)

    def test_mean_geocentric_longitude(self):
        """
        test Mean Geocentric Longitude
        """
        # print('testing solar.py Mean Geocentric Longitude')
        mgl0 = solar.mean_solar_longitude(self.jd1, self.jd2)
        self.assertEqual(205.89640791951274, mgl0, 12)

        mgl1 = solar.mean_solar_longitude(self.jd1, self.default + self.jd2)
        self.assertEqual(205.8971442062218, mgl1, 12)

        mgl2 = solar.mean_solar_longitude(self.jd1, self.delta_t + self.jd2)
        self.assertEqual(205.89717225252048, mgl2, 12)

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
    def setUp(self):
        self.hours = self.dt_list[3] / 24.0
        self.minutes = self.dt_list[4] / 1440.0
        self.seconds = self.dt_list[5] / 86400.0
        self.jd1 = time.jdn(self.dt_list) - 0.5
        self.jd2 = self.hours + self.minutes + self.seconds
        self.jd3 = 0.5 + self.minutes + self.seconds
        self.jd4 = self.jd3 - self.longitude_offset
        print(self.jd3)

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
        64.5415 11.539308774930333
        67      11.549553930897702
        """
        # print(self.test_local_hour_angle.__doc__)
        # print('testing solar.py Local Hour Angle method')
        lha0 = solar.local_hour_angle(self.jd1, self.jd3, self.param_list[2])
        self.assertEqual(11.270321708900212, lha0, 12)
        self.assertAlmostEqual(11.270347359044564, lha0, 10)

        lha1 = solar.local_hour_angle(self.jd1, self.default + self.jd3, self.param_list)
        self.assertEqual(11.539282957106366, lha1, 12)
        self.assertAlmostEqual(11.539308774930333, lha1, 4)

        lha2 = solar.local_hour_angle(self.jd1, self.delta_t + self.jd3, self.param_list)
        self.assertEqual(11.549528280718278, lha2, 12)
        self.assertAlmostEqual(11.549553930897702, lha2, 4)

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

class TestTopocentricSolar(unittest.TestCase):
    """
    Test solar and time methods
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
    def setUp(self):
        self.hours = self.dt_list[3] / 24.0
        self.minutes = self.dt_list[4] / 1440.0
        self.seconds = self.dt_list[5] / 86400.0
        self.jd1 = time.jdn(self.dt_list) - 0.5
        self.jd2 = self.hours + self.minutes + self.seconds
        self.jd3 = 12 / 24.0 + self.minutes + self.seconds
        self.jd4 = self.jd1 - self.longitude_offset + self.minutes + self.seconds
        self.default = time.delta_t(self.jd1 + self.jd2) / 86400.0

    def test_incidence_angle(self):
        """
        testing Surface incidence angle
        0       25.187244
        67      25.187000
        """
        # print(self.test_incidence_angle.__doc__)
        # print('testing solar.py Angle of Incedence method')
        aoi0 = solar.incidence_angle(self.jd1, self.jd2, self.param_list)
        self.assertEqual(25.187243852174234, aoi0, 12)
        self.assertAlmostEqual(25.187244, aoi0, 6)

        aoi1 = solar.incidence_angle(self.jd1, self.default + self.jd2, self.param_list)
        self.assertEqual(25.187243852174234, aoi1, 12)

        aoi2 = solar.incidence_angle(self.jd1, self.delta_t + self.jd2, self.param_list)
        self.assertEqual(25.187243852174234, aoi2, 12)
        self.assertAlmostEqual(25.187000, aoi2, 3)

    def test_right_ascension_parallax(self):
        """
        testing right ascension parallax
        0       -0.000369
        67      -0.000369
        """
        # print(self.test_right_ascension_parallax.__doc__)
        # print('testing solar.py Right Ascension Parallax method')
        rap = solar.right_ascension_parallax(self.jd1, self.jd3, self.param_list)
        self.assertEqual(-0.0003712574562188372, rap, 12)
        self.assertAlmostEqual(-0.000369, rap, 5)

        rap1 = solar.right_ascension_parallax(self.jd1, self.default + self.jd3, self.param_list)
        self.assertEqual(-0.000371257666589018, rap1, 12)

        rap2 = solar.right_ascension_parallax(self.jd1, self.delta_t + self.jd3, self.param_list)
        self.assertEqual(-0.0003712576746026329, rap2, 12)
        self.assertAlmostEqual(-0.000369, rap1, 5)

    def topocentric_azimuth_angle(self):
        """
        testing Topocentric azimuth angle (eastward from N)
        0       194.341226
        67      194.340241
        """
        # print(self.test_topocentric_azimuth_angle.__doc__)
        # print('testing solar.py Topocentric Azimuth Angle method')
        taa0 = solar.topocentric_azimuth_angle(self.jd1, self.jd3, self.param_list)
        self.assertEqual(192.5390051547504, taa0, 12)
        # self.assertAlmostEqual(194.341226, taa1, 6)

        taa1 = solar.topocentric_azimuth_angle(self.jd1, self.default + self.jd3, self.param_list)
        self.assertEqual(192.83460525461655, taa1, 12)

        taa2 = solar.topocentric_azimuth_angle(self.jd1, self.delta_t + self.jd3, self.param_list)
        self.assertEqual(192.8458604056448, taa2, 12)
        # self.assertAlmostEqual(194.340241, taa0, 6)

    def topocentri_elevation_angle(self):
        """
        0   39.888518
        67  39.888378
        """
        tea0 = solar.topocentric_elevation_angle(self.jd1, self.jd2, self.param_list)
        self.assertEqual(0.7781227515104502, tea0, 12)
        self.assertAlmostEqual(39.888518, tea0, 6)

    def topocentric_lha(self):
        """
        testing Topocentric local hour angle
        0       11.106996
        67      11.106271
        """
        # print(self.test_topocentric_lha.__doc__)
        # print('testing solar.py Topocentric Local Hour Angle method')
        tlha = solar.topocentric_lha(self.jd1, self.jd3, self.param_list)
        self.assertEqual(11.270692965522414, tlha, 12)
        self.assertAlmostEqual(11.106996, tlha, 0)

        tlha1 = solar.topocentric_lha(self.jd1, self.default + self.jd3, self.param_list)
        self.assertEqual(11.539662955118587, tlha1, 12)

        tlha2 = solar.topocentric_lha(self.jd1, self.delta_t + self.jd3, self.param_list)
        self.assertEqual(11.54990861154505, tlha2, 12)
        self.assertAlmostEqual(11.106271, tlha2, 0)

    def test_topocentri_right_ascension(self):
        """
        testing Topocentric sun right ascension
        0       202.226314 / 15
        67      202.227039 / 15
        """
        # print(self.test_topo_right_ascension.__doc__)
        # print('testing solar.py Topocentric Right Ascension method')
        tsra0 = solar.topocentric_right_ascension(self.jd1, self.jd2, self.param_list)
        self.assertEqual(202.22631375040177, tsra0, 12)
        self.assertAlmostEqual(202.226314, tsra0, 5)

        tsra1 = solar.topocentric_right_ascension(
            self.jd1, self.default + self.jd3, self.param_list)
        self.assertEqual(201.95442996738063, tsra1, 12)

        tsra2 = solar.topocentric_right_ascension(
            self.jd1, self.delta_t + self.jd2, self.param_list)
        self.assertEqual(202.2270387597097, tsra2, 12)
        self.assertAlmostEqual(202.227039, tsra2, 5)

    def topocentri_sun_declination(self):
        """
        testing Topocentric sun declination
        0       -9.315895
        67      -9.316179
        """
        # print(self.test_topo_sun_declination.__doc__)
        # print('testing solar.py Topocentric Sun Declination method')
        tsd = solar.topocentric_solar_declination(self.jd1, self.jd2, self.param_list)
        self.assertEqual(-9.315344821603071, tsd, 12)
        self.assertAlmostEqual(-9.315895, tsd, 3)

        tsd1 = solar.topocentric_solar_declination(
            self.jd1, self.default + self.jd3, self.param_list)
        self.assertEqual(-9.209430183563855, tsd1, 12)

        tsd2 = solar.topocentric_solar_declination(
            self.jd1, self.delta_t + self.jd2, self.param_list)
        self.assertEqual(-9.315751832121887, tsd2, 12)
        self.assertAlmostEqual(-9.316179, tsd2, 3)

    def topocentric_zenith_angle(self):
        """
        testing Topocentric zenith angle
        0       50.111482
        67      50.111622
        """
        # print(self.test_topocentric_zenith_angle.__doc__)
        # print('testing solar.py Topocentric Zenith Angle method')
        tza = solar.topocentric_zenith_angle(self.jd1, self.jd2, self.param_list)
        self.assertEqual(92.77235684567964, tza, 12)
        # self.assertAlmostEqual(50.111482, tza, 6)

        tza1 = solar.topocentric_zenith_angle(self.jd1, self.default + self.jd2, self.param_list)
        self.assertEqual(92.74242219333381, tza1, 12)

        tza2 = solar.topocentric_zenith_angle(self.jd1, self.delta_t + self.jd2, self.param_list)
        self.assertEqual(92.74128330323576, tza2, 12)
        # self.assertAlmostEqual(50.111622, tza2, 6)

class TestAzElSolar(unittest.TestCase):
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

    def altitude(self):
        """
        testing Altitude Angle
        """
        # print(self.test_altitude.__doc__)
        # print('testing solar.py Altitude Angle method')
        alt = solar.altitude(self.when0, self.param_list)
        self.assertEqual(-7.215175951695366, alt, 12)

        alt1 = solar.altitude(self.when1, self.param_list)
        self.assertEqual(-7.290024996742759, alt1, 12)

        alt2 = solar.altitude(self.when2, self.param_list)
        self.assertEqual(-7.293531168309954, alt2, 12)

    def azimuth(self):
        """
        testing Azimuth
        """
        # print(self.test_azimuth.__doc__)
        # print('testing solar.py Azimuth Angle method')
        azm = solar.azimuth(self.when0, self.param_list)
        self.assertEqual(-270.61722305824236, azm, 12)

        azm1 = solar.azimuth(self.when1, self.param_list)
        self.assertEqual(-270.82120360201225, azm1, 12)

        azm2 = solar.azimuth(self.when2, self.param_list)
        self.assertEqual(-270.83073645178627, azm2, 12)

class TestSolarSolar(unittest.TestCase):
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
    when = datetime.datetime(
        2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)

    def test_solar_test(self):
        """
        test for solar_test
        """
        # print('testing solar.py Solar Test method')
        solar.solar_test(self.param_list)

if __name__ == "__main__":
    NUTATION = unittest.defaultTestLoader.loadTestsFromTestCase(TestNutation)
    SOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    HSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestHeliocentricSolar)
    GSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestGeocentricSolar)
    TSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestTopocentricSolar)
    AESOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestAzElSolar)
    SIDEREAL = unittest.defaultTestLoader.loadTestsFromTestCase(TestSiderealTime)
    INSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolarSolar)
    # unittest.TextTestRunner(verbosity=2).run(SIDEREAL)
    # unittest.TextTestRunner(verbosity=2).run(NUTATION)
    # unittest.TextTestRunner(verbosity=2).run(HSOLAR)
    # unittest.TextTestRunner(verbosity=2).run(GSOLAR)
    unittest.TextTestRunner(verbosity=2).run(SOLAR)
    # unittest.TextTestRunner(verbosity=2).run(TSOLAR)
    # unittest.TextTestRunner(verbosity=2).run(AESOLAR)
    # unittest.TextTestRunner(verbosity=2).run(INSOLAR)

#end if
