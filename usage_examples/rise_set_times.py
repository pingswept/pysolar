"""
Examples
    --------
    >>> lat = 50.111512
    >>> lon = 8.680506
    >>> timezone_local = pytz.timezone('Europe/Berlin')
    >>> now = datetime.now(timezone_local)
    >>> sr, ss = sb.get_sunrise_sunset(lat, lon, now)
    >>> print('sunrise: ', sr)
    >>> print('sunset:', ss)
"""

import datetime
# import pytz
from pysolar import util

DTN = datetime
LAT = 39.742476
LON = -105.1786
PARAMS_LIST = [0, LAT, LON]

UTC = DTN.datetime(2003, 10, 17, tzinfo=datetime.timezone.utc)
# UTC = pytz.utc.localize(UTC)

SUNRISE, SUNSET = util.sunrise_sunset(UTC, PARAMS_LIST)

print(DTN.date(UTC.year, UTC.month, UTC.day))
print('sunrise: ', SUNRISE.strftime('%H:%M:%S'), ' UTC')
print('sunset:  ', SUNSET.strftime('%H:%M:%S'), ' UTC')
