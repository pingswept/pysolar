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
""" Tests for time.py and solar.py """
import datetime
import unittest
from pysolar import solar, elevation, time, constants
 # R0902: Too many instance attributes 7 is recommended (solved)
 # R0904: Too many public methods 20 is recommended (solved)
class TestTime(unittest.TestCase):
    """
    Test time methods
    """
    delta_t = 67
    longitude = -105.1786
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
        return 'Testing pysolar time functions'

    def test_all_jdn(self):
        """
        MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        Date, Time,
        10/17/2003, 12:30:30
        Julian day, Julian century,
        Julian ephemeris day, Julian ephemeris century, Julian ephemeris millennium
        with delta t
        2452930.312847, 0.037928,
        2452930.313623, 0.037928, 0.003793
        with no delta t
        2452930.312847, 0.037928,
        2452930.312847, 0.037928, 0.003793
        """
        print('testing all Julian values plus')
        print(self.test_all_jdn.__doc__)

        print('testing Julian Day')
        jdn = time.get_jdn(self.dt_list)
        self.assertEqual(2452930, jdn)

        ajd = time.get_ajd(self.dt_list)
        self.assertEqual(2452930.312847222, ajd, 6)

        ajd = time.get_ajd(self.dt_list, 0)
        self.assertEqual(2452930.312847222, ajd, 6)

        ajd = time.get_ajd(self.dt_list, self.delta_t)
        self.assertEqual(2452930.312847222, ajd, 6)

        jsd = time.get_julian_day(self.dt_list)
        self.assertEqual(2452930.312847222, jsd, 6)

        jsd = time.get_julian_day(self.dt_list, 0)
        self.assertEqual(2452930.312847222, jsd, 6)

        jsd = time.get_julian_day(self.dt_list, self.delta_t)
        self.assertEqual(2452930.312847222, jsd, 6)

        print('testing Julian Century')
        jct = time.get_julian_century(self.dt_list)
        self.assertEqual(0.03792779869191517, jct, 6)
        self.assertAlmostEqual(0.037928, jct, 6)

        jct1 = time.get_julian_century(self.dt_list, 0)
        self.assertEqual(0.03792779869191517, jct1, 6)
        self.assertAlmostEqual(0.037928, jct1, 6)

        jct2 = time.get_julian_century(self.dt_list, self.delta_t)
        self.assertEqual(0.03792779869191517, jct2, 6)
        self.assertAlmostEqual(0.037928, jct2, 6)

        print('testing Julian Ephemeris Day')
        jed = time.get_julian_ephemeris_day(self.dt_list, self.delta_t)
        self.assertEqual(2452930.313622685, jed, 6)
        self.assertAlmostEqual(2452930.313623, jed, 6)

        jed1 = time.get_julian_ephemeris_day(self.dt_list, 0)
        self.assertEqual(2452930.312847222, jed1, 6)
        self.assertAlmostEqual(2452930.312847, jed1, 6)

        jed2 = time.get_julian_ephemeris_day(self.dt_list)
        self.assertEqual(2452930.3135942305, jed2, 6)
        self.assertAlmostEqual(2452930.313594, jed2, 6)

        print('testing Julian Ephemeris Century')
        jec = time.get_julian_ephemeris_century(self.dt_list)
        self.assertEqual(0.0379278191438864, jec, 6)
        self.assertAlmostEqual(0.037928, jec, 6)

        jec1 = time.get_julian_ephemeris_century(self.dt_list, 0)
        self.assertEqual(0.03792779869191517, jec1, 6)
        self.assertAlmostEqual(0.037928, jec1, 6)

        jec2 = time.get_julian_ephemeris_century(self.dt_list, self.delta_t)
        self.assertEqual(0.037927819922933585, jec2, 6)
        self.assertAlmostEqual(0.037928, jec2, 6)

        print('testing Julian Ephemeris Millennium')
        jem = time.get_julian_ephemeris_millennium(self.dt_list)
        self.assertEqual(0.0037927819143886397, jem, 6)
        self.assertAlmostEqual(0.003793, jem, 6)

        jem1 = time.get_julian_ephemeris_millennium(self.dt_list, 0)
        self.assertEqual(0.003792779869191517, jem1, 6)
        self.assertAlmostEqual(0.003793, jem1, 6)

        jem2 = time.get_julian_ephemeris_millennium(self.dt_list, self.delta_t)
        self.assertEqual(0.003792781992293359, jem2, 6)
        self.assertAlmostEqual(0.003793, jem2, 6)

        jlon = time.get_julian_day(self.dt_list) - self.lon_offset
        self.assertEqual(2452930.60501, jlon, 6)

        jlon1 = time.get_julian_day(self.dt_list, 0) - self.lon_offset
        self.assertEqual(2452930.60501, jlon1, 6)

        jlon2 = time.get_julian_day(self.dt_list, self.delta_t) - self.lon_offset
        self.assertEqual(2452930.60501, jlon2, 6)

    def test_delta_epsilon(self):
        """
        testing Nutation obliquity
        Date,Time,Nutation obliquity
        delta t
        10/17/2003,12:30:30,0.001667
        no delta t
        10/17/2003,12:30:30,0.001667
        """
        print(self.test_delta_epsilon.__doc__)
        deps = solar.get_nutation(self.dt_list)['obliquity']
        self.assertEqual(0.0016665681017130273, deps, 6)
        self.assertAlmostEqual(0.001667, deps, 6)

        deps1 = solar.get_nutation(self.dt_list, 0)['obliquity']
        self.assertEqual(0.001666566120130517, deps1, 6)
        self.assertAlmostEqual(0.001667, deps1, 6)

        deps2 = solar.get_nutation(self.dt_list, self.delta_t)['obliquity']
        self.assertEqual(0.0016665681772496856, deps2, 6)
        self.assertAlmostEqual(0.001667, deps2, 6)

    def test_delta_psi(self):
        """
        testing Nutation longitude
        Date,Time,Nutation longitude
        delta t
        10/17/2003,12:30:30,-0.003998
        no delta t
        10/17/2003,12:30:30,-0.003998
        """
        print(self.test_delta_psi.__doc__)
        dpsi = solar.get_nutation(self.dt_list)['longitude']
        self.assertEqual(-0.003998404804368993, dpsi, 6)
        self.assertAlmostEqual(-0.003998, dpsi, 6)

        dpsi = solar.get_nutation(self.dt_list, 0)['longitude']
        self.assertEqual(-0.003998417958822815, dpsi, 6)
        self.assertAlmostEqual(-0.003998, dpsi, 6)

        dpsi = solar.get_nutation(self.dt_list, self.delta_t)['longitude']
        self.assertEqual(-0.003998404303332777, dpsi, 6)
        self.assertAlmostEqual(-0.003998, dpsi, 6)

    def test_eqeq(self):
        """
        testing
        Equation of equinox = delta psi * cosine epsilon
        """
        print(self.test_eqeq.__doc__)
        eqeq = solar.get_equation_of_equinox(self.dt_list) * 240.0
        self.assertEqual(-0.8807484707542705, eqeq, 12)
        self.assertAlmostEqual(-0.880748, eqeq, 6)

        eqeq = solar.get_equation_of_equinox(self.dt_list, 0) * 240.0
        self.assertEqual(-0.8807513681877716, eqeq, 12)
        self.assertAlmostEqual(-0.880751, eqeq, 6)

        eqeq = solar.get_equation_of_equinox(self.dt_list, self.delta_t) * 240.0
        self.assertEqual(-0.8807483603947576, eqeq, 12)
        self.assertAlmostEqual(-0.880748, eqeq, 6)


    def test_get_dut1(self):
        """
        testing
        see DUT1 http://asa.usno.navy.mil/SecM/Glossary.html#ut1
        MIDC SPA is set to 0 sec DUT1
        """
        print(self.test_get_dut1.__doc__)
        dut1 = datetime.timedelta(0)
        self.assertEqual(dut1, self.dut1)

    def test_get_leap_seconds(self):
        """
        testing
        Leap seconds
        """
        gls = time.get_leap_seconds(self.dt_list)
        print(self.test_get_leap_seconds.__doc__)
        self.assertEqual(gls, 32)

    def test_sidereal_angles(self):
        """
        testing
        with or without delta t on the site calculator
        Mean sidereal time is not effected by delta t
        Date,Time,Greenwich mean sidereal time,Greenwich sidereal time
        delta t
        10/17/2003,12:30:30,318.515578,318.511910
        no delta t
        10/17/2003,12:30:30,318.515578,318.511910
        """
        print(self.test_sidereal_angles.__doc__)
        gmst = solar.get_gmst(self.dt_list)
        self.assertEqual(318.5155918879318, gmst, 6)
        self.assertAlmostEqual(318.515592, gmst, 6)

        gmst1 = solar.get_gmst(self.dt_list, 0)
        self.assertEqual(318.5155918879318, gmst1, 6)
        # self.assertAlmostEqual(318.515578, gmst1, 6)

        gmst2 = solar.get_gmst(self.dt_list, self.delta_t)
        self.assertEqual(318.5155918879318, gmst2, 6)
        # self.assertAlmostEqual(318.515578, gmst2, 6)

        gast = solar.get_gast(self.dt_list)
        self.assertEqual(318.511922102637, gast, 6)
        self.assertAlmostEqual(318.511922, gast, 6)

        gast1 = solar.get_gast(self.dt_list, 0)
        self.assertEqual(318.5119220905644, gast1, 6)
        # self.assertAlmostEqual(318.511910, gast, 6)

        gast2 = solar.get_gast(self.dt_list, self.delta_t)
        self.assertEqual(318.5119221030968, gast2, 6)
        # self.assertAlmostEqual(318.511910, gast, 6)


        # lmst = solar.get_lmst(self.dt_list)
        # lmst = solar.get_lmst(self.dt_list, 0)
        # lmst = solar.get_lmst(self.dt_list, self.delta_t)


        # last = solar.get_last(self.dt_list)
        # last = solar.get_last(self.dt_list, 0)
        # last = solar.get_last(self.dt_list, self.delta_t)


    def test_jed1_jsd1(self):
        """
        doc
        """
        print(self.test_jed1_jsd1.__doc__)
        jed1 = time.get_julian_ephemeris_day(self.dt_list)
        jed1 += self.delta_t / 86400.0
        jsd1 = time.get_julian_day(self.dt_list)
        print((jed1 - jsd1) * 86400 - self.delta_t)

    def test_solar_solar(self):
        """
        doc
        """
        #solar.solar_test()

    def test_timestamp(self):
        """
        testing
        Timestamp
        """
        print(self.test_timestamp.__doc__)
        tss = time.timestamp(self.dt_list)
        self.assertEqual(1066437094.5415, tss, 6)

        tss = time.timestamp(self.dt_list, 0)
        self.assertEqual(1066437030.0, tss, 6)

        tss = time.timestamp(self.dt_list, self.delta_t)
        self.assertEqual(1066437097.0, tss, 6)

class TestSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786 # -105:
    lon_offset = longitude / 360.0
    latitude = 39.742476 # 39:44:32
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    slope = 30.0 # degrees
    slope_orientation = -10.0 # degrees east from south
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    params_list = [elevation, latitude, longitude, slope, slope_orientation, temperature, pressure]
    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        # Reda & Andreas say that this time is in "Local Standard Time", which they
        # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
        # to UTC.
        return None

    def test_get_ac(self):
        """
        testing
        Date,Time,Aberration correction
        delta t
        10/17/2003,12:30:30,-0.005711
        no delta t
        10/17/2003,12:30:30,-0.005711
        """
        print(self.test_get_ac.__doc__)
        gac = solar.get_aberration_correction(self.dt_list)
        self.assertEqual(-0.00571135860114326, gac, 6)
        self.assertAlmostEqual(-0.005711, gac, 6)

        gac1 = solar.get_aberration_correction(self.dt_list, 0)
        self.assertEqual(-0.005711357420612273, gac1, 6)
        self.assertAlmostEqual(-0.005711, gac1, 6)

        gac2 = solar.get_aberration_correction(self.dt_list, self.delta_t)
        self.assertEqual(-0.0057113586461114444, gac2, 6)
        self.assertAlmostEqual(-0.005711, gac2, 6)

    def test_get_asl(self):
        """

        Date,Time,Apparent sun longitude
        delta t
        10/17/2003,12:30:30,204.008552
        no delta t
        10/17/2003,12:30:30,204.007782
        """
        print(self.test_get_asl.__doc__)
        asl = solar.get_apparent_sun_longitude(self.dt_list)
        self.assertEqual(204.00852551801194, asl, 6)
        self.assertAlmostEqual(204.008526, asl, 6)

        asl1 = solar.get_apparent_sun_longitude(self.dt_list, 0)
        self.assertEqual(204.0077842363739, asl1, 6)
        # self.assertAlmostEqual(204.007782, asl1, 6)

        asl2 = solar.get_apparent_sun_longitude(self.dt_list, self.delta_t)
        self.assertEqual(204.00855375458207, asl2, 6)
        # self.assertAlmostEqual(204.008552, asl2, 6)

    def test_get_ehp(self):
        """
        testing
        Date,Time,Sun equatorial horizontal parallax
        no delta t
        10/17/2003,12:30:30,0.002451
        delta t
        10/17/2003,12:30:30,0.002451
        """
        print(self.test_get_ehp.__doc__)
        ehp = solar.get_max_horizontal_parallax(self.dt_list)
        self.assertEqual(0.0024343316735867776, ehp, 6)
        self.assertAlmostEqual(0.002434, ehp, 6)

        ehp1 = solar.get_max_horizontal_parallax(self.dt_list, 0)
        self.assertEqual(0.002434332176760325, ehp1, 6)
        # self.assertAlmostEqual(0.002451, ehp1, 6)

        ehp2 = solar.get_max_horizontal_parallax(self.dt_list, self.delta_t)
        self.assertEqual(0.0024343316544201514, ehp2, 6)
        # self.assertAlmostEqual(0.002451, ehp2, 6)

    def test_get_lha(self):
        """
        testing
        Date,Time,Observer hour angle
        delta t
        10/17/2003,12:33:30,11.856008
        no delta t
        10/17/2003,12:30:30,11.106627
        """
        print(self.test_get_lha.__doc__)
        lha = solar.get_local_hour_angle(self.dt_list, self.params_list)
        self.assertEqual(11.098538789968956, lha, 6)
        self.assertAlmostEqual(11.098539, lha, 6)

        lha1 = solar.get_local_hour_angle(self.dt_list, self.params_list, 0)
        self.assertEqual(11.099237371963284, lha1, 6)
        # self.assertAlmostEqual(11.106627, lha1, 6)

        lha2 = solar.get_local_hour_angle(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(11.098512179873097, lha2, 6)
        # self.assertAlmostEqual(11.856008, lha2, 6)

    def test_get_pad(self):
        """
        testing
        Projected axial distance
        MIDC SPA is not at 12:30
        """
        print(self.test_get_pad.__doc__)
        pad = solar.get_projected_axial_distance(self.params_list)
        self.assertEqual(0.6361121708785658, pad, 6)

    def test_get_prd(self):
        """
        testing
        Projected radial distance
        MIDC SPA is not at 12:30
        """
        print(self.test_get_prd.__doc__)
        prd = solar.get_projected_radial_distance(self.params_list)
        self.assertEqual(0.7702006191191089, prd, 6)

    def test_get_pwe(self):
        """
        testing
        Pressure with elevation
        MIDC SPA is not at 12:30
        """
        print(self.test_get_pwe.__doc__)
        pwe = elevation.get_pressure_with_elevation(1567.7)
        self.assertAlmostEqual(83855.90227687225, pwe, 6)

    def test_get_sed(self):
        """
        testing
        Date,Time,Earth radius vector
        delta t
        10/17/2003,12:30:30,0.996542
        no delta t
        10/17/2003,12:30:30,0.996543
        """
        print(self.test_get_sed.__doc__)
        sed = solar.get_sun_earth_distance(self.dt_list)
        self.assertEqual(0.9965424181160335, sed, 6)
        self.assertAlmostEqual(0.996542, sed, 6)

        sed1 = solar.get_sun_earth_distance(self.dt_list, 0)
        self.assertEqual(0.9965426241002012, sed1, 6)
        self.assertAlmostEqual(0.996543, sed1, 6)

        sed2 = solar.get_sun_earth_distance(self.dt_list, self.delta_t)
        self.assertEqual(0.9965424102697913, sed2, 6)
        self.assertAlmostEqual(0.996542, sed2, 6)

    def test_get_twe(self):
        """
        testing
        Temperature with elevation
        MIDC SPA is not at 12:30
        """
        print(self.test_get_twe.__doc__)
        twe = elevation.get_temperature_with_elevation(1567.7)
        self.assertAlmostEqual(277.95995, twe, 6)

class TestGeocentricSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786
    lon_offset = longitude / 360.0
    latitude = 39.742476
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    slope = 30.0 # degrees
    slope_orientation = -10.0 # degrees east from south
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    params_list = [elevation, latitude, longitude, slope, slope_orientation, temperature, pressure]
    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        # Reda & Andreas say that this time is in "Local Standard Time", which they
        # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
        # to UTC.
        return None

    def test_lat_lon(self):
        """
        testing
        Date, Time
        10/17/2003, 12:30:30
        Heliocentric longitude, Heliocentric latitude, Geocentric longitude, Geocentric latitude
        delta t
        24.018262, -0.000101, 204.018262, 0.000101
        no delta t
        24.017492, -0.000101, 204.017492, 0.000101
        """
        print(self.test_lat_lon.__doc__)
        hlon = solar.get_heliocentric_longitude(self.dt_list)
        self.assertEqual(24.018235281417446, hlon, 6)
        self.assertAlmostEqual(24.018235, hlon, 6)

        hlon1 = solar.get_heliocentric_longitude(self.dt_list, 0)
        self.assertEqual(24.017494011753342, hlon1, 6)
        # self.assertAlmostEqual(24.017492, hlon1, 6)

        hlon2 = solar.get_heliocentric_longitude(self.dt_list, self.delta_t)
        self.assertEqual(24.018263517531523, hlon2, 6)
        # self.assertAlmostEqual(24.018262, hlon2, 6)

        hlat = solar.get_heliocentric_latitude(self.dt_list)
        self.assertEqual(-0.0001011213954488705, hlat, 6)
        self.assertAlmostEqual(-0.000101, hlat, 6)

        hlat1 = solar.get_heliocentric_latitude(self.dt_list, 0)
        self.assertEqual(-0.00010110749648050061, hlat1, 6)
        self.assertAlmostEqual(-0.000101, hlat1, 6)

        hlat2 = solar.get_heliocentric_latitude(self.dt_list, self.delta_t)
        self.assertEqual(-0.00010112192480034693, hlat2, 6)
        self.assertAlmostEqual(-0.000101, hlat2, 6)

        glon = solar.get_geocentric_longitude(self.dt_list)
        self.assertEqual(204.01823528141745, glon, 6)
        self.assertAlmostEqual(204.018235, glon, 6)

        glon1 = solar.get_geocentric_longitude(self.dt_list, 0)
        self.assertEqual(204.01749401175334, glon1, 6)
        # self.assertAlmostEqual(204.017492, glon1, 6)

        glon2 = solar.get_geocentric_longitude(self.dt_list, self.delta_t)
        self.assertEqual(204.01826351753152, glon2, 6)
        # self.assertAlmostEqual(204.018262, glon2, 6)

        glat = solar.get_geocentric_latitude(self.dt_list)
        self.assertEqual(0.0001011213954488705, glat, 6)
        self.assertAlmostEqual(0.000101, glat, 6)

        glat1 = solar.get_geocentric_latitude(self.dt_list, 0)
        self.assertEqual(0.00010110749648050061, glat1, 6)
        self.assertAlmostEqual(0.000101, glat1, 6)

        glat2 = solar.get_geocentric_latitude(self.dt_list, self.delta_t)
        self.assertEqual(0.00010112192480034693, glat2, 6)
        self.assertAlmostEqual(0.000101, glat2, 6)


    def test_rad_dec(self):
        """
        testing
        Date,Time,Geocentric sun right ascension,Geocentric sun declination
        delta t
        10/17/2003,12:30:30,202.227408,-9.314340
        no delta t
        10/17/2003,12:30:30,202.226683,-9.314057
        """
        print(self.test_rad_dec.__doc__)
        gsra = solar.get_geocentric_right_ascension(self.dt_list)
        self.assertEqual(202.23478331266804, gsra, 6)
        self.assertAlmostEqual(202.234783, gsra, 5)

        gsra1 = solar.get_geocentric_right_ascension(self.dt_list, 0)
        self.assertEqual(202.23408471860108, gsra1, 6)
        # self.assertAlmostEqual(202.226683, gsra, 5)

        gsra2 = solar.get_geocentric_right_ascension(self.dt_list, self.delta_t)
        self.assertEqual(202.2348099232237, gsra2, 6)
        # self.assertAlmostEqual(202.227408, gsra, 5)

        gsd = solar.get_geocentric_sun_declination(self.dt_list)
        self.assertEqual(-9.29586981453048, gsd, 6)
        self.assertAlmostEqual(-9.295870, gsd, 6)

        gsd1 = solar.get_geocentric_sun_declination(self.dt_list, 0)
        self.assertEqual(-9.295597420338579, gsd1, 6)
        # self.assertAlmostEqual(-9.314057, gsd, 6)

        gsd2 = solar.get_geocentric_sun_declination(self.dt_list, self.delta_t)
        self.assertEqual(-9.295880190422015, gsd2, 6)
        # self.assertAlmostEqual(-9.314340, gsd, 6)

class TestTopocentricSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786
    lon_offset = longitude / 360.0
    latitude = 39.742476
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    slope = 30.0 # degrees
    slope_orientation = -10.0 # degrees east from south
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    params_list = [elevation, latitude, longitude, slope, slope_orientation, temperature, pressure]
    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        # Reda & Andreas say that this time is in "Local Standard Time", which they
        # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
        # to UTC.
        return None

    def test_get_aoi(self):
        """
        testing
        """
        print(self.test_get_aoi.__doc__)

        aoi = solar.get_incidence_angle(self.dt_list, self.params_list)
        self.assertEqual(25.12448748951714, aoi, 6)
        self.assertAlmostEqual(25.10861, aoi, 6)

        aoi1 = solar.get_incidence_angle(self.dt_list, self.params_list, 0)
        self.assertEqual(25.12448748951714, aoi1, 6)
        self.assertAlmostEqual(25.10861, aoi1, 6)

        aoi2 = solar.get_incidence_angle(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(25.12448748951714, aoi2, 6)
        self.assertAlmostEqual(25.10861, aoi2, 6)

    def test_get_srap(self):
        """
        testing

        """
        print(self.test_get_srap.__doc__)
        srap = solar.get_right_ascension_parallax(self.dt_list, self.params_list)
        self.assertEqual(-0.00036205752935090436, srap, 6)
        self.assertAlmostEqual(-0.000364, srap, 6)

        srap1 = solar.get_right_ascension_parallax(self.dt_list, self.params_list, 0)
        self.assertEqual(-0.00036205752935090436, srap1, 6)
        self.assertAlmostEqual(-0.000364, srap1, 6)

        srap2 = solar.get_right_ascension_parallax(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(-0.00036205752935090436, srap2, 6)
        self.assertAlmostEqual(-0.000364, srap2, 6)

    def test_get_taa(self):
        """
        testing
        """
        print(self.test_get_taa.__doc__)
        taa = solar.get_topocentric_azimuth_angle(self.dt_list, self.params_list)
        self.assertEqual(194.18777361875783, taa, 6)
        self.assertAlmostEqual(194.184400, taa, 6)

        taa1 = solar.get_topocentric_azimuth_angle(self.dt_list, self.params_list, 0)
        self.assertEqual(194.18777361875783, taa1, 6)
        self.assertAlmostEqual(194.184400, taa1, 6)

        taa2 = solar.get_topocentric_azimuth_angle(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(194.18777361875783, taa2, 6)
        self.assertAlmostEqual(194.184400, taa2, 6)

    def test_get_teo(self):
        """
        testing

        """
        print(self.test_get_teo.__doc__)
        teo = solar.get_true_ecliptic_obliquity(self.dt_list)
        self.assertEqual(23.440464516774025, teo, 6)
        self.assertAlmostEqual(23.440465, teo, 6)

        teo1 = solar.get_true_ecliptic_obliquity(self.dt_list, 0)
        self.assertEqual(23.440464516774025, teo1, 6)
        self.assertAlmostEqual(23.440465, teo1, 6)

        teo2 = solar.get_true_ecliptic_obliquity(self.dt_list, self.delta_t)
        self.assertEqual(23.440464516774025, teo2, 6)
        self.assertAlmostEqual(23.440465, teo2, 6)

    def test_get_tlha(self):
        """
        testing
        """
        print(self.test_get_tlha.__doc__)
        tlha = solar.get_topocentric_lha(self.dt_list, self.params_list)
        self.assertEqual(10.98542433427071, tlha, 6)
        self.assertAlmostEqual(10.982765, tlha, 6)

        tlha1 = solar.get_topocentric_lha(self.dt_list, self.params_list, 0)
        self.assertEqual(10.98542433427071, tlha1, 6)
        self.assertAlmostEqual(10.982765, tlha1, 6)

        tlha2 = solar.get_topocentric_lha(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(10.98542433427071, tlha2, 6)
        self.assertAlmostEqual(10.982765, tlha2, 6)

    def test_get_tsd(self):
        """
        MIDC SPA
        """
        print('testing Topocentric sun declination')
        tsd = solar.get_topocentric_sun_declination(self.dt_list, self.params_list)
        self.assertEqual(-9.31597764750972, tsd, 6)
        # self.assertAlmostEqual(-9.316043, self.t_tsd(), 6)

        tsd1 = solar.get_topocentric_sun_declination(self.dt_list, self.params_list, 0)
        self.assertEqual(-9.31597764750972, tsd1, 6)
        # self.assertAlmostEqual(-9.316043, tsd1, 6)

        tsd2 = solar.get_topocentric_sun_declination(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(-9.31597764750972, tsd2, 6)
        # self.assertAlmostEqual(-9.316043, tsd2, 6)

    def test_get_tsra(self):
        """
        MIDC SPA
        """
        print('testing Topocentric sun right ascension')
        tsra = solar.get_topocentric_right_ascension(self.dt_list, self.params_list)
        self.assertEqual(202.22669624203763, tsra, 6)
        self.assertAlmostEqual(202.226696, tsra, 6)

        tsra1 = solar.get_topocentric_right_ascension(self.dt_list, self.params_list, 0)
        self.assertEqual(202.22669624203763, tsra1, 6)
        self.assertAlmostEqual(202.226696, tsra1, 6)

        tsra2 = solar.get_topocentric_right_ascension(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(202.22669624203763, tsra2, 6)
        self.assertAlmostEqual(202.226696, tsra2, 6)

    def test_get_tza(self):
        """
        MIDC SPA
        """
        print('testing Topocentric zenith angle')
        tza = solar.get_topocentric_zenith_angle(self.dt_list, self.params_list)
        self.assertAlmostEqual(89.60770246659617, tza, 6)
        # self.assertAlmostEqual(50.088106, tza, 6)

        tza1 = solar.get_topocentric_zenith_angle(self.dt_list, self.params_list, 0)
        self.assertAlmostEqual(50.08855158690924, tza1, 6)
        # self.assertAlmostEqual(50.088106, tza1, 6)

        tza2 = solar.get_topocentric_zenith_angle(self.dt_list, self.params_list, self.delta_t)
        self.assertAlmostEqual(50.08855158690924, tza2, 6)
        # self.assertAlmostEqual(50.088106, tza2, 6)

class TestAzElSolar(unittest.TestCase):
    """
    Test azimuth and elevation
    """
    longitude = -105.1786
    lon_offset = longitude / 360.0
    latitude = 39.742476
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.CELSIUS_OFFSET # kelvin
    slope = 30.0 # degrees
    slope_orientation = -10.0 # degrees east from south
    dt_list = [2003, 10, 17, 19, 30, 30, 0, 0, 0]
    delta_t = 67
    params_list = [elevation, latitude, longitude, slope, slope_orientation, temperature, pressure]
    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        # Reda & Andreas say that this time is in "Local Standard Time", which they
        # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
        # to UTC.
        return None

    def test_get_azimuth(self):
        """
        testing
        Azimuth
        """
        print(self.test_get_azimuth.__doc__)
        azm = solar.get_azimuth(self.dt_list, self.params_list)
        self.assertAlmostEqual(-14.182528371336758, azm, 6)

        azm1 = solar.get_azimuth(self.dt_list, self.params_list, 0)
        self.assertAlmostEqual(-14.182528371336758, azm1, 6)

        azm2 = solar.get_azimuth(self.dt_list, self.params_list, self.delta_t)
        self.assertAlmostEqual(-14.182528371336758, azm2, 6)

    def test_get_altitude(self):
        """
        testing
        Altitude
        """
        print(self.test_get_altitude.__doc__)
        alt = solar.get_altitude(self.dt_list, self.params_list)
        self.assertEqual(-5.590197393234738, alt, 6)

        alt1 = solar.get_altitude(self.dt_list, self.params_list, 0)
        self.assertEqual(-5.590197393234738, alt1, 6)

        alt2 = solar.get_altitude(self.dt_list, self.params_list, self.delta_t)
        self.assertEqual(-5.590197393234738, alt2, 6)



if __name__ == "__main__":
    SOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    TIME = unittest.defaultTestLoader.loadTestsFromTestCase(TestTime)
    GSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestGeocentricSolar)
    TSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestTopocentricSolar)
    AESOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestAzElSolar)
    unittest.TextTestRunner(verbosity=2).run(TIME)
    unittest.TextTestRunner(verbosity=2).run(SOLAR)
    unittest.TextTestRunner(verbosity=2).run(GSOLAR)
    unittest.TextTestRunner(verbosity=2).run(TSOLAR)
    unittest.TextTestRunner(verbosity=2).run(AESOLAR)

#end if
