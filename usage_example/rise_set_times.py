import datetime
import pytz
from pysolar import util

LAT = 51.477811 # approximate Greenwich Maritime Museum
LON = -0.001475 # new prime merridian :D
local_system_utc = datetime.datetime.utcnow()
# print(local_system_utc)
local_system_utc = pytz.utc.localize(local_system_utc)
print('system time now UTC:', local_system_utc)
sun_rise, sun_set = util.get_sunrise_sunset(LAT, LON, local_system_utc)
print('sunrise: ', sun_rise)
print('sunset:', sun_set)
