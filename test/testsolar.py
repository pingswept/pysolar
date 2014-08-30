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

from pysolar import \
	solar, \
	constants, \
	time, \
	elevation
import datetime
import unittest

class testSolar(unittest.TestCase):

	def setUp(self):
		self.d = datetime.datetime(2003, 10, 17, 19, 30, 30, tzinfo = datetime.timezone.utc)
		self.d += datetime.timedelta(seconds = time.get_delta_t(self.d) - time.tt_offset - time.get_leap_seconds(self.d))
		  # Reda & Andreas say that this time is in “Local Standard Time”, which they
		  # define as 7 hours behind UT (not UTC). Hence the adjustment to convert UT
		  # to UTC.
		self.longitude = -105.1786
		self.latitude = 39.742476
		self.pressure = 82000.0 # pascals
		self.elevation = 1830.14 # meters
		self.temperature = 11.0 + constants.celsius_offset # kelvin
		self.slope = 30.0 # degrees
		self.slope_orientation = -10.0 # degrees east from south
		self.jd = time.get_julian_solar_day(self.d)
		self.jc = time.get_julian_century(self.jd)
		self.jde = time.get_julian_ephemeris_day(self.d)
		self.jce = time.get_julian_ephemeris_century(self.jde)
		self.jme = time.get_julian_ephemeris_millennium(self.jce)
		self.geocentric_longitude = solar.get_geocentric_longitude(self.jme)
		self.geocentric_latitude = solar.get_geocentric_latitude(self.jme)
		self.nutation = solar.get_nutation(self.jce)
		self.sun_earth_distance = solar.get_sun_earth_distance(self.jme)
		self.true_ecliptic_obliquity = solar.get_true_ecliptic_obliquity(self.jme, self.nutation)
		self.aberration_correction = solar.get_aberration_correction(self.sun_earth_distance)
		self.apparent_sun_longitude = solar.get_apparent_sun_longitude(self.geocentric_longitude, self.nutation, self.aberration_correction)
		self.apparent_sidereal_time = solar.get_apparent_sidereal_time(self.jd, self.jme, self.nutation)
		self.geocentric_sun_right_ascension = solar.get_geocentric_sun_right_ascension(self.apparent_sun_longitude, self.true_ecliptic_obliquity, self.geocentric_latitude)
		self.geocentric_sun_declination = solar.get_geocentric_sun_declination(self.apparent_sun_longitude, self.true_ecliptic_obliquity, self.geocentric_latitude)
		self.local_hour_angle = solar.get_local_hour_angle(318.5119, self.longitude, self.geocentric_sun_right_ascension) #self.apparent_sidereal_time only correct to 5 sig figs, so override
		self.equatorial_horizontal_parallax = solar.get_equatorial_horizontal_parallax(self.sun_earth_distance)
		self.projected_radial_distance = solar.get_projected_radial_distance(self.elevation, self.latitude)
		self.projected_axial_distance = solar.get_projected_axial_distance(self.elevation, self.latitude)
		self.topocentric_sun_right_ascension = solar.get_topocentric_sun_right_ascension(self.projected_radial_distance,
		self.equatorial_horizontal_parallax, self.local_hour_angle, self.apparent_sun_longitude, self.true_ecliptic_obliquity, self.geocentric_latitude)
		self.parallax_sun_right_ascension = solar.get_parallax_sun_right_ascension(self.projected_radial_distance, self.equatorial_horizontal_parallax, self.local_hour_angle, self.geocentric_sun_declination)
		self.topocentric_sun_declination = solar.get_topocentric_sun_declination(self.geocentric_sun_declination, self.projected_axial_distance, self.equatorial_horizontal_parallax, self.parallax_sun_right_ascension, self.local_hour_angle)
		self.topocentric_local_hour_angle = solar.get_topocentric_local_hour_angle(self.local_hour_angle, self.parallax_sun_right_ascension)
		self.topocentric_zenith_angle = solar.get_topocentric_zenith_angle(self.latitude, self.topocentric_sun_declination, self.topocentric_local_hour_angle, self.pressure, self.temperature)
		self.topocentric_azimuth_angle = solar.get_topocentric_azimuth_angle(self.topocentric_local_hour_angle, self.latitude, self.topocentric_sun_declination)
		self.incidence_angle = solar.get_incidence_angle(self.topocentric_zenith_angle, self.slope, self.slope_orientation, self.topocentric_azimuth_angle)
		self.pressure_with_elevation = elevation.get_pressure_with_elevation(1567.7)
		self.temperature_with_elevation = elevation.get_temperature_with_elevation(1567.7)

	def test_get_julian_solar_day(self):
		self.assertAlmostEqual(2452930.312847, self.jd, 6) # value from Reda and Andreas (2005)

	def test_get_julian_ephemeris_day(self):
		self.assertAlmostEqual(2452930.3136, self.jde, 4) # value not validated

	def test_get_julian_century(self):
		self.assertAlmostEqual(0.03792779869191517, self.jc, 12) # value not validated

	def test_get_julian_ephemeris_millennium(self):
		self.assertAlmostEqual(0.0037927819143886397, self.jme, 12) # value not validated

	def test_get_geocentric_longitude(self):
		# self.assertAlmostEqual(204.0182635175, self.geocentric_longitude, 10) # value from Reda and Andreas (2005)
		self.assertAlmostEqual(204.0182635175, self.geocentric_longitude, 4) # above fails with more accurate Julian Ephemeris correction

	def test_get_geocentric_latitude(self):
		# self.assertAlmostEqual(0.0001011219, self.geocentric_latitude, 9) # value from Reda and Andreas (2005)
		self.assertAlmostEqual(0.0001011219, self.geocentric_latitude, 8) # above fails with more accurate Julian Ephemeris correction

	def test_get_nutation(self):
		self.assertAlmostEqual(0.00166657, self.nutation['obliquity'], 8) # value from Reda and Andreas (2005)
		self.assertAlmostEqual(-0.00399840, self.nutation['longitude'], 8) # value from Reda and Andreas (2005)

	def test_get_sun_earth_distance(self):
		self.assertAlmostEqual(0.9965421031, self.sun_earth_distance, 7) # value from Reda and Andreas (2005)

	def test_get_true_ecliptic_obliquity(self):
		self.assertAlmostEqual(23.440465, self.true_ecliptic_obliquity, 6) # value from Reda and Andreas (2005)

	def test_get_aberration_correction(self):
		self.assertAlmostEqual(-0.0057113603, self.aberration_correction, 9) # value not validated

	def test_get_apparent_sun_longitude(self):
		# self.assertAlmostEqual(204.0085537528, self.apparent_sun_longitude, 10) # value from Reda and Andreas (2005)
		self.assertAlmostEqual(204.0085537528, self.apparent_sun_longitude, 4) # above fails with more accurate Julian Ephemeris correction

	def test_get_apparent_sidreal_time(self):
		self.assertAlmostEqual(318.5119, self.apparent_sidereal_time, 2) # value derived from Reda and Andreas (2005)

	def test_get_geocentric_sun_right_ascension(self):
		self.assertAlmostEqual(202.22741, self.geocentric_sun_right_ascension, 4) # value from Reda and Andreas (2005)

	def test_get_geocentric_sun_declination(self):
		self.assertAlmostEqual(-9.31434, self.geocentric_sun_declination, 4) # value from Reda and Andreas (2005)

	def test_get_local_hour_angle(self):
		self.assertAlmostEqual(11.105900, self.local_hour_angle, 4) # value from Reda and Andreas (2005)

	def test_get_projected_radial_distance(self):
		self.assertAlmostEqual(0.7702006, self.projected_radial_distance, 6) # value not validated

	def test_get_topocentric_sun_right_ascension(self):
		self.assertAlmostEqual(202.22741, self.topocentric_sun_right_ascension, 3) # value from Reda and Andreas (2005)

	def test_get_parallax_sun_right_ascension(self):
		self.assertAlmostEqual(-0.0003659911495454668, self.parallax_sun_right_ascension, 12) # value not validated
		
	def test_get_topocentric_sun_declination(self):
		self.assertAlmostEqual(-9.316179, self.topocentric_sun_declination, 3) # value from Reda and Andreas (2005)

	def test_get_topocentric_local_hour_angle(self):
		self.assertAlmostEqual(11.10629, self.topocentric_local_hour_angle, 4) # value from Reda and Andreas (2005)

	def test_get_topocentric_zenith_angle(self):
		self.assertAlmostEqual(50.11162, self.topocentric_zenith_angle, 3) # value from Reda and Andreas (2005)

	def test_get_topocentric_azimuth_angle(self):
		# self.assertAlmostEqual(194.34024, self.topocentric_azimuth_angle, 5) # value from Reda and Andreas (2005)
		self.assertAlmostEqual(194.34024, self.topocentric_azimuth_angle, 4) # above fails with more accurate Julian Ephemeris correction

	def test_get_incidence_angle(self):
		self.assertAlmostEqual(25.18700, self.incidence_angle, 3) # value from Reda and Andreas (2005)

	def testPressureWithElevation(self):
		self.assertAlmostEqual(83855.90228, self.pressure_with_elevation, 4)

	def testTemperatureWithElevation(self):
		self.assertAlmostEqual(277.9600, self.temperature_with_elevation, 4)


if __name__ == "__main__":
	suite = unittest.defaultTestLoader.loadTestsFromTestCase(testSolar)
	unittest.TextTestRunner(verbosity=2).run(suite)
#end if
