Pysolar is a collection of Python libraries for simulating the irradiation of any point on earth by the sun. It includes code for extremely precise ephemeris calculations, and more.

# Note: right now, the latest commits of Pysolar don't work with Python 2.x #

* The latest release, 0.6, is still good: https://github.com/pingswept/pysolar/releases/tag/0.6 but HEAD has just had bunch of changes. They have been validated for Python 3.4, but not the 2.x series. *

Also, the API has changed slightly:

  * Pysolar now expects you to supply a **timezone-aware datetime**, rather than a naive datetime in UTC. If your results seem crazy, this is probably why.
  * Function names are now `lowercase_separated_by_underscores`, in compliance with [PEP8](https://www.python.org/dev/peps/pep-0008/#function-names).

Documentation now appears on [docs.pysolar.org](http://docs.pysolar.org).

## A request ##

If you use Pysolar, please let me know how accurate it is. It's difficult to measure sun location with great precision, but I'd love to hear reports like, "Yeah, it worked to within a degree over the course of an afternoon in Spain."

## Developer contact info ##

[Brandon Stafford](http://pingswept.org)

brandon at pingswept org
