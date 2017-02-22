#!/usr/bin/python3

#    Library for calculating location of the sun

#    Copyright Brandon Stafford
#
#    This file is part of Pysolar.
#
#    Pysolar is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Pysolar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with Pysolar. If not, see <http://www.gnu.org/licenses/>.
"""
tests for util.py
"""
import datetime
import unittest
from pysolar import util
class TestUtil(unittest.TestCase):
    """
    Tests functions that use when as a time parameter
    """
    when = datetime.datetime(2003, 10, 17, tzinfo=datetime.timezone.utc)
    param_list = [39.742476, -105.1786]
    def setUp(self):
        """
        set up
        """
        return None

    def test_sunrise(self):
        """
        testing Local sunrise time
        10/17/2003, 12:30:30, 6.212002
        """
        # print(self.test_sunrise_sunset.__doc__)
        print('testing util.py Sunrise Time method')
        usr = util.sunrise_time(self.when, self.param_list)
        # print(usr)
        rval = datetime.datetime(
            2003, 10, 17, 13, 21, 59, 486508, tzinfo=datetime.timezone.utc)
        self.assertEqual(rval, usr)


    def test_sunrise_sunset(self):
        """
        testing
        Date, Time, Local sunrise time
        10/17/2003, 12:30:30, 6.212067
        Date, Time, Local sunset time

        """
        # print(self.test_sunrise_sunset.__doc__)
        print('testing util.py Sunrise Sunset method')
        srs = util.sunrise_sunset(self.when, self.param_list)
        # print(srs)
        rtv = datetime.datetime(
            2003, 10, 17, 13, 21, 59, 486508, tzinfo=datetime.timezone.utc)
        stv = datetime.datetime(
            2003, 10, 18, 0, 10, 3, 617537, tzinfo=datetime.timezone.utc)
        self.assertEqual((rtv, stv), srs)


    def test_sunset(self):
        """
        testing
        Date, Time, Local sunrise time
        10/17/2003, 12:30:30, 6.212067
        Date, Time, Local sunset time

        """
        # print(self.test_sunrise_sunset.__doc__)
        print('testing util.py Sunset Time method')
        uss = util.sunset_time(self.when, self.param_list)
        # print(uss)
        sval = datetime.datetime(
            2003, 10, 18, 0, 10, 3, 617537, tzinfo=datetime.timezone.utc)
        self.assertEqual(sval, uss)

if __name__ == "__main__":
    UTIL = unittest.defaultTestLoader.loadTestsFromTestCase(TestUtil)
    unittest.TextTestRunner(verbosity=2).run(UTIL)
