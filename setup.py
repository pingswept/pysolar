#!/usr/bin/env python

from distutils.core import setup
import setuptools

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
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3']


setup(name='Pysolar',
    version='0.6',
    description='Collection of Python libraries for simulating the irradiation of any point on earth by the sun',
    author='Brandon Stafford',
    author_email='brandon@pingswept.org',
    license = 'GNU General Public License (GPL)',
    url='http://pysolar.org',
    packages=['Pysolar'],
    requires = ['numpy', 'pytz'],
    )

