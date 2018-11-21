
#    Copyright François Steinmetz
#
#    This file is part of Pysolar.
#
#    Pysolar is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Pysolar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with Pysolar. If not, see <http://www.gnu.org/licenses/>.


"""
Import math functions from either numpy (in order to vectorize operations) or
builtins math module.

By default, use numpy when available.

To force builtins math module usage when numpy is available:
    import pysolar
    pysolar.use_math()
"""

from math import degrees, cos, sin, radians, tan, pi
from math import acos, atan, asin, atan2, exp, e

current_mod = 'math'


def globals_import_from(module, name, name_as):
    """
    Does "from <module> import <name> as <name_as>" (globally)
    """
    module = __import__(module, fromlist=[name])
    globals()[name_as] = getattr(module, name)


def where_math(condition, x, y):
    """ scalar version of numpy.where """
    if condition:
        return x
    else:
        return y

where = where_math


def tm_yday_math(d):
    return d.utctimetuple().tm_yday

tm_yday = tm_yday_math


def tm_yday_numpy(d):
    dd = numpy.array(d, dtype='datetime64[D]')
    dy = numpy.array(d, dtype='datetime64[Y]')
    return (dd - dy).astype('int') + 1


def tm_hour_math(d):
    return d.utctimetuple().tm_hour

tm_hour = tm_hour_math


def tm_hour_numpy(d):
    dh = numpy.array(d, dtype='datetime64[h]')
    dd = numpy.array(d, dtype='datetime64[D]')
    return (dh - dd).astype('int')


def tm_min_math(d):
    return d.utctimetuple().tm_min

tm_min = tm_min_math


def tm_min_numpy(d):
    dm = numpy.array(d, dtype='datetime64[m]')
    dh = numpy.array(d, dtype='datetime64[h]')
    return (dm - dh).astype('int')


def use_numpy():
    """
    Import required functions/constants from numpy
    """
    globals_import_from('numpy', 'degrees', 'degrees')
    globals_import_from('numpy', 'cos', 'cos')
    globals_import_from('numpy', 'sin', 'sin')
    globals_import_from('numpy', 'radians', 'radians')
    globals_import_from('numpy', 'tan', 'tan')
    globals_import_from('numpy', 'pi', 'pi')
    globals_import_from('numpy', 'arccos', 'acos')
    globals_import_from('numpy', 'arctan', 'atan')
    globals_import_from('numpy', 'arcsin', 'asin')
    globals_import_from('numpy', 'arctan2', 'atan2')
    globals_import_from('numpy', 'exp', 'exp')
    globals_import_from('numpy', 'e', 'e')
    globals_import_from('numpy', 'where', 'where')
    globals()['tm_yday'] = tm_yday_numpy
    globals()['tm_hour'] = tm_hour_numpy
    globals()['tm_min'] = tm_min_numpy
    globals()['current_mod'] = 'numpy'


def use_math():
    """
    Import required functions/constants from builtins math module
    """
    globals_import_from('math', 'degrees', 'degrees')
    globals_import_from('math', 'cos', 'cos')
    globals_import_from('math', 'sin', 'sin')
    globals_import_from('math', 'radians', 'radians')
    globals_import_from('math', 'tan', 'tan')
    globals_import_from('math', 'pi', 'pi')
    globals_import_from('math', 'acos', 'acos')
    globals_import_from('math', 'atan', 'atan')
    globals_import_from('math', 'asin', 'asin')
    globals_import_from('math', 'atan2', 'atan2')
    globals_import_from('math', 'exp', 'exp')
    globals_import_from('math', 'e', 'e')
    globals()['where'] = where
    globals()['tm_yday'] = tm_yday_math
    globals()['tm_hour'] = tm_hour_math
    globals()['tm_min'] = tm_min_math
    globals()['current_mod'] = 'math'


try:
    import numpy
    use_numpy()
except ImportError:
    pass
