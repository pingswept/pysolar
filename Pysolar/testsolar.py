#!/usr/bin/python

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

from . import solar
from . import constants
from . import julian
from . import elevation
import datetime
import unittest

class testSolar(unittest.TestCase):

	def setUp(self):
		self.d = datetime.datetime(2003, 10, 17, 19, 30, 30)
		self.longitude = -105.1786
		self.latitude = 39.742476
		self.pressure = 820.0 # millibars
		self.elevation = 1830.14 # meters
		self.temperature = 11.0 # degrees Celsius
		self.slope = 30.0 # degrees
		self.slope_orientation = -10.0 # degrees east from south
		self.jd = julian.GetJulianDay(self.d)
		self.jc = julian.GetJulianCentury(self.jd)
		self.jde = julian.GetJulianEphemerisDay(self.jd, 67.0)
		self.jce = julian.GetJulianEphemerisCentury(self.jde)
		self.jme = julian.GetJulianEphemerisMillenium(self.jce)
		self.geocentric_longitude = solar.GetGeocentricLongitude(self.jme)
		self.geocentric_latitude = solar.GetGeocentricLatitude(self.jme)
		self.nutation = solar.GetNutation(self.jde)
		self.radius_vector = solar.GetRadiusVector(self.jme)
		self.true_ecliptic_obliquity = solar.GetTrueEclipticObliquity(self.jme, self.nutation)
		self.aberration_correction = solar.GetAberrationCorrection(self.radius_vector)
		self.apparent_sun_longitude = solar.GetApparentSunLongitude(self.geocentric_longitude, self.nutation, self.aberration_correction)
		self.apparent_sidereal_time = solar.GetApparentSiderealTime(self.jd, self.jme, self.nutation)
		self.geocentric_sun_right_ascension = solar.GetGeocentricSunRightAscension(self.apparent_sun_longitude, self.true_ecliptic_obliquity, self.geocentric_latitude)
		self.geocentric_sun_declination = solar.GetGeocentricSunDeclination(self.apparent_sun_longitude, self.true_ecliptic_obliquity, self.geocentric_latitude)
		self.local_hour_angle = solar.GetLocalHourAngle(318.5119, self.longitude, self.geocentric_sun_right_ascension) #self.apparent_sidereal_time only correct to 5 sig figs, so override
		self.equatorial_horizontal_parallax = solar.GetEquatorialHorizontalParallax(self.radius_vector)
		self.projected_radial_distance = solar.GetProjectedRadialDistance(self.elevation, self.latitude)
		self.projected_axial_distance = solar.GetProjectedAxialDistance(self.elevation, self.latitude)
		self.topocentric_sun_right_ascension = solar.GetTopocentricSunRightAscension(self.projected_radial_distance,
		self.equatorial_horizontal_parallax, self.local_hour_angle, self.apparent_sun_longitude, self.true_ecliptic_obliquity, self.geocentric_latitude)
		self.parallax_sun_right_ascension = solar.GetParallaxSunRightAscension(self.projected_radial_distance, self.equatorial_horizontal_parallax, self.local_hour_angle, self.geocentric_sun_declination)
		self.topocentric_sun_declination = solar.GetTopocentricSunDeclination(self.geocentric_sun_declination, self.projected_axial_distance, self.equatorial_horizontal_parallax, self.parallax_sun_right_ascension, self.local_hour_angle)
		self.topocentric_local_hour_angle = solar.GetTopocentricLocalHourAngle(self.local_hour_angle, self.parallax_sun_right_ascension)
		self.topocentric_zenith_angle = solar.GetTopocentricZenithAngle(self.latitude, self.topocentric_sun_declination, self.topocentric_local_hour_angle, self.pressure, self.temperature)
		self.topocentric_azimuth_angle = solar.GetTopocentricAzimuthAngle(self.topocentric_local_hour_angle, self.latitude, self.topocentric_sun_declination)
		self.incidence_angle = solar.GetIncidenceAngle(self.topocentric_zenith_angle, self.slope, self.slope_orientation, self.topocentric_azimuth_angle)
		self.pressure_with_elevation = elevation.GetPressureWithElevation(1567.7)
		self.temperature_with_elevation = elevation.GetTemperatureWithElevation(1567.7)

	def testGetJulianDay(self):
		self.assertAlmostEqual(2452930.312847, self.jd, 6) # value from Reda and Andreas (2005)

	def testGetJulianEphemerisDay(self):
		self.assertAlmostEqual(2452930.3136, self.jde, 4) # value not validated

	def testGetJulianCentury(self):
		self.assertAlmostEqual(0.03792779869191517, self.jc, 12) # value not validated

	def testGetJulianEphemerisMillenium(self):
		self.assertAlmostEqual(0.0037927819922933584, self.jme, 12) # value not validated

	def testGetGeocentricLongitude(self):
		self.assertAlmostEqual(204.0182635175, self.geocentric_longitude, 10) # value from Reda and Andreas (2005)

	def testGetGeocentricLatitude(self):
		self.assertAlmostEqual(0.0001011219, self.geocentric_latitude, 9) # value from Reda and Andreas (2005)

	def testGetNutation(self):
		self.assertAlmostEqual(0.00166657, self.nutation['obliquity'], 8) # value from Reda and Andreas (2005)
		self.assertAlmostEqual(-0.00399840, self.nutation['longitude'], 8) # value from Reda and Andreas (2005)

	def testGetRadiusVector(self):
		self.assertAlmostEqual(0.9965421031, self.radius_vector, 7) # value from Reda and Andreas (2005)

	def testGetTrueEclipticObliquity(self):
		self.assertAlmostEqual(23.440465, self.true_ecliptic_obliquity, 6) # value from Reda and Andreas (2005)

	def testGetAberrationCorrection(self):
		self.assertAlmostEqual(-0.0057113603, self.aberration_correction, 9) # value not validated

	def testGetApparentSunLongitude(self):
		self.assertAlmostEqual(204.0085537528, self.apparent_sun_longitude, 10) # value from Reda and Andreas (2005)

	def testGetApparentSiderealTime(self):
		self.assertAlmostEqual(318.5119, self.apparent_sidereal_time, 2) # value derived from Reda and Andreas (2005)

	def testGetGeocentricSunRightAscension(self):
		self.assertAlmostEqual(202.22741, self.geocentric_sun_right_ascension, 4) # value from Reda and Andreas (2005)

	def testGetGeocentricSunDeclination(self):
		self.assertAlmostEqual(-9.31434, self.geocentric_sun_declination, 4) # value from Reda and Andreas (2005)

	def testGetLocalHourAngle(self):
		self.assertAlmostEqual(11.105900, self.local_hour_angle, 4) # value from Reda and Andreas (2005)

	def testGetProjectedRadialDistance(self):
		self.assertAlmostEqual(0.7702006, self.projected_radial_distance, 6) # value not validated

	def testGetTopocentricSunRightAscension(self):
		self.assertAlmostEqual(202.22741, self.topocentric_sun_right_ascension, 3) # value from Reda and Andreas (2005)

	def testGetParallaxSunRightAscension(self):
		self.assertAlmostEqual(-0.00036599029186055283, self.parallax_sun_right_ascension, 12) # value not validated
		
	def testGetTopocentricSunDeclination(self):
		self.assertAlmostEqual(-9.316179, self.topocentric_sun_declination, 3) # value from Reda and Andreas (2005)

	def testGetTopocentricLocalHourAngle(self):
		self.assertAlmostEqual(11.10629, self.topocentric_local_hour_angle, 4) # value from Reda and Andreas (2005)

	def testGetTopocentricZenithAngle(self):
		self.assertAlmostEqual(50.11162, self.topocentric_zenith_angle, 3) # value from Reda and Andreas (2005)

	def testGetTopocentricAzimuthAngle(self):
		self.assertAlmostEqual(194.34024, self.topocentric_azimuth_angle, 5) # value from Reda and Andreas (2005)

	def testGetIncidenceAngle(self):
		self.assertAlmostEqual(25.18700, self.incidence_angle, 3) # value from Reda and Andreas (2005)

	def testPressureWithElevation(self):
		self.assertAlmostEqual(83855.90228, self.pressure_with_elevation, 4)

	def testTemperatureWithElevation(self):
		self.assertAlmostEqual(277.9600, self.temperature_with_elevation, 4)

suite = unittest.TestLoader().loadTestsFromTestCase(testSolar)
unittest.TextTestRunner(verbosity=2).run(suite)

# if __name__ == "__main__":
#	unittest.main()

