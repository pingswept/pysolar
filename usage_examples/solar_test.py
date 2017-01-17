
import datetime
import pysolar

TZ0 = datetime.timezone.utc
print(TZ0)
DATE = datetime.datetime(2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)
print(DATE)
QLS = pysolar.time.leap_seconds(DATE)
print(QLS)
TDT = pysolar.time.delta_t(DATE)
print(TDT)
TTOFFSET = pysolar.time.TTOFFSET
print(TTOFFSET)
TTDATE = datetime.timedelta(seconds=TDT - TTOFFSET - QLS)
print(TTDATE)
CDS = TTDATE.microseconds
print(CDS)
JDN = pysolar.time.julian_solar_day(DATE)
print(JDN)
TTJDN = JDN + CDS / 86_400_000_000
print(TTJDN)
LAT = 39.742476
LON = -105.1786
print(LAT)
print(LON)
DTT = DATE.utctimetuple()
print(DTT.tm_yday)
VMA = pysolar.solar.my_eot(TTJDN)
