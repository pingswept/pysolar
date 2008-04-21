Pysolar performs calculations useful for the development of photovoltaic 
systems. Rough steps for use, until either forever or I have time to 
write more documentation:

1. Install python.
2. Get to a prompt that looks like: >>>
3. >>> import solar
4. >>> import datetime
5. >>> d = datetime.datetime.utcnow()
6. >>> lat = 42.0
7. >>> long = -71.0
8. >>> solar.GetAltitude(lat, long, d)
9. >>> solar.GetAzimuth(lat, long, d)

For better examples of usage, check http://pysolar.sourceforge.net/#examples

At this point, Pysolar has basic functionality, but it is relatively untested.
I did validate it against the data in a paper by Reda and Andreas; it agrees
to 4 significant figures, but that's just one data point.

If you use Pysolar, please let me know how accurate it is. It's difficult to
measure sun location with great precision, but I'd love to hear reports of
"Yeah, it worked to within a degree over the course of an afternoon in Spain."

Brandon Stafford
first_name @ pingswept org