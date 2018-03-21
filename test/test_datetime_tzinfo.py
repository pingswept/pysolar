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

"""This test file makes sure that every function that requires 
'datetime.datetime' objects as parameters 
receives only timezone-aware ones.
"""

from pysolar import solar
from pysolar import solartime
from pysolar import util
import datetime
import pytz
import unittest
from pysolar.tzinfo_check import NoTimeZoneInfoError


class TestTimeZone(unittest.TestCase):
  unaware = datetime.datetime(2000, 1, 1)
  aware = unaware.replace(tzinfo=pytz.utc)

  lat = 0.0
  lon = 0.0

  def test_solar_topocentric_position(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_topocentric_position(self.lat, self.lon, self.unaware)

  def test_solar_get_position(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_position(self.lat, self.lon, self.unaware)

  def test_solar_get_altitude(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_altitude(self.lat, self.lon, self.unaware)

  def test_solar_get_altitude_fast(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_altitude_fast(self.lat, self.lon, self.unaware)

  def test_solar_get_azimuth(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_azimuth(self.lat, self.lon, self.unaware)

  def test_solar_get_azimuth_fast(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_azimuth_fast(self.lat, self.lon, self.unaware)

  def test_solar_get_hour_angle(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_hour_angle(self.unaware, self.lon)

  def test_solar_get_solar_time(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_hour_angle(self.unaware, self.lon)

  def test_solartime_get_leap_seconds(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solartime.get_leap_seconds(self.unaware)

  def test_solartime_get_delta_t(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solartime.get_delta_t(self.unaware)

  def test_solartime_get_julian_solar_day(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solartime.get_julian_solar_day(self.unaware)

  def test_solartime_get_julian_ephemeris_day(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solartime.get_julian_ephemeris_day(self.unaware)

  def test_util_get_sunrise_sunset(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.get_sunrise_sunset(self.lat, self.lon, self.unaware)

  def test_util_get_sunrise_time(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.get_sunrise_time(self.lat, self.lon, self.unaware)

  def test_util_get_sunset_time(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.get_sunset_time(self.lat, self.lon, self.unaware)

  def test_util_mean_earth_sun_distance(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.mean_earth_sun_distance(self.unaware)

  def test_util_extraterrestrial_irrad(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.extraterrestrial_irrad(self.lat, self.lon, self.unaware)

  def test_util_declination_degree(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.declination_degree(self.unaware)

  def test_util_solarelevation_function_overcast(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.solarelevation_function_overcast(self.lat, self.lon, self.unaware)

  def test_util_diffuse_underclear(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.diffuse_underclear(self.lat, self.lon, self.unaware)

  def test_util_diffuse_underovercast(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.diffuse_underovercast(self.lat, self.lon, self.unaware)

  def test_util_direct_underclear(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.direct_underclear(self.lat, self.lon, self.unaware)

  def test_util_global_irradiance_clear(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.global_irradiance_clear(self.lat, self.lon, self.unaware)

  def test_util_global_irradiance_overcast(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.global_irradiance_overcast(self.lat, self.lon, self.unaware)

  def test_util_clear_index(self):
    with self.assertRaises(NoTimeZoneInfoError):
      ghi_data = Ellipsis # Don't know what ghi_data is supposed to be
      util.clear_index(ghi_data, self.lat, self.lon, self.unaware)