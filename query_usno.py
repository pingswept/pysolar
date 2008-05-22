#!/usr/bin/python
 
# Tool for requesting data from US Naval Observatory
 
# Copyright 2007 Brandon Stafford
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

import urllib, urllib2, datetime, solar

def EncodeRequest(latitude, longitude, timestamp, elevation):
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

	(deg, rem) = divmod(longitude, 1)
	(min, sec) = divmod(rem, 1.0/60.0)
	params['xx0'] = '1' # longitude (1 = east, -1 = west)
	params['xx1'] = str(deg) # degrees
	params['xx2'] = str(min) # minutes
	params['xx3'] = str(sec) # seconds

	(deg, rem) = divmod(latitude, 1)
	(min, sec) = divmod(rem, 1.0/60.0)	
	params['yy0'] = '1' # latitude (1 = north, -1 = south)
	params['yy1'] = str(deg) # degrees
	params['yy2'] = str(min) # minutes
	params['yy3'] = str(sec) # seconds
	
	params['hh1'] = str(elevation) # height above sea level in meters
	params['ZZZ'] = 'END'
	data = urllib.urlencode(params)
	return data

latitude = 70
longitude = 42
d = datetime.datetime.utcnow()
elevation = 100.0
data = EncodeRequest(latitude, longitude, d, elevation)
url = 'http://aa.usno.navy.mil/cgi-bin/aa_topocentric2.pl'
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)

lines = response.readlines()
response.close()

print lines[21]
result = lines[21]
tokens = result.split(' ')
print tokens

usno_alt = float(tokens[9]) + float(tokens[10])/60.0 + float(tokens[11])/3600.0
usno_az = float(tokens[16]) + float(tokens[17])/60.0 + float(tokens[18])/3600.0
print usno_alt
print usno_az

alt = solar.GetAltitude(latitude, longitude, d, elevation)
pysolar_alt = (90.0 - alt)
az = solar.GetAzimuth(latitude, longitude, d, elevation)
pysolar_az = (180.0 - az)%360.0

print pysolar_alt
print pysolar_az

alt_delta = usno_alt - pysolar_alt
az_delta = usno_az - pysolar_az

print alt_delta
print az_delta