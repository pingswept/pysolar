import datetime
import unittest
import warnings

import numpy as np

from pysolar import util


class TestClearIndexNight(unittest.TestCase):
    def test_clear_index_nighttime_zero_extr_emits_no_warning(self):
        night = datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            scalar_kt = util.clear_index(0.0, 1.0, 1.0, night)
            arr_kt = util.clear_index(np.asarray([0, 0]), 1.0, 1.0, night)

        self.assertEqual(scalar_kt, 0.0)
        self.assertIsInstance(scalar_kt, float)
        np.testing.assert_array_equal(arr_kt, np.array([0.0, 0.0]))
        self.assertEqual(arr_kt.dtype, np.float64)

    def test_clear_index_daytime_matches_ghi_over_extr(self):
        noon = datetime.datetime(2000, 3, 20, 12, 0, tzinfo=datetime.timezone.utc)
        extr = util.extraterrestrial_irrad(0.0, 0.0, noon)
        self.assertGreater(extr, 1000.0)
        kt = util.clear_index(np.asarray([0.0, extr * 0.5]), 0.0, 0.0, noon)
        np.testing.assert_allclose(kt, np.array([0.0, 0.5]))


if __name__ == "__main__":
    unittest.main()
