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
import pytz
from pysolar import util

DTN = datetime
LAT = 51.477811 # approximate Greenwich Maritime Museum
LON = -0.001475 # new prime merridian :D
PARAMS_LIST = [0, LAT, LON]

UTC = DTN.datetime.utcnow()
UTC = pytz.utc.localize(UTC)

SUNRISE, SUNSET = util.sunrise_sunset(UTC, PARAMS_LIST)

print(DTN.date(UTC.year, UTC.month, UTC.day))
print('sunrise: ', SUNRISE.strftime('%H:%M:%S'))
print('sunset:  ', SUNSET.strftime('%H:%M:%S'))
