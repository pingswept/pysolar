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
 # R0902: Too many instance attributes 7 is recommended
 # R0904: Too many public methods 20 is recommended
class TestSolar(unittest.TestCase):
    """ Test solar and time methods """
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

        self.jsd = time.get_julian_solar_day(self.dio) - self.lon_offset

        self.nut = solar.get_nutation(self.jsd)

        self.jed = time.get_julian_ephemeris_day(self.dio)
        self.jec = time.get_julian_ephemeris_century(self.jed)
        self.jem = time.get_julian_ephemeris_millennium(self.jec)
        self.geo_lon = solar.get_geocentric_longitude(self.jem)
        self.geo_lat = solar.get_geocentric_latitude(self.jem)

        self.ast = solar.get_apparent_sidereal_time(self.jsd, self.jem, self.nut)
        self.sed = solar.get_sun_earth_distance(self.jem)
        self.teo = solar.get_true_ecliptic_obliquity(self.jem, self.nut)
        self.gac = solar.get_aberration_correction(self.sed)
        self.asl = solar.get_apparent_sun_longitude(self.geo_lon, self.nut, self.gac)
        self.gsra = solar.get_geocentric_sun_right_ascension(self.asl, self.teo, self.geo_lat)
        self.gsd = solar.get_geocentric_sun_declination(self.asl, self.teo, self.geo_lat)
        self.lha = solar.get_local_hour_angle(318.5119, self.longitude, self.gsra)
            #self.apparent_sidereal_time only correct to 5 sig figs, so override
        self.ehp = solar.get_equatorial_horizontal_parallax(self.sed)
        self.prd = solar.get_projected_radial_distance(self.elevation, self.latitude)
        self.srap = solar.get_parallax_sun_right_ascension(self.prd, self.ehp, self.lha, self.gsd)
        self.tlha = solar.get_topocentric_local_hour_angle(self.lha, self.srap)
        self.pad = solar.get_projected_axial_distance(self.elevation, self.latitude)
        self.tsd = solar.get_topocentric_sun_declination(
            self.gsd, self.pad, self.ehp, self.srap, self.lha)

        self.tsra = solar.get_topocentric_sun_right_ascension(
            self.prd, self.ehp, self.lha, self.asl, self.teo, self.geo_lat)

        self.tlha = solar.get_topocentric_local_hour_angle(self.lha, self.srap)
        self.taa = solar.get_topocentric_azimuth_angle(self.tlha, self.latitude, self.tsd)
        self.pwe = elevation.get_pressure_with_elevation(1567.7)
        self.twe = elevation.get_temperature_with_elevation(1567.7)

        self.tza = solar.get_topocentric_zenith_angle(
            self.latitude, self.tsd, self.tlha, self.pressure, self.temperature)

        self.aoi = solar.get_incidence_angle(
            self.tza, self.slope, self.slope_orientation, self.taa)

    def test_get_ac(self):
        """
        MIDC SPA is -0.005711 at 12:30
        """
        self.assertAlmostEqual(-0.005711359813021086, self.gac, 6)

    def test_get_aoi(self):
        """
        MIDC SPA is 25.108613 at 12:30
        """
        self.assertAlmostEqual(25.18706694022789, self.aoi, 6)

    def test_get_ast(self):
        """
        MIDC SPA is 318.388061 at 12:30
        """
        self.assertAlmostEqual(63.857289471120964, self.ast, 6)

    def test_get_asl(self):
        """
        MIDC SPA is 204.008183 at 12:30
        """
        # 204.00818592528472 below
        self.assertAlmostEqual(204.0085537528, self.asl, 10)
        self.assertAlmostEqual(204.008183, self.asl, 4)

    def test_get_dut1(self):
        """
        see DUT1 http://asa.usno.navy.mil/SecM/Glossary.html#ut1
        datetime.timedelta(0, 0, 357500)
        MIDC SPA is set to 0.3575 sec DUT1
        """
        self.assertEqual(datetime.timedelta(0, 0, 357500), self.dut1)

    def test_get_glat(self):
        """
        MIDC SPA is 0.000101 at 12:30
        """
        self.assertAlmostEqual(0.00010111493548486615, self.geo_lat, 6)

    def test_get_glon(self):
        """
        MIDC SPA is 204.017893 at 12:30
        """
        self.assertAlmostEqual(204.01789072656447, self.geo_lon, 6)

    def test_get_gsd(self):
        """
        MIDC SPA is -9.314204 at 12:30
        """
        self.assertAlmostEqual(-9.314205693497897, self.gsd, 6)

    def test_get_gsra(self):
        """
        MIDC SPA is 202.227060 at 12:30
        """
        self.assertAlmostEqual(202.2270628443805, self.gsra, 6)

    def test_get_jct(self):
        """
        MIDC SPA is 0.037928 at 12:30
        """
        self.assertAlmostEqual(0.037935788166402626, time.get_julian_century(self.jsd), 6)

    def test_get_jec(self):
        """
        MIDC SPA is 0.037928 at 12:30
        """
        self.assertAlmostEqual(0.0379278191438864, self.jec, 6)

    def test_get_jed(self):
        """
        MIDC SPA is 2452930.313251 at 12:30
        """
        self.assertAlmostEqual(2452930.3132470082, self.jed, 6)

    def test_get_jem(self):
        """
        MIDC SPA is 0.003793 at 12:30
        """
        self.assertAlmostEqual(0.003792780963746062, self.jem, 6)

    def test_get_jsd(self):
        """
        MIDC SPA is 2452930.604171 at 19:30
        """
        self.assertAlmostEqual(2452930.604662778, self.jsd, 6)

    def test_get_lha(self):
        """
        MIDC SPA is 10.982401 at 12:30
        """
        self.assertAlmostEqual(11.10623715561951, self.lha, 6)

    def test_get_nut(self):
        """
        MIDC SPA is 0.001667 at 12:30
        MIDC SPA is -0.003998 at 12:30
        """
        self.assertAlmostEqual(0.0016675503502552294, self.nut['obliquity'], 6)
        self.assertAlmostEqual(-0.003993441466726428, self.nut['longitude'], 6)

    def test_get_prd(self):
        """
        MIDC SPA is not at 12:30
        """
        self.assertAlmostEqual(0.7702006191191089, self.prd, 6)

    def test_get_pwe(self):
        """
        MIDC SPA is not at 12:30
        """
        self.assertAlmostEqual(83855.90227687225, self.pwe, 6)

    def test_get_sed(self):
        """
        MIDC SPA is 0.996542 at 12:30
        """
        self.assertAlmostEqual(0.9965421031, self.sed, 6)

    def test_get_srap(self):
        """ MIDC SPA is -0.000364 at 12:30 """
        self.assertAlmostEqual(-0.0003659911495454668, self.srap, 6)

    def test_get_taa(self):
        """
        MIDC SPA is 194.184400 at 12:30
        """
        # self.assertAlmostEqual(194.34024, self.topocentric_azimuth_angle, 5)
        self.assertAlmostEqual(194.34071016096647, self.taa, 6)

    def test_get_teo(self):
        """
        MIDC SPA is 23.440465 at 12:30
        """
        self.assertAlmostEqual(23.440465501924272, self.teo, 6)

    def test_get_tlha(self):
        """
        MIDC SPA is 10.982765 at 12:30
        """
        self.assertAlmostEqual(11.106603157089864, self.tlha, 6)

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

    def test_get_tsd(self):
        """
        MIDC SPA is -9.316043 at 12:30
        """
        self.assertAlmostEqual(-9.315979753419532, self.tsd, 6)

    def test_get_tsra(self):
        """
        MIDC SPA is 202.226696 at 12:30
        """
        self.assertAlmostEqual(202.22669684291014, self.tsra, 6)

    def test_get_twe(self):
        """
        MIDC SPA is not at 12:30
        """
        self.assertAlmostEqual(277.95995, self.twe, 6)

    def test_get_tza(self):
        """
        MIDC SPA is 50.088106 at 12:30
        """
        self.assertAlmostEqual(50.111498860710185, self.tza, 6)

class TestTime(unittest.TestCase):
    """ Test time methods """
    def setUp(self):
        # time at MIDC SPA https://www.nrel.gov/midc/solpos/spa.html
        # has no seconds setting so let's consider new test data.
        # changing the docstring to values found in MIDC SPA for expectation tests.
        self.dio = datetime.datetime(2003, 10, 17, 19, 30, 0, tzinfo=datetime.timezone.utc)
        self.dut1 = datetime.timedelta(seconds=time.get_delta_t(
            self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))
        self.dio += datetime.timedelta(seconds=time.get_delta_t(
            self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))

    def test_get_ajd(self):
        """
        MIDC SPA is 2452930.312504 at 12:30
        """
        self.assertAlmostEqual(2452930.3125, time.ajd(self.dio), 6)

    def test_get_jdn(self):
        """
        MIDC SPA is 2452930
        """
        self.assertEqual(2452930, time.jdn(self.dio))

if __name__ == "__main__":
    SOLAR = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    TIME = unittest.defaultTestLoader.loadTestsFromTestCase(TestTime)
    unittest.TextTestRunner(verbosity=2).run(TIME)
    unittest.TextTestRunner(verbosity=2).run(SOLAR)
#end if
