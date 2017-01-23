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
from pysolar import \
    solar, \
    constants, \
    time, \
    elevation
 # R0902: Too many instance attributes 7 is recommended (solved)
 # R0904: Too many public methods 20 is recommended
class TestSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786
    lon_offset = longitude / 360.0
    latitude = 39.742476
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.celsius_offset # kelvin
    slope = 30.0 # degrees
    slope_orientation = -10.0 # degrees east from south

    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        self.dio = datetime.datetime(2003, 10, 17, 19, 30, 0, tzinfo=datetime.timezone.utc)
        self.dut1 = datetime.timedelta(seconds=time.get_delta_t(
            self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))
        self.dio += datetime.timedelta(seconds=time.get_delta_t(
            self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))
        # Reda & Andreas say that this time is in "Local Standard Time", which they
        # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
        # to UTC.

    def t_jem(self):
        """
        used for tests
        """
        jed = time.get_julian_ephemeris_day(self.dio)
        jec = time.get_julian_ephemeris_century(jed)
        return time.get_julian_ephemeris_millennium(jec)

    def t_gac(self):
        """
        used for tests
        """
        return solar.get_aberration_correction(self.t_sed())

    def test_get_ac(self):
        """
        MIDC SPA is -0.005711 at 12:30
        """
        jed = time.get_julian_ephemeris_day(self.dio)
        jec = time.get_julian_ephemeris_century(jed)
        jem = time.get_julian_ephemeris_millennium(jec)
        sed = solar.get_sun_earth_distance(jem)
        gac = solar.get_aberration_correction(sed)
        self.assertAlmostEqual(
            -0.005711359813021086, gac, 6)

    def t_aoi(self):
        """
        used for tests
        """
        aoi = solar.get_incidence_angle(
            self.t_tza(), self.slope, self.slope_orientation, self.t_taa())
        return aoi

    def t_asl(self):
        """
        used for tests
        """
        g_lon = solar.get_geocentric_longitude(
            self.t_jem())
        return solar.get_apparent_sun_longitude(
            g_lon, self.t_nut(), self.t_gac())

    def test_get_asl(self):
        """
        MIDC SPA is 204.008183 at 12:30
        """
        # 204.00818592528472 below
        self.assertAlmostEqual(
            204.00818094267757, self.t_asl(), 13
            )
        self.assertAlmostEqual(
            204.008183, self.t_asl(), 4
            )

    def t_ast(self):
        """
        used for tests
        """
        jed = time.get_julian_ephemeris_day(self.dio)
        jec = time.get_julian_ephemeris_century(jed)
        jem = time.get_julian_ephemeris_millennium(jec)
        jsd = time.get_julian_solar_day(self.dio)
        nut = solar.get_nutation(jec)
        return solar.get_apparent_sidereal_time(jsd, jem, nut)

    def t_ehp(self):
        """
        used for tests
        """
        return solar.get_equatorial_horizontal_parallax(self.t_sed())

    def test_get_ehp(self):
        """
        test
        """
        self.assertAlmostEqual(
            0.002434331157052594, self.t_ehp(), 6
        )

    def t_g_lat(self):
        """
        used for tests
        """
        return solar.get_geocentric_latitude(self.t_jem())

    def t_g_lon(self):
        """
        used for tests
        """
        return solar.get_geocentric_longitude(self.t_jem())

    def t_gsd(self):
        """
        used for tests
        """
        return solar.get_geocentric_sun_declination(
            self.t_asl(), self.t_teo(), self.t_g_lat())

    def test_get_gsd(self):
        """
        MIDC SPA is -9.314204 at 12:30
        """
        self.assertAlmostEqual(
            -9.314203486059162, self.t_gsd(), 6)

    def t_gsra(self):
        """
        used for tests
        """
        return solar.get_geocentric_sun_right_ascension(
            self.t_asl(), self.t_teo(), self.t_g_lat())

    def test_get_gsra(self):
        """
        MIDC SPA is 202.227060 at 12:30
        """
        self.assertAlmostEqual(
            202.22705829956698, self.t_gsra(), 6)

    def t_lha(self):
        """
        used for tests not sure why ast=318.5119 was hardcoded.
        we should have 318.388061 here any way so somethings wrong.
        """
        return solar.get_local_hour_angle(
            self.t_ast(), self.longitude, self.t_gsra())

    def test_get_lha(self):
        """
        MIDC SPA is 10.982401 at 12:30
        """
        self.assertAlmostEqual(
            10.98506227674136, self.t_lha(), 6)

    def t_nut(self):
        """
        used for tests
        """
        jsd = time.get_julian_solar_day(
            self.dio)
        return solar.get_nutation(
            time.get_julian_century(jsd))

    def test_get_nut(self):
        """
        MIDC SPA is 0.001667 at 12:30
        MIDC SPA is -0.003998 at 12:30
        """
        self.assertAlmostEqual(
            0.0016665652000061504, self.t_nut()['obliquity'], 6)
        self.assertAlmostEqual(
            -0.003998424073879077, self.t_nut()['longitude'], 6)

    def t_pad(self):
        """
        used for tests
        """
        return solar.get_projected_axial_distance(
            self.elevation, self.latitude)

    def test_get_pad(self):
        """
        don't know what it should be
        """
        self.assertAlmostEqual(0.6361121708785658, self.t_pad(), 6)

    def t_prd(self):
        """
        used for tests
        """
        return solar.get_projected_radial_distance(
            self.elevation, self.latitude)

    def test_get_prd(self):
        """
        MIDC SPA is not at 12:30
        """
        self.assertAlmostEqual(
            0.7702006191191089, self.t_prd(), 6)

    def test_get_pwe(self):
        """
        MIDC SPA is not at 12:30
        """
        self.assertAlmostEqual(
            83855.90227687225, elevation.get_pressure_with_elevation(
                1567.7), 6)

    def t_sed(self):
        """
        used for tests
        """
        return solar.get_sun_earth_distance(self.t_jem())

    def test_get_sed(self):
        """
        MIDC SPA is 0.996542 at 12:30
        """
        self.assertAlmostEqual(
            0.9965421031, self.t_sed(), 6)

    def t_srap(self):
        """
        used for tests
        """
        return solar.get_parallax_sun_right_ascension(
            self.t_prd(), self.t_ehp(), self.t_lha(), self.t_gsd())

    def test_get_srap(self):
        """
        MIDC SPA is -0.000364 at 12:30
        """
        self.assertAlmostEqual(
            -0.00036205752935090436, self.t_srap(), 6)

    def t_taa(self):
        """
        used for tests
        """
        return solar.get_topocentric_azimuth_angle(
            self.t_tlha(), self.latitude, self.t_tsd())

    def test_get_taa(self):
        """
        MIDC SPA is 194.184400 at 12:30
        """
        self.assertAlmostEqual(
            194.18777361875783, self.t_taa(), 6)

    def t_teo(self):
        """
        used for tests
        """
        return solar.get_true_ecliptic_obliquity(
            self.t_jem(), self.t_nut())

    def test_get_teo(self):
        """
        MIDC SPA is 23.440465 at 12:30
        """
        self.assertAlmostEqual(
            23.440464516774025, self.t_teo(), 6)

    def t_tlha(self):
        """
        used for tests
        """
        return solar.get_topocentric_local_hour_angle(
            self.t_lha(), self.t_srap())

    def test_get_tlha(self):
        """
        MIDC SPA is 10.982765 at 12:30
        """
        self.assertAlmostEqual(
            10.98542433427071, self.t_tlha(), 6)

    def t_tsd(self):
        """
        used for tests
        """
        return solar.get_topocentric_sun_declination(
            self.t_gsd(), self.t_pad(), self.t_ehp(), self.t_srap(), self.t_lha())

    def test_get_tsd(self):
        """
        MIDC SPA is -9.316043 at 12:30
        """
        self.assertAlmostEqual(
            -9.31597764750972, self.t_tsd(), 6)

    def t_tsra(self):
        """
        used for tests
        """
        return solar.get_topocentric_sun_right_ascension(
            self.t_prd(), self.t_ehp(), self.t_lha(), self.t_asl(), self.t_teo(), self.t_g_lat())

    def test_get_tsra(self):
        """
        MIDC SPA is 202.226696 at 12:30
        """
        self.assertAlmostEqual(
            202.22669624203763, self.t_tsra(), 6)

    def test_get_twe(self):
        """
        MIDC SPA is not at 12:30
        """
        self.assertAlmostEqual(
            277.95995, elevation.get_temperature_with_elevation(
                1567.7), 6)

    def t_tza(self):
        """
        solar.get_topocentric_sun_declination(
                self.t_gsd(), self.t_pad(), self.t_ehp(), self.t_srap(), self.t_lha())
        """
        return solar.get_topocentric_zenith_angle(
            self.latitude, self.t_tsd(), self.t_tlha(), self.pressure, self.temperature)

    def test_get_tza(self):
        """
        MIDC SPA is 50.088106 at 12:30
        """
        self.assertAlmostEqual(
            50.08855158690924, self.t_tza(), 6)

