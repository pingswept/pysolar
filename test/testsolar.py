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
from pysolar import solar, time, elevation

class TestSolar(unittest.TestCase):
    """
    Non Az El Geocentric or Topocentric
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
    delta_t = 67 / 86400.0
    default = 64.5415 / 86400.0
    param_list = [latitude, longitude, elevation, surface_slope,
                  surface_azimuth_rotation, temperature, pressure]

    hours = dt_list[3] / 24.0
    minutes = dt_list[4] / 1440.0
    seconds = dt_list[5] / 86400.0
    jd0 = time.jdn(dt_list) - 0.5 # julian day midnight
    jdfd = hours + minutes + seconds # fractional day
    jdt = jd0 + jdfd
    print(jdt)
    jdd = jdt + default
    print(jdd)
    jddt = jdt + delta_t
    print(jddt)
    jct0 = time.julian_century(jdt)
    jct1 = time.julian_century(jdd)
    jct2 = time.julian_century(jddt)
    # need to take the timezone offset out because all
    # whole julian day numbers begin at noon.
    jd3 = 0.5 + minutes + seconds - 7 / 24.0
    jd4 = jd3 - longitude_offset
    jct3 = time.julian_century(jd0 + jd4)
    jct4 = time.julian_century(jd0 + jd4 + default)
    jct5 = time.julian_century(jd0 + jd4 + delta_t)
    def setUp(self):
        """
        set up
        """
        return None

    def test_aberration_correction(self):
        """
        testing Aberration correction
        0       -0.005711
        67      -0.005711
        """
        # print(self.test_aberration_correction.__doc__)
        # print('testing solar.py Aberration Correction method')
        ac0 = solar.aberration_correction(self.jct0)
        self.assertEqual(-0.005711357233874447, ac0, 12)
        self.assertAlmostEqual(-0.005711, ac0, 6)

        ac1 = solar.aberration_correction(self.jct1)
        self.assertEqual(-0.005711358414406401, ac1, 12)

        ac2 = solar.aberration_correction(self.jct2)
        self.assertEqual(-0.005711358459374628, ac2, 12)
        self.assertAlmostEqual(-0.005711, ac2, 6)

    def test_astronomical_units(self):
        """
        testing Earth radius vector
        0       0.996543
        67      0.996542
        """
        # print(self.test_sun_earth_distance.__doc__)
        # print('testing solar.py Sun Earth Distance method')
        sed = solar.astronomical_units(self.jct0)
        self.assertEqual(0.9965426547375934, sed, 12)
        self.assertAlmostEqual(0.996542, sed, 5)

        sed1 = solar.astronomical_units(self.jct1)
        self.assertEqual(0.9965424487532439, sed1, 12)

        sed2 = solar.astronomical_units(self.jct2)
        self.assertEqual(0.9965424409069937, sed2, 12)
        self.assertAlmostEqual(0.996543, sed1, 5)

    def test_equation_of_center(self):
        """
        doc
        """
        eoc0 = solar.equation_of_center(self.jct3)
        self.assertEqual(-0.004641904251279983, eoc0, 12)

        eoc1 = solar.equation_of_center(self.jct4)
        self.assertEqual(-0.004617026169606156, eoc1, 12)

        eoc2 = solar.equation_of_center(self.jct5)
        self.assertEqual(-0.0046160784722622675, eoc2, 12)

    def test_equation_of_time(self):
        """
        A mockup of equation of time
        MIDC SPA
        14.641353
        """
        mas = solar.mean_anomaly(self.jct0)
        self.assertEqual(282.8938441648961, mas, 12)
        tas = solar.true_anomaly(self.jct0)
        self.assertEqual(282.8989597150029, tas, 12)
        orbital = mas - tas
        self.assertEqual(-0.005115550106779665, orbital, 12)

        mls = solar.mean_solar_longitude(self.jct0)
        self.assertEqual(205.89640791951274, mls, 12)
        tls = mls + solar.equation_of_center(self.jct0)
        self.assertEqual(205.90152346961955, tls, 12)
        # slam = solar.geocentric_lambda(self.jct0)
        # self.assertEqual(204.0078134676852, slam, 12)
        gra = solar.geocentric_right_ascension(self.jct0)
        self.assertEqual(202.22671748072085, gra, 12)

        # oblique = slam - gra
        oblique = tls - gra
        self.assertEqual(3.6748059888986973, oblique, 12)
        eot = orbital + oblique
        self.assertEqual(3.6696904387919176, eot, 15)
        self.assertEqual(0.2446460292527945, eot / 15, 15)
        self.assertEqual(14.67876175516767, eot * 4, 15)
        self.assertAlmostEqual(14.641353, eot * 4, 1)


    def test_greenwich_hour_angle(self):
        """
        testing Greenwich hour angle

        0       116.28525082273921
        64.5415 116.55421349133425
        67      116.56445862621047
        """
        # print(self.test_local_hour_angle.__doc__)
        # print('testing solar.py Greewich Hour Angle method')
        gha = solar.greenwich_hour_angle(self.jct0)
        self.assertEqual(116.28519276766215, gha, 12)
        self.assertAlmostEqual(116.28525082273921, gha, 6)

        gha1 = solar.greenwich_hour_angle(self.jct1)
        self.assertEqual(116.55415363053996, gha1, 12)
        self.assertAlmostEqual(116.55421349133425, gha1, 6)

        gha2 = solar.greenwich_hour_angle(self.jct2)
        self.assertEqual(116.56439876544152, gha2, 12)
        self.assertAlmostEqual(116.56445862621047, gha2, 6)

    def test_local_hour_angle(self):
        """
        testing Observer hour angle
        0       11.106627
        64.5415 11.105929
        67      11.105902
        """
        # print(self.test_local_hour_angle.__doc__)
        # print('testing solar.py Local Hour Angle method')
        lha0 = solar.local_hour_angle(self.jct0, self.longitude)
        self.assertEqual(11.10659276766215, lha0, 12)
        self.assertAlmostEqual(11.106627, lha0, 4)

        lha1 = solar.local_hour_angle(self.jct1, self.longitude)
        self.assertEqual(11.375553630539954, lha1, 12)
        self.assertAlmostEqual(11.105929, lha1, 0)

        lha2 = solar.local_hour_angle(self.jct2, self.longitude)
        self.assertEqual(11.385798765441521, lha2, 12)
        self.assertAlmostEqual(11.105902, lha2, 0)

    def test_max_horizontal_parallax(self):
        """
        testing equatorial horizontal parallax
        0       0.002451
        67      0.002451
        """
        # print(self.test_max_horizontal_parallax.__doc__)
        # print('testing solar.py Equitorial Horizontal Parallax method')
        ehp0 = solar.max_horizontal_parallax(self.jct3)
        self.assertEqual(0.0024345284997929813, ehp0, 12)
        self.assertAlmostEqual(0.002451, ehp0, 4)

        ehp1 = solar.max_horizontal_parallax(self.jct4)
        self.assertEqual(0.002434527996001367, ehp1, 12)

        ehp2 = solar.max_horizontal_parallax(self.jct5)
        self.assertEqual(0.0024345279768111954, ehp2, 12)
        self.assertAlmostEqual(0.002451, ehp2, 4)

    def test_mean_anomaly(self):
        """
        test mean anomaly
        """
        mas0 = solar.mean_anomaly(self.jct0)
        self.assertEqual(282.8938441648961, mas0, 12)

        mas1 = solar.mean_anomaly(self.jct1)
        self.assertEqual(282.8945804164375, mas1, 12)

        mas2 = solar.mean_anomaly(self.jct2)
        self.assertEqual(282.8946084613963, mas2, 12)

    def test_mean_gha_aries(self):
        """
        testing mean longitude aries
        0       318.51557827281067
        64.5415 318.78523752919864
        67      318.7955092670163
        """
        mla0 = solar.mean_gha_aries(self.jct0)
        self.assertEqual(318.51557827281067, mla0, 12)

        mla1 = solar.mean_gha_aries(self.jct1)
        self.assertEqual(318.78523752919864, mla1, 12)

        mla2 = solar.mean_gha_aries(self.jct2)
        self.assertEqual(318.7955092670163, mla2, 12)


    def test_mean_solar_longitude(self):
        """
        test Mean Geocentric Longitude
        """
        # print('testing solar.py Mean Geocentric Longitude')
        msl0 = solar.mean_solar_longitude(self.jct0)
        self.assertEqual(205.89640791951274, msl0, 12)

        msl1 = solar.mean_solar_longitude(self.jct1)
        self.assertEqual(205.8971442062218, msl1, 12)

        msl2 = solar.mean_solar_longitude(self.jct2)
        self.assertEqual(205.89717225252048, msl2, 12)

    def test_orbital_eccentricity(self):
        """
        test earths eliptic orbit
        """
        eoe0 = solar.orbital_eccentricity(self.jct0)
        self.assertEqual(0.016707022451469423, eoe0, 12)

        eoe1 = solar.orbital_eccentricity(self.jct1)
        self.assertEqual(0.016707022450609493, eoe1, 12)

        eoe2 = solar.orbital_eccentricity(self.jct2)
        self.assertEqual(0.016707022450576738, eoe2, 12)

    def test_pressure_with_elevation(self):
        """
        testing Pressure with elevation
        MIDC SPA is not at 12:30
        """
        # print(self.test_pressure_with_elevation.__doc__)
        # print('testing solar.py Pressure with Elevation method')
        pwe = elevation.pressure_with_elevation(1567.7)
        self.assertEqual(83855.90227687225, pwe, 12)

    def test_radius_vector_list(self):
        """
        test radius vector list
        R0 99653849.037796
        R1 100378.567146
        R2 -1140.953507
        R3 -141.115419
        R4 1.232361
        """
        rvl = solar.radius_vector_list(self.jct0)
        self.assertAlmostEqual(99653849.037796 / 100, rvl[0] /100, 0)
        self.assertAlmostEqual(100378.567146 / 100, rvl[1] / 100, 0)
        self.assertAlmostEqual(-1140.953507 / 10, rvl[2] / 10, 0)
        self.assertAlmostEqual(-141.115419 / 10, rvl[3] / 10, 0)
        self.assertAlmostEqual(1.232361, rvl[4], 0)
        self.assertAlmostEqual(0.08032350370223192, rvl[5], 16)

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
        self.assertEqual(282.8989597150029, tas0, 12)

        tas1 = solar.true_anomaly(self.jct1)
        self.assertEqual(282.89972078816123, tas1, 12)

        tas2 = solar.true_anomaly(self.jct2)
        self.assertEqual(282.89974977855513, tas2, 12)

    def test_true_gha_aries(self):
        """
        testing true gha aries
        0       318.51191008811094
        64.5415 318.7815693566207
        67      318.7918410949001
        """
        tga0 = solar.true_gha_aries(self.jct0)
        self.assertEqual(318.511910248383, tga0, 15)
        self.assertAlmostEqual(318.51191008811094, tga0, 6)

        tga1 = solar.true_gha_aries(self.jct1)
        self.assertEqual(318.7815695166464, tga1, 15)
        self.assertAlmostEqual(318.7815693566207, tga1, 6)

        tga2 = solar.true_gha_aries(self.jct2)
        self.assertEqual(318.7918412549164, tga2, 15)
        self.assertAlmostEqual(318.7918410949001, tga2, 6)



    def test_true_solar_longitude(self):
        """
        true not apparent solar longitude
        """
        tsl0 = solar.true_solar_longitude(self.jct0)
        self.assertEqual(204.01752278491387, tsl0, 12)

        tsl1 = solar.true_solar_longitude(self.jct1)
        self.assertEqual(204.0182640533638, tsl1, 12)

        tsl2 = solar.true_solar_longitude(self.jct2)
        self.assertEqual(204.01829228943149, tsl2, 12)

if __name__ == "__main__":

    SOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    unittest.TextTestRunner(verbosity=2).run(SOLAR)
#end if
