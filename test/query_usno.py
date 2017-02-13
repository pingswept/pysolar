#!/usr/bin/python3

# Copyright Brandon Stafford
#
# This file is part of Pysolar.
#
# Pysolar is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Pysolar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Pysolar. If not, see <http://www.gnu.org/licenses/>.

"""Tool for requesting data from US Naval Observatory

"""
import datetime
import random
from time import strptime
import pytz
from pysolar import solar

try:
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportWarning:
    from urllib2.request import Request, urlopen
    from urllib.parse import urlencode

class Ephemeris:
    """
    docstring here please
    """
    @classmethod
    def params(cls, params):
        """
        setup params
        """
        params = [params[0], params[1], params[2], params[3], params[4]]
        return params

    @classmethod
    def dummy(cls):
        """
        tmp for at least two public methods
        need to be defined for a class
        """
        return None

    def __init__(self, timestamp, params, alt, azm):
        self.timestamp = timestamp
        params = self.params(params)
        self.elevation = float(params[0])
        self.latitude = float(params[1])
        self.longitude = float(params[2])
        self.altitude = float(alt)
        self.azimuth = float(azm)

class EphemerisComparison:
    """
    docstring here please
    """
    @classmethod
    def eph1_params(cls, eph1):
        """
        setup params
        """
        cls.elevation = eph1.elevation
        cls.latitude = eph1.latitude
        cls.longitude = eph1.longitude
        cls.alt1 = eph1.altitude
        cls.az1 = eph1.azimuth
        params = [cls.elevation, cls.latitude, cls.longitude, cls.alt1, cls.az1]
        return params

    @classmethod
    def eph2_params(cls, eph2):
        """
        setup params
        """
        cls.elevation = eph2.elevation
        cls.latitude = eph2.latitude
        cls.longitude = eph2.longitude
        cls.alt1 = eph2.altitude
        cls.az1 = eph2.azimuth
        params = [cls.elevation, cls.latitude, cls.longitude, cls.alt1, cls.az1]
        return params

    def __init__(self, name1, eph1, name2, eph2):
        self.timestamp = eph1.timestamp
        self.name1 = name1
        self.name2 = name2
        self.alt2 = self.eph2_params(eph2)[3]
        self.az2 = self.eph2_params(eph2)[4]
        self.alt_error = abs(self.eph1_params(eph1)[3] - self.eph2_params(eph2)[3])
        self.az_error = abs(self.eph1_params(eph1)[4] - self.eph2_params(eph2)[4])

    @classmethod
    def request_ephemeris_data(cls, datum):
        """
        docstring here please
        """
        data = cls.encode_request(
            datum.latitude, datum.longitude, datum.timestamp, datum.elevation)
        url = 'http://aa.usno.navy.mil/cgi-bin/aa_topocentric2.pl'
        if isinstance(data) == str:
            req = Request(url, data.encode())
        else:
            req = Request(url, data)
        response = urlopen(req)

        lines = response.readlines()
        response.close()
        #print(lines)
        #print(lines[21]) # should not we do some try catch here?
        result = lines[21]
        tokens = [x for x in result.split(b' ') if x not in b' ']
        print('Tokens: \n', tokens)

        usno_alt = float(tokens[4]) + float(tokens[5])/60.0 + float(tokens[6])/3600.0
        usno_az = float(tokens[7]) + float(tokens[8])/60.0 + float(tokens[9])/3600.0

        #   print(usno_alt)
        #   print(usno_az)
        params = [datum.elevation, datum.latitude, datum.longitude]
        result = Ephemeris(datum.timestamp, params, usno_alt, usno_az)

        return result

    @classmethod
    def compare_pysolar_2_usno(cls, datum):
        """
        docstring here please
        """
        params = [datum.elevation, float(datum.latitude), float(datum.longitude)]
        alt = solar.altitude(datum.timestamp, params)
        pysolar_alt = (90.0 - alt)
        azm = solar.azimuth(datum.timestamp, params)
        pysolar_az = (180.0 - azm)%360.0

        #   print(pysolar_alt)
        #   print(pysolar_az)

        py_solar = Ephemeris(datum.timestamp, params, pysolar_az, pysolar_alt)
        comp = EphemerisComparison('pysolar', py_solar, 'usno', datum)
        return comp

    @classmethod
    def encode_request(cls, latitude, longitude, timestamp, elevation):
        """
        Builds a string of arguments to be passed to the Perl script at the USNO
        Note that the degree arguments must be integers, or the USNO script chokes.
        """
        params = {}
        params['FFX'] = '2' # use worldwide locations script
        params['ID'] = 'pysolar'
        params['pos'] = '9'
        params['obj'] = '10' # Sun
        params['xxy'] = str(timestamp.year)
        params['xxm'] = str(timestamp.month)
        params['xxd'] = str(timestamp.day)
        params['t1'] = str(timestamp.hour)
        params['t2'] = str(timestamp.minute)
        params['t3'] = str(timestamp.second)
        params['intd'] = '1.0'
        params['unit'] = '1'
        params['rep'] = '1'
        params['place'] = 'Name omitted'

        sign = lambda x: ('1', '-1')[x < 0]
        (deg, rem) = divmod(longitude, 1)
        (minutes, sec) = divmod(rem, 1.0/60.0)
        params['xx0'] = sign(deg)# longitude (1 = east, -1 = west)
        params['xx1'] = str(abs(int(deg))) # degrees
        params['xx2'] = str(int(minutes)) # minutes
        params['xx3'] = str(sec) # seconds

        (deg, rem) = divmod(latitude, 1)
        (minutes, sec) = divmod(rem, 1.0/60.0)
        params['yy0'] = sign(deg) # latitude (1 = north, -1 = south)
        params['yy1'] = str(abs(int(deg))) # degrees
        params['yy2'] = str(int(minutes)) # minutes
        params['yy3'] = str(sec) # seconds

        params['hh1'] = str(elevation) # height above sea level in meters
        params['ZZZ'] = 'END'
        data = urlencode(params)
        return data

    @classmethod
    def gather_random_ephemeris(cls):
        """
        docstring here please
        """
        latitude = random.randrange(-90, 90)
        longitude = random.randrange(0, 360)
        elevation = 0.0
        dt0 = datetime.datetime(
            random.randrange(2013, 2014),
            random.randrange(1, 13),
            random.randrange(1, 28),
            random.randrange(0, 24),
            random.randrange(0, 60),
            random.randrange(0, 60))
        params = [elevation, latitude, longitude]
        query = Ephemeris(dt0, params, alt=0, azm=0)
        cls.print_ephemeris_datum(query)
        data = cls.request_ephemeris_data(query)
        cls.print_ephemeris_datum(data)
        cls.write_eph_datum(data, 'usno_data.txt')

    @classmethod
    def print_ephemeris_datum(cls, datum):
        """
        docstring here please
        """
        print(
            datum.timestamp,
            datum.latitude,
            datum.longitude,
            datum.elevation,
            datum.azimuth,
            datum.altitude)

    @classmethod
    def read_ephemerides_log(cls, logname):
        """
        docstring here please
        """
        data = []
        log = open(logname, 'r')
        lines = log.readlines()
        log.close()
        for line in lines:
            args = line.split(' ')
            unaware = datetime.datetime(
                *(strptime(args[0] + ' ' + args[1], '%Y-%m-%d %H:%M:%S')[0:6]))
            dt0 = unaware.replace(tzinfo=pytz.UTC)
            params = [args[4], args[2], args[3]]
            eph = Ephemeris(dt0, params, args[5], args[6])
            data.append(eph)
        return data

    @classmethod
    def write_eph_datum(cls, dti, filename):
        """
        docstring here please
        """
        log = open(filename, 'a')
        log.write(
            '%s %s %s %s %s %s\n' % (
                dti.timestamp,
                dti.latitude,
                dti.longitude,
                dti.elevation,
                dti.azimuth,
                dti.altitude))
        log.close()

    @classmethod
    def write_comp_cvs(cls, comps, filename):
        """
        docstring here please
        """
        out = open(filename, 'w')
        out.write(
            'timestamp,latitude,longitude,elevation,alt1,alt2,alt_error,az1,az2,az_error\n')
        for comp in comps:
            out.write(
                '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (
                    comp.timestamp,
                    comp.latitude,
                    comp.longitude,
                    comp.elevation,
                    comp.alt1,
                    comp.alt2,
                    comp.alt_error,
                    comp.az1,
                    comp.az2,
                    comp.az_error))
        out.close()

