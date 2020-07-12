import pysolar
from pysolar import radiation, solar
from pysolar import numeric as math
import datetime
import numpy as np
from nose.tools import raises, assert_equal


@raises(TypeError)
def test_fail_with_math():
    pysolar.use_math()
    lat = np.array([45., 40.])
    lon = np.array([3., 4.])
    time = datetime.datetime(2018, 5, 8, 12, 0, 0, tzinfo=datetime.timezone.utc)

    solar.get_altitude(lat, lon, time)


def test_scalar_with_math():
    pysolar.use_math()

    lat = 45.
    lon = 3.
    time = datetime.datetime(2018, 5, 8, 12, 0, 0, tzinfo=datetime.timezone.utc)

    print(solar.get_altitude(lat, lon, time))
    print(solar.get_azimuth(lat, lon, time))


def test_scalar_with_numpy():
    pysolar.use_numpy()

    lat = 50.63
    lon = 3.05
    time = datetime.datetime(2018, 5, 8, 12, 0, 0, tzinfo=datetime.timezone.utc)
    print(solar.get_altitude(lat, lon, time))
    print(solar.get_azimuth(lat, lon, time))


def test_with_fixed_time():
    """ get_altitude and get_azimuth, with scalar date """
    pysolar.use_numpy()

    lat = np.array([45., 40.])
    lon = np.array([3., 4.])

    time = datetime.datetime(2018, 5, 8, 12, 0, 0, tzinfo=datetime.timezone.utc)

    print(solar.get_altitude(lat, lon, time))
    print(solar.get_azimuth(lat, lon, time))
    print(solar.get_altitude_fast(lat, lon, time))
    print(solar.get_azimuth_fast(lat, lon, time))


def test_with_fixed_position():
    """ get_altitude and get_azimuth, with scalar position """
    pysolar.use_numpy()

    lat = 50.
    lon = 3.

    time = np.array(['2018-05-08T12:15:00',
                     '2018-05-08T15:00:00'], dtype='datetime64')

    print(solar.get_altitude_fast(lat, lon, time))
    print(solar.get_azimuth_fast(lat, lon, time))

def test_datetime_operations():

    d0 = datetime.datetime(2018,5,8,12,0,0)
    d1 = np.array(d0)

    assert_equal(math.tm_yday_math(d0),
                 math.tm_yday_numpy(d1))

    assert_equal(math.tm_hour_math(d0),
                 math.tm_hour_numpy(d1))

    assert_equal(math.tm_min_math(d0),
                 math.tm_min_numpy(d1))


def test_numpy():
    """ get_altitude and get_azimuth, with lat, lon and date arrays """
    pysolar.use_numpy()

    lat = np.array([45., 40.])
    lon = np.array([3., 4.])

    time = np.array(['2018-05-08T12:15:00',
                     '2018-05-08T15:00:00'], dtype='datetime64')

    print(solar.get_altitude_fast(lat, lon, time))
    print(solar.get_azimuth_fast(lat, lon, time))


def test_numpy_radiation():
    """
    get_radiation_direct with lat, lon, and date as arrays
    """
    pysolar.use_numpy()

    lat = np.array([45., 40., 40.])
    lon = np.array([3., 4., 3.])

    time = np.array([
        '2018-05-08T12:15:00',
        '2018-05-08T15:00:00',
        '2018-05-08T03:00:00',
    ], dtype='datetime64')

    altitude = solar.get_altitude_fast(lat, lon, time)
    rad_results = radiation.get_radiation_direct(time, altitude)
    assert rad_results[2] == 0
    print(rad_results)
