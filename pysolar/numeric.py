
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

import datetime
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


def _strip_tz_to_utc_naive(value):
    if isinstance(value, datetime.datetime) and value.tzinfo is not None:
        return value.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return value


def to_utc_datetime64(d, unit=None):
    """Convert scalar or array-like datetime/datetime64 inputs to UTC datetime64 without timezone warnings."""
    dtype = 'datetime64' if unit is None else f'datetime64[{unit}]'
    if isinstance(d, datetime.datetime):
        return numpy.array(_strip_tz_to_utc_naive(d), dtype=dtype)
    if hasattr(d, "tz_convert") and getattr(d, "tz", None) is not None:
        d = d.tz_convert("UTC").tz_localize(None)
    elif hasattr(d, "dt") and getattr(d.dt, "tz", None) is not None:
        d = d.dt.tz_convert("UTC").dt.tz_localize(None)
    arr = numpy.asarray(d)
    if numpy.issubdtype(arr.dtype, numpy.datetime64):
        return arr if unit is None else arr.astype(dtype)
    if arr.dtype == object:
        if arr.ndim == 0:
            return numpy.array(_strip_tz_to_utc_naive(arr.item()), dtype=dtype)
        flat = [_strip_tz_to_utc_naive(x) for x in arr.flat]
        return numpy.array(flat, dtype=dtype).reshape(arr.shape)
    return numpy.array(d, dtype=dtype)


def tm_yday_numpy(d):
    dd = to_utc_datetime64(d, 'D')
    dy = to_utc_datetime64(d, 'Y')
    return (dd - dy).astype('int') + 1


def tm_hour_math(d):
    return d.utctimetuple().tm_hour

tm_hour = tm_hour_math


def tm_hour_numpy(d):
    dh = to_utc_datetime64(d, 'h')
    dd = to_utc_datetime64(d, 'D')
    return (dh - dd).astype('int')


def tm_min_math(d):
    return d.utctimetuple().tm_min

tm_min = tm_min_math


def tm_min_numpy(d):
    dm = to_utc_datetime64(d, 'm')
    dh = to_utc_datetime64(d, 'h')
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
