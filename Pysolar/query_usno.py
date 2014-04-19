#!/usr/bin/python
 
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
import datetime, random, time

try:
  from urllib.request import Request,urlopen
  from urllib.parse import urlencode
except:
  from urllib2 import Request,urlopen
  from urllib import urlencode

import Pysolar as solar



class Ephemeris:
    def __init__(self, timestamp, latitude, longitude, elevation, azimuth=0, altitude=0):
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = float(elevation)
        self.azimuth = float(azimuth)
        self.altitude = float(altitude)

class EphemerisComparison:
    def __init__(self, name1, eph1, name2, eph2):
        self.timestamp = eph1.timestamp
        self.latitude = eph1.latitude
        self.longitude = eph1.longitude
        self.elevation = eph1.elevation
        self.name1 = name1
        self.alt1 = eph1.altitude
        self.az1 = eph1.azimuth
        self.name2 = name2
        self.alt2 = eph2.altitude
        self.az2 = eph2.azimuth
        self.alt_error = abs(eph1.altitude - eph2.altitude)
        self.az_error = abs(eph1.azimuth - eph2.azimuth)

def RequestEphemerisData(datum):
    data = EncodeRequest(datum.latitude, datum.longitude, datum.timestamp, datum.elevation)
    url = 'http://aa.usno.navy.mil/cgi-bin/aa_topocentric2.pl'
    if type(data) == str:
      req = Request(url, data.encode())
    else:
      req = Request(url, data)
    response = urlopen(req)

    lines = response.readlines()
    response.close()
    #print lines
    #print lines[21] # should not we do some try catch here?
    result = lines[21]
    tokens = [x for x in result.split(b' ') if x not in b' ']
    print('Tokens: \n', tokens)

    usno_alt = float(tokens[4]) + float(tokens[5])/60.0 + float(tokens[6])/3600.0
    usno_az = float(tokens[7]) + float(tokens[8])/60.0 + float(tokens[9])/3600.0

#   print usno_alt
#   print usno_az

    result  = Ephemeris(datum.timestamp, datum.latitude, datum.longitude, datum.elevation, usno_az, usno_alt)

    return result

def ComparePysolarToUSNO(datum):
    alt = solar.GetAltitude(float(datum.latitude), float(datum.longitude), datum.timestamp, datum.elevation)
    pysolar_alt = (90.0 - alt)
    az = solar.GetAzimuth(float(datum.latitude), float(datum.longitude), datum.timestamp, datum.elevation)
    pysolar_az = (180.0 - az)%360.0

#   print pysolar_alt
#   print pysolar_az

    pysolar = Ephemeris(datum.timestamp, datum.latitude, datum.longitude, datum.elevation, pysolar_az, pysolar_alt)
    c = EphemerisComparison('pysolar', pysolar, 'usno', datum)
    return c

def EncodeRequest(latitude, longitude, timestamp, elevation):
    """Builds a string of arguments to be passed to the Perl script at the USNO
    
    Note that the degree arguments must be integers, or the USNO script chokes."""
    params = {}
    params['FFX'] = '2' # use worldwide locations script
    params['ID'] = 'Pysolar'
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
    (min, sec) = divmod(rem, 1.0/60.0)
    params['xx0'] = sign(deg)# longitude (1 = east, -1 = west)
    params['xx1'] = str(abs(int(deg))) # degrees
    params['xx2'] = str(int(min)) # minutes
    params['xx3'] = str(sec) # seconds

    (deg, rem) = divmod(latitude, 1)
    (min, sec) = divmod(rem, 1.0/60.0)  
    params['yy0'] = sign(deg) # latitude (1 = north, -1 = south)
    params['yy1'] = str(abs(int(deg))) # degrees
    params['yy2'] = str(int(min)) # minutes
    params['yy3'] = str(sec) # seconds
    
    params['hh1'] = str(elevation) # height above sea level in meters
    params['ZZZ'] = 'END'
    data = urlencode(params)
    return data

def GatherRandomEphemeris():
    latitude = random.randrange(-90, 90)
    longitude = random.randrange(0, 360)
    elevation = 0.0
    t = datetime.datetime(random.randrange(2013,2014), random.randrange(1, 13), random.randrange(1, 28), random.randrange(0, 24), random.randrange(0, 60), random.randrange(0,60))
    query = Ephemeris(t, latitude, longitude, elevation)
    PrintEphemerisDatum(query)
    d = RequestEphemerisData(query)
    PrintEphemerisDatum(d)
    WriteEphemerisDatumToFile(d, 'usno_data.txt')

def PrintEphemerisDatum(datum):
    print(datum.timestamp, datum.latitude, datum.longitude, datum.elevation, datum.azimuth, datum.altitude)

def ReadEphemeridesLog(logname):
    data = []
    log = open(logname, 'r')
    lines = log.readlines()
    log.close()
    for line in lines:
        args = line.split(' ')
        d = datetime.datetime(*(time.strptime(args[0] + ' ' + args[1], '%Y-%m-%d %H:%M:%S')[0:6]))
        e = Ephemeris(d, args[2], args[3], args[4], args[5], args[6])
        data.append(e)
    return data

def WriteEphemerisDatumToFile(d, filename):
    log = open(filename, 'a')
    log.write('%s %s %s %s %s %s\n' % (d.timestamp, d.latitude, d.longitude, d.elevation, d.azimuth, d.altitude))
    log.close()

def WriteComparisonsToCSV(comps, filename):
    out = open(filename, 'a')
    for c in comps:
        out.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (c.timestamp, c.latitude, c.longitude, c.elevation, c.alt1, c.alt2, c.alt_error, c.az1, c.az2, c.az_error))
    out.close()


if __name__ == '__main__':
    from scipy import stats
    import numpy as np
    import sys
    
    if len(sys.argv) >= 2:
                ephemerides = ReadEphemeridesLog(sys.argv[1])
    else:
        for i in range(100):
            GatherRandomEphemeris()
            ephemerides = ReadEphemeridesLog('usno_data.txt')

    comps = []
    for e in ephemerides:
        c = ComparePysolarToUSNO(e)
        comps.append(c)

    az_errors = np.array([c.az_error for c in comps])
    alt_errors = np.array([c.alt_error for c in comps])

    print('---------------------')
    print('Azimuth stats')
    print('Mean error: ' + str(np.mean(az_errors)))
    print('Std dev: ' + str(np.std(az_errors)))
    print('Min error: ' + str(stats.tmin(az_errors, None)))
    print('Max error: ' + str(stats.tmax(az_errors, None)))

    print('----------------------')
    print('Altitude stats')
    
    print('Mean error: ' + str(np.mean(alt_errors)))
    print('Std dev: '+ str(np.std(alt_errors)))
    print('Min error: ' + str(stats.tmin(alt_errors, None)))
    print('Max error: ' + str(stats.tmax(alt_errors, None)))

    WriteComparisonsToCSV(comps, 'pysolar_v_usno.csv')
