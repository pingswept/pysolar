import datetime
import unittest
import warnings

import numpy as np

import pysolar
from pysolar import numeric, solar
from pysolar.vectorised import get_radiation_direct_vector, get_solar_angles_vector


class TestTimezoneAwareDatetime64(unittest.TestCase):
    def setUp(self):
        pysolar.use_numpy()

    def test_numeric_tm_helpers_emit_no_timezone_warnings_and_match_math(self):
        tz_minus5 = datetime.timezone(datetime.timedelta(hours=-5))
        tz_ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        cases = [
            datetime.datetime(2024, 5, 8, 12, 45, 0, tzinfo=datetime.timezone.utc),
            # Crosses UTC midnight forward (2024-05-09 03:30 UTC)
            datetime.datetime(2024, 5, 8, 22, 30, 0, tzinfo=tz_minus5),
            # Crosses UTC midnight backward (2024-12-31 20:15 UTC)
            datetime.datetime(2025, 1, 1, 1, 45, 0, tzinfo=tz_ist),
        ]
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            for dt in cases:
                self.assertEqual(int(numeric.tm_yday_numpy(dt)), numeric.tm_yday_math(dt))
                self.assertEqual(int(numeric.tm_hour_numpy(dt)), numeric.tm_hour_math(dt))
                self.assertEqual(int(numeric.tm_min_numpy(dt)), numeric.tm_min_math(dt))

            # Fast solar helpers use tm_*_numpy under pysolar.use_numpy()
            alt = solar.get_altitude_fast(42.36, -71.11, cases[1])
            az = solar.get_azimuth_fast(42.36, -71.11, cases[1])
            self.assertTrue(np.isfinite(alt))
            self.assertTrue(np.isfinite(az))

    def test_array_and_2d_tzaware_datetimes_preserve_shape_without_warnings(self):
        tz = datetime.timezone(datetime.timedelta(hours=2))
        grid = np.array(
            [
                [
                    datetime.datetime(2024, 6, 21, 1, 15, tzinfo=tz),
                    datetime.datetime(2024, 6, 21, 14, 45, tzinfo=tz),
                ],
                [
                    datetime.datetime(2024, 12, 21, 8, 5, tzinfo=tz),
                    datetime.datetime(2024, 12, 21, 20, 55, tzinfo=tz),
                ],
            ],
            dtype=object,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            yday = numeric.tm_yday_numpy(grid)
            hour = numeric.tm_hour_numpy(grid)
            minute = numeric.tm_min_numpy(grid)
            az, zen = get_solar_angles_vector(51.48, 0.0, grid)
            rad = get_radiation_direct_vector(90.0 - zen, grid)

        self.assertEqual(yday.shape, (2, 2))
        self.assertEqual(hour.shape, (2, 2))
        self.assertEqual(minute.shape, (2, 2))
        self.assertEqual(az.shape, (2, 2))
        self.assertEqual(rad.shape, (2, 2))
        # First entry 01:15+02:00 == 23:15 UTC on 2024-06-20
        self.assertEqual(int(hour[0, 0]), 23)
        self.assertEqual(int(minute[0, 0]), 15)


if __name__ == "__main__":
    unittest.main()
