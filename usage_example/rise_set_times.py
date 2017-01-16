

import datetime
import pytz
from pysolar import util

DT = datetime
LAT = 51.477811 # approximate Greenwich Maritime Museum
LON = -0.001475 # new prime merridian :D

UTC = DT.datetime.utcnow()
UTC = pytz.utc.localize(UTC)
SUNRISE, SUNSET = util.get_sunrise_sunset(LAT, LON, UTC)

# print('system time now UTC:', UTC)
print(DT.date(UTC.year, UTC.month, UTC.day))
print('sunrise: ', SUNRISE.strftime('%H:%M:%S'))
print('sunset:  ', SUNSET.strftime('%H:%M:%S'))