class TestTime(unittest.TestCase):
    """
    Test time methods
    """
    longitude = -105.1786
    lon_offset = longitude / 360.0
    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        self.dio = datetime.datetime(
            2003, 10, 17, 19, 30, 0, tzinfo=datetime.timezone.utc)
        self.dut1 = datetime.timedelta(
            seconds=time.get_delta_t(
                self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))
        self.dio += datetime.timedelta(
            seconds=time.get_delta_t(
                self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))

    def test_get_ajd(self):
        """
        MIDC SPA is 2452930.312504 at 12:30
        """
        self.assertAlmostEqual(
            2452930.3125, time.ajd(self.dio), 6)

    def test_get_ast(self):
        """
        MIDC SPA is 318.388061 at 12:30
        """
        jed = time.get_julian_ephemeris_day(self.dio)
        jec = time.get_julian_ephemeris_century(jed)
        jem = time.get_julian_ephemeris_millennium(jec)
        jsd = time.get_julian_solar_day(self.dio)
        nut = solar.get_nutation(jec)
        ast = solar.get_apparent_sidereal_time(jsd, jem, nut)
        self.assertAlmostEqual(
            318.39072057630835, ast, 6)

    def test_get_dut1(self):
        """
        see DUT1 http://asa.usno.navy.mil/SecM/Glossary.html#ut1
        datetime.timedelta(0, 0, 357500)
        MIDC SPA is set to 0.3575 sec DUT1
        """
        self.assertEqual(
            datetime.timedelta(0, 0, 357500), self.dut1)

    def test_get_jct(self):
        """
        MIDC SPA is 0.037928 at 12:30
        """
        self.assertAlmostEqual(
            0.03792778918548939, time.get_julian_century(
                time.ajd(self.dio)), 6)

    def test_get_jdn(self):
        """
        MIDC SPA is 2452930
        """
        self.assertEqual(
            2452930, time.jdn(self.dio))

    def test_get_jec(self):
        """
        MIDC SPA is 0.037928 at 12:30
        """
        self.assertAlmostEqual(
            0.0379278191438864, time.get_julian_century(
                time.ajd(self.dio)), 6)

    def test_get_jed(self):
        """
        MIDC SPA is 2452930.313251 at 12:30
        """
        self.assertAlmostEqual(
            2452930.3132470082, time.get_julian_ephemeris_day(
                self.dio), 6)

    def test_get_jem(self):
        """
        MIDC SPA is 0.003793 at 12:30
        """
        self.assertAlmostEqual(
            0.03792778918548939, time.get_julian_century(
                time.ajd(self.dio)), 6)

    def test_get_jsd(self):
        """
        MIDC SPA is 2452930.604171 at 19:30
        """
        self.assertAlmostEqual(
            2452930.604662778, time.get_julian_solar_day(
                self.dio) - self.lon_offset, 6)

    def test_get_ts(self):
        """
        d = 1066419000.3575 seconds
        no tzinfo 1066437030.0
        """
        no_tzinfo = datetime.datetime(2003, 10, 17, 19, 30, 0, tzinfo=None)
        self.assertEqual(1066419000.3575, time.timestamp(self.dio))
        self.assertEqual(1066437000.0, time.timestamp(no_tzinfo))
        # print('dio =', time.timestamp(self.dio), 'seconds')
        # print('dio no tzinfo =', time.timestamp(no_tzinfo), 'seconds')

class TestGeocentricSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786
    lon_offset = longitude / 360.0
    latitude = 39.742476
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.celsius_offset # kelvin
    slope = 30.0 # degrees
    slope_orientation = -10.0 # degrees east from south

    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        self.dio = datetime.datetime(2003, 10, 17, 19, 30, 0, tzinfo=datetime.timezone.utc)
        self.dut1 = datetime.timedelta(seconds=time.get_delta_t(
            self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))
        self.dio += datetime.timedelta(seconds=time.get_delta_t(
            self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))
        # Reda & Andreas say that this time is in "Local Standard Time", which they
        # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
        # to UTC.

    def test_get_glat(self):
        """
        MIDC SPA is 0.000101 at 12:30
        """
        jed = time.get_julian_ephemeris_day(self.dio)
        jec = time.get_julian_ephemeris_century(jed)
        jem = time.get_julian_ephemeris_millennium(jec)
        glat = solar.get_geocentric_latitude(jem)
        self.assertAlmostEqual(
            0.00010111493548486615, glat, 6)

    def test_get_glon(self):
        """
        MIDC SPA is 204.017893 at 12:30
        """
        jed = time.get_julian_ephemeris_day(self.dio)
        jec = time.get_julian_ephemeris_century(jed)
        jem = time.get_julian_ephemeris_millennium(jec)
        glon = solar.get_geocentric_longitude(jem)
        self.assertAlmostEqual(
            204.01789072656447, glon, 6)

