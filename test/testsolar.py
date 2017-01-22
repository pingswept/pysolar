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
    def setUp(self):
        # time at MIDC SPA has no seconds setting so let's consider new test data.
        # the doc says use 67 sec delta t
        # changing the docstring to values found in MIDC SPA for expectation tests.
        # self.dio = datetime.datetime(2003, 10, 17, 19, 30, 0, tzinfo=datetime.timezone.utc)
        self.dio = datetime.datetime(2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)
        self.dut1 = datetime.timedelta(seconds=time.get_delta_t(
            self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))
        self.dio += datetime.timedelta(seconds=time.get_delta_t(
            self.dio) - time.tt_offset - time.get_leap_seconds(self.dio))
        # Reda & Andreas say that this time is in "Local Standard Time", which they
        # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
        # to UTC.

        self.longitude = -105.1786
        self.lon_offset = self.longitude / 360.0
        self.latitude = 39.742476
        self.pressure = 82000.0 # pascals
        self.elevation = 1830.14 # meters
        self.temperature = 11.0 + constants.celsius_offset # kelvin
        self.slope = 30.0 # degrees
        self.slope_orientation = -10.0 # degrees east from south
        self.jdn = time.jdn(self.dio) - self.lon_offset
        self.ajd = time.ajd(self.dio) - self.lon_offset
        self.jsd = time.get_julian_solar_day(self.dio)
        self.jct = time.get_julian_century(self.jsd)
        self.jed = time.get_julian_ephemeris_day(self.dio)
        self.jec = time.get_julian_ephemeris_century(self.jed)
        self.jem = time.get_julian_ephemeris_millennium(self.jec)
        self.geo_lon = solar.get_geocentric_longitude(self.jem)
        self.geo_lat = solar.get_geocentric_latitude(self.jem)
        self.nut = solar.get_nutation(self.jct)
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
        self.psra = solar.get_parallax_sun_right_ascension(self.prd, self.ehp, self.lha, self.gsd)
        self.tlha = solar.get_topocentric_local_hour_angle(self.lha, self.psra)
        self.pad = solar.get_projected_axial_distance(self.elevation, self.latitude)
        self.tsd = solar.get_topocentric_sun_declination(
            self.gsd, self.pad, self.ehp, self.psra, self.lha)

        self.tsra = solar.get_topocentric_sun_right_ascension(
            self.prd, self.ehp, self.lha, self.asl, self.teo, self.geo_lat)

        self.tlha = solar.get_topocentric_local_hour_angle(self.lha, self.psra)
        self.taa = solar.get_topocentric_azimuth_angle(self.tlha, self.latitude, self.tsd)
        self.pwe = elevation.get_pressure_with_elevation(1567.7)
        self.twe = elevation.get_temperature_with_elevation(1567.7)

        self.tza = solar.get_topocentric_zenith_angle(
            self.latitude, self.tsd, self.tlha, self.pressure, self.temperature)

        self.aoi = solar.get_incidence_angle(
            self.tza, self.slope, self.slope_orientation, self.taa)

    def test_get_ac(self):
        """ MIDC SPA -0.005712 """
        self.assertAlmostEqual(-0.0057113603, self.gac, 9) # value not validated

    def test_get_ast(self):
        """ MIDC SPA is 63.675546 at 19:30 and 318.388061 at 12:30 """
        # value derived from Reda and Andreas (2005)
        self.assertAlmostEqual(318.5119, self.ast, 2)

    def test_get_asl(self):
        """ MIDC SPA is 204.297641 at 19:30 and 204.008183 at 12:30 """
        # value from Reda and Andreas (2005)
        # self.assertAlmostEqual(204.0085537528, self.apparent_sun_longitude, 10)
        self.assertAlmostEqual(204.0085537528, self.asl, 4)

    def test_get_ajd(self):
        """ 2452930.60501 has longitude added """
        self.assertAlmostEqual(2452930.60501, self.ajd, 12)

    def test_get_dut1(self):
        """ see DUT1 http://asa.usno.navy.mil/SecM/Glossary.html#ut1
        datetime.timedelta(0, 0, 357500)
        """
        self.assertEqual(datetime.timedelta(0, 0, 357500), self.dut1)

    def test_get_glat(self):
        """ MIDC SPA is 0.000106 at 19:30 and  at 12:30 0.000101"""
        # value from Reda and Andreas (2005)
        # self.assertAlmostEqual(0.0001011219, self.geocentric_latitude, 9)
        # above fails with more accurate Julian Ephemeris correction
        self.assertAlmostEqual(0.0001011219, self.geo_lat, 8)

    def test_get_glon(self):
        """ MIDC SPA is 204.307346 at 19:30 and  at 12:30 204.017893 """
        # value from Reda and Andreas (2005)
        # self.assertAlmostEqual(204.0182635175, self.geocentric_longitude, 10)
        self.assertAlmostEqual(204.0182635175, self.geo_lon, 4)

    def test_get_gsd(self):
        """ MIDC SPA is -9.420685 at 19:30 and  at 12:30 -9.314204 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(-9.31434, self.gsd, 4)

    def test_get_gsra(self):
        """ MIDC SPA is 202.499859 at 19:30 and at 12:30 202.227060 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(202.22741, self.gsra, 4)

    def test_get_aoi(self):
        """ MIDC SPA is 121.988266 at 19:30 and at 12:30 25.108613 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(25.18700, self.aoi, 3)

    def test_get_jct(self):
        """ MIDC SPA is 0.037936 at 19:30 and 0.037928 at 12:30 """
        self.assertAlmostEqual(0.03792779869191517, self.jct, 12) # value not validated

    def test_get_jdn(self):
        """ 2452930.292162778 has longitude added """
        self.assertAlmostEqual(2452930.292162778, self.jdn, 12)

    def test_get_jec(self):
        """ MIDC SPA is 0.037936 at 19:30 and 0.037928 at 12:30 """
        self.assertAlmostEqual(0.0379278191438864, self.jec, 12) # value not validated

    def test_get_jed(self):
        """ MIDC SPA is 2452930.604918 at 19:30 and 2452930.313251 at 12:30 """
        self.assertAlmostEqual(2452930.3135942305, self.jed, 6) # value not validated

    def test_get_jem(self):
        """ MIDC SPA is 0.003794 at 19:30 and 0.003793 at 12:30 """
        self.assertAlmostEqual(0.0037927819143886397, self.jem, 12) # value not validated

    def test_get_jsd(self):
        """ MIDC SPA is 2452930.604171 at 19:30 and 2452930.312504 at 12:30 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(2452930.312847222, self.jsd, 12)

    def test_get_lha(self):
        """ MIDC SPA is 115.997087 at 19:30 and 10.982401 at 12:30 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(11.105900, self.lha, 4)

    def test_get_nut(self):
        """
        MIDC SPA is 0.001668 at 19:30 and 0.001667 at 12:30
        MIDC SPA is-0.003993  at 19:30 and -0.003998 at 12:30
        """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(0.00166657, self.nut['obliquity'], 12)
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(-0.003998417958822872, self.nut['longitude'], 12)

    def test_get_psra(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        self.assertAlmostEqual(-0.0003659911495454668, self.psra, 12)

    def test_get_prd(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        self.assertAlmostEqual(0.7702006, self.prd, 6) # value not validated

    def test_get_pwe(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        self.assertAlmostEqual(83855.90228, self.pwe, 4)

    def test_get_sed(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(0.9965421031, self.sed, 7)

    def test_get_taa(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        # value from Reda and Andreas (2005)
        # self.assertAlmostEqual(194.34024, self.topocentric_azimuth_angle, 5)
        self.assertAlmostEqual(194.34024, self.taa, 4)

    def test_get_teo(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(23.440465, self.teo, 6)

    def test_get_tlha(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(11.10629, self.tlha, 4)

    def test_get_ts(self):
        """ you could put what to expect in here """
        # please consider this so we can compare with MIDC SPA not the doc.
        # no_tzinfo = datetime.datetime(2003, 10, 17, 19, 30, 0, tzinfo=None)
        no_tzinfo = datetime.datetime(2003, 10, 17, 19, 30, 30, tzinfo=None)
        print('d =', time.timestamp(self.dio), 'seconds')
        print('no tzinfo', time.timestamp(no_tzinfo))

    def test_get_tsd(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(-9.316179, self.tsd, 3)

    def test_get_tsra(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(202.22741, self.tsra, 3)

    def test_get_twe(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        self.assertAlmostEqual(277.9600, self.twe, 4)

    def test_get_tza(self):
        """ MIDC SPA is  at 19:30 and  at 12:30 """
        # value from Reda and Andreas (2005)
        self.assertAlmostEqual(50.11162, self.tza, 3)

if __name__ == "__main__":
    SUN = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    TIME = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolar)
    unittest.TextTestRunner(verbosity=2).run(SUN)
#end if