if __name__ == '__main__':
    # from scipy import stats
    import numpy as np
    import sys

    if len(sys.argv) >= 2:
        EPH = EphemerisComparison.read_ephemerides_log(sys.argv[1])
    else:
        for i in range(100):
            EphemerisComparison.gather_random_ephemeris()
            ephemerides = EphemerisComparison.read_ephemerides_log('usno_data.txt')

    COMPS = []
    for ephemeride in EPH:
        COMPS.append(EphemerisComparison.compare_pysolar_2_usno(ephemeride))

    AZ_ERRORS = np.array([c.az_error for c in COMPS])
    ALT_ERRORS = np.array([c.alt_error for c in COMPS])

    print('---------------------')
    print('Azimuth stats')
    print('Mean error: ' + str(np.mean(AZ_ERRORS)))
    print('Std dev: ' + str(np.std(AZ_ERRORS)))
    # print('Min error: ' + str(stats.tmin(AZ_ERRORS, None)))
    # print('Max error: ' + str(stats.tmax(AZ_ERRORS, None)))

    print('----------------------')
    print('Altitude stats')

    print('Mean error: ' + str(np.mean(ALT_ERRORS)))
    print('Std dev: '+ str(np.std(ALT_ERRORS)))
    # print('Min error: ' + str(stats.tmin(ALT_ERRORS, None)))
    # print('Max error: ' + str(stats.tmax(ALT_ERRORS, None)))

    EphemerisComparison.write_comp_cvs(COMPS, 'pysolar_v_usno.csv')
