import urllib, urllib2, datetime

def EncodeRequest(timestamp, longitude, latitude, height):
	params = {}
	params['FFX'] = '2' # use worldwide locations script
	params['ID'] = 'Pysolar'
	params['pos'] = '8'
	params['obj'] = '10' # Sun
	params['xxy'] = str(timestamp.year)
	params['xxm'] = str(timestamp.month)
	params['xxd'] = str(timestamp.day)
	params['t1'] = str(timestamp.hour)
	params['t2'] = str(timestamp.minute)
	params['t3'] = str(timestamp.second)
	params['intd'] = '1.0'
	params['unit'] = '1'
	params['rep'] = '5'
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
	
	params['hh1'] = str(height) # height above sea level in meters
	params['ZZZ'] = 'END'
	data = urllib.urlencode(params)
	return data

d = datetime.datetime.utcnow()
data = EncodeRequest(d,2,3,0)
url = 'http://aa.usno.navy.mil/cgi-bin/aa_topocentric2.pl'
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)

lines = response.readlines()
for line in lines:
	print line

the_page = response.read()
response.close()
# FFX=1&ID=AA&pos=8&obj=10&xxy=2008&xxm=4&xxd=19&t1=0&t2=0&t3=0.0&intd=1.0&unit=1&rep=5&st=MA&place=Boston&hh1=0&ZZZ=END