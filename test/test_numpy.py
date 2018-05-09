import pysolar
from pysolar import solar
from pysolar import numeric as math
from datetime import datetime
import pytz
import numpy as np
from nose.tools import raises


@raises(TypeError)
def test_fail_with_math():
    pysolar.use_math()
    lat = np.array([45., 40.])
    lon = np.array([3., 4.])
    time = datetime(2018, 5, 8, 12, 0, 0, tzinfo=pytz.UTC)

    solar.get_altitude(lat, lon, time)


def test_scalar_with_math():
    pysolar.use_math()

    lat = 45.
    lon = 3.
    time = datetime(2018, 5, 8, 12, 0, 0, tzinfo=pytz.UTC)

    print(solar.get_altitude(lat, lon, time))
    print(solar.get_azimuth(lat, lon, time))


def test_scalar_with_numpy():
    pysolar.use_numpy()

    lat = 50.63
    lon = 3.05
    time = datetime(2018, 5, 8, 12, 0, 0, tzinfo=pytz.UTC)
    print(solar.get_altitude(lat, lon, time))
    print(solar.get_azimuth(lat, lon, time))


def test_with_fixed_time():
    """ get_altitude and get_azimuth, test with scalar date """
    pysolar.use_numpy()

    lat = np.array([45., 40.])
    lon = np.array([3., 4.])

    time = datetime(2018, 5, 8, 12, 0, 0, tzinfo=pytz.UTC)

    print(solar.get_altitude(lat, lon, time))
    print(solar.get_azimuth(lat, lon, time))
