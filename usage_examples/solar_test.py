""" module """
import unittest
import datetime
import pysolar


class TestSetup(unittest.TestCase):
    """ class """
    def setUp(self):
        self.tz0 = datetime.timezone.utc
        self.now = datetime.datetime(2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)
        print(self.now.tzinfo)
        self.lon = -105.1786
        self.jdn = pysolar.time.julian_solar_day(self.now) - self.lon / 360.0
        self.qls = pysolar.time.leap_seconds(self.now) - self.lon / 360.0
        self.jed = pysolar.time.julian_ephemeris_day(self.now) - self.lon / 360.0
        self.mas = pysolar.solar.my_eot(self.now)
        self.hle = pysolar.solar.heliocentric_longitude(self.jed)
    def test_time_zone(self):
        """ UTC """
        self.assertEqual("UTC", str(self.tz0))

    def test_datetime(self):
        """ 2003-10-17 19:30:30+00:00 """
        self.assertEqual("2003-10-17 19:30:30+00:00", str(self.now))

    def test_qls(self):
        """ 32.2921627777777776 """
        self.assertAlmostEqual(32.292162777777776, self.qls, 12)

    def test_jdn(self):
        """ 2452930.605005862 """
        self.assertAlmostEqual(2452930.605005862, self.jdn, 12)

    def test_jed(self):
        """ 2452930.6057528704 """
        self.assertAlmostEqual(2452930.6057528704, self.jed, 12)

    def test_mas(self):
        """ 1723.1817931397495 """
        self.assertAlmostEqual(1723.1817931397495, self.mas, 12)

    def test_hle(self):
        """ 16.0 """
        self.assertAlmostEqual(16.0, self.hle, 12)


    DATE = datetime.datetime(2003, 10, 17, 19, 30, 30, tzinfo=datetime.timezone.utc)
    QLS = pysolar.time.leap_seconds(DATE)
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

if __name__ == '__main__':
    SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestSetup)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
    # unittest.main()
    """
    data for https://www.nrel.gov/midc/solpos/spa.html
    10/17/2003,
    19:30:00,

    """
