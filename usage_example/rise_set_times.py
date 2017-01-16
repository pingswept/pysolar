

import datetime
import pytz
from pysolar import util

LAT = 51.477811 # approximate Greenwich Maritime Museum
LON = -0.001475 # new prime merridian :D

UTC = datetime.datetime.utcnow()
UTC = pytz.utc.localize(UTC)
SUNRISE, SUNSET = util.get_sunrise_sunset(LAT, LON, UTC)

print('system time now UTC:', UTC)
print('sunrise: ', SUNRISE)
print('sunset:', SUNSET)
