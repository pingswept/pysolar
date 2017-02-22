"""
doc string here
"""


import datetime
import time as _time
import pytz
from pysolar import util

LAT = 51.477811 # approximate Greenwich Maritime Museum
LON = -0.001475 # new prime merridian :D

UTC = datetime.datetime.utcnow()
LTZ = pytz.utc.localize(UTC)
PARAMS = [LAT, LON]
SUNRISE, SUNSET = util.sunrise_sunset(LTZ, PARAMS)

print('system time now UTC:', UTC)
print(datetime.date(LTZ.year, LTZ.month, LTZ.day))
print('sunrise: ', SUNRISE.strftime('%H:%M:%S'))
print('sunset:  ', SUNSET.strftime('%H:%M:%S'))

DTO = datetime.datetime.toordinal(UTC)
print('dto:', DTO)
CST = datetime.datetime.now()
print('cst', CST)
UTCOFFSET = datetime.datetime.utcoffset(CST) # was DTO but int error
print('utc offset', UTCOFFSET)

POSIXEPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc).toordinal()
print('posix epoch:', POSIXEPOCH)

print('cst something?', CST.toordinal() - POSIXEPOCH)

# OFFSET = tzinfo.utcoffset(CST)
ZERO = datetime.timedelta(0)
HOUR = datetime.timedelta(hours=1)
SECOND = datetime.timedelta(seconds=1)

STDOFFSET = datetime.timedelta(seconds=-_time.timezone)
if _time.daylight:
    DSTOFFSET = datetime.timedelta(seconds=-_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(datetime.tzinfo):
    """ docs """
    def fromutc(self, dti):
        assert dti.tzinfo is self
        stamp = (dti - datetime.datetime(1970, 1, 1, tzinfo=self)) // SECOND
        args = _time.localtime(stamp)[:6]
        dst_diff = DSTDIFF // SECOND
        # Detect fold
        fold = (args == _time.localtime(stamp - dst_diff))
        return datetime.datetime(*args, microsecond=dti.microsecond,
                                 tzinfo=self, fold=fold)

    def utcoffset(self, dti):
        if self.dst(dti):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dti):
        if self.dst(dti):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dti):
        return _time.tzname[self.dst(dti)]

    def dayst(self, dti):
        """
        doc_header()
        """
        tto = (dti.year, dti.month, dti.day,
               dti.hour, dti.minute, dti.second,
               dti.weekday(), 0, 0)
        stamp = _time.mktime(tto)
        tto = _time.localtime(stamp)
        return tto.tm_isdst > 0

LOCAL = LocalTimezone()


# A complete implementation of current DST rules for major US time zones.

def first_sunday_on_or_after(dti):
    """
    func doc string
    """
    days_to_go = 6 - dti.weekday()
    if days_to_go:
        dti += datetime.timedelta(days_to_go)
    return dti


# US DST Rules
#
# This is a simplified (i.e., wrong for a few cases) set of rules for US
# DST start and end times. For a complete and up-to-date set of DST rules
# and timezone definitions, visit the Olson Database (or try pytz):
# http://www.twinsun.com/tz/tz-link.htm
# http://sourceforge.net/projects/pytz/ (might not be up-to-date)
#
# In the US, since 2007, DST starts at 2am (standard time) on the second
# Sunday in March, which is the first Sunday on or after Mar 8.
DSTSTART_2007 = datetime.datetime(1, 3, 8, 2)
# and ends at 2am (DST time) on the first Sunday of Nov.
DSTEND_2007 = datetime.datetime(1, 11, 1, 2)
# From 1987 to 2006, DST used to start at 2am (standard time) on the first
# Sunday in April and to end at 2am (DST time) on the last
# Sunday of October, which is the first Sunday on or after Oct 25.
DSTSTART_1987_2006 = datetime.datetime(1, 4, 1, 2)
DSTEND_1987_2006 = datetime.datetime(1, 10, 25, 2)
# From 1967 to 1986, DST used to start at 2am (standard time) on the last
# Sunday in April (the one on or after April 24) and to end at 2am (DST time)
# on the last Sunday of October, which is the first Sunday
# on or after Oct 25.
DSTSTART_1967_1986 = datetime.datetime(1, 4, 24, 2)
DSTEND_1967_1986 = DSTEND_1987_2006