class TestTopocentricSolar(unittest.TestCase):
    """
    Test solar and time methods
    """
    longitude = -105.1786
    lon_offset = longitude / 360.0
    latitude = 39.742476
    pressure = 82000.0 # pascals
    elevation = 1830.14 # meters
    temperature = 11.0 + constants.celsius_offset # kelvin
    slope = 30.0 # degrees
    slope_orientation = -10.0 # degrees east from south

    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        self.dio = datetime.datetime(2003, 10, 17, 19, 30, 0, tzinfo=datetime.timezone.utc)
        self.dut1 = datetime.timedelta(seconds=time.get_delta_t(
            self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))
        self.dio += datetime.timedelta(seconds=time.get_delta_t(
            self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))
        # Reda & Andreas say that this time is in "Local Standard Time", which they
        # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
        # to UTC.

    def test_get_aoi(self):
        """
        MIDC SPA is 25.108613 at 12:30
        """
        ele = self.elevation
        lat = self.latitude
        lon = self.longitude
        press = self.pressure
        slope = self.slope
        slope_orientation = self.slope_orientation
        temp = self.temperature
        jed = time.get_julian_ephemeris_day(self.dio)
        jec = time.get_julian_ephemeris_century(jed)
        jem = time.get_julian_ephemeris_millennium(jec)
        g_lon = solar.get_geocentric_longitude(jem)
        jsd = time.get_julian_solar_day(self.dio)
        jct = time.get_julian_century(jsd)
        nut = solar.get_nutation(jct)
        sed = solar.get_sun_earth_distance(jem)
        gac = solar.get_aberration_correction(sed)
        asl = solar.get_apparent_sun_longitude(g_lon, nut, gac)
        teo = solar.get_true_ecliptic_obliquity(jem, nut)
        glat = solar.get_geocentric_latitude(jem)
        gsd = solar.get_geocentric_sun_declination(asl, teo, glat)
        pad = solar.get_projected_axial_distance(ele, lat)
        ehp = solar.get_equatorial_horizontal_parallax(sed)
        prd = solar.get_projected_radial_distance(ele, lat)
        ast = solar.get_apparent_sidereal_time(jsd, jem, nut)
        gsra = solar.get_geocentric_sun_right_ascension(asl, teo, glat)
        lha = solar.get_local_hour_angle(ast, lon, gsra)
        srap = solar.get_parallax_sun_right_ascension(prd, ehp, lha, gsd)
        tsd = solar.get_topocentric_sun_declination(gsd, pad, ehp, srap, lha)
        tlha = solar.get_topocentric_local_hour_angle(lha, srap)
        tza = solar.get_topocentric_zenith_angle(lat, tsd, tlha, press, temp)
        taa = solar.get_topocentric_azimuth_angle(tlha, lat, tsd)
        aoi = solar.get_incidence_angle(tza, slope, slope_orientation, taa)
        self.assertAlmostEqual(
            25.11025215046496, aoi, 6)


if __name__ == "__main__":
    SOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    TIME = unittest.defaultTestLoader.loadTestsFromTestCase(TestTime)
    GSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestGeocentricSolar)
    TSOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestTopocentricSolar)
    unittest.TextTestRunner(verbosity=2).run(TIME)
    unittest.TextTestRunner(verbosity=2).run(SOLAR)
    unittest.TextTestRunner(verbosity=2).run(GSOLAR)
    unittest.TextTestRunner(verbosity=2).run(TSOLAR)
#end if
