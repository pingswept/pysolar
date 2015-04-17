.. Pysolar documentation master file, created by
   sphinx-quickstart on Sun Dec  7 10:41:31 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pysolar: staring directly at the sun since 2007
===============================================

Pysolar is a collection of Python libraries for simulating the irradiation of any point on earth by the sun. It includes code for extremely precise ephemeris calculations, and more.

Difference from PyEphem
-----------------------

Pysolar is similar to `PyEphem <http://rhodesmill.org/pyephem/>`_, with a few key differences. Both libraries compute the location of the sun based on `Bretagnon's VSOP 87 theory <http://articles.adsabs.harvard.edu/cgi-bin/nph-iarticle_query?1988A%26A...202..309B>`_. Pysolar is aimed at modeling photovoltaic systems, while PyEphem is targeted at astronomers. Pysolar is written in pure Python, while PyEphem is a Python wrapper for the libastro library, written in C, which is part of `XEphem <http://www.clearskyinstitute.com/xephem/>`_.

Difference from Sunpy
---------------------

Pysolar is similar to the sun position module in `Sunpy <http://sunpy.org>`_, which is a project focused on solar physics modeling. See, for example, their beautiful gallery of `sun image renderings <http://sunpy.org/gallery/index.html>`_. The Sunpy position module is based on the same algorithm originally described by Jean Meeus, but it appears to omit the later work by Reda and Andreas at NREL that Pysolar uses, or at least the code is shorter. In any case, Sunpy is aimed at solar physics; Pysolar is aimed at modeling solar radiation on the earth. 

Prerequisites for use
---------------------

