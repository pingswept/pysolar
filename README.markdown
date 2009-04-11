Pysolar is a collection of Python libraries for simulating the irradiation of any point on earth by the sun. It includes code for extremely precise ephemeris calculations, and more.

Rough steps for use, until either forever or I have time to 
write more documentation:

1. Install python.
2. Get to a Python prompt.
3. Execute code:
<pre>
    import datetime, solar
    d = datetime.datetime.utcnow()
    lat = 42.0
    long = -71.0
    solar.GetAltitude(lat, long, d)
    solar.GetAzimuth(lat, long, d)
</pre>

For better examples of usage, see [the examples on Github](http://wiki.github.com/pingswept/pysolar/examples).

## Difference from PyEphem ##

Pysolar is similar to [PyEphem](http://rhodesmill.org/pyephem/), with a few key differences. Both libraries compute the location of the sun based on [Bretagnon's VSOP 87 theory](http://articles.adsabs.harvard.edu/cgi-bin/nph-iarticle_query?1988A%26A...202..309B). Pysolar is aimed at modeling photovoltaic systems, while PyEphem is targeted at astronomers. Pysolar is written in pure Python, while PyEphem is a Python wrapper for the libastro library, written in C, which is part of [XEphem](http://www.clearskyinstitute.com/xephem/).

## Validation ##

Pysolar has recently been validated against similar ephemeris code maintained by the US Naval Observatory. In a random sampling of 6000 locations distributed across the Northern Hemisphere at random times in 2008, Pysolar matched the observatory’s predictions very accurately. The azimuth estimations correlated much more closely than the altitude estimations, but both agreed with the naval observatory’s to within less than 0.1 degrees on average.

More details on [the validation page on Github](http://wiki.github.com/pingswept/pysolar/validation).

## A request ##

If you use Pysolar, please let me know how accurate it is. It's difficult to measure sun location with great precision, but I'd love to hear reports like, "Yeah, it worked to within a degree over the course of an afternoon in Spain."

## Developer contact info ##

[Brandon Stafford](http://pingswept.org)

brandon at pingswept org

