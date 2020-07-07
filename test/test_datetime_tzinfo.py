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
import unittest
from pysolar.tzinfo_check import NoTimeZoneInfoError
import numpy as np


class TestErrorTimeZoneIsNone(unittest.TestCase):
  unaware = datetime.datetime(2000, 1, 1)

  lat = 1.0
  lon = 1.0

  def test_solar_topocentric_position_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_topocentric_position(self.lat, self.lon, self.unaware)

  def test_solar_get_position_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_position(self.lat, self.lon, self.unaware)

  def test_solar_get_altitude_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_altitude(self.lat, self.lon, self.unaware)

  def test_solar_get_altitude_fast_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_altitude_fast(self.lat, self.lon, self.unaware)

  def test_solar_get_azimuth_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_azimuth(self.lat, self.lon, self.unaware)

  def test_solar_get_azimuth_fast_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_azimuth_fast(self.lat, self.lon, self.unaware)

  def test_solar_get_hour_angle_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_hour_angle(self.unaware, self.lon)

  def test_solar_get_solar_time_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solar.get_hour_angle(self.unaware, self.lon)

  def test_solartime_get_leap_seconds_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solartime.get_leap_seconds(self.unaware)

  def test_solartime_get_delta_t_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solartime.get_delta_t(self.unaware)

  def test_solartime_get_julian_solar_day_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solartime.get_julian_solar_day(self.unaware)

  def test_solartime_get_julian_ephemeris_day_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      solartime.get_julian_ephemeris_day(self.unaware)

  def test_util_get_sunrise_sunset_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.get_sunrise_sunset(self.lat, self.lon, self.unaware)

  def test_util_get_sunrise_time_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.get_sunrise_time(self.lat, self.lon, self.unaware)

  def test_util_get_sunset_time_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.get_sunset_time(self.lat, self.lon, self.unaware)

  def test_util_get_transit_time_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.get_transit_time(self.lat, self.lon, self.unaware)

  def test_util_mean_earth_sun_distance_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.mean_earth_sun_distance(self.unaware)

  def test_util_extraterrestrial_irrad_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.extraterrestrial_irrad(self.lat, self.lon, self.unaware)

  def test_util_declination_degree_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.declination_degree(self.unaware)

  def test_util_solarelevation_function_overcast_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.solarelevation_function_overcast(self.lat, self.lon, self.unaware)

  def test_util_diffuse_underclear_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.diffuse_underclear(self.lat, self.lon, self.unaware)

  def test_util_diffuse_underovercast_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.diffuse_underovercast(self.lat, self.lon, self.unaware)

  def test_util_direct_underclear_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.direct_underclear(self.lat, self.lon, self.unaware)

  def test_util_global_irradiance_clear_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.global_irradiance_clear(self.lat, self.lon, self.unaware)

  def test_util_global_irradiance_overcast_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      util.global_irradiance_overcast(self.lat, self.lon, self.unaware)

  def test_util_clear_index_raise_error(self):
    with self.assertRaises(NoTimeZoneInfoError):
      ghi_data = np.asarray([0, 0]) # Don't know what ghi_data is supposed to be
      util.clear_index(ghi_data, self.lat, self.lon, self.unaware)



class TestTimeZoneNotNone(unittest.TestCase):
  aware = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)

  lat = 1.0
  lon = 1.0

  def test_solar_topocentric_position_no_error(self):
    try:
      solar.get_topocentric_position(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solar_get_position_no_error(self):
    try:
      solar.get_position(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solar_get_altitude_no_error(self):
    try:
      solar.get_altitude(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solar_get_altitude_fast_no_error(self):
    try:
      solar.get_altitude_fast(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solar_get_azimuth_no_error(self):
    try:
      solar.get_azimuth(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solar_get_azimuth_fast_no_error(self):
    try:
      solar.get_azimuth_fast(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solar_get_hour_angle_no_error(self):
    try:
      solar.get_hour_angle(self.aware, self.lon)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solar_get_solar_time_no_error(self):
    try:
      solar.get_hour_angle(self.aware, self.lon)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solartime_get_leap_seconds_no_error(self):
    try:
      solartime.get_leap_seconds(self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solartime_get_delta_t_no_error(self):
    try:
      solartime.get_delta_t(self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solartime_get_julian_solar_day_no_error(self):
    try:
      solartime.get_julian_solar_day(self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_solartime_get_julian_ephemeris_day_no_error(self):
    try:
      solartime.get_julian_ephemeris_day(self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_get_sunrise_sunset_no_error(self):
    try:
      util.get_sunrise_sunset(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_get_sunrise_time_no_error(self):
    try:
      util.get_sunrise_time(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_get_sunset_time_no_error(self):
    try:
      util.get_sunset_time(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_mean_earth_sun_distance_no_error(self):
    try:
      util.mean_earth_sun_distance(self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_extraterrestrial_irrad_no_error(self):
    try:
      util.extraterrestrial_irrad(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_declination_degree_no_error(self):
    try:
      util.declination_degree(self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_solarelevation_function_overcast_no_error(self):
    try:
      util.solarelevation_function_overcast(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_diffuse_underclear_no_error(self):
    try:
      util.diffuse_underclear(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_diffuse_underovercast_no_error(self):
    try:
      util.diffuse_underovercast(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_direct_underclear_no_error(self):
    try:
      util.direct_underclear(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_global_irradiance_clear_no_error(self):
    try:
      util.global_irradiance_clear(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_global_irradiance_overcast_no_error(self):
    try:
      util.global_irradiance_overcast(self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")

  def test_util_clear_index(self):
    try:
      ghi_data = np.asarray([0, 0]) # Don't know what ghi_data is supposed to be
      util.clear_index(ghi_data, self.lat, self.lon, self.aware)
    except NoTimeZoneInfoError:
      self.fail("""'NoTimeZoneInfoError' should not be raised \
as 'datetime' object is tz-aware.""")