def us_dst_range(year):
    """
    Find start and end times for US DST. For years before 1967,
    return
    start = end for no DST.
    """
    if year > 2006:
        dststart, dstend = DSTSTART_2007, DSTEND_2007
    elif 1986 < year < 2007:
        dststart, dstend = DSTSTART_1987_2006, DSTEND_1987_2006
    elif 1966 < year < 1987:
        dststart, dstend = DSTSTART_1967_1986, DSTEND_1967_1986
    else:
        return (datetime.datetime(year, 1, 1), ) * 2

    start = first_sunday_on_or_after(dststart.replace(year=year))
    end = first_sunday_on_or_after(dstend.replace(year=year))
    return start, end


class USTimeZone(datetime.tzinfo):
    """ from pydoc """
    def __init__(self, hours, reprname, stdname, dstname):
        self.stdoffset = datetime.timedelta(hours=hours)
        self.reprname = reprname
        self.stdname = stdname
        self.dstname = dstname

    def __repr__(self):
        return self.reprname

    def tzname(self, dt):
        if self.dst(dt):
            return self.dstname
        else:
            return self.stdname

    def utcoffset(self, dt):
        return self.stdoffset + self.dst(dt)

    def dst(self, dt):
        if dt is None or dt.tzinfo is None:
            # An exception may be sensible here, in one or both cases.
            # It depends on how you want to treat them.  The default
            # fromutc() implementation (called by the default astimezone()
            # implementation) passes a datetime with dt.tzinfo is self.
            return ZERO
        assert dt.tzinfo is self
        start, end = us_dst_range(dt.year)
        # Can't compare naive to aware objects, so strip the timezone from
        # dt first.
        dt = dt.replace(tzinfo=None)
        if start + HOUR <= dt < end - HOUR:
            # DST is in effect.
            return HOUR
        if end - HOUR <= dt < end:
            # Fold (an ambiguous hour): use dt.fold to disambiguate.
            return ZERO if dt.fold else HOUR
        if start <= dt < start + HOUR:
            # Gap (a non-existent hour): reverse the fold rule.
            return HOUR if dt.fold else ZERO
        # DST is off.
        return ZERO

    def fromutc(self, dt):
        assert dt.tzinfo is self
        start, end = us_dst_range(dt.year)
        start = start.replace(tzinfo=self)
        end = end.replace(tzinfo=self)
        std_time = dt + self.stdoffset
        dst_time = std_time + HOUR
        if end <= dst_time < end + HOUR:
            # Repeated hour
            return std_time.replace(fold=1)
        if std_time < start or dst_time >= end:
            # Standard time
            return std_time
        if start <= std_time < end - HOUR:
            # Daylight saving time
            return dst_time


EASTERN = USTimeZone(-5, "Eastern", "EST", "EDT")
CENTRAL = USTimeZone(-6, "Central", "CST", "CDT")
MOUNTAIN = USTimeZone(-7, "Mountain", "MST", "MDT")
PACIFIC = USTimeZone(-8, "Pacific", "PST", "PDT")

U0 = datetime.datetime(2016, 3, 13, 5, tzinfo=datetime.timezone.utc)
for i in range(4):
    u = U0 + i*HOUR
    t = u.astimezone(EASTERN)
    # print(u.time(), 'UTC =', t.time(), t.tzname())

U1 = datetime.datetime(2016, 11, 6, 4, tzinfo=datetime.timezone.utc)
for i in range(4):
    u = U1 + i*HOUR
    t = u.astimezone(EASTERN)
    # print(u.time(), 'UTC =', t.time(), t.tzname(), t.fold)
