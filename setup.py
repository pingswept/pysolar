#!/usr/bin/env python

from distutils.core import setup

classifiers = ['Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Software Development :: Libraries :: Python Modules']


setup(name='Pysolar',
    version='0.4.1',
    description='Collection of Python libraries for simulating the irradiation of any point on earth by the sun',
    author='Brandon Stafford',
    author_email='brandon@pingswept.org',
    license = 'GNU General Public License (GPL)',
    url='http://pysolar.org',
    py_modules=['constants', 'horizon', 'julian', 'poly', 'query_usno', 'radiation', 'shade', 'shade_test', 'simulate', 'solar', 'testsolar', 'util'],
    requires = ['decimaldegrees', 'gtk', 'numpy', 'PIL', 'pygtk', 'pylab', 'pytz'],
    )