Pysolar requires Python, which comes preinstalled on most Unix machines, including Apple's OS X. You can check to see if you have it installed on a Unix machine by typing python at a command prompt. If the result is something like::

    Python 2.5.1c1 (release25-maint, Apr 12 2007, 21:00:25)
    [GCC 4.1.2 (Ubuntu 4.1.2-0ubuntu4)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

you have Python. (You can escape from the Python prompt with Ctrl-D.)

If the result is more like::

    bash: python: command not found

you probably don't have Python.

If you need to, you can download Python from the `Python.org download page <http://python.org/download/>`_.

Examples
========

Location calculation
--------------------

You can figure out your latitude and longitude from the URL from the "Link to this page" link on Google maps. Find your location on the map, click on the "Link to this page" link, and then look at the URL in the address bar of your browser. In between ampersands, you should see something like ``ll=89.123456,-78.912345``. The first number is your latitude; the second is your longitude.

The reference frame for Pysolar is shown in the figure below. Altitude is reckoned with zero at the horizon. The altitude is positive when the sun is above the horizon. Azimuth is reckoned with zero corresponding to south. Positive azimuth estimates correspond to estimates east of south; negative estimates are west of south. In the northern hemisphere, if we speak in terms of (altitude, azimuth), the sun comes up around (0, 90), reaches (70, 0) around noon, and sets around (0, -90).

.. image:: img/reference_frame.png

Then, use the solar.GetAltitude() function to calculate the angle between the sun and a plane tangent to the earth where you are. The result is returned in degrees.::

    host:~/pysolar$ python3
    Python 3.4.0 (default, Apr 11 2014, 13:05:18) 
    [GCC 4.8.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from pysolar.solar import *
    >>> import datetime
    >>> d = datetime.datetime.now()
    >>> get_altitude(42.206, -71.382, d)
    24.39867440096082
    >>> d = datetime.datetime(2007, 2, 18, 15, 13, 1, 130320)
    >>> get_altitude(42.206, -71.382, d)
    20.374937135509537

You can also calculate the azimuth of the sun, as shown below.::

    >>> get_azimuth(42.206, -71.382, datetime.datetime(2007, 2, 18, 15, 18, 0, 0))
    -52.418308823492794

Estimate of clear-sky radiation
-------------------------------

Once you calculate azimuth and altitude of the sun, you can predict the direct irradiation from the sun using Pysolar. ``get_radiation_direct()`` returns a value in watts per square meter. As of version 0.7, the function is *not* smart enough to return zeros at night. It does account for the scattering of light by the atmosphere, though it uses an atmospheric model based on data taken in the United States.::

    >>> latitude_deg = 42.3 # positive in the northern hemisphere
    >>> longitude_deg = -71.4 # negative reckoning west from prime meridian in Greenwich, England
    >>> d = datetime.datetime(2007, 2, 18, 15, 13, 1, 130320)
    >>> altitude_deg = get_altitude(latitude_deg, longitude_deg, d)
    >>> azimuth_deg = get_azimuth(latitude_deg, longitude_deg, d)
    >>> radiation.get_radiation_direct(d, altitude_deg)
    793.0379291685598

Troubleshooting
===============

If you find yourself getting errors like `AttributeError: 'datetime.datetime' object has no attribute 'timestamp'`, this probably means that you are using Python 2 instead of Python 3.

Pysolar no longer supports Python 2. So far, nobody has volunteered to do the work to backport the code to Python 2. If you're stuck on Python 2 because of some other dependency, you should use Pysolar 0.6, which is the last version that works with Python 2.

Validation
==========

Pysolar has been validated against similar ephemeris code maintained by the United States Naval Observatory (USNO). In a random sampling of 6000 locations distributed across the northern hemisphere at random times in 2008, Pysolar matched the observatory's predictions very accurately. The azimuth estimations correlated much more closely than the altitude estimations, but both agreed with the naval observatory's to within less than 0.1 degrees on average.

Using the script included in Pysolar called ``query_usno.py``, around 6200 datapoints were gathered from the website of the US Naval Observatory. The datapoints were randomly distributed in time and space, with the following restrictions:

* Times were limited to 2008 and, to match the USNO's resolution, rounded to the nearest second.
* Locations were limited to integral degrees of latitude and longitude in the northern hemisphere to match USNO's resolution. (In theory, the USNO script should accept locations in the southern hemisphere; in practice, negative latitudes caused the script to fail.)
* Elevation was limited to sea level to make the search space smaller.

Error statistics
----------------

The statistics below are generated by ``query_usno.py`` when run on the data file ``usno_data_6259.txt``, as in::

    python3 -i query_usno.py usno_data_6259.txt

Azimuth error
-------------

* Mean error: 0.00463 degrees
* Standard deviation of error: 0.00550 degrees
* Minimum error: 6.10 x 10e-6 degrees
* Maximum error: 0.176 degrees

Altitude error
--------------

* Mean error: 0.0736 degrees
* Standard deviation: 0.124 degrees
* Minimum error: 7.02 x 10e-5 degrees
* Maximum error: 0.737 degrees

Validation data
---------------

The full validation data files are included in Pysolar. See the files: ``usno_data_6259.txt`` and ``pysolar_v_usno.csv``.

Click on charts for larger versions.

.. image:: img/chart_Pysolar_error_v_altitude_2014-12-13.png
   :scale: 50%

.. image:: img/chart_Pysolar_error_v_azimuth_2014-12-13.png
   :scale: 50%

.. image:: img/chart_Pysolar_error_v_longitude_2014-12-13.png
   :scale: 50%

.. image:: img/chart_Pysolar_error_v_latitude_2014-12-13.png
   :scale: 50%

Validation procedure
--------------------

You can check the accuracy of Pysolar yourself using the iPython Notebook file ``test/validation.ipynb``. The validation steps are:

1. Install IPython Notebook: http://ipython.org/install.html

2. Make sure you have installed only the version of Pysolar that you want to validate.

3. Run ``python3 -i test/query_usno.py test/usno_data_6259.txt``. This runs Pysolar's ``get_altitude()`` and ``get_azimuth()`` functions repeatedly, compares the results to a file included in Pysolar of data pulled from the USNO website, and writes the results to a .CSV file.

4. Start IPython Notebook and open ``validation.ipynb``.

5. Run the code in ``test/validation.ipynb``, which will calculate the error statistics and generate the graphs shown above.

References
==========

`Abstract <http://www.osti.gov/bridge/product.biblio.jsp?query_id=1&amp;page=0&amp;osti_id=15003974>`_ `1.1 MB PDF <http://www.osti.gov/bridge/servlets/purl/15003974-iP3z6k/native/15003974.PDF>`_ I. Reda and A. Andreas, "Solar Position Algorithm for Solar Radiation Applications," National Renewable Energy Laboratory, NREL/TP-560-34302, revised November 2005.

`Online book <http://onlinelibrary.wiley.com/book/10.1002/0471668826>`_ G. Masters, "Renewable and Efficient Electric Power Systems," Wiley-IEEE Press, 2004.

`Abstract <http://pubs.giss.nasa.gov/abs/bi03000u.html>`_ `4.6 MB PDF <http://pubs.giss.nasa.gov/docs/1997/1997_Bishop_etal_1.pdf>`_ J. K. B.
Bishop, W. B. Rossow, and E. G. Dutton, "Surface solar irradiance from the International Satellite Cloud Climatology Project 1983-1991," Journal of Geophysical Research, vol. 102, no. D6, March 27, 1997, pp. 6883-6910.

Hosting history
===============

Pysolar was initially hosted on Sourceforge with Subversion, but we switched to git and Github in 2008. Earlier releases are still on `the Sourceforge site <http://pysolar.sf.net>`_ for now, but you're probably wrong if you think you want to download them.

Contributors
============

Many people have contributed to Pysolar since its inception.

Thanks to Holger Zebner, Pietro Zambelli, Sean Taylor, Simeon Obinna Nwaogaidu, Tim Michelsen, Jon Little, and Lahmeyer International for their contributions of code, bugfixes, documentation, and general encouragement.

Pysolar has been used at several universities, including the University of Oldenburg in Germany, the University of Trento in Italy, and the University of Texas at Austin. It is also deployed in at least one commercial solar tracking system.

Old download statistics
=======================

* version 0.1.0: 22 downloads, 2007-04-18 - 2007-07-01
* version 0.2.0: 97 downloads, 2007-07-01 - 2008-03-10

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

