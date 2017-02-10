# -*- coding: utf-8 -*-

#
# Copyright 2010 Frédéric Grollier
#
# Distributed under the terms of the MIT license
#

import warnings

from ctypes import CDLL, byref, POINTER
from ctypes.util import find_library
from ctypes import c_int, c_char, c_double

from numpy.ctypeslib import ndpointer
from numpy import ndarray, array, zeros, asarray, asfarray, asmatrix

_sofalib_filename = find_library('sofa_c')
if _sofalib_filename is None:
    raise ImportError('Unable to find the shared C library "sofa_c".')
_sofa = CDLL(_sofalib_filename)


# Try to guess what SOFA version we're dealing with,
# by testing the presence of newly created functions
# between each version.
__sofa_version = None
try:
    _sofa.iauTaitt
    __sofa_version = (2010, 12, 1)
except AttributeError:
    __sofa_version = (2009, 12, 31)

def get_sofa_version():
    """ Return a tuple containing the three components of the
    |SOFA| library release wich has been loaded, in the form
    (year, month, day).

    In case the release number hasn't been resolved (*None*, *None*, *None*)
    is returned. This should never occur and shall be signaled as a bug.

    .. note:: this only deals with *major* release numbers and does not
        account for *revised* versions of |SOFA|.
    """

    if __sofa_version is None:
        return (None, None, None)
    else:
        return __sofa_version


def has_function(funcname):
    """ Helper function that returns True if this particular release of |SOFA|
    provides the function *funcname*, and False otherwise. This is only the
    case with function names that are legal |SOFA| function names, wich means
    that calling ``has_function`` with a *funcname* that isn't known by any
    version of |SOFA| will raise :exc:`AttributeError`.

    """

    if not funcname in globals():
        raise AttributeError('%s does not know any function "named" %s' % \
                                (__package__, funcname))
    # convert 'funcname' to its equivalent SOFA name
    funcname = 'iau' + funcname[0].upper() + funcname[1:]
    return hasattr(_sofa, funcname)


# iauA2af
_sofa.iauA2af.argtypes = [c_int, #ndp
                            c_double, #angle
                            POINTER(c_char), #sign
                            c_int * 4] #idmsf
def a2af(ndp, angle):
    """ Decompose radians into degrees, arcminutes, arcseconds, fraction.

    :param ndp: the requested resolution.
    :type ndp: int

    :param angle: the value to decompose.
    :type angle: float

    :returns: a tuple whose first member is a string containing the sign, and
        the second member is itself a tuple (degrees, arcminutes, arcseconds,
        fraction).

    .. seealso:: |MANUAL| page 19
    """
    sign = c_char()
    idmsf = (c_int * 4)()
    _sofa.iauA2af(ndp, float(angle), byref(sign), idmsf)
    return sign.value, tuple([v for v in idmsf])


# iauA2tf
_sofa.iauA2tf.argtypes = [c_int, #ndp
                            c_double, #angle
                            POINTER(c_char), #sign
                            c_int * 4] #ihmsf
def a2tf(ndp, angle):
    """ Decompose radians into hours, arcminutes, arcseconds, fraction.

    :param ndp: the requested resolution.
    :type ndp: int

    :param angle: the value to decompose.
    :type angle: float

    :returns: a tuple whose first member is a string containing the sign, and
        the second member is itself a tuple (hours, arcminutes, arcseconds,
        fraction).

    .. seealso:: |MANUAL| page 20
    """
    sign = c_char()
    ihmsf = (c_int * 4)()
    _sofa.iauA2tf(ndp, float(angle), byref(sign), ihmsf)
    return sign.value, tuple([v for v in ihmsf])


# iauAf2a
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauAf2a.argtypes = [c_char, #sign
                            c_int, #ideg
                            c_int, #iamin
                            c_double, #asec
                            POINTER(c_double)] #rad
    _sofa.iauAf2a.restype = c_int
except AttributeError:
    pass

af2a_msg = {0: 'OK', # Unused
                1:'Af2a: degrees outside the range 0-359',
                2:'Af2a: arcminutes outside the range 0-59',
                3:'Af2a: arcseconds outside the range 0-59.999...'}
def af2a(s, ideg, iamin, asec):
    """ Convert degrees, arcminutes, arcseconds to radians.

    :param s: sign, '-' for negative, otherwise positive.

    :param ideg: degrees.
    :type ideg: int

    :param iamin: arcminutes.
    :type iamin: int

    :param asec: arcseconds.
    :type asec: float

    :returns: the converted value in radians as a float.

    A UserWarning may be issued in case *ideg*, *iamin* or *asec*
        values are outside the range 0-359, 0-59 or 0-59.999...

    .. seealso:: |MANUAL| page 21
    """

    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    rad = c_double()
    s = _sofa.iauAf2a(str(s), ideg, iamin, asec, byref(rad))
    if s != 0:
        warnings.warn(af2a_msg[s], UserWarning, 2)
    return rad.value



# iauAnp
_sofa.iauAnp.argtypes = [c_double]
_sofa.iauAnp.restype = c_double
def anp(a):
    """ Normalize *a* into the range 0 <= result < 2pi.

    :param a: the value to normalize.
    :type a: float

    :returns: the normalized value as a float.

    .. seealso:: |MANUAL| page 22
    """
    return _sofa.iauAnp(float(a))


# iauAnpm
_sofa.iauAnpm.argtypes = [c_double]
_sofa.iauAnpm.restype = c_double
def anpm(a):
    """ Normalize *a* into the range -pi <= result < +pi.

    :param a: the value to normalize.
    :type a: float

    :returns: the normalized value as a float.

    .. seealso:: |MANUAL| page 23
    """
    return _sofa.iauAnpm(float(a))


# iauBi00
_sofa.iauBi00.argtypes = [POINTER(c_double), #dpsibi
                            POINTER(c_double), #depsbi
                            POINTER(c_double)] #dra
def bi00():
    """ Frame bias components of IAU 2000 precession-nutation models.

    :returns: a tuple of three items:

        * longitude correction (float)
        * obliquity correction (float)
        * the ICRS RA of the J2000.0 mean equinox (float).

    .. seealso:: |MANUAL| page 24
    """
    dpsibi = c_double()
    depsbi = c_double()
    dra = c_double()
    _sofa.iauBi00(byref(dpsibi), byref(depsbi), byref(dra))
    return dpsibi.value, depsbi.value, dra.value

# iauBp00
_sofa.iauBp00.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float), #rb
                            ndpointer(shape=(3,3), dtype=float), #rp
                            ndpointer(shape=(3,3), dtype=float)] #rbp
def bp00(date1, date2):
    """ Frame bias and precession, IAU 2000.

    :param date1, date2: TT as a two-part Julian date.

    :returns: a tuple of three items:

        * frame bias matrix (numpy.matrix of shape 3x3)
        * precession matrix (numpy.matrix of shape 3x3)
        * bias-precession matrix (numpy.matrix of shape 3x3)

    .. seealso:: |MANUAL| page 25
    """
    rb = asmatrix(zeros(shape=(3,3), dtype=float))
    rp = asmatrix(zeros(shape=(3,3), dtype=float))
    rbp = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauBp00(date1, date2, rb, rp, rbp)
    return rb, rp, rbp


# iauBp06
_sofa.iauBp06.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float), #rb
                            ndpointer(shape=(3,3), dtype=float), #rp
                            ndpointer(shape=(3,3), dtype=float)] #rbp
def bp06(date1, date2):
    """ Frame bias and precession, IAU 2006.

    :param date1, date2: TT as a two-part Julian date.

    :returns: a tuple of three items:

        * frame bias matrix (numpy.matrix of shape 3x3)
        * precession matrix (numpy.matrix of shape 3x3)
        * bias-precession matrix (numpy.matrix of shape 3x3)

    .. seealso:: |MANUAL| page 27
    """
    rb = asmatrix(zeros(shape=(3,3), dtype=float))
    rp = asmatrix(zeros(shape=(3,3), dtype=float))
    rbp = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauBp06(date1, date2, rb, rp, rbp)
    return rb, rp, rbp


# iauBpn2xy
_sofa.iauBpn2xy.argtypes = [ndpointer(shape=(3,3), dtype=float), #rbpn
                            POINTER(c_double), #x
                            POINTER(c_double)] #y
def bpn2xy(rbpn):
    """ Extract from the bias-precession-nutation matrix the X,Y coordinates
    of the Celestial Intermediate Pole.

    :param rbpn: celestial-to-true matrix
    :type rbpn: numpy.ndarray, matrix or nested sequences of shape 3x3

    :returns: a tuple of two items containing *x* and *y*, as floats.

    .. seealso:: |MANUAL| page 28
    """
    x = c_double()
    y = c_double()
    _sofa.iauBpn2xy(asmatrix(rbpn, dtype=float), x, y)
    return x.value, y.value


# iauC2i00a
_sofa.iauC2i00a.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rc2i
def c2i00a(date1, date2):
    """ Form the celestial-to-intermediate matrix for a given date using the
    IAU 2000A precession-nutation model.

    :param date1, date2: TT as a two-part Julian date.

    :returns: the celestial-to-intermediate matrix, as a numpy.matrix of
        shape 3x3.

    .. seealso:: |MANUAL| page 29
    """
    rc2i = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2i00a(date1, date2, rc2i)
    return rc2i


# iauC2i00b
_sofa.iauC2i00b.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rc2i
def c2i00b(date1, date2):
    """ Form the celestial-to-intermediate matrix for a given date using the
    IAU 2000B precession-nutation model.

    :param date1, date2: TT as a two-part Julian date.

    :returns: the celestial-to-intermediate matrix, as a numpy.matrix of
        shape 3x3.

    .. seealso:: |MANUAL| page 31
    """
    rc2i = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2i00b(date1, date2, rc2i)
    return rc2i


# iauC2i06a
_sofa.iauC2i06a.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rc2i
def c2i06a(date1, date2):
    """ Form the celestial-to-intermediate matrix for a given date using the
    IAU 2006 precession-nutation model.

    :param date1, date2: TT as a two-part Julian date.

    :returns: the celestial-to-intermediate matrix, as a numpy.matrix of
        shape 3x3.

    .. seealso:: |MANUAL| page 33
    """
    rc2i = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2i06a(date1, date2, rc2i)
    return rc2i


# iauC2ibpn
_sofa.iauC2ibpn.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float), #rbpn
                            ndpointer(shape=(3,3), dtype=float)] #rc2i
def c2ibpn(date1, date2, rbpn):
    """ Form the celestial-to-intermediate matrix for a given date given the
    bias-precession-nutation matrix. IAU 2000.

    :param date1, date2: TT as a two-part Julian date.

    :param rbpn: celestial-to-true matrix.
    :type rbpn: numpy.ndarray, numpy.matrix or nested sequences of shape 3x3

    :returns: the celestial-to-intermediate matrix, as a numpy.matrix of
        shape 3x3.

    .. seealso:: |MANUAL| page 34
    """
    rc2i = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2ibpn(date1, date2, asmatrix(rbpn, dtype=float), rc2i)
    return rc2i


# iauC2ixy
_sofa.iauC2ixy.argtypes = [c_double, #date1
                            c_double, #date2
                            c_double, #x
                            c_double, #y
                            ndpointer(shape=(3,3), dtype=float)] #rc2i
def c2ixy(date1, date2, x, y):
    """ Form the celestial to intermediate-frame-of-date matrix for a given
    date when CIP X,Y coordinates are known. IAU 2000.

    :param date1, date2: TT as a two-part Julian date.

    :param x, y: celestial intermediate pole coordinates.
    :type x, y: float

    :returns: the celestial-to-intermediate matrix as a numpy.matrix of shape
        3x3.

    .. seealso:: |MANUAL| page 36
    """
    rc2i = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2ixy(date1, date2, float(x), float(y), rc2i)
    return rc2i


# iauC2ixys
_sofa.iauC2ixys.argtypes = [c_double, #x
                            c_double, #y
                            c_double, #s
                            ndpointer(shape=(3,3), dtype=float)] #rc2i
def c2ixys(x, y, s):
    """ Form the celestial to intermediate-frame-of-date matrix given the CIP
    X,Y coordinates and the CIO locator s.

    :param x, y: celestial intermediate pole coordinates.
    :type x, y: float

    :param s: the CIO locator.
    :type s: float

    :returns: the celestial-to-intermediate matrix as a numpy.matrix of shape
        3x3.

    .. seealso:: |MANUAL| page 38
    """
    rc2i = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2ixys(float(x), float(y), float(s), rc2i)
    return rc2i


# iauC2s
_sofa.iauC2s.argtypes = [ndpointer(shape=(1,3), dtype=float), #p
                        POINTER(c_double), #theta
                        POINTER(c_double)] #phi
def c2s(p):
    """ P-vector to spherical coordinates.

    :param p: p-vector
    :type p: numpy.ndarray, matrix or nested sequences of shape (1,3)

    :returns: a tuple of two items:

        * the longitude angle in radians (float)
        * the latitude angle in radians (float)

    .. seealso:: |MANUAL| page 39
    """
    theta = c_double()
    phi = c_double()
    _sofa.iauC2s(asmatrix(p, dtype=float), byref(theta), byref(phi))
    return theta.value, phi.value


# iauC2t00a
_sofa.iauC2t00a.argtypes = [c_double, #tta
                            c_double, #ttb
                            c_double, #uta
                            c_double, #utb
                            c_double, #xp
                            c_double, #yp
                            ndpointer(shape=(3,3), dtype=float)]
def c2t00a(tta, ttb, uta, utb, xp, yp):
    """ Form the celestial-to-terrestrial matrix given the date, the UT1 and
    the polar motion, using IAU 2000A nutation model.

    :param tta, ttb: TT as a two-part Julian date.
    :type tta, ttb: float

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :param xp, yp: coordinates of the pole in radians.
    :type xp, yp: float

    :returns: the celestial-to-terrestrial matrix, as a numpy.matrix of shape
        3x3.

    .. seealso:: |MANUAL| page 40
    """
    rc2t = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2t00a(tta, ttb, uta, utb, float(xp), float(yp), rc2t)
    return rc2t


# iauC2t00b
_sofa.iauC2t00b.argtypes = [c_double, #tta
                            c_double, #ttb
                            c_double, #uta
                            c_double, #utb
                            c_double, #xp
                            c_double, #yp
                            ndpointer(shape=(3,3), dtype=float)]
def c2t00b(tta, ttb, uta, utb, xp, yp):
    """ Form the celestial-to-terrestrial matrix given the date, the UT1 and
    the polar motion, using IAU 2000B nutation model.

    :param tta, ttb: TT as a two-part Julian date.
    :type tta, ttb: float

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :param xp, yp: coordinates of the pole in radians.
    :type xp, yp: float

    :returns: the celestial-to-terrestrial matrix, as a numpy.matrix of shape
        3x3.

    .. seealso:: |MANUAL| page 42
    """
    rc2t = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2t00b(tta, ttb, uta, utb, float(xp), float(yp), rc2t)
    return rc2t


# iauC2t06a
_sofa.iauC2t06a.argtypes = [c_double, #tta
                            c_double, #ttb
                            c_double, #uta
                            c_double, #utb
                            c_double, #xp
                            c_double, #yp
                            ndpointer(shape=(3,3), dtype=float)]
def c2t06a(tta, ttb, uta, utb, xp, yp):
    """ Form the celestial-to-terrestrial matrix given the date, the UT1 and
    the polar motion, using the IAU 2006 precession and IAU 2000A nutation
    models.

    :param tta, ttb: TT as a two-part Julian date.
    :type tta, ttb: float

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :param xp, yp: coordinates of the pole in radians.
    :type xp, yp: float

    :returns: the celestial-to-terrestrial matrix, as a nunmp.matrix of shape
        3x3.

    .. seealso:: |MANUAL| page 44
    """
    rc2t = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2t06a(tta, ttb, uta, utb, float(xp), float(yp), rc2t)
    return rc2t


# iauC2tcio
_sofa.iauC2tcio.argtypes = [ndpointer(shape=(3,3), dtype=float), #rc2i
                            c_double, #era
                            ndpointer(shape=(3,3), dtype=float), #rpom
                            ndpointer(shape=(3,3), dtype=float)] #rc2t
def c2tcio(rc2i, era, rpom):
    """ Assemble the celestial-to-terrestrial matrix from CIO-based
    components (the celestial-to-intermediate matrix, the Earth Rotation Angle
    and the polar motion matrix).

    :param rc2i: celestial-to-intermediate matrix.
    :type rc2i: array-like object of shape (3,3)

    :param era: Earth rotation angle
    :type era: float

    :param rpom: polar-motion matrix.
    :type rpom: array-like of shape (3,3)

    :returns: celestial-to-terrestrial matrix as a numpy.matrix of shape
        3x3.

    .. seealso:: |MANUAL| page 46
    """
    rc2t = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2tcio(asmatrix(rc2i, dtype=float), float(era),
                                            asmatrix(rpom, dtype=float), rc2t)
    return rc2t


# iauC2teqx
_sofa.iauC2teqx.argtypes = [ndpointer(shape=(3,3), dtype=float), #rbpn
                            c_double, #gst
                            ndpointer(shape=(3,3), dtype=float), #rpom
                            ndpointer(shape=(3,3), dtype=float)] #rc2t
def c2teqx(rbpn, gst, rpom):
    """ Assemble the celestial-to-terrestrial matrix from equinox-based
    components (the celestial-to-true matrix, the Greenwich Apparent Sidereal
    Time and the polar motion matrix).

    :param rbpn: celestial-to-true matrix.
    :type rbpn: array-like of shape (3,3)

    :param gst: Greenwich apparent sidereal time.
    :type gst: float

    :param rpom: polar-motion matrix.
    :type rpom: array-like of shape (3,3)

    :returns: celestial-to-terrestrial matrix as a numpy.matrix of shape
        3x3.

    *sofa manual.pdp page 47*
    """
    rc2t = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2teqx(asmatrix(rbpn, dtype=float), float(gst),
                                            asmatrix(rpom, dtype=float), rc2t)
    return rc2t


# iauC2tpe
_sofa.iauC2tpe.argtypes = [c_double, #tta,
                            c_double, #ttb
                            c_double, #uta
                            c_double, #utb
                            c_double, #dpsi
                            c_double, #deps
                            c_double, #xp
                            c_double, #yp
                            ndpointer(shape=(3,3), dtype=float)] #rc2t
def c2tpe(tta, ttb, uta, utb, dpsi, deps, xp, yp):
    """ Form the celestial-to-terrestrial matrix given the date, the UT1,
    the nutation and the polar motion. IAU 2000.

    :param tta, ttb: TT as a two-part Julian date.
    :type tta, ttb: float

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :param dpsi, deps: nutation
    :type dpsi, deps: float

    :param xp, yp: coordinates of the pole in radians.
    :type xp, yp: float

    :returns: the celestial-to-terrestrial matrix as a nump.matrix of shape
        3x3.

    .. seealso:: |MANUAL| page 48
    """
    rc2t = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2tpe(tta, ttb, uta, utb, float(dpsi), float(deps), float(xp),
                                                            float(yp), rc2t)
    return rc2t



# iauC2txy
_sofa.iauC2txy.argtypes = [c_double, #tta
                            c_double, #ttb
                            c_double, #uta
                            c_double, #utb
                            c_double, #x
                            c_double, #y,
                            c_double, #xp,
                            c_double, #yp
                            ndpointer(shape=(3,3), dtype=float)] #rc2t
def c2txy(tta, ttb, uta, utb, x, y, xp, yp):
    """ Form the celestial-to-terrestrial matrix given the date, the UT1,
    the CIP coordinates and the polar motion. IAU 2000.

    :param tta, ttb: TT as a two-part Julian date.
    :type tta, ttb: float

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :param x, y: Celestial Intermediate Pole.
    :type x, y: float

    :param xp, yp: coordinates of the pole in radians.
    :type xp, yp: float

    :returns: celestial-to-terrestrial matrix as a numpy.matrix of shape
        3x3.

    .. seealso:: |MANUAL| page 50
    """
    rc2t = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauC2txy(tta, ttb, uta, utb, float(x), float(y),
                                                float(xp), float(yp), rc2t)
    return rc2t


# iauCal2jd
_sofa.iauCal2jd.argtypes = [c_int, #iy
                            c_int, #im
                            c_int, #id
                            POINTER(c_double), #djm0
                            POINTER(c_double)] #djm
_sofa.iauCal2jd.restype = c_int
cal2jd_msg = {
            -1: 'minimum year allowed is -4799',
            -2: 'month must be in 1..12',
            -3: 'day is out of range for this month'}

def cal2jd(iy, im, id):
    """ Gregorian calendar to Julian date.

    :param iy: year.
    :type iy: int

    :param im: month.
    :type im: int

    :param id: day.
    :type id: int

    :returns: a tuple of two items:

        * MJD zero-point : always 2400000.5 (float)
        * Modified Julian date for 0 hours (float)

    :raises: :exc:`ValueError` if one of the supplied values is out of its
        allowed range.

    .. seealso:: |MANUAL| page 52
    """
    djm0 = c_double()
    djm = c_double()
    s = _sofa.iauCal2jd(iy, im, id, byref(djm0), byref(djm))
    if s != 0:
        raise ValueError(cal2jd_msg[s])
    return djm0.value, djm.value


# iauCp
_sofa.iauCp.argtypes = [ndpointer(shape=(1,3), dtype=float), #p
                        ndpointer(shape=(1,3), dtype=float)] #c
def cp(p):
    """ Copy a p-vector.

    :param p: p-vector to copy.
    :type p: array-like of shape (1,3)

    :returns: a copy of *p* as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 53
    """

    c = asmatrix(zeros(shape=(1,3)), dtype=float)
    _sofa.iauCp(asmatrix(p, dtype=float), c)
    return c


# iauCpv
_sofa.iauCpv.argtypes = [ndpointer(shape=(2,3), dtype=float), #pv
                        ndpointer(shape=(2,3), dtype=float)] #c
def cpv(pv):
    """ Copy a pv-vector.

    :param pv: pv-vector to copy.
    :type pv: array-like of shape (2,3)

    :returns: a copy of *pv* as a numpy.matrix of shape 2x3.

    .. seealso:: |MANUAL| page 54
    """

    c = asmatrix(zeros(shape=(2,3)), dtype=float)
    _sofa.iauCpv(asmatrix(pv, dtype=float), c)
    return c


# iauCr
_sofa.iauCr.argtypes = [ndpointer(shape=(3,3), dtype=float), #r
                        ndpointer(shape=(3,3), dtype=float)] #c
def cr(r):
    """ Copy a rotation matrix.

    :param r: rotation matrix to copy.
    :type r: array-like of shape (3,3)

    :returns: a copy of *r* as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 55
    """

    c = asmatrix(zeros(shape=(3,3)), dtype=float)
    _sofa.iauCr(asmatrix(r, dtype=float), c)
    return c


# iauD2dtf
# the routine was added in release 2010-12-01
try:
    _sofa.iauD2dtf.argtypes = [POINTER(c_char), #scale
                            c_int, #ndp
                            c_double, #d1
                            c_double, #d2
                            POINTER(c_int), #iy
                            POINTER(c_int), #im
                            POINTER(c_int), #id
                            c_int * 4] #ihmsf
    _sofa.iauD2dtf.restype = c_int
except AttributeError:
    pass
d2dtf_msg = {
            1: 'D2dtf: dubious year',
            -1: 'unacceptable date',
            }
def d2dtf(scale, ndp, d1, d2):
    """ Format for output a 2-part Julian Date.

    :param scale: timescale ID.
    :type scale: str

    :param ndp: resolution.
    :type ndp: int

    :param d1, d2: time as a two-part Julian Date.
    :type d1, d2: float

    :returns: a tuple of 7 items:

        * year (int)
        * month (int)
        * day (int)
        * hours (int)
        * minutes (int)
        * seconds (int)
        * fraction of second (int)

    :raises: :exc:`ValueError` if the date is outside the range of valid values
        handled by this function.

        :exc:`UserWarning` if *scale* is "UTC" and the value predates the
        introduction of the timescale or is too far in the future to be
        trusted.

    .. seealso:: |MANUAL| page 56
    """
    if __sofa_version < (2010, 12, 1):
        raise NotImplementedError
    iy = c_int()
    im = c_int()
    id = c_int()
    ihmsf = (c_int * 4)()
    s = _sofa.iauD2dtf(scale, ndp, d1, d2, byref(iy), byref(im), byref(id), ihmsf)
    if s < 0:
        raise ValueError(d2dtf_msg[s])
    elif s > 0:
        warnings.warn(d2dtf_msg[s], UserWarning, 2)
    return (iy.value, im.value, id.value) + tuple([v for v in ihmsf])




# iauD2tf
_sofa.iauD2tf.argtypes = [c_int, #ndp
                            c_double, #days
                            POINTER(c_char), #sign
                            c_int * 4] #ihmsf
def d2tf(ndp, days):
    """ Decompose days into hours, minutes, seconds, fraction.

    :param ndp: the requested resolution.
    :type ndp: int

    :param days: the value to decompose.
    :type days: float

    :returns: a tuple of two items:

        * the sign as a string ('+' or '-')
        * a tuple (hours, minutes, seconds, fraction).

    .. seealso:: |MANUAL| page 58
    """
    sign = c_char()
    ihmsf = (c_int * 4)()
    _sofa.iauD2tf(ndp, days, byref(sign), ihmsf)
    return sign.value, tuple([v for v in ihmsf])


# iauDat
_sofa.iauDat.argtypes = [c_int, #iy
                        c_int, #im
                        c_int, #id
                        c_double, #fd
                        POINTER(c_double)] #deltat
_sofa.iauDat.restype = c_int
dat_msg = {
        1: 'Dat: dubious year',
        -1: 'minimum year allowed is -4799',
        -2: 'month must be in 1..12',
        -3: 'day is out of range for this month',
        -4: 'bad fraction of day',}
def dat(iy, im, id, fd):
    """ Calculate delta(AT) = TAI - UTC for a given UTC date.

    :param iy: UTC year.
    :type iy: int

    :param im: month.
    :type im: int

    :param id: day.
    :type id: int

    :param fd: fraction of day.
    :type fd: float

    :returns: deltat (TAI-UTC) in seconds as a float.

    :raises: :exc:`ValueError` if *iy*, *im*, *id* or *fd* are not in valid ranges.

        :exc:`UserWarning` if the value predates the
        introduction of UTC or is too far in the future to be
        trusted.

    .. seealso:: |MANUAL| page 59
    """
    deltat = c_double()
    s = _sofa.iauDat(iy, im, id, fd, byref(deltat))
    if s < 0:
        raise ValueError(dat_msg[s])
    elif s > 0:
        warnings.warn(dat_msg[s], UserWarning, 2)
    return deltat.value


# iauDtdb
_sofa.iauDtdb.argtypes = [c_double, #date1,
                            c_double, #date2
                            c_double, #ut
                            c_double, #elong
                            c_double, #u
                            c_double] #v
_sofa.iauDtdb.restype = c_double
def dtdb(date1, date2, ut, elong, u, v):
    """ Approximation of TDB - TT, the difference between barycentric dynamical
    time and terrestrial time, for an observer on Earth.

    :param date1, date2: TDB as a two-part date.
    :type date1, date2: float

    :param ut: universal time (UT1, fraction of one day).
    :type ut: float

    :param elong: longitude in radians (east positive)
    :type elong: float

    :param u: distance from Earth's spin axis in kilometers.
    :type u: float

    :param v: distance north of equatorial plane in kilometers
    :type v: float

    :returns: TDB - TT in seconds (float)

    .. seealso:: |MANUAL| page 61
    """
    return _sofa.iauDtdb(date1, date2, ut, float(elong), u, v)


# iauDtf2d
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauDtf2d.argtypes = [POINTER(c_char), #scale
                            c_int, #iy
                            c_int, #im
                            c_int, #id
                            c_int, #ihr
                            c_int, #imn
                            c_double, #sec
                            POINTER(c_double), #d1
                            POINTER(c_double)] #d2
    _sofa.iauDtf2d.restype = c_int
except AttributeError:
    pass
dtf2d_msg = {
        3: 'Dtf2d: dubious year and time is after end of day',
        2: 'Dtf2d: time is after end of day',
        1: 'Dtf2d: dubious year',
        -1: 'minimum year allowed is -4799',
        -2: 'month must be in 1..12',
        -3: 'day is out of range for this month',
        -4: 'hour must be in 0..23',
        -5: 'minute must be in 0..59',
        -6: 'second < 0',}
def dtf2d(scale, iy, im, id, ihr, imn, sec):
    """ Encode date and time fields into a two-part Julian Date.

    :param scale: Timescale id.
    :type scale: str

    :param iy: year.
    :type iy: int

    :param im: month.
    :type im: int

    :param id: day.
    :type id: int

    :param ihr: hour.
    :type ihr: int

    :param imn: minute.
    :type imn: int

    :param sec: seconds.
    :type sec: float

    :returns: the two-part Julian Date as a tuple of floats.

    :raises: :exc:`ValueError` if supplied values for *iy*, *im*, etc. are outside
        their valid range.

        :exc:`UserWarning` if the value predates the
        introduction of UTC or is too far in the future to be
        trusted.

    .. seealso:: |MANUAL| page 64
    """

    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    d1 = c_double()
    d2 = c_double()
    s = _sofa.iauDtf2d(scale, iy, im, id, ihr, imn, sec, byref(d1), byref(d2))
    if s < 0:
        raise ValueError(dtf2d_msg[s])
    elif s > 0:
        warnings.warn(dtf2d_msg[s], UserWarning, 2)
    return d1.value, d2.value



# iauEe00
_sofa.iauEe00.argtypes = [c_double, #date1
                            c_double, #date2
                            c_double, # epsa
                            c_double] #dpsi
_sofa.iauEe00.restype = c_double
def ee00(date1, date2, epsa, dpsi):
    """ The equation of the equinoxes, compatible with IAU 2000 resolutions,
    given the nutation in longitude and the mean obliquity.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :param epsa: mean obliquity.
    :type epsa: float

    :param dpsi: nutation in longitude.
    :type dpsi: float

    :returns: equation of the equinoxes (float).

    .. seealso:: |MANUAL| page 66
    """
    return _sofa.iauEe00(date1, date2, float(epsa), float(dpsi))

# iauEe00a
_sofa.iauEe00a.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauEe00a.restype = c_double
def ee00a(date1, date2):
    """ Equation of the equinoxes, compatible with IAU 2000 resolutions.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: equation of the equinoxes (float)

    .. seealso:: |MANUAL| page 67
    """
    return _sofa.iauEe00a(date1, date2)


# iauEe00b
_sofa.iauEe00b.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauEe00b.restype = c_double
def ee00b(date1, date2):
    """ Equation of the equinoxes, compatible with IAU 2000 resolutions, using
    truncated nutation model IAU 2000B.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: equation of the equinoxes (float)

    .. seealso:: |MANUAL| page 68
    """
    return _sofa.iauEe00b(date1, date2)


# iauEe06a
_sofa.iauEe06a.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauEe06a.restype = c_double
def ee06a(date1, date2):
    """ Equation of the equinoxes, compatible with IAU 2000 resolutions and
    IAU 2006/2000A precession-nutation.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: equation of the equinoxes (float)

    .. seealso:: |MANUAL| page 69
    """
    return _sofa.iauEe06a(date1, date2)


# iauEect00
_sofa.iauEect00.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauEect00.restype = c_double
def eect00(date1, date2):
    """ Equation of the equinoxes complementary terms, consistent with IAU
    2000 resolutions.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: complementary terms (float).

    .. seealso:: |MANUAL| page 70
    """
    return _sofa.iauEect00(date1, date2)


# iauEform
_sofa.iauEform.argtypes = [c_int, #n
                            POINTER(c_double), #a
                            POINTER(c_double)] #f
_sofa.iauEform.restype = c_int
def eform(n):
    """ Earth's reference ellipsoids.

    :param n: ellipsoid identifier, should be one of:

        #. WGS84
        #. GRS80
        #. WGS72
    :type n: int

    :returns: a tuple of two items:

        * equatorial radius in meters (float)
        * flattening (float)

    .. seealso:: |MANUAL| page 72
    """
    a = c_double()
    f = c_double()
    s = _sofa.iauEform(n, byref(a), byref(f))
    if s != 0:
        raise ValueError('illegal ellipsoid identifier')
    return a.value, f.value


# iauEo06a
_sofa.iauEo06a.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauEo06a.restype = c_double
def eo06a(date1, date2):
    """ Equation of the origins, IAU 2006 precession and IAU 2000A nutation.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: equation of the origins in radians (float).

    .. seealso:: |MANUAL| page 73
    """
    return _sofa.iauEo06a(date1, date2)


# iauEors
_sofa.iauEors.argtypes = [ndpointer(shape=(3,3), dtype=float), #rnpb
                            c_double] #s
_sofa.iauEors.restype = c_double
def eors(rnpb, s):
    """ Equation of the origins, given the classical NPB matrix and the
    quantity s.

    :param rnpb: classical nutation x precession x bias matrix.
    :type rnpb: array-like of shape (3,3)

    :param s: the CIO locator.
    :type s: float

    :returns: the equation of the origins in radians (float).

    .. seealso:: |MANUAL| page 74
    """
    return _sofa.iauEors(asmatrix(rnpb, dtype=float), float(s))


# iauEpb
_sofa.iauEpb.argtypes = [c_double, #dj1
                        c_double] #dj2
_sofa.iauEpb.restype = c_double
def epb(dj1, dj2):
    """ Julian date to Besselian epoch.

    :param dj1, dj2: two-part Julian date.
    :type date1, date2: float

    :returns: Besselian epoch (float).

    .. seealso:: |MANUAL| page 75
    """
    return _sofa.iauEpb(dj1, dj2)


# iauEpb2jd
_sofa.iauEpb2jd.argtypes = [c_double, #epb
                            POINTER(c_double), #djm0
                            POINTER(c_double)] #djm
def epb2jd(epb):
    """ Besselian epoch to Julian date.

    :param epb: Besselian epoch.
    :type epb: float

    :returns: a tuple of two items:

        * MJD zero-point, always 2400000.5 (float)
        * modified Julian date (float).

    .. seealso:: |MANUAL| page 76
    """
    djm0 = c_double()
    djm = c_double()
    _sofa.iauEpb2jd(epb, byref(djm0), byref(djm))
    return djm0.value, djm.value


# iauEpj
_sofa.iauEpj.argtypes = [c_double, #dj1
                        c_double] #dj2
_sofa.iauEpj.restype = c_double
def epj(dj1, dj2):
    """ Julian date to Julian epoch.

    :param dj1, dj2: two-part Julian date.
    :type dj1, dj2: float

    :returns: Julian epoch (float)

    .. seealso:: |MANUAL| page 77
    """
    return _sofa.iauEpj(dj1, dj2)


# iauEpj2jd
_sofa.iauEpj2jd.argtypes = [c_double, #epj
                POINTER(c_double), #djm0
                POINTER(c_double)] #djm
def epj2jd(epj):
    """ Julian epoch to Julian date.

    :param epj: Julian epoch.
    :type epj: float

    :returns: a tuple of two items:

        * MJD zero-point, always 2400000.5 (float)
        * modified Julian date (float).

    .. seealso:: |MANUAL| page 78
    """
    djm0 = c_double()
    djm = c_double()
    _sofa.iauEpj2jd(epj, byref(djm0), byref(djm))
    return djm0.value, djm.value


# iauEpv00
_sofa.iauEpv00.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(2,3), dtype=float), #pvh
                            ndpointer(shape=(2,3), dtype=float)] # pvb
_sofa.iauEpv00.restype = c_int
epv00_msg = {
            1: 'Epv00: date outside the range 1900-2100 AD',
            }
def epv00(date1, date2):
    """ Earth position and velocity, heliocentric and barycentric, with
    respect to the Barycentric Celestial Reference System.

    :param date1, date2: TDB as a two-part Julian date.
    :type date1, date2: float

    :returns: a tuple of two items:

        * heliocentric Earth position velocity as a numpy.matrix of shape \
           2x3.
        * barycentric Earth position/velocity as a numpy.matrix of shape \
           2x3.

    :raises: :exc:`UserWarning` if the date falls outside the range 1900-2100.

    .. seealso:: |MANUAL| page 79
    """
    pvh = asmatrix(zeros(shape=(2,3), dtype=float))
    pvb = asmatrix(zeros(shape=(2,3), dtype=float))
    s = _sofa.iauEpv00(date1, date2, pvh, pvb)
    if s != 0:
        warnings.warn(epv00_msg[s], UserWarning, 2)
    return pvh, pvb


# iauEqeq94
_sofa.iauEqeq94.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauEqeq94.restype = c_double
def eqeq94(date1, date2):
    """ Equation of the equinoxes, IAU 1994 model.

    :param date1, date2: TDB as a two-part Julian date.
    :type date1, date2: float

    :returns: equation of the equinoxes (float).

    .. seealso:: |MANUAL| page 81
    """
    return _sofa.iauEqeq94(date1, date2)


# iauEra00
_sofa.iauEra00.argtypes = [c_double, #dj1
                            c_double] #dj2
_sofa.iauEra00.restype = c_double
def era00(dj1, dj2):
    """ Earth rotation angle IAU 2000 model.

    :param dj1, dj2: UT1 as a two-part Julian date.
    :type dj1, dj2: float

    :returns: Earth rotation angle in radians, in the range 0-2pi (float).

    .. seealso:: |MANUAL| page 82
    """
    return _sofa.iauEra00(dj1, dj2)


# iauFad03
_sofa.iauFad03.argtypes = [c_double] #t
_sofa.iauFad03.restype = c_double
def fad03(t):
    """ Mean elongation of the Moon from the Sun (fundamental argument, IERS
    conventions 2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean elongation of the Moon from the Sun in radians (float).

    .. seealso:: |MANUAL| page 83
    """
    return _sofa.iauFad03(t)


# iauFae03
_sofa.iauFae03.argtypes = [c_double] #t
_sofa.iauFae03.restype = c_double
def fae03(t):
    """ Mean longitude of Earth (fundamental argument, IERS conventions 2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean longitude of Earth in radians (float).

    .. seealso:: |MANUAL| page 84
    """
    return _sofa.iauFae03(t)


# iauFaf03
_sofa.iauFaf03.argtypes = [c_double] #t
_sofa.iauFaf03.restype = c_double
def faf03(t):
    """ Mean longitude of the Moon minus mean longitude of the ascending node
    (fundamental argument, IERS conventions 2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: result in radians (float).

    .. seealso:: |MANUAL| page 85
    """
    return _sofa.iauFaf03(t)


# iauFaju03
_sofa.iauFaju03.argtypes = [c_double] #t
_sofa.iauFaju03.restype = c_double
def faju03(t):
    """ Mean longitude of Jupiter (fundamental argument, IERS conventions
    2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean longitude of Jupiter in radians (float).

    .. seealso:: |MANUAL| page 86
    """
    return _sofa.iauFaju03(t)


# iauFal03
_sofa.iauFal03.argtypes = [c_double] #t
_sofa.iauFal03.restype = c_double
def fal03(t):
    """ Mean anomaly of the Moon (fundamental argument, IERS conventions
    2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean anomaly of the Moon in radians (float).

    .. seealso:: |MANUAL| page 87
    """
    return _sofa.iauFal03(t)


# iauFalp03
_sofa.iauFalp03.argtypes = [c_double] #t
_sofa.iauFalp03.restype = c_double
def falp03(t):
    """ Mean anomaly of the Sun (fundamental argument, IERS conventions
    2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean anomaly of the Sun in radians (float).

    .. seealso:: |MANUAL| page 88
    """
    return _sofa.iauFalp03(t)


# iauFama03
_sofa.iauFama03.argtypes = [c_double] #t
_sofa.iauFama03.restype = c_double
def fama03(t):
    """ Mean longitude of Mars (fundamental argument, IERS conventions
    2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean longitude of Mars in radians (float).

    .. seealso:: |MANUAL| page 89
    """
    return _sofa.iauFama03(t)


# iauFame03
_sofa.iauFame03.argtypes = [c_double] #t
_sofa.iauFame03.restype= c_double
def fame03(t):
    """ Mean longitude of Mercury (fundamental argument, IERS conventions
    2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean longitude of Mercury in radians (float).

    .. seealso:: |MANUAL| page 90
    """
    return _sofa.iauFame03(t)


# iauFane03
_sofa.iauFane03.argtypes = [c_double] #t
_sofa.iauFane03.restype = c_double
def fane03(t):
    """ Mean longitude of Neptune (fundamental argument, IERS conventions
    2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean longitude of Neptune in radians (float).

    .. seealso:: |MANUAL| page 91
    """
    return _sofa.iauFane03(t)


# iauFaom03
_sofa.iauFaom03.argtypes = [c_double] #t
_sofa.iauFaom03.restype = c_double
def faom03(t):
    """ Mean longitude of the Moon's ascending node (fundamental argument,
    IERS conventions 2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean longitude of of the Moon's ascending node in radians
        (float).

    .. seealso:: |MANUAL| page 92
    """
    return _sofa.iauFaom03(t)


# iauFapa03
_sofa.iauFapa03.argtypes = [c_double] #t
_sofa.iauFapa03.restype = c_double
def fapa03(t):
    """ General accumulated precession in longitude (fundamental argument,
    IERS conventions 2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: general accumulated precession in longitude in radians
        (float).

    .. seealso:: |MANUAL| page 93
    """
    return _sofa.iauFapa03(t)


# iauFasa03
_sofa.iauFasa03.argtypes = [c_double] #t
_sofa.iauFasa03.restype = c_double
def fasa03(t):
    """ Mean longitude of Saturn (fundamental argument, IERS conventions
    2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean longitude of Saturn in radians (float).

    .. seealso:: |MANUAL| page 94
    """
    return _sofa.iauFasa03(t)


# iauFaur03
_sofa.iauFaur03.argtypes = [c_double] #t
_sofa.iauFaur03.restype = c_double
def faur03(t):
    """ Mean longitude of Uranus (fundamental argument, IERS conventions
    2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean longitude of Uranus in radians (float).

    .. seealso:: |MANUAL| page 95
    """
    return _sofa.iauFaur03(t)


# iauFave03
_sofa.iauFave03.argtypes = [c_double] #t
_sofa.iauFave03.restype = c_double
def fave03(t):
    """ Mean longitude of Venus (fundamental argument, IERS conventions
    2003).

    :param t: TDB in Julian centuries since J2000.0
    :type t: float

    :returns: mean longitude of Venus in radians (float).

    .. seealso:: |MANUAL| page 96
    """
    return _sofa.iauFave03(t)


# iauFk52h
_sofa.iauFk52h.argtypes = [c_double, #r5
                            c_double, #d5
                            c_double, #dr5
                            c_double, #dd5
                            c_double, #px5
                            c_double, #rv5
                            POINTER(c_double), #rh
                            POINTER(c_double), #dh
                            POINTER(c_double), #drh
                            POINTER(c_double), #ddh
                            POINTER(c_double), #pxh
                            POINTER(c_double)] #rvh
def fk52h(r5, d5, dr5, dd5, px5, rv5):
    """ Transform FK5 (J2000.0) star data into the Hipparcos system.

    :param r5: right ascension in radians.
    :type r5: float

    :param d5: declination in radians.
    :type d5: float

    :param dr5: proper motion in RA (dRA/dt, rad/Jyear).
    :type dr5: float

    :param dd5: proper motion in Dec (dDec/dt, rad/Jyear).
    :type dd5: float

    :param px5: parallax (arcseconds)
    :type px5: float

    :param rv5: radial velocity (km/s, positive = receding)
    :type rv5: float

    :returns: a tuple of six items corresponding to Hipparcos epoch J2000.0:

        * right ascension
        * declination
        * proper motion in RA (dRa/dt, rad/Jyear)
        * proper motion in Dec (dDec/dt, rad/Jyear)
        * parallax in arcseconds
        * radial velocity (km/s, positive = receding).

    .. seealso:: |MANUAL| page 97
    """
    rh = c_double()
    dh = c_double()
    drh = c_double()
    ddh = c_double()
    pxh = c_double()
    rvh = c_double()
    _sofa.iauFk52h(float(r5), float(d5), float(dr5), float(dd5), float(px5),
                    float(rv5),
                    byref(rh), byref(dh), byref(drh), byref(ddh),
                    byref(pxh), byref(rvh))
    return rh.value, dh.value, drh.value, ddh.value, pxh.value, rvh.value


# iauFk5hip
_sofa.iauFk5hip.argtypes = [ndpointer(shape=(3,3), dtype=float), #r5h
                            ndpointer(shape=(1,3), dtype=float)] #s5h
def fk5hip():
    """ FK5 to Hipparcos rotation and spin.

    :returns: a tuple of two items:

        * FK5 rotation wrt Hipparcos as a numpy.matrix of shape 3x3
        * FK5 spin wrt Hipparcos as a numpy.matrix of shape 1x3

    .. seealso:: |MANUAL| page 98
    """
    r5h = asmatrix(zeros(shape=(3,3), dtype=float))
    s5h = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauFk5hip(r5h, s5h)
    return r5h, s5h


# iauFk5hz
_sofa.iauFk5hz.argtypes = [c_double, #r5
                            c_double, #d5
                            c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #rh
                            POINTER(c_double)] #dh
def fk5hz(r5, d5, date1, date2):
    """ Transform an FK5 (J2000.0) star position into the system of the
    Hipparcos catalogue, assuming zero Hipparcos proper motion.

    :param r5: right ascension in radians, equinox J2000.0, at date.
    :type r5: float

    :param d5: declination in radians, equinox J2000.0, at date.
    :type d5: float

    :param date1, date2: TDB date as a two-part Julian date.
    :type date1, date2: float

    :returns: a tuple of two items:

        * Hipparcos right ascension in radians (float)
        * Hipparcos declination in radians (float).

    .. seealso:: |MANUAL| page 99
    """
    rh = c_double()
    dh = c_double()
    _sofa.iauFk5hz(float(r5), float(d5), date1, date2, byref(rh), byref(dh))
    return rh.value, dh.value


# iauFw2m
_sofa.iauFw2m.argtypes = [c_double, #gamb
                            c_double, #phib
                            c_double, #psi
                            c_double, #eps
                            ndpointer(shape=(3,3), dtype=float)] #r
def fw2m(gamb, phib, psi, eps):
    """ Form rotation matrix given the Fukushima-Williams angles.

    :param gamb: F-W angle gamma_bar in radians.
    :type gamb: float

    :param phib: F-W angle phi_bar in radians.
    :type phib: float

    :param psi: F-W angle psi in radians.
    :type psi: float

    :param eps: F-W angle epsilon in radians.
    :type epsilon: float

    :returns: rotation matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 101
    """
    r = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauFw2m(float(gamb), float(phib), float(psi), float(eps), r)
    return r


# iauFw2xy
_sofa.iauFw2xy.argtypes = [c_double, #gamb
                            c_double, #phib
                            c_double, #psi
                            c_double, #eps
                            POINTER(c_double), #x
                            POINTER(c_double)] #y
def fw2xy(gamb, phib, psi, eps):
    """ CIP X and Y given Fukushima-Williams bias-precession-nutation angles.

    :param gamb: F-W angle gamma_bar in radians.
    :type gamb: float

    :param phib: F-W angle phi_bar in radians.
    :type phib: float

    :param psi: F-W angle psi in radians.
    :type psi: float

    :param eps: F-W angle epsilon in radians.
    :type epsilon: float

    :returns: a tuple containing CIP X and X in radians (float).

    .. seealso:: |MANUAL| page 103
    """
    x = c_double()
    y = c_double()
    _sofa.iauFw2xy(float(gamb), float(phib), float(psi), float(eps),
                                                        byref(x), byref(y))
    return x.value, y.value


# iauGc2gd
_sofa.iauGc2gd.argtypes = [c_int, #n
                            ndpointer(shape=(1,3), dtype=float), #xyz
                            POINTER(c_double), #elong
                            POINTER(c_double), #phi
                            POINTER(c_double)] #height
_sofa.iauGc2gd.restype = c_int
gc2gd_msg = {
        -1: 'Gc2gd: illegal ellipsoid identifier',
        }
def gc2gd(n, xyz):
    """ Transform geocentric coordinates to geodetic using the specified
    reference ellipsoid.

    :param n: ellipsoid identifier, should be one of:

        #. WGS84
        #. GRS80
    :type n: int

    :param xyz: geocentric vector.
    :type xyz: array-like of shape (1,3)

    :returns: a tuple of three items:

        * longitude in radians (float)
        * geodetic latitude in radians (float)
        * geodetic height above ellipsoid (float).

    :raises: :exc:`ValueError` for invalid ellipsoid identifier.

    .. seealso:: |MANUAL| page 104
    """
    elong = c_double()
    phi = c_double()
    height = c_double()
    s = _sofa.iauGc2gd(n, asmatrix(xyz, dtype=float), byref(elong),
                            byref(phi), byref(height))
    if s != 0:
        raise ValueError(gc2gd_msg[s])
    return elong.value, phi.value, height.value


# iauGc2gde
_sofa.iauGc2gde.argtypes = [c_double, #a
                            c_double, #f
                            ndpointer(shape=(1,3), dtype=float), #xyz
                            POINTER(c_double), #elong
                            POINTER(c_double), #phi
                            POINTER(c_double)] #height
_sofa.iauGc2gde.restype = c_int
gc2gde_msg = {
        -1: 'Gc2gde: illegal value for flattening',
        -2: 'Gc2gde: illegal value for equatorial radius',
        }
def gc2gde(a, f, xyz):
    """ Transform geocentric coordinates to geodetic for a reference
    ellipsoid of specified form.

    :param a: equatorial radius.
    :type a: float

    :param f: flattening.
    :type f: float

    :param xyz: geocentric vector.
    :type xyz: array-like of shape (1,3)

    :returns: a tuple of three items:

        * longitude in radians
        * geodetic latitude in radians
        * geodetic height above ellipsoid

    :raises: :exc:`ValueError` if supplied values for *a* or *f* are nor valid.

    .. seealso:: |MANUAL| page 105
    """
    elong = c_double()
    phi = c_double()
    height = c_double()
    s = _sofa.iauGc2gde(a, f, asmatrix(xyz, dtype=float), byref(elong),
                                byref(phi), byref(height))
    if s != 0:
        raise ValueError(gc2gde_msg[s])
    return elong.value, phi.value, height.value


# iauGd2gc
_sofa.iauGd2gc.argtypes = [c_int, #n
                            c_double, #elong
                            c_double, #phi,
                            c_double, #height
                            ndpointer(shape=(1,3), dtype=float)] #xyz
_sofa.iauGd2gc.restype = c_int
gd2gc_msg = {
        -1: 'invalid ellipsoid identifier',
        -2: 'illegal case',
        }
def gd2gc(n, elong, phi, height):
    """ Transform geodetic coordinates to geocentric using specified reference
    ellipsoid.

    :param n: ellipsoid identifier, should be one of:

        #. WGS84
        #. GRS80
        #. WGS72
    :type n: int

    :param elong: longitude in radians.
    :type elong: float

    :param phi: geodetic latitude in radians.
    :type phi: float

    :param height: geodetic height above ellipsoid in meters.
    :type height: float

    :returns: geocentric vector as a numpy.matrix of shape 1x3.

    :raises: :exc:`ValueError` in case of invalid ellipsoid identifier or
        invalid coordinate values.

    .. seealso:: |MANUAL| page 106
    """
    xyz = asmatrix(zeros(shape=(1,3), dtype=float))
    s = _sofa.iauGd2gc(n, float(elong), float(phi), height, xyz)
    if s != 0:
        raise ValueError(gd2gc_msg[s])
    return xyz


# iauGd2gce
_sofa.iauGd2gce.argtypes = [c_double, #a
                            c_double, #f
                            c_double, #elong
                            c_double, #phi
                            c_double, #height
                            ndpointer(shape=(1,3), dtype=float)] #xyz
_sofa.iauGd2gce.restype = c_int
gd2gce_msg = {
        -1: 'illegal case'
        }
def gd2gce(a, f, elong, phi, height):
    """ Transform geodetic coordinates to geocentric for a reference
    ellipsoid of specified form.

    :param a: equatorial radius.
    :type a: float

    :param f: flattening.
    :type f: float

    :param elong: longitude in radians.
    :type elong: float

    :param phi: geodetic latitude in radians.
    :type phi: float

    :param height: geodetic height above ellipsoid in meters.
    :type height: float

    :returns: geocentric vector as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 107
    """
    xyz = asmatrix(zeros(shape=(1,3), dtype=float))
    s = _sofa.iauGd2gce(a, f, float(elong), float(phi), height, xyz)
    if s != 0:
        raise ValueError(gd2gce_msg[s])
    return xyz


# iauGmst00
_sofa.iauGmst00.argtypes = [c_double, #uta
                            c_double, #utb
                            c_double, #tta
                            c_double] #ttb
_sofa.iauGmst00.restype = c_double
def gmst00(uta, utb, tta, ttb):
    """ Greenwich mean sidereal time, consistent with IAU 2000 resolutions.

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :param tta, ttb: TT as a two-part Julian date.
    :type tta, ttb: float

    :returns: Greenwich mean sidereal time in radians (float).

    .. seealso:: |MANUAL| page 108
    """
    return _sofa.iauGmst00(uta, utb, tta, ttb)


# iauGmst06
_sofa.iauGmst06.argtypes = [c_double, #uta
                            c_double, #utb
                            c_double, #tta
                            c_double] #ttb
_sofa.iauGmst06.restype = c_double
def gmst06(uta, utb, tta, ttb):
    """ Greenwich mean sidereal time, consistent with IAU 2006 precession.

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :param tta, ttb: TT as a two-part Julian date.
    :type tta, ttb: float

    :returns: Greenwich mean sidereal time in radians (float).

    .. seealso:: |MANUAL| page 110
    """
    return _sofa.iauGmst06(uta, utb, tta, ttb)


# iauGmst82
_sofa.iauGmst82.argtypes = [c_double, #dj1
                            c_double] #dj2
_sofa.iauGmst82.restype = c_double
def gmst82(dj1, dj2):
    """ Greenwich mean sidereal time, IAU 1982 model.

    :param dj1, dj2: UT1 as a two-part Julian date.
    :type uta, utb: float

    :returns: Greenwich mean sidereal time in radians (float).

    .. seealso:: |MANUAL| page 111
    """
    return _sofa.iauGmst82(dj1, dj2)


# iauGst00a
_sofa.iauGst00a.argtypes = [c_double, #uta
                            c_double, #utb
                            c_double, #tta
                            c_double] #ttb
_sofa.iauGst00a.restype = c_double
def gst00a(uta, utb, tta, ttb):
    """ Greenwich apparent sidereal time, consistent with IAU 2000 resolutions.

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :param tta, ttb: TT as a two-part Julian date.
    :type tta, ttb: float

    :returns: Greenwich apparent sidereal time in radians (float).

    .. seealso:: |MANUAL| page 112
    """
    return _sofa.iauGst00a(uta, utb, tta, ttb)


# iauGst00b
_sofa.iauGst00b.argtypes = [c_double, #uta
                            c_double] #utb
_sofa.iauGst00b.restype = c_double
def gst00b(uta, utb):
    """ Greenwich apparent sidereal time, consistent with IAU 2000 resolutions,
    using truncated nutation model IAU 2000B.

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :returns: Greenwich apparent sidereal time in radians (float).

    .. seealso:: |MANUAL| page 114
    """
    return _sofa.iauGst00b(uta, utb)


# iauGst06
_sofa.iauGst06.argtypes = [c_double, #uta
                            c_double, #utb
                            c_double, #tta
                            c_double, #ttb
                            ndpointer(shape=(3,3), dtype=float)] #rnpb
_sofa.iauGst06.restype = c_double
def gst06(uta, utb, tta, ttb, rnpb):
    """ Greenwich apparent sidereal time, IAU 2006, given the *npb* matrix.

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :param tta, ttb: TT as a two-part Julian date.
    :type tta, ttb: float

    :param rnpb: nutation x precession x bias matrix.
    :type rnpb: array-like of shape (3,3)

    :returns: Greenwich apparent sidereal time in radians (float).

    .. seealso:: |MANUAL| page 116
    """
    return _sofa.iauGst06(uta, utb, tta, ttb, asmatrix(rnpb, dtype=float))


# iauGst06a
_sofa.iauGst06a.argtypes = [c_double, #uta
                            c_double, #utb
                            c_double, #tta
                            c_double] #ttb
_sofa.iauGst06a.restype = c_double
def gst06a(uta, utb, tta, ttb):
    """ Greenwich apparent sidereal time, consistent with IAU 2000 and 2006
    resolutions.

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :param tta, ttb: TT as a two-part Julian date.
    :type tta, ttb: float

    :returns: Greenwich apparent sidereal time in radians (float).

    .. seealso:: |MANUAL| page 117
    """
    return _sofa.iauGst06a(uta, utb, tta, ttb)


# iauGst94
_sofa.iauGst94.argtypes = [c_double, #uta
                            c_double] #utb
_sofa.iauGst94.restype = c_double
def gst94(uta, utb):
    """ Greenwich apparent sidereal time, consistent with IAU 1982/94
    resolutions.

    :param uta, utb: UT1 as a two-part Julian date.
    :type uta, utb: float

    :returns: Greenwich apparent sidereal time in radians (float).

    .. seealso:: |MANUAL| page 118
    """
    return _sofa.iauGst94(uta, utb)


# iauH2fk5
_sofa.iauH2fk5.argtypes = [c_double, #rh
                            c_double, #dh
                            c_double, #drh
                            c_double, #ddh
                            c_double, #pxh
                            c_double, #rvh
                            POINTER(c_double), #r5
                            POINTER(c_double), #d5
                            POINTER(c_double), #dr5
                            POINTER(c_double), #dd5
                            POINTER(c_double), #px5
                            POINTER(c_double)] #rv5
def h2fk5(rh, dh, drh, ddh, pxh, rvh):
    """ Transform Hipparcos star data into FK5 (J2000.0) system.

    :param rh: right ascension in radians.
    :type rh: float

    :param dh: declination in radians.
    :type dh: float

    :param drh: proper motion in RA (dRA/dt, rad/Jyear).
    :type drh: float

    :param ddh: proper motion in Dec (dDec/dt, rad/Jyear).
    :type ddh: float

    :param pxh: parallax in arcseconds.
    :type pxh: float

    :param rvh: radial velocity (km/s, positive = receding).
    :type rvh: float

    :returns: a tuple of six items:

        * right ascension in radians
        * declination in radians
        * proper motion in RA (dRA/dt, rad/Jyear)
        * proper motion in Dec (dDec/dt, rad/Jyear)
        * parallax in arcseconds
        * radial velocity (km/s, positive = receding).

    .. seealso:: |MANUAL| page 119
    """
    r5 = c_double()
    d5 = c_double()
    dr5 = c_double()
    dd5 = c_double()
    px5 = c_double()
    rv5 = c_double()
    _sofa.iauH2fk5(float(rh), float(dh), float(drh), float(ddh),
                    float(pxh), float(rvh), byref(r5), byref(d5),
                    byref(dr5), byref(dd5), byref(px5),byref(rv5))
    return r5.value, d5.value, dr5.value, dd5.value, px5.value, rv5.value


# iauHfk5z
_sofa.iauHfk5z.argtypes = [c_double, #rh
                            c_double, #dh
                            c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #r5
                            POINTER(c_double), #d5
                            POINTER(c_double), #dr5
                            POINTER(c_double)] #dd5
def hfk5z(rh, dh, date1, date2):
    """ Transform Hipparcos star position into FK5 (J2000.0), assuming
    zero Hipparcos proper motion.

    :param rh: right ascension in radians.
    :type rh: float

    :param dh: declination in radians.
    :type dh: float

    :param date1, date2: TDB as a two-part Julian date.
    :type date1, date2: float

    :returns: a tuple of four items:

        * right ascension in radians
        * declination in radians
        * proper motion in RA (rad/year)
        * proper motion in Dec (rad/year)

    .. seealso:: |MANUAL| page 120
    """
    r5 = c_double()
    d5 = c_double()
    dr5 = c_double()
    dd5 = c_double()
    _sofa.iauHfk5z(float(rh), float(dh), date1, date2, byref(r5), byref(d5),
                                                    byref(dr5), byref(dd5))
    return r5.value, d5.value, dr5.value, dd5.value


# iauIr
_sofa.iauIr.argtypes = [ndpointer(shape=(3,3), dtype=float)] #r
def ir():
    """ Create a new rotation matrix initialized to the identity matrix.

    :returns: an identity matrix as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 122
    """

    r = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauIr(r)
    return r


# iauJd2cal
_sofa.iauJd2cal.argtypes = [c_double, #dj&
                            c_double, #dj2
                            POINTER(c_int), #iy
                            POINTER(c_int), #im
                            POINTER(c_int), #id
                            POINTER(c_double)] #fd
_sofa.iauJd2cal.restype = c_int
jd2cal_msg = {
            -1: 'date outside valid range -68569.5 to 1e9',
            }
def jd2cal(dj1, dj2):
    """ Julian date to Gregorian year, month, day and fraction of day.

    :param dj1, dj2: two-part Julian date.
    :type dj1, dj2: float

    :returns: a tuple of five values:

        * year (int)
        * month (int)
        * day (int)
        * fraction of day (float)

    :raises: :exc:`ValueError` if input date is outside valid range.

    .. seealso:: |MANUAL| page 123
    """
    iy = c_int()
    im = c_int()
    id = c_int()
    fd = c_double()
    s = _sofa.iauJd2cal(dj1, dj2, byref(iy), byref(im), byref(id),
                            byref(fd))
    if s != 0:
        raise ValueError(jd2cal_msg[s])
    return iy.value, im.value, id.value, fd.value


# iauJdcalf
_sofa.iauJdcalf.argtypes = [c_int, #ndp
                            c_double, #dj1
                            c_double, #dj2
                            c_int * 4] #iymdf
_sofa.iauJdcalf.restype = c_int
jdcalf_msg = {
            -1: 'date out of range',
            1: 'Jdcalf: invalid value for "ndp", modified to be zero',
            }
def jdcalf(ndp, dj1, dj2):
    """ Julian date to Gregorian calendar, expressed in a form convenient
    for formatting messages: rounded to a specified precision.

    :param ndp: number of decimal places of days fraction.
    :type ndp: int

    :param dj1, dj2: two-part Julian date.
    :type dj1, dj2: float

    :returns: a 4-tuple containing year, month, day, fraction of day.

    :raises: :exc:`ValueError` if date is outside the valid range.

    .. seealso:: |MANUAL| page 124
    """
    iymdf = (c_int * 4)()
    s = _sofa.iauJdcalf(ndp, dj1, dj2, iymdf)
    if s < 0:
        raise ValueError(jdcalf_msg[s])
    elif s > 0:
        warnings.warn(jdcalf_msg[s], UserWarning, 2)
    return tuple([v for v in iymdf])


# iauNum00a
_sofa.iauNum00a.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rmatn
def num00a(date1, date2):
    """ Form the matrix of nutation for a given date, IAU 2000A model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: nutation matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 125
    """
    rmatn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauNum00a(date1, date2, rmatn)
    return rmatn


# iauNum00b
_sofa.iauNum00b.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rmatn
def num00b(date1, date2):
    """ Form the matrix of nutation for a given date, IAU 2000B model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: nutation matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 126
    """
    rmatn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauNum00b(date1, date2, rmatn)
    return rmatn


# iauNum06a
_sofa.iauNum06a.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rmatn
def num06a(date1, date2):
    """ Form the matrix of nutation for a given date, IAU 2006/2000A model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: nutation matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 127
    """
    rmatn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauNum06a(date1, date2, rmatn)
    return rmatn


# iauNumat
_sofa.iauNumat.argtypes = [c_double, #epsa
                            c_double, #dpsi
                            c_double, #deps
                            ndpointer(shape=(3,3), dtype=float)] #rmatn
def numat(epsa, dpsi, deps):
    """ Form the matrix of nutation.

    :param epsa: mean obliquity of date.
    :type epsa: float

    :param dpsi, deps: nutation.
    :type dpsi, deps: float

    :returns: nutation matrix as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 128
    """
    rmatn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauNumat(float(epsa), float(dpsi), float(deps), rmatn)
    return rmatn


# iauNut00a
_sofa.iauNut00a.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #dpsi
                            POINTER(c_double)] #deps
def nut00a(date1, date2):
    """ Nutation, IAU 2000A model (MHB2000 luni-solar and planetary nutation
    with free core nutation omitted).

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 2-tuple:

        * nutation in longitude in radians (float)
        * nutation in obliquity in radians (float).

    .. seealso:: |MANUAL| page 129
    """
    dpsi = c_double()
    deps = c_double()
    _sofa.iauNut00a(date1, date2, byref(dpsi), byref(deps))
    return dpsi.value, deps.value


# iauNut00b
_sofa.iauNut00b.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #dpsi
                            POINTER(c_double)] #deps
def nut00b(date1, date2):
    """ Nutation, IAU 2000B model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 2-tuple:

        * nutation in longitude in radians (float)
        * nutation in obliquity in radians (float).

    .. seealso:: |MANUAL| page 132
    """
    dpsi = c_double()
    deps = c_double()
    _sofa.iauNut00b(date1, date2, byref(dpsi), byref(deps))
    return dpsi.value, deps.value


# iauNut06a
_sofa.iauNut06a.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #dpsi
                            POINTER(c_double)] #deps
def nut06a(date1, date2):
    """ IAU 2000A nutation with adjustments to match the IAU 2006 precession.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 2-tuple:

        * nutation in longitude in radians (float)
        * nutation in obliquity in radians (float).

    .. seealso:: |MANUAL| page 134
    """
    dpsi = c_double()
    deps = c_double()
    _sofa.iauNut06a(date1, date2, byref(dpsi), byref(deps))
    return dpsi.value, deps.value


# iauNut80
_sofa.iauNut80.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #dpsi
                            POINTER(c_double)] #deps
def nut80(date1, date2):
    """ Nutation, IAU 1980 model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 2-tuple:

        * nutation in longitude in radians (float)
        * nutation in obliquity in radians (float).

    .. seealso:: |MANUAL| page 136
    """
    dpsi = c_double()
    deps = c_double()
    _sofa.iauNut80(date1, date2, byref(dpsi), byref(deps))
    return dpsi.value, deps.value


# iauNutm80
_sofa.iauNutm80.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rmatn
def nutm80(date1, date2):
    """ Form the nutation matrix for a given date, IAU 1980 model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: the nutation matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 137
    """
    rmatn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauNutm80(date1, date2, rmatn)
    return rmatn


# iauObl06
_sofa.iauObl06.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauObl06.restype = c_double
def obl06(date1, date2):
    """ Mean obliquity of the ecliptic, IAU 2006 precession model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: obliquity of the ecliptic in radians (float).

    .. seealso:: |MANUAL| page 138
    """
    return _sofa.iauObl06(date1, date2)


# iauObl80
_sofa.iauObl80.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauObl80.restype = c_double
def obl80(date1, date2):
    """ Mean obliquity of the ecliptic, IAU 1980 model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: obliquity of the ecliptic in radians (float).

    .. seealso:: |MANUAL| page 139
    """
    return _sofa.iauObl80(date1, date2)


# iauP06e
_sofa.iauP06e.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #eps0
                            POINTER(c_double), #psia
                            POINTER(c_double), #oma
                            POINTER(c_double), #bpa
                            POINTER(c_double), #bqa
                            POINTER(c_double), #pia
                            POINTER(c_double), #bpia
                            POINTER(c_double), #epsa
                            POINTER(c_double), #chia
                            POINTER(c_double), #za
                            POINTER(c_double), #zetaa
                            POINTER(c_double), #thetaa
                            POINTER(c_double), #pa
                            POINTER(c_double), #gam
                            POINTER(c_double), #phi
                            POINTER(c_double)] #psi
def p06e(date1, date2):
    """ Precession angles, IAU 2006, equinox based.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 16-tuple:

        * epsilon_0
        * psi_A
        * omega_A
        * P_A
        * Q_A
        * pi_A
        * Pi_A
        * obliquity epsilon_A
        * chi_A
        * z_A
        * zeta_A
        * theta_A
        * p_A
        * F-W angle gamma_J2000
        * F-W angle phi_J2000
        * F-W angle psi_J2000

    .. seealso:: |MANUAL| page 140
    """
    eps0 = c_double()
    psia = c_double()
    oma = c_double()
    bpa = c_double()
    bqa = c_double()
    pia = c_double()
    bpia = c_double()
    epsa = c_double()
    chia = c_double()
    za = c_double()
    zetaa = c_double()
    thetaa = c_double()
    pa = c_double()
    gam = c_double()
    phi = c_double()
    psi = c_double()
    _sofa.iauP06e(date1, date2, byref(eps0), byref(psia), byref(oma),
                    byref(bpa), byref(bqa), byref(pia), byref(bpia),
                    byref(epsa), byref(chia), byref(za), byref(zetaa),
                    byref(thetaa), byref(pa), byref(gam), byref(phi),
                    byref(psi))
    return eps0.value, psia.value, oma.value, bpa.value, bqa.value, pia.value,\
            bpia.value, epsa.value, chia.value, za.value, zetaa.value, \
            thetaa.value, pa.value, gam.value, phi.value, psi.value


# iauP2pv
_sofa.iauP2pv.argtypes = [ndpointer(shape=(1,3), dtype=float), #p
                            ndpointer(shape=(2,3), dtype=float)] #pv
def p2pv(p):
    """ Extend a p-vector to a pv-vector by appending a zero velocity.

    :param p: p-vector to extend.
    :type p: array-like of shape (1,3)

    :returns: pv-vector as a numpy.matrix of shape 2x3.

    .. seealso:: |MANUAL| page 142
    """
    pv = asmatrix(zeros(shape=(2,3), dtype=float))
    _sofa.iauP2pv(asmatrix(p, dtype=float), pv)
    return pv


# iauP2s
_sofa.iauP2s.argtypes = [ndpointer(shape=(1,3), dtype=float), #p
                        POINTER(c_double), #theta
                        POINTER(c_double), #phi
                        POINTER(c_double)] #r
def p2s(p):
    """ P-vector to spherical polar coordinates.

    :param p: the p-vector
    :type p: array-like of shape (1,3)

    :returns: a 3-tuple:

        * longitude angle in radians (float)
        * latitude angle in radians (float)
        * radial distance (float).

    .. seealso:: |MANUAL| page 143
    """
    theta = c_double()
    phi = c_double()
    r = c_double()
    _sofa.iauP2s(asmatrix(p, dtype=float), theta, phi, r)
    return theta.value, phi.value, r.value


# iauPap
_sofa.iauPap.argtypes = [ndpointer(shape=(1,3), dtype=float), #a
                        ndpointer(shape=(1,3), dtype=float)] #b
_sofa.iauPap.restype = c_double
def pap(a, b):
    """ Position-angle from two p-vectors.

    :param a: direction of the reference point.
    :type a: array-like of shape (1,3)

    :param b: direction of point whose position angle is required.
    :type b: array-like of shape (1,3)

    :returns: position angle of *b* with respect to *a* in radians (float).

    .. seealso:: |MANUAL| page 144
    """
    return _sofa.iauPap(asmatrix(a, dtype=float), asmatrix(b, dtype=float))


# iauPas
_sofa.iauPas.argtypes = [c_double, #al
                        c_double, #ap
                        c_double, #bl
                        c_double] #bp
_sofa.iauPas.restype = c_double
def pas(al, ap, bl,bp):
    """ Postion-angle from spherical coordinates.

    :param al: longitude of point A in radians.
    :type al: float

    :param ap: latitude of point A in radians.
    :type ap: float

    :param bl: longitude of point B in radians.
    :type bl: float

    :param bp: latitude of point B in radians.
    :type bp: float

    :returns: position angle of B with respect to A in radians (float).

    .. seealso:: |MANUAL| page 145
    """
    return _sofa.iauPas(float(al), float(ap), float(bl), float(bp))


# iauPb06
_sofa.iauPb06.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #bzeta
                            POINTER(c_double), #bz
                            POINTER(c_double)] #btheta
def pb06(date1, date2):
    """ Form the three Euler angles which implement general precession from
    epoch J2000.0, using IAU 2006 model. Frame bias is included.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 3-tuple:

        * 1st rotation: radians cw around z (float)
        * 3rd rotation: radians cw around z (float)
        * 2nd rotation: radians ccw around y.

    .. seealso:: |MANUAL| page 146
    """
    bzeta = c_double()
    bz = c_double()
    btheta = c_double()
    _sofa.iauPb06(date1, date2, bzeta, bz, btheta)
    return bzeta.value, bz.value, btheta.value


# iauPdp
_sofa.iauPdp.argtypes = [ndpointer(shape=(1,3), dtype=float), #a
                        ndpointer(shape=(1,3), dtype=float)] #b
_sofa.iauPdp.restype = c_double
def pdp(a, b):
    """ P-vector inner product.

    :param a: first p-vector.
    :type a: array-like of shape (1,3)

    :param b: second p-vector.
    :type b: array-like of shape (1,3)

    :returns: a dot b as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 147
    """
    return _sofa.iauPdp(asmatrix(a, dtype=float), asmatrix(b, dtype=float))


# iauPfw06
_sofa.iauPfw06.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #gamb
                            POINTER(c_double), #phib
                            POINTER(c_double), #psib
                            POINTER(c_double)] #epsa
def pfw06(date1, date2):
    """ Precession angles, IAU 2006 (Fukushima-Williams 4-angle formulation).

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 4-tuple:

        * F-W angle gamma_bar in radians (float)
        * F-W angle phi_bar in radians (float)
        * F-W angle psi_bar in radians (float)
        * F-W angle epsilon_A in radians (float).

    .. seealso:: |MANUAL| page 148
    """
    gamb = c_double()
    phib = c_double()
    psib = c_double()
    epsa = c_double()
    _sofa.iauPfw06(date1, date2, gamb, phib, psib, epsa)
    return gamb.value, phib.value, psib.value, epsa.value


# iauPlan94
_sofa.iauPlan94.argtypes = [c_double, #date1
                            c_double, #date2
                            c_int, #np
                            ndpointer(shape=(2,3), dtype=float)] #pv
_sofa.iauPlan94.restype = c_int
plan94_msg = {
            -1: 'illegal planet identifier',
            1: 'Plan94: year outside the range 1000-3000',
            2: 'Plan94: failed to converge'
            }
def plan94(date1, date2, np):
    """ Approximate heliocentric position and velocity of a nominated major
    planet : Mercury, Venus, EMB, Mars, Jupiter, Saturn, Uranus or Neptune.

    :param date1, date2: TDB as a two-part Julian date.
    :type date1, date2: float

    :param np: planet identifier (1=Mercury, 2=Venus, 3=EMB, 4=Mars, 5=Jupiter,
                                6=Saturn, 7=Uranus, 8=Neptune).
    :type np: int

    :returns: planet's position and velocity (heliocentric, J2000.0, AU, AU/d) as \
            a numpy.matrix of shape 2x3

    :raises: :exc:`ValueError` if the planet identifier is invalid (outside 1..8).

        :exc:`UserWarning` if the year is outside the range 1000-3000.

    .. seealso:: |MANUAL| page 150
    """
    pv = asmatrix(zeros(shape=(2,3), dtype=float))
    s = _sofa.iauPlan94(date1, date2, np, pv)
    if s < 0:
        raise ValueError(plan94_msg[s])
    elif s > 0:
        warnings.warn(plan94_msg[s], UserWarning, 2)
    return pv


# iauPm
_sofa.iauPm.argtypes = [ndpointer(shape=(1,3), dtype=float)] #p
_sofa.iauPm.restype = c_double
def pm(p):
    """ Modulus of p-vector.

    :param p: p-vector.
    :type p: array-like of shape (1,3)

    :returns: modulus (float).

    .. seealso:: |MANUAL| page 153
    """
    return _sofa.iauPm(asmatrix(p, dtype=float))


# iauPmat00
_sofa.iauPmat00.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rbp
def pmat00(date1, date2):
    """ Precession matrix (including frame bias) from GCRS to a specified
    date, IAU 2000 model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: bias-precession matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 154
    """
    rbp = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPmat00(date1, date2, rbp)
    return rbp


# iauPmat06
_sofa.iauPmat06.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rbp
def pmat06(date1, date2):
    """ Precession matrix (including frame bias) from GCRS to a specified
    date, IAU 2006 model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: bias-precession matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 155
    """
    rbp = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPmat06(date1, date2, rbp)
    return rbp


# iauPmat76
_sofa.iauPmat76.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rmatp
def pmat76(date1, date2):
    """ Precession matrix from J2000.0 to a specified date, IAU 1976 model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: bias-precession matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 156
    """
    rmatp = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPmat76(date1, date2, rmatp)
    return rmatp


# iauPmp
_sofa.iauPmp.argtypes = [ndpointer(shape=(1,3), dtype=float), #a
                        ndpointer(shape=(1,3), dtype=float), #b
                        ndpointer(shape=(1,3), dtype=float)] #amb
def pmp(a, b):
    """ P-vector subtraction.

    :param a: first p-vector.
    :type a: array-like of shape (1,3)

    :param b: second p-vector.
    :type b: array-like of shape (1,3)

    :returns: a - b as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 158
    """
    amb = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauPmp(asmatrix(a, dtype=float), asmatrix(b, dtype=float), amb)
    return amb


# iauPn
_sofa.iauPn.argtypes = [ndpointer(shape=(1,3), dtype=float), #p
                        POINTER(c_double), #r
                        ndpointer(shape=(1,3), dtype=float)] #u
def pn(p):
    """ Convert a p-vector into modulus and unit vector.

    :param p: p-vector.
    :type p: array-like of shape (1,3)

    :returns: 2-tuple:

            * the modulus (float)
            * unit vector (numpy.matrix of shape 1x3)

    .. seealso:: |MANUAL| page 159
    """
    r = c_double()
    u = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauPn(asmatrix(p, dtype=float), byref(r), u)
    return r.value, u


# iauPn00
_sofa.iauPn00.argtypes = [c_double, #date1
                            c_double, #date2
                            c_double, #dpsi
                            c_double, #deps
                            POINTER(c_double), #epsa
                            ndpointer(shape=(3,3), dtype=float), #rb
                            ndpointer(shape=(3,3), dtype=float), #rp
                            ndpointer(shape=(3,3), dtype=float), #rbp
                            ndpointer(shape=(3,3), dtype=float), #rn
                            ndpointer(shape=(3,3), dtype=float)] #rbpn
def pn00(date1, date2, dpsi, deps):
    """ Precession-nutation, IAU 2000 model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :param dpsi, deps: nutation.
    :type dpsi, deps: float

    :returns: a 6-tuple:

            * mean obliquity (float)
            * frame bias matrix (numpy.matrix of shape 3x3)
            * precession matrix (numpy.matrix of shape 3x3)
            * bias-precession matrix (numpy.matrix of shape 3x3)
            * nutation matrix (numpy.matrix of shape 3x3)
            * GCRS-to-true matrix (numpy.matrix of shape 3x3).

    .. seealso:: |MANUAL| page 160
    """
    epsa = c_double()
    rb = asmatrix(zeros(shape=(3,3), dtype=float))
    rp = asmatrix(zeros(shape=(3,3), dtype=float))
    rbp = asmatrix(zeros(shape=(3,3), dtype=float))
    rn = asmatrix(zeros(shape=(3,3), dtype=float))
    rbpn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPn00(date1, date2, float(dpsi), float(deps), byref(epsa),
                                                    rb, rp, rbp, rn, rbpn)
    return epsa.value, rb, rp, rbp, rn, rbpn


# iauPn00a
_sofa.iauPn00a.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #dpsi
                            POINTER(c_double), #deps
                            POINTER(c_double), #epsa
                            ndpointer(shape=(3,3), dtype=float), #rb
                            ndpointer(shape=(3,3), dtype=float), #rp
                            ndpointer(shape=(3,3), dtype=float), #rbp
                            ndpointer(shape=(3,3), dtype=float), #rn
                            ndpointer(shape=(3,3), dtype=float)] #rbpn
def pn00a(date1, date2):
    """ Precession-nutation, IAU 2000A model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 8-tuple:

            * nutation in longitude (float)
            * nutation in obliquity (float)
            * mean obliquity (float)
            * frame bias matrix (numpy.matrix of shape 3x3)
            * precession matrix (numpy.matrix of shape 3x3)
            * bias-precession matrix (numpy.matrix of shape 3x3)
            * nutation matrix (numpy.matrix of shape 3x3)
            * GCRS-to-true matrix (numpy.matrix of shape 3x3).

    .. seealso:: |MANUAL| page 162
    """
    dpsi = c_double()
    deps = c_double()
    epsa = c_double()
    rb = asmatrix(zeros(shape=(3,3), dtype=float))
    rp = asmatrix(zeros(shape=(3,3), dtype=float))
    rbp = asmatrix(zeros(shape=(3,3), dtype=float))
    rn = asmatrix(zeros(shape=(3,3), dtype=float))
    rbpn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPn00a(date1, date2, byref(dpsi), byref(deps), byref(epsa), rb,
                    rp, rbp, rn, rbpn)
    return dpsi.value, deps.value, epsa.value, rb, rp, rbp, rn, rbpn


# iauPn00b
_sofa.iauPn00b.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #dpsi
                            POINTER(c_double), #deps
                            POINTER(c_double), #epsa
                            ndpointer(shape=(3,3), dtype=float), #rb
                            ndpointer(shape=(3,3), dtype=float), #rp
                            ndpointer(shape=(3,3), dtype=float), #rbp
                            ndpointer(shape=(3,3), dtype=float), #rn
                            ndpointer(shape=(3,3), dtype=float)] #rbpn
def pn00b(date1, date2):
    """ Precession-nutation, IAU 2000B model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 8-tuple:

            * nutation in longitude (float)
            * nutation in obliquity (float)
            * mean obliquity (float)
            * frame bias matrix (numpy.matrix of shape 3x3)
            * precession matrix (numpy.matrix of shape 3x3)
            * bias-precession matrix (numpy.matrix of shape 3x3)
            * nutation matrix (numpy.matrix of shape 3x3)
            * GCRS-to-true matrix (numpy.matrix of shape 3x3).

    .. seealso:: |MANUAL| page 164
    """
    dpsi = c_double()
    deps = c_double()
    epsa = c_double()
    rb = asmatrix(zeros(shape=(3,3), dtype=float))
    rp = asmatrix(zeros(shape=(3,3), dtype=float))
    rbp = asmatrix(zeros(shape=(3,3), dtype=float))
    rn = asmatrix(zeros(shape=(3,3), dtype=float))
    rbpn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPn00b(date1, date2, byref(dpsi), byref(deps), byref(epsa), rb,
                    rp, rbp, rn, rbpn)
    return dpsi.value, deps.value, epsa.value, rb, rp, rbp, rn, rbpn


# iauPn06
_sofa.iauPn06.argtypes = [c_double, #date1
                            c_double, #date2
                            c_double, #dpsi
                            c_double, #deps
                            POINTER(c_double), #epsa
                            ndpointer(shape=(3,3), dtype=float), #rb
                            ndpointer(shape=(3,3), dtype=float), #rp
                            ndpointer(shape=(3,3), dtype=float), #rbp
                            ndpointer(shape=(3,3), dtype=float), #rn
                            ndpointer(shape=(3,3), dtype=float)] #rbpn
def pn06(date1, date2, dpsi, deps):
    """ Precession-nutation, IAU 2006 model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :param dpsi, deps: nutation.
    :type dpsi, deps: float

    :returns: a 6-tuple:

            * mean obliquity (float)
            * frame bias matrix (numpy.matrix of shape 3x3)
            * precession matrix (numpy.matrix of shape 3x3)
            * bias-precession matrix (numpy.matrix of shape 3x3)
            * nutation matrix (numpy.matrix of shape 3x3)
            * GCRS-to-true matrix (numpy.matrix of shape 3x3).

    .. seealso:: |MANUAL| page 166
    """
    epsa = c_double()
    rb = asmatrix(zeros(shape=(3,3), dtype=float))
    rp = asmatrix(zeros(shape=(3,3), dtype=float))
    rbp = asmatrix(zeros(shape=(3,3), dtype=float))
    rn = asmatrix(zeros(shape=(3,3), dtype=float))
    rbpn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPn06(date1, date2, float(dpsi), float(deps), byref(epsa),
                                                        rb, rp, rbp, rn, rbpn)
    return epsa.value, rb, rp, rbp, rn, rbpn


# iauPn06a
_sofa.iauPn06a.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #dpsi
                            POINTER(c_double), #deps
                            POINTER(c_double), #epsa
                            ndpointer(shape=(3,3), dtype=float), #rb
                            ndpointer(shape=(3,3), dtype=float), #rp
                            ndpointer(shape=(3,3), dtype=float), #rbp
                            ndpointer(shape=(3,3), dtype=float), #rn
                            ndpointer(shape=(3,3), dtype=float)] #rbpn
def pn06a(date1, date2):
    """ Precession-nutation, IAU 2006/2000A models.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 8-tuple:

            * nutation in longitude (float)
            * nutation in obliquity (float)
            * mean obliquity (float)
            * frame bias matrix (numpy.matrix of shape 3x3)
            * precession matrix (numpy.matrix of shape 3x3)
            * bias-precession matrix (numpy.matrix of shape 3x3)
            * nutation matrix (numpy.matrix of shape 3x3)
            * GCRS-to-true matrix (numpy.matrix of shape 3x3).

    .. seealso:: |MANUAL| page 168
    """
    dpsi = c_double()
    deps = c_double()
    epsa = c_double()
    rb = asmatrix(zeros(shape=(3,3), dtype=float))
    rp = asmatrix(zeros(shape=(3,3), dtype=float))
    rbp = asmatrix(zeros(shape=(3,3), dtype=float))
    rn = asmatrix(zeros(shape=(3,3), dtype=float))
    rbpn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPn06a(date1, date2, byref(dpsi), byref(deps), byref(epsa), rb,
                    rp, rbp, rn, rbpn)
    return dpsi.value, deps.value, epsa.value, rb, rp, rbp, rn, rbpn


# iauPnm00a
_sofa.iauPnm00a.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rbpn
def pnm00a(date1, date2):
    """ Form the matrix of precession-nutation for a given date (including
    frame bias), equinox-based, IAU 2000A model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: classical *NPB* matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 170
    """
    rbpn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPnm00a(date1, date2, rbpn)
    return rbpn


# iauPnm00b
_sofa.iauPnm00b.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rbpn
def pnm00b(date1, date2):
    """ Form the matrix of precession-nutation for a given date (including
    frame bias), equinox-based, IAU 2000B model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: bias-precession-nutation matrix, as a numpy.matrix of shape \
        3x3.

    .. seealso:: |MANUAL| page 171
    """
    rbpn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPnm00b(date1, date2, rbpn)
    return rbpn


# iauPnm06a
_sofa.iauPnm06a.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rbpn
def pnm06a(date1, date2):
    """ Form the matrix of precession-nutation for a given date (including
    frame bias), IAU 2006 precession and IAU 2000A nutation models.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: bias-precession-nutation matrix, as a numpy.matrix of shape \
        3x3.

    .. seealso:: |MANUAL| page 172
    """
    rbpn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPnm06a(date1, date2, rbpn)
    return rbpn


# iauPnm80
_sofa.iauPnm80.argtypes = [c_double, #date1
                            c_double, #date2
                            ndpointer(shape=(3,3), dtype=float)] #rmatpn
def pnm80(date1, date2):
    """ Form the matrix of precession/nutation for a given date, IAU 1976
    precession model, IAU 1980 nutation model).

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: combined precessoin/nutation matrix, as a numpy.matrix of shape \
        3x3.

    .. seealso:: |MANUAL| page 173
    """
    rmatpn = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPnm80(date1, date2, rmatpn)
    return rmatpn


# iauPom00
_sofa.iauPom00.argtypes = [c_double, #xp
                            c_double, #yp
                            c_double, #sp
                            ndpointer(shape=(3,3), dtype=float)] #rpom
def pom00(xp, yp, sp):
    """ Form the matrix of polar motion for a given date, IAU 2000.

    :param xp, yp: coordinates of the pole in radians.
    :type xp, yp: float

    :param sp: the TIO locator in radians.
    :type sp: float

    :returns: the polar motion matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 174
    """
    rpom = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauPom00(float(xp), float(yp), float(sp), rpom)
    return rpom


# iauPpp
_sofa.iauPpp.argtypes = [ndpointer(shape=(1,3), dtype=float), #a
                        ndpointer(shape=(1,3), dtype=float), #b
                        ndpointer(shape=(1,3), dtype=float)] #apb
def ppp(a, b):
    """ P-vector addition.

    :param a: first p-vector.
    :type a: array-like of shape (1,3)

    :param b: second p-vector.
    :type b: array-like of shape (1,3)

    :returns: a + b as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 175
    """
    apb = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauPpp(asmatrix(a, dtype=float), asmatrix(b, dtype=float), apb)
    return apb


# iauPpsp
_sofa.iauPpsp.argtypes = [ndpointer(shape=(1,3), dtype=float), #a
                        c_double, #s
                        ndpointer(shape=(1,3), dtype=float), #b
                        ndpointer(shape=(1,3), dtype=float)] #apsb
def ppsp(a, s, b):
    """ P-vector plus scaled p-vector.

    :param a: first p-vector.
    :type a: array-like of shape (1,3)

    :param s: scalar (multiplier for *b*).
    :type s: float

    :param b: second p-vector.
    :type b: array-like of shape (1,3)

    :returns: a + s*b as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 176
    """
    apsb = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauPpsp(asmatrix(a, dtype=float), s, asmatrix(b, dtype=float), apsb)
    return apsb


# iauPr00
_sofa.iauPr00.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #dpsipr
                            POINTER(c_double)] #depspr
def pr00(date1, date2):
    """ Precession-rate part of the IAU 2000 precession-nutation models.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 2-tuple:

        * precession correction in longitude (float)
        * precession correction in obliquity (float).

    .. seealso:: |MANUAL| page 177
    """
    dpsipr = c_double()
    depspr = c_double()
    _sofa.iauPr00(date1, date2, byref(dpsipr), byref(depspr))
    return dpsipr.value, depspr.value


# iauPrec76
_sofa.iauPrec76.argtypes = [c_double, #ep01
                            c_double, #ep02
                            c_double, #ep11
                            c_double, #ep12
                            POINTER(c_double), #zeta
                            POINTER(c_double), #z
                            POINTER(c_double)] #theta
def prec76(ep01, ep02, ep11, ep12):
    """ Form the three Euler angles wich implement general precession between
    two epochs, using IAU 1976 model (as for FK5 catalog).

    :param ep01, ep02: two-part TDB starting epoch.
    :type ep01, ep02: float

    :param ep11, ep12: two-part TDB ending epoch.
    :type ep11, ep12: float

    :returns: a 3-tuple:

            * 1st rotation: radians cw around z (float)
            * 3rd rotation: radians cw around z (float)
            * 2nd rotation: radians ccw around y (float).

    .. seealso:: |MANUAL| page 179
    """
    zeta = c_double()
    z = c_double()
    theta = c_double()
    _sofa.iauPrec76(ep01, ep02, ep11, ep12, byref(zeta), byref(z), byref(theta))
    return zeta.value, z.value, theta.value


# iauPv2p
_sofa.iauPv2p.argtypes = [ndpointer(shape=(2,3), dtype=float), #pv
                            ndpointer(shape=(1,3), dtype=float)] #p
def pv2p(pv):
    """ Discard velocity component of a pv-vector.

    :param pv: pv-vector.
    :type pv: array-like of shape (2,3)

    :returns: p-vector as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 181
    """
    p = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauPv2p(asmatrix(pv, dtype=float), p)
    return p


# iauPv2s
_sofa.iauPv2s.argtypes = [ndpointer(shape=(2,3), dtype=float), #pv
                            POINTER(c_double), #theta
                            POINTER(c_double), #phi
                            POINTER(c_double), #r
                            POINTER(c_double), #td
                            POINTER(c_double), #pd
                            POINTER(c_double)] #rd
def pv2s(pv):
    """ Convert position/velocity from cartesian to spherical coordinates.

    :param pv: pv-vector.
    :type pv: array-like of shape (2,3)

    :returns: a 6-tuple:

        * longitude angle :math:`\\theta`  in radians (float)
        * latitude angle :math:`\phi` in radians (float)
        * radial distance *r* (float)
        * rate of change of :math:`\\theta` (float)
        * rate of change of :math:`\phi` (float)
        * rate of change of *r* (float)

    .. seealso:: |MANUAL| page 182
    """
    theta = c_double()
    phi = c_double()
    r = c_double()
    td = c_double()
    pd = c_double()
    rd = c_double()
    _sofa.iauPv2s(asmatrix(pv, dtype=float), byref(theta), byref(phi), byref(r),
                    byref(td), byref(pd), byref(rd))
    return theta.value, phi.value, r.value, td.value, pd.value, rd.value


# iauPvdpv
_sofa.iauPvdpv.argtypes = [ndpointer(shape=(2,3), dtype=float), #a
                            ndpointer(shape=(2,3), dtype=float), #b
                            ndpointer(shape=(1,2), dtype=float)] #adb
def pvdpv(a, b):
    """ Inner product of two pv-vectors.

    :param a: first pv-vector.
    :type a: array-like of shape (2,3)

    :param b: second pv-vector.
    :type b: array-like of shape (2,3)

    :returns: a . b as a numpy.matrix of shape 1x2.

    .. seealso:: |MANUAL| page 183
    """
    adb = asmatrix(zeros(shape=(2), dtype=float))
    _sofa.iauPvdpv(asmatrix(a, dtype=float), asmatrix(b, dtype=float), adb)
    return adb


# iauPvm
_sofa.iauPvm.argtypes = [ndpointer(shape=(2,3), dtype=float), #pv
                        POINTER(c_double), #r
                        POINTER(c_double)] #s
def pvm(pv):
    """ Modulus of pv-vector.

    :param pv: pv-vector.
    :type pv: array-like of shape (2,3)

    :returns: a 2-tuple:

        * modulus of position component (float)
        * modulus of velocity component (float).

    .. seealso:: |MANUAL| page 184
    """
    r = c_double()
    s = c_double()
    _sofa.iauPvm(asmatrix(pv, dtype=float), byref(r), byref(s))
    return r.value, s.value


# iauPvmpv
_sofa.iauPvmpv.argtypes = [ndpointer(shape=(2,3), dtype=float), #a
                            ndpointer(shape=(2,3), dtype=float), #b
                            ndpointer(shape=(2,3), dtype=float)] #amb
def pvmpv(a, b):
    """ Subtract one pv-vector from another.

    :param a: first pv-vector.
    :type a: array-like of shape (2,3)

    :param b: second pv-vector.
    :type b: array-like of shape (2,3)

    :returns: a - b as a numpy.matrix of shape 2x3.

    .. seealso:: |MANUAL| page 185
    """
    amb = asmatrix(zeros(shape=(2,3), dtype=float))
    _sofa.iauPvmpv(asmatrix(a, dtype=float), asmatrix(b, dtype=float), amb)
    return amb


# iauPvppv
_sofa.iauPvppv.argtypes = [ndpointer(shape=(2,3), dtype=float), #a
                            ndpointer(shape=(2,3), dtype=float), #b
                            ndpointer(shape=(2,3), dtype=float)] #apb
def pvppv(a, b):
    """ Add one pv-vector to another.

    :param a: first pv-vector.
    :type a: array-like of shape (2,3)

    :param b: second pv-vector.
    :type b: array-like of shape (2,3)

    :returns: a + b as a numpy.matrix of shape 2x3.

    .. seealso:: |MANUAL| page 186
    """
    apb = asmatrix(zeros(shape=(2,3), dtype=float))
    _sofa.iauPvppv(asmatrix(a, dtype=float), asmatrix(b, dtype=float), apb)
    return apb


# iauPvstar
_sofa.iauPvstar.argtypes = [ndpointer(shape=(2,3), dtype=float), #pv
                            POINTER(c_double), #ra
                            POINTER(c_double), #dec
                            POINTER(c_double), #pmr
                            POINTER(c_double), #pmd
                            POINTER(c_double), #px
                            POINTER(c_double)] #rv
_sofa.iauPvstar.restype = c_int
pvstar_msg = {
            -1: 'superluminal speed',
            -2: 'null position vector'
            }
def pvstar(pv):
    """ Convert star position-velocity vector to catalog coordinates.

    :param pv: pv-vector (AU, AU/day).
    :type pv: array-like of shape (2,3)

    :returns: a 6-tuple:

        * right ascensin in radians (float)
        * declination in radians (float)
        * RA proper motion (radians/year) (float)
        * Dec proper motion (radians/year) (float)
        * parallax in arcseconds (float)
        * radial velocity (km/s, positive = receding)

    :raises: :exc:`ValueError` if the speed is greater than or equal to the
        speed of light.

    .. seealso:: |MANUAL| page 187
    """
    ra = c_double()
    dec = c_double()
    pmr = c_double()
    pmd = c_double()
    px = c_double()
    rv = c_double()
    s = _sofa.iauPvstar(asmatrix(pv, dtype=float), byref(ra), byref(dec),
                                byref(pmr), byref(pmd), byref(px), byref(rv))
    if s != 0:
        raise ValueError(pvstar_msg[s])
    return ra.value, dec.value, pmr.value, pmd.value, px.value, rv.value


# iauPvu
_sofa.iauPvu.argtypes = [c_double, #dt
                        ndpointer(shape=(2,3), dtype=float), #pv
                        ndpointer(shape=(2,3), dtype=float)] #upv
def pvu(dt, pv):
    """ Update a pv-vector.

    :param dt: time interval.
    :type dt: float

    :param pv: pv-vector.
    :type pv: array-like of shape (2,3)

    :returns: a new pv-vector as a numpy.matrix of shape 2x3, with p \
        updated and v unchanged.

    .. seealso:: |MANUAL| page 189
    """
    upv = asmatrix(zeros(shape=(2,3), dtype=float))
    _sofa.iauPvu(dt, asmatrix(pv, dtype=float), upv)
    return upv


# iauPvup
_sofa.iauPvup.argtypes = [c_double, #dt
                            ndpointer(shape=(2,3), dtype=float), #pv
                            ndpointer(shape=(1,3), dtype=float)] #p
def pvup(dt, pv):
    """ Update a pv-vector, discarding the velocity component.

    :param dt: time interval.
    :type dt: float

    :param pv: pv-vector.
    :type pv: array-like of shape (2,3)

    :returns: a new p-vector, as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 190
    """
    p = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauPvup(dt, asmatrix(pv, dtype=float), p)
    return p


# iauPvxpv
_sofa.iauPvxpv.argtypes = [ndpointer(shape=(2,3), dtype=float), #a
                            ndpointer(shape=(2,3), dtype=float), #b
                            ndpointer(shape=(2,3), dtype=float)] #axb
def pvxpv(a, b):
    """ Outer product of two pv-vectors.

    :param a: first pv-vector.
    :type a: array-like of shape (2,3)

    :param b: second pv-vector.
    :type b: array-like of shape (2,3)

    :returns: a x b as a numpy.matrix of shape 2x3.

    .. seealso:: |MANUAL| page 191
    """
    axb = asmatrix(zeros(shape=(2,3), dtype=float))
    _sofa.iauPvxpv(asmatrix(a, dtype=float), asmatrix(b, dtype=float), axb)
    return axb


# iauPxp
_sofa.iauPxp.argtypes = [ndpointer(shape=(1,3), dtype=float), #a
                        ndpointer(shape=(1,3), dtype=float), #b
                        ndpointer(shape=(1,3), dtype=float)] #axb
def pxp(a, b):
    """ P-vector outer product.

    :param a: first p-vector.
    :type a: array-like of shape (1,3)

    :param b: second p-vector.
    :type b: array-like of shape (1,3)

    :returns: a x b as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 192
    """
    axb = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauPxp(asmatrix(a, dtype=float), asmatrix(b, dtype=float), axb)
    return axb


# iauRm2v
_sofa.iauRm2v.argtypes = [ndpointer(shape=(3,3), dtype=float), #r
                        ndpointer(shape=(1,3), dtype=float)] #w
def rm2v(r):
    """ Express a r-matrix as a r-vector.

    :param r: rotation matrix.
    :type r: array-like of shape (3,3)

    :returns: rotation vector as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 193
    """
    w = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauRm2v(asmatrix(r, dtype=float), w)
    return w


# iauRv2m
_sofa.iauRv2m.argtypes = [ndpointer(shape=(1,3), dtype=float), #w
                        ndpointer(shape=(3,3), dtype=float)] #r
def rv2m(w):
    """ Form the rotation matrix corresponding to a given r-vector.

    :param w: rotation vector.
    :type w: array-like of shape (1,3)

    :returns: rotation matrix as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 194
    """
    r = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauRv2m(asmatrix(w, dtype=float), r)
    return r


# iauRx
_sofa.iauRx.argtypes = [c_double, #phi
                        ndpointer(shape=(3,3), dtype=float)] #r
def rx(phi, r):
    """ Rotate a r-matrix about the x-axis.

    :param phi: angle in radians.
    :type phi: float

    :param r: rotation matrix.
    :type r: array-like of shape (3,3)

    :returns: the new rotation matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 195
    """
    r2 = asmatrix(r, dtype=float).copy()
    _sofa.iauRx(float(phi), r2)
    return r2


# iauRxp
_sofa.iauRxp.argtypes = [ndpointer(shape=(3,3), dtype=float), #r
                        ndpointer(shape=(1,3), dtype=float), #p
                        ndpointer(shape=(1,3), dtype=float)] #rp
def rxp(r, p):
    """ Multiply a p-vector by a r-matrix.

    :param r: rotation matrix.
    :type r: array-like of shape (3,3)

    :param p: p-vector.
    :type p: array-like of shape (1,3)

    :returns: r * p as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 196
    """
    rp = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauRxp(asmatrix(r, dtype=float), asmatrix(p, dtype=float), rp)
    return rp


# iauRxpv
_sofa.iauRxpv.argtypes = [ndpointer(shape=(3,3), dtype=float), #r
                        ndpointer(shape=(2,3), dtype=float), #pv
                        ndpointer(shape=(2,3), dtype=float)] #rpv
def rxpv(r, pv):
    """ Multiply a pv-vector by a r-matrix.

    :param r: rotation matrix.
    :type r: array-like of shape (3,3)

    :param pv: pv-vector.
    :type pv: array-like of shape (2,3)

    :returns: r * pv as a numpy.matrix of shape 2x3.

    .. seealso:: |MANUAL| page 197
    """
    rpv = asmatrix(zeros(shape=(2,3), dtype=float))
    _sofa.iauRxpv(asmatrix(r, dtype=float), asmatrix(pv, dtype=float), rpv)
    return rpv


# iauRxr
_sofa.iauRxr.argtypes = [ndpointer(shape=(3,3), dtype=float), #a
                        ndpointer(shape=(3,3), dtype=float), #b
                        ndpointer(shape=(3,3), dtype=float)] #atb
def rxr(a, b):
    """ Multiply two rotation matrices.

    :param a: first r-matrix.
    :type a: array-like of shape (3,3)

    :param b: second r-matrix.
    :type b: array-like of shape (3,3)

    :returns: a * b as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 198
    """
    atb = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauRxr(asmatrix(a, dtype=float), asmatrix(b, dtype=float), atb)
    return atb


# iauRy
_sofa.iauRy.argtypes = [c_double, #theta
                        ndpointer(shape=(3,3), dtype=float)] #r
def ry(theta, r):
    """ Rotate a r-matrix about the y-axis.

    :param theta: angle in radians.
    :type theta: float

    :param r: rotation matrix.
    :type r: array-like of shape (3,3)

    :returns: the new rotation matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 199
    """
    r2 = asmatrix(r).copy()
    _sofa.iauRy(float(theta), r2)
    return r2


# iauRz
_sofa.iauRz.argtypes = [c_double, #psi
                        ndpointer(shape=(3,3), dtype=float)] #r
def rz(psi, r):
    """ Rotate a r-matrix about the z-axis.

    :param psi: angle in radians.
    :type psi: float

    :param r: rotation matrix.
    :type r: array-like of shape (3,3)

    :returns: the new rotation matrix, as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 200
    """
    r2 = asmatrix(r).copy()
    _sofa.iauRz(float(psi), r2)
    return r2


# iauS00
_sofa.iauS00.argtypes = [c_double, #date1
                        c_double, #date2
                        c_double, #x
                        c_double] #y
_sofa.iauS00.restype = c_double
def s00(date1, date2, x, y):
    """ The CIO locator *s*, positioning the celestial intermediate
    origin on the equator of the celestial intermediate pole, given the
    CIP's X,Y coordinates. Compatible with IAU 2000A precession-nutation.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :param x, y: CIP coordinates.
    :type x, y: float

    :returns: the CIO locator *s* in radians (float).

    .. seealso:: |MANUAL| page 201
    """
    return _sofa.iauS00(date1, date2, float(x), float(y))


# iauS00a
_sofa.iauS00a.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauS00a.restype = c_double
def s00a(date1, date2):
    """ The CIO locator, positioning the celestial intermediate origin
    on the equator of the celestial intermediate pole, using IAU 2000A
    precession-nutation model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: the CIO locator *s* in radians (float):

    .. seealso:: |MANUAL| page 203
    """
    return _sofa.iauS00a(date1, date2)


# iauS00b
_sofa.iauS00b.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauS00b.restype = c_double
def s00b(date1, date2):
    """ The CIO locator, positioning the celestial intermediate origin
    on the equator of the celestial intermediate pole, using IAU 2000B
    precession-nutation model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: the CIO locator *s* in radians (float):

    .. seealso:: |MANUAL| page 205
    """
    return _sofa.iauS00b(date1, date2)


# iauS06
_sofa.iauS06.argtypes = [c_double, #date1
                        c_double, #date2
                        c_double, #x
                        c_double] #y
_sofa.iauS06.restype = c_double
def s06(date1, date2, x, y):
    """ The CIO locator *s*, positioning the celestial intermediate
    origin on the equator of the celestial intermediate pole, given the
    CIP's X,Y coordinates. Compatible with IAU 2006/2000A precession-nutation.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :param x, y: CIP coordinates.
    :type x, y: float

    :returns: the CIO locator *s* in radians (float).

    .. seealso:: |MANUAL| page 207
    """
    return _sofa.iauS06(date1, date2, float(x), float(y))


# iauS06a
_sofa.iauS06a.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauS06a.restype = c_double
def s06a(date1, date2):
    """ The CIO locator, positioning the celestial intermediate origin
    on the equator of the celestial intermediate pole, using IAU 2006
    precession and IAU 2000A nutation models.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: the CIO locator *s* in radians (float):

    .. seealso:: |MANUAL| page 209
    """
    return _sofa.iauS06a(date1, date2)


# iauS2c
_sofa.iauS2c.argtypes = [c_double, #theta
                        c_double, #phi
                        ndpointer(shape=(1,3), dtype=float)] #c
def s2c(theta, phi):
    """ Convert spherical coordinates to cartesian.

    :param theta: longitude angle in radians.
    :type theta: float

    :param phi: latitude angle in radians.
    :type phi: float

    :returns: direction cosines as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 211
    """
    c = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauS2c(float(theta), float(phi), c)
    return c


# iauS2p
_sofa.iauS2p.argtypes = [c_double, #theta
                        c_double, #phi
                        c_double, #r
                        ndpointer(shape=(1,3), dtype=float)] #p
def s2p(theta, phi, r):
    """ Convert spherical polar coordinates to p-vector.

    :param theta: longitude angle in radians.
    :type theta: float

    :param phi: latitude angle in radians.
    :type phi: float

    :param r: radial distance.
    :type r: float

    :returns: cartesian coordinates as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 212
    """
    p = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauS2p(float(theta), float(phi), r, p)
    return p


# iauS2pv
_sofa.iauS2pv.argtypes = [c_double, #theta
                            c_double, #phi
                            c_double, #r
                            c_double, #td
                            c_double, #pd
                            c_double, #rd
                            ndpointer(shape=(2,3), dtype=float)] #pv
def s2pv(theta, phi, r, td, pd, rd):
    """ Convert position/velocity from spherical to cartesian coordinates.

    :param theta: longitude angle in radians.
    :type theta: float

    :param phi: latitude angle in radians.
    :type phi: float

    :param r: radial distance.
    :type r: float

    :param td: rate of change of *theta*.
    :type td: float

    :param pd: rate of change of *phi*.
    :type pd: float

    :param rd: rate of change of *r*.
    :type rd: float

    :returns: pv-vector as a numpy.matrix of shape 2x3.

    .. seealso:: |MANUAL| page 213
    """
    pv = asmatrix(zeros(shape=(2,3), dtype=float))
    _sofa.iauS2pv(float(theta), float(phi), r, float(td), float(pd), rd, pv)
    return pv


# iauS2xpv
_sofa.iauS2xpv.argtypes = [c_double, #s1
                            c_double, #s2
                            ndpointer(shape=(2,3), dtype=float), #pv
                            ndpointer(shape=(2,3), dtype=float)] #spv
def s2xpv(s1, s2, pv):
    """ Multiply a pv-vector by two scalars.

    :param s1: scalar to multiply position component by.
    :type s1: float

    :param s2: scalar to multiply velocity component by.
    :type s2: float

    :param pv: pv-vector.
    :type pv: array-like of shape (2,3)

    :returns: a new pv-vector (with p scaled by s1 and v scaled by s2) as a \
        numpy.matrix of shape 2x3.

    .. seealso:: |MANUAL| page 214
    """
    spv = asmatrix(zeros(shape=(2,3), dtype=float))
    _sofa.iauS2xpv(s1, s2, asmatrix(pv, dtype=float), spv)
    return spv


# iauSepp
_sofa.iauSepp.argtypes = [ndpointer(shape=(1,3), dtype=float), #a
                            ndpointer(shape=(1,3), dtype=float)] #b
_sofa.iauSepp.restype = c_double
def sepp(a, b):
    """ Angular separation between two p-vectors.

    :param a: first p-vector.
    :type a: array-like of shape (1,3)

    :param b: second p-vector.
    :type b: array-like of shape (1,3)

    :returns: angular separation in radians, always positive (float).

    .. seealso:: |MANUAL| page 215
    """
    return _sofa.iauSepp(asmatrix(a, dtype=float), asmatrix(b, dtype=float))


# iauSeps
_sofa.iauSeps.argtypes = [c_double, #al
                            c_double, #ap
                            c_double, #bl
                            c_double] #bp
_sofa.iauSeps.restype = c_double
def seps(al, ap, bl, bp):
    """ Angular separation between two sets of spherical coordinates.

    :param al: first longitude in radians.
    :type al: float

    :param ap: first latitude in radians.
    :type ap: float

    :param bl: second longitude in radians.
    :type bl: float

    :param bl: second latitude in radians.
    :type bp: float

    :returns: angular separation in radians (float).

    .. seealso:: |MANUAL| page 216
    """
    return _sofa.iauSeps(float(al), float(ap), float(bl), float(bp))


# iauSp00
_sofa.iauSp00.argtypes = [c_double, #date1
                            c_double] #date2
_sofa.iauSp00.restype = c_double
def sp00(date1, date2):
    """ The TIO locator, positioning the terrestrial intermediate origin on
    the equator of the celestial intermediate pole.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: the TIO locator in radians (float).

    .. seealso:: |MANUAL| page 217
    """
    return _sofa.iauSp00(date1, date2)


# iauStarpm
_sofa.iauStarpm.argtypes = [c_double, #ra1
                            c_double, #dec1
                            c_double, #pmr1
                            c_double, #pmd1
                            c_double, #px1
                            c_double, #rv1
                            c_double, #ep1a
                            c_double, #ep1b
                            c_double, #ep2a
                            c_double, #ep2b
                            POINTER(c_double), #ra2
                            POINTER(c_double), #dec2
                            POINTER(c_double), #pmr2
                            POINTER(c_double), #pmd2
                            POINTER(c_double), #px2
                            POINTER(c_double)] #rv2
_sofa.iauStarpm.restype = c_int
# TODO: handle function's return statuses
def starpm(ra1, dec1, pmr1, pmd1, px1, rv1, ep1a, ep1b, ep2a, ep2b):
    """ Update star catalog data for space motion.

    :param ra1: right ascension in radians.
    :type ra1: float

    :param dec1: declination in radians.
    :type dec1: float

    :param pmr1: proper motion in RA (radians/year).
    :type pmr1: float

    :param pmd1: proper motion in Dec (radians/year).
    :type pmd1: float

    :param px1: parallax in arcseconds.
    :type px1: float

    :param rv1: radial velocity (km/s, positive = receding).
    :type rv1: float

    :param ep1a, ep1b: two-part starting epoch.
    :type ep1a, ep1b: float

    :param ep2a, ep2b: two-part ending epoch.
    :type ep2a, ep2b: float

    :returns: a 6-tuple:

        * the new right ascension in radians (float)
        * the new declination in radians (float)
        * the new RA proper motion in radians/year (float)
        * the new Dec proper motion in radians/year (float)
        * the new parallax in arcseconds (float)
        * the new radial velocity (km/s)

    .. seealso:: |MANUAL| page 218
    """
    ra2 = c_double()
    dec2 = c_double()
    pmr2 = c_double()
    pmd2 = c_double()
    px2 = c_double()
    rv2 = c_double()
    status = _sofa.iauStarpm(float(ra1), float(dec1), float(pmr1), float(pmd1),
                                float(px1), float(rv1), ep1a, ep1b, ep2a,
                    ep2b, byref(ra2), byref(dec2), byref(pmr2), byref(pmd2),
                    byref(px2), byref(rv2))
    return ra2.value, dec2.value, pmr2.value, pmd2.value, px2.value, rv2.value


# iauStarpv
_sofa.iauStarpv.argtypes = [c_double, #ra
                            c_double, #dec
                            c_double, #pmr
                            c_double, #pmd
                            c_double, #px
                            c_double, #rv
                            ndpointer(shape=(2,3), dtype=float)] #pv
_sofa.iauStarpv.restype = c_int
# TODO: return function's return statuses
def starpv(ra, dec, pmr, pmd, px, rv):
    """ Convert star catalog coordinates to position+velocity vector.

    :param ra: right ascension in radians.
    :type ra: float

    :param dec: declination in radians.
    :type dec: float

    :param pmr: proper motion in RA (radians/year).
    :type pmr: float

    :param pmd: proper motion in Dec (radians/year).
    :type pmd: float

    :param px: parallax in arcseconds.
    :type px: float

    :param rv: radial velocity (km/s, positive = receding).
    :type rv: float

    :returns: the pv-vector (AU, AU/day) as a numpy.matrix of shape 2x3

    .. seealso:: |MANUAL| page 220
    """
    pv = asmatrix(zeros(shape=(2,3), dtype=float))
    status = _sofa.iauStarpv(float(ra), float(dec), float(pmr), float(pmd),
                                                    float(px), float(rv), pv)
    return pv


# iauSxp
_sofa.iauSxp.argtypes = [c_double, #s
                        ndpointer(shape=(1,3), dtype=float), #p
                        ndpointer(shape=(1,3), dtype=float)] #sp
def sxp(s, p):
    """ Multiply a p-vector by a scalar.

    :param s: scalar.
    :type s: float

    :param p: p-vector
    :type p: array-like of shape (1,3)

    :returns: s * p as a numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 222
    """
    sp = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauSxp(s, asmatrix(p, dtype=float), sp)
    return sp


# iauSxpv
_sofa.iauSxpv.argtypes = [c_double, #s
                            ndpointer(shape=(2,3), dtype=float), #pv
                            ndpointer(shape=(2,3), dtype=float)] #spv
def sxpv(s, pv):
    """ Multiply a pv-vector by a scalar.

    :param s: scalar.
    :type s: float

    :param pv: pv-vector
    :type pv: array-like of shape (2,3)

    :returns: s * pv as a numpy.matrix of shape 2x3.

    .. seealso:: |MANUAL| page 223
    """
    spv = asmatrix(zeros(shape=(2,3), dtype=float))
    _sofa.iauSxpv(s, asmatrix(pv, dtype=float), spv)
    return spv


# iauTaitt
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTaitt.argtypes = [c_double, #tai1
                            c_double, #tai2
                            POINTER(c_double), #tt1
                            POINTER(c_double)] #tt2
    _sofa.iauTaitt.restype = c_int
except AttributeError:
    pass
def taitt(tai1, tai2):
    """ Timescale transformation: International Atomic Time (TAI) to
    Terrestrial Time (TT).

    :param tai1, tai2: TAI as a two-part Julian Date.
    :type tai1, tai2: float

    :returns: TT as a two-part Julian Date.

    .. seealso:: |MANUAL| page 224
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tt1 = c_double()
    tt2 = c_double()
    s = _sofa.iauTaitt(tai1, tai2, byref(tt1), byref(tt2))
    return tt1.value, tt2.value


# iauTaiut1
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTaiut1.argtypes = [c_double, #tai1
                            c_double, #tai2
                            c_double, #dta
                            POINTER(c_double), #ut11
                            POINTER(c_double)] #ut12
    _sofa.iauTaiut1.restype = c_int
except AttributeError:
    pass
def taiut1(tai1, tai2, dta):
    """ Timescale transformation: International Atomic Time (TAI) to
    Universal Time (UT1).

    :param tai1, tai2: TAI as a two-part Julian Date.
    :type tai1, tai2: float

    :param dta: UT1-TAI in seconds.
    :type dta: float

    :returns: UT1 as a two-part Julian Date.

    .. seealso:: |MANUAL| page 225
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    ut11 = c_double()
    ut12 = c_double()
    s = _sofa.iauTaiut1(tai1, tai2, dta, byref(ut11), byref(ut12))
    return ut11.value, ut12.value


# iauTaiutc
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTaiutc.argtypes = [c_double, #tai1
                            c_double, #tai2
                            POINTER(c_double), #utc1
                            POINTER(c_double)] #utc2
    _sofa.iauTaiutc.restype = c_int
except AttributeError:
    pass
taiutc_msg = {
            1: 'Taiutc: dubious year',
            -1: 'unacceptable date'
            }
def taiutc(tai1, tai2):
    """ Timescale transformation: International Atomic Time (TAI) to
    Coordinated Universal Time (UTC).

    :param tai1, tai2: TAI as a two-part Julian Date.
    :type tai1, tai2: float

    :returns: UTC as a two-part Julian Date.

    :raises: :exc:`ValueError` if the date is outside the range of valid values
        handled by this function.

        :exc:`UserWarning` if the value predates the
        introduction of UTC or is too far in the future to be
        trusted.

    .. seealso:: |MANUAL| page 226
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    utc1 = c_double()
    utc2 = c_double()
    s = _sofa.iauTaiutc(tai1, tai2, byref(utc1), byref(utc2))
    if s < 0:
        raise ValueError(taiutc_msg[s])
    elif s > 0:
        warnings.warn(taiutc_msg[s], UserWarning, 2)
    return utc1.value, utc2.value


# iauTcbtdb
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTcbtdb.argtypes = [c_double, #tcb1
                            c_double, #tcb2
                            POINTER(c_double), #tdb1
                            POINTER(c_double)] #tdb2
    _sofa.iauTcbtdb.restype = c_int
except AttributeError:
    pass
def tcbtdb(tcb1, tcb2):
    """ Timescale transformation: Barycentric Coordinate Time (TCB) to
    Barycentric Dynamical Time (TDB).

    :param tcb1, tcb2: TCB as a two-part Julian Date.
    :type tcb1, tcb2: float

    :returns: TDB as a two-part Julian Date.

    .. seealso:: |MANUAL| page 227
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tdb1 = c_double()
    tdb2 = c_double()
    s = _sofa.iauTcbtdb(tcb1, tcb2, byref(tdb1), byref(tdb2))
    return tdb1.value, tdb2.value


# iauTcgtt
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTcgtt.argtypes = [c_double, #tcg1
                            c_double, #tcg2
                            POINTER(c_double), #tt1
                            POINTER(c_double)] #tt2
    _sofa.iauTcgtt.restype = c_int
except AttributeError:
    pass
def tcgtt(tcg1, tcg2):
    """ Timescale transformation: Geocentric Coordinate Time (TCG) to
    Terrestrial Time (TT).

    :param tcg1, tcg2: TCG as a two-part Julian Date.
    :type tcg1, tcg2: float

    :returns: TT as a two-part Julian Date.

    .. seealso:: |MANUAL| page 228
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tt1 = c_double()
    tt2 = c_double()
    s = _sofa.iauTcgtt(tcg1, tcg2, byref(tt1), byref(tt2))
    return tt1.value, tt2.value


# iauTdbtcb
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTdbtcb.argtypes = [c_double, #tdb1
                            c_double, #tdb2
                            POINTER(c_double), #tcb1
                            POINTER(c_double)] #tcb2
    _sofa.iauTdbtcb.restype = c_int
except AttributeError:
    pass
def tdbtcb(tdb1, tdb2):
    """ Timescale transformation: Barycentric Dynamical Time (TDB) to
    Barycentric Coordinate Time (TCB).

    :param tdb1, tdb2: TDB as a two-part Julian Date.
    :type tdb1, tdb2: float

    :returns: TCB as a two-part Julian Date.

    .. seealso:: |MANUAL| page 229
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tcb1 = c_double()
    tcb2 = c_double()
    s = _sofa.iauTdbtcb(tdb1, tdb2, byref(tcb1), byref(tcb2))
    return tcb1.value, tcb2.value


# iauTdbtt
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTdbtt.argtypes = [c_double, #tdb1
                            c_double, #tdb2
                            c_double, #dtr
                            POINTER(c_double), #tt1
                            POINTER(c_double)] #tt2
    _sofa.iauTdbtt.restype = c_int
except AttributeError:
    pass
def tdbtt(tdb1, tdb2, dtr):
    """ Timescale transformation: Barycentric Dynamical Time (TDB) to
    Terrestrial Time (TT).

    :param tdb1, tdb2: TDB as a two-part Julian Date.
    :type tdb1, tdb2: float

    :param dtr: TDB-TT in seconds.
    :type dtr: float

    :returns: TT as a two-part Julian Date.

    .. seealso:: |MANUAL| page 230
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tt1 = c_double()
    tt2 = c_double()
    s = _sofa.iauTdbtt(tdb1, tdb2, dtr, byref(tt1), byref(tt2))
    return tt1.value, tt2.value


# iauTf2a
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTf2a.argtypes = [c_char, #s
                            c_int, #ihour
                            c_int, #imin
                            c_double, #sec
                            POINTER(c_double)] #rad
    _sofa.iauTf2a.restype = c_int
except AttributeError:
    pass
# TODO: handle function's return statuses
def tf2a(s, ihour, imin, sec):
    """ Convert hours, minutes, seconds to radians.

    :param s: sign, '-' is negative, everything else positive.

    :param ihour: hours.
    :type ihour: int

    :param imin: minutes.
    :type imin: int

    :param sec: seconds.
    :type sec: float

    :returns: the converted value in radians (float).

    .. seealso:: |MANUAL| page 231
    """

    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    rad = c_double()
    s = _sofa.iauTf2a(str(s), ihour, imin, sec, byref(rad))
    return rad.value


# iauTf2d
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTf2d.argtypes = [c_char, #s
                            c_int, #ihour
                            c_int, #imin
                            c_double, #sec
                            POINTER(c_double)] #days
    _sofa.iauTf2d.restype = c_int
except AttributeError:
    pass
# TODO: handle function's return statuses
def tf2d(s, ihour, imin, sec):
    """ Convert hours, minutes, seconds to days.

    :param s: sign, '-' is negative, everything else positive.

    :param ihour: hours.
    :type ihour: int

    :param imin: minutes.
    :type imin: int

    :param sec: seconds.
    :type sec: float

    :returns: the converted value in days (float).

    .. seealso:: |MANUAL| page 232
    """

    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    days = c_double()
    s = _sofa.iauTf2d(str(s), ihour, imin, sec, byref(days))
    return days.value


# iauTr
_sofa.iauTr.argtypes = [ndpointer(shape=(3,3), dtype=float), #r
                        ndpointer(shape=(3,3), dtype=float)] #rt
def tr(r):
    """ Transpose a rotation matrix.

    :param r: rotation matrix.
    :type r: array-like of shape (3,3)

    :returns: transpose as a numpy.matrix of shape 3x3.

    .. seealso:: |MANUAL| page 233
    """
    rt = asmatrix(zeros(shape=(3,3), dtype=float))
    _sofa.iauTr(asmatrix(r, dtype=float), rt)
    return rt


# iauTrxp
_sofa.iauTrxp.argtypes = [ndpointer(shape=(3,3), dtype=float), #r
                        ndpointer(shape=(1,3), dtype=float), #p
                        ndpointer(shape=(1,3), dtype=float)] #trp
def trxp(r, p):
    """ Multiply a p-vector by the transpose of a rotation matrix.

    :param r: rotation matrix.
    :type r: array-like of shape (3,3)

    :param p: p-vector.
    :type p: array-like of shape (1,3)

    :returns: numpy.matrix of shape 1x3.

    .. seealso:: |MANUAL| page 234
    """
    trp = asmatrix(zeros(shape=(1,3), dtype=float))
    _sofa.iauTrxp(asmatrix(r, dtype=float), asmatrix(p, dtype=float), trp)
    return trp


# iauTrxpv
_sofa.iauTrxpv.argtypes = [ndpointer(shape=(3,3), dtype=float), #r
                            ndpointer(shape=(2,3), dtype=float), #pv
                            ndpointer(shape=(2,3), dtype=float)] #trpv
def trxpv(r, pv):
    """ Multiply a pv-vector by the transpose of a rotation matrix.

    :param r: rotation matrix.
    :type r: array-like of shape (3,3)

    :param pv: pv-vector.
    :type pv: array-like of shape (2,3)

    :returns: numpy.matrix of shape 2x3.

    .. seealso:: |MANUAL| page 235
    """
    trpv = asmatrix(zeros(shape=(2,3), dtype=float))
    _sofa.iauTrxpv(asmatrix(r, dtype=float), asmatrix(pv, dtype=float), trpv)
    return trpv


# iauTttai
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTttai.argtypes = [c_double, #tt1
                            c_double, #tt2
                            POINTER(c_double), #tai1
                            POINTER(c_double)] #tai2
    _sofa.iauTttai.restype = c_int
except AttributeError:
    pass
def tttai(tt1, tt2):
    """ Timescale transformation: Terrestrial Time (TT) to
    International Atomic Time (TAI).

    :param tt1, tt2: TT as a two-part Julian Date.
    :type tt1, tt2: float

    :returns: TAI as a two-part Julian Date.

    .. seealso:: |MANUAL| page 236
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tai1 = c_double()
    tai2 = c_double()
    s = _sofa.iauTttai(tt1, tt2, byref(tai1), byref(tai2))
    return tai1.value, tai2.value


# iauTttcg
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTttcg.argtypes = [c_double, #tt1
                            c_double, #tt2
                            POINTER(c_double), #tcg1
                            POINTER(c_double)] #tcg2
    _sofa.iauTttcg.restype = c_int
except AttributeError:
    pass
def tttcg(tt1, tt2):
    """ Timescale transformation: Terrestrial Time (TT) to
    Geocentric Coordinate Time (TCG).

    :param tt1, tt2: TT as a two-part Julian Date.
    :type tt1, tt2: float

    :returns: TCG as a two-part Julian Date.

    .. seealso:: |MANUAL| page 237
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tcg1 = c_double()
    tcg2 = c_double()
    s = _sofa.iauTttcg(tt1, tt2, byref(tcg1), byref(tcg2))
    return tcg1.value, tcg2.value


# iauTttdb
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTttdb.argtypes = [c_double, #tt1
                            c_double, #tt2
                            c_double, #dtr
                            POINTER(c_double), #tdb1
                            POINTER(c_double)] #tdb2
    _sofa.iauTttdb.restype = c_int
except AttributeError:
    pass
def tttdb(tt1, tt2, dtr):
    """ Timescale transformation: Terrestrial Time (TT) to
    Barycentric Dynamical Time (TDB)

    :param tt1, tt2: TT as a two-part Julian Date.
    :type tt1, tt2: float

    :param dtr: TDB-TT in seconds.
    :type dtr: float

    :returns: TDB as a two-part Julian Date.

    .. seealso:: |MANUAL| page 238
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tdb1 = c_double()
    tdb2 = c_double()
    s = _sofa.iauTttdb(tt1, tt2, dtr, byref(tdb1), byref(tdb2))
    return tdb1.value, tdb2.value


# iauTtut1
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauTtut1.argtypes = [c_double, #tt1
                            c_double, #tt2
                            c_double, #dt
                            POINTER(c_double), #ut11
                            POINTER(c_double)] #ut12
    _sofa.iauTtut1.restype = c_int
except AttributeError:
    pass
def ttut1(tt1, tt2, dt):
    """ Timescale transformation: Terrestrial Time (TT) to
    Universal Time (UT1).

    :param tt1, tt2: TT as a two-part Julian Date.
    :type tt1, tt2: float

    :param dt: TT-UT1 in seconds.
    :type dt: float

    :returns: UT1 as a two-part Julian Date.

    .. seealso:: |MANUAL| page 239
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    ut11 = c_double()
    ut12 = c_double()
    s = _sofa.iauTtut1(tt1, tt2, dt, byref(ut11), byref(ut12))
    return ut11.value, ut12.value


# iauUt1tai
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauUt1tai.argtypes = [c_double, #ut11
                            c_double, #ut12
                            c_double, #dta
                            POINTER(c_double), #tai1
                            POINTER(c_double)] #tai2
    _sofa.iauUt1tai.restype = c_int
except AttributeError:
    pass
def ut1tai(ut11, ut12, dta):
    """ Timescale transformation: Universal Time (UT1) to
    International Atomic Time (TAI).

    :param ut11, ut12: UT1 as a two-part Julian Date.
    :type ut11, ut12: float

    :param dta: UT1-TAI in seconds.
    :type dta: float

    :returns: TAI as a two-part Julian Date

    .. seealso:: |MANUAL| page 240
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tai1 = c_double()
    tai2 = c_double()
    s = _sofa.iauUt1tai(ut11, ut12, dta, byref(tai1), byref(tai2))
    return tai1.value, tai2.value


# iauUt1tt
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauUt1tt.argtypes = [c_double, #ut11
                            c_double, #ut12
                            c_double, #dt
                            POINTER(c_double), #tt1
                            POINTER(c_double)] #tt2
    _sofa.iauUt1tt.restype = c_int
except AttributeError:
    pass
def ut1tt(ut11, ut12, dt):
    """ Timescale transformation: Universal Time (UT1) to
    Terrestrial Time (TT).

    :param ut11, ut12: UT1 as a two-part Julian Date.
    :type ut11, ut12: float

    :param dt: TT-UT1 in seconds.
    :type dt: float

    :returns: TT as a two-part Julian Date.

    .. seealso:: |MANUAL| page 241
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tt1 = c_double()
    tt2 = c_double()
    s = _sofa.iauUt1tt(ut11, ut12, dt, byref(tt1), byref(tt2))
    return tt1.value, tt2.value


# iauUt1utc
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauUt1utc.argtypes = [c_double, #ut11
                            c_double, #ut12
                            c_double, #dut1
                            POINTER(c_double), #utc1
                            POINTER(c_double)] #utc2
    _sofa.iauUt1utc.restype = c_int
except AttributeError:
    pass
ut1utc_msg = {
            1: 'Ut1utc: dubious year',
            -1: 'unacceptable date'
            }
def ut1utc(ut11, ut12, dut1):
    """ Timescale transformation: Universal Time (UT1) to
    Coordinated Universal Time (UTC)

    :param ut11, ut12: UT1 as a two-part Julian Date.
    :type ut11, ut12: float

    :param dut1: UT1-UTC in seconds.
    :type dut1: float

    :returns: UTC as a two-part Julian Date.

    :raises: :exc:`ValueError` if the date is outside the range of valid values
        handled by this function.

        :exc:`UserWarning` if the value predates the
        introduction of UTC or is too far in the future to be
        trusted.

    .. seealso:: |MANUAL| page 242
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    utc1 = c_double()
    utc2 = c_double()
    s = _sofa.iauUt1utc(ut11, ut12, dut1, byref(utc1), byref(utc2))
    if s < 0:
        raise ValueError(ut1utc_msg[s])
    elif s > 1:
        warnings.warn(ut1utc_msg[s], UserWarning, 2)
    return utc1.value, utc2.value


# iauUtctai
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauUtctai.argtypes = [c_double, #utc1
                            c_double, #utc2
                            POINTER(c_double), #tai1
                            POINTER(c_double)] #tai2
    _sofa.iauUtctai.restype = c_int
except AttributeError:
    pass
utctai_msg = {
            1: 'Utctai: dubious year',
            -1: 'unacceptable date'
            }
def utctai(utc1, utc2):
    """ Timescale transformation: Coordinated Universal Time (UTC) to
    International Atomic Time (TAI).

    :param utc1, utc2: UTC as a two-part Julian Date.
    :type utc1, utc2: float

    :returns: TAI as a two-part Julian Date.

    :raises: :exc:`ValueError` if the date is outside the range of valid values
        handled by this function.

        :exc:`UserWarning` if the value predates the
        introduction of UTC or is too far in the future to be
        trusted.

    .. seealso:: |MANUAL| page 243
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    tai1 = c_double()
    tai2 = c_double()
    s = _sofa.iauUtctai(utc1, utc2, byref(tai1), byref(tai2))
    if s < 0:
        raise ValueError(utctai_msg[s])
    elif s > 1:
        warnings.warn(utctai_msg[s], UserWarning, 2)
    return tai1.value, tai2.value


# iauUtcut1
# this routine was added in release 2010-12-01 of SOFA
try:
    _sofa.iauUtcut1.argtypes = [c_double, #utc1
                            c_double, #utc2
                            c_double, #dut1
                            POINTER(c_double), #ut11
                            POINTER(c_double)] #ut12
    _sofa.iauUtcut1.restype = c_int
except AttributeError:
    pass
utcut1_msg = {
            1: 'Utcut1: dubious year',
            -1: 'unacceptable date'
            }
def utcut1(utc1, utc2, dut1):
    """ Timescale transformation: Coordinated Universal Time (UTC) to
    Universal Time (UT1)

    :param utc1, utc2: UTC as a two-part Julian Date.
    :type utc1, utc2: float

    :param dut1: UT1-UTC in seconds.
    :type dut1: float

    :returns: UT1 as a two-part Julian Date.

    :raises: :exc:`ValueError` if the date is outside the range of valid values
        handled by this function.

        :exc:`UserWarning` if the value predates the
        introduction of UTC or is too far in the future to be
        trusted.

    .. seealso:: |MANUAL| page 244
    """
    if __sofa_version < (2010, 12, 01):
        raise NotImplementedError
    ut11 = c_double()
    ut12 = c_double()
    s = _sofa.iauUtcut1(utc1, utc2, dut1, byref(ut11), byref(ut12))
    if s < 0:
        raise ValueError(utcut1_msg[s])
    elif s > 1:
        warnings.warn(utcut1_msg[s], UserWarning, 2)
    return ut11.value, ut12.value


# iauXy06
_sofa.iauXy06.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #x
                            POINTER(c_double)] #y
def xy06(date1, date2):
    """ X,Y coordinates of the celestial intermediate pole from series
    based on IAU 2006 precession and IAU 2000A nutation.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 2-tuple containing X and Y CIP coordinates.

    .. seealso:: |MANUAL| page 246
    """
    x = c_double()
    y = c_double()
    _sofa.iauXy06(date1, date2, byref(x), byref(y))
    return x.value, y.value


# iauXys00a
_sofa.iauXys00a.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #x
                            POINTER(c_double), #y
                            POINTER(c_double)] #s
def xys00a(date1, date2):
    """ For a given TT date, compute X, Y coordinates of the celestial
    intermediate pole and the CIO locator *s*, using IAU 2000A
    precession-nutation model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 3-tuple:

        * X CIP coordinate
        * Y CIP coordinate
        * the CIO locator *s*.

    .. seealso:: |MANUAL| page 248
    """
    x = c_double()
    y = c_double()
    s = c_double()
    _sofa.iauXys00a(date1, date2, byref(x), byref(y), byref(s))
    return x.value, y.value, s.value


# iauXys00b
_sofa.iauXys00b.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #x
                            POINTER(c_double), #y
                            POINTER(c_double)] #s
def xys00b(date1, date2):
    """ For a given TT date, compute X, Y coordinates of the celestial
    intermediate pole and the CIO locator *s*, using IAU 2000B
    precession-nutation model.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 3-tuple:

        * X CIP coordinate
        * Y CIP coordinate
        * the CIO locator *s*.

    .. seealso:: |MANUAL| page 249
    """
    x = c_double()
    y = c_double()
    s = c_double()
    _sofa.iauXys00b(date1, date2, byref(x), byref(y), byref(s))
    return x.value, y.value, s.value


# iauXys06a
_sofa.iauXys06a.argtypes = [c_double, #date1
                            c_double, #date2
                            POINTER(c_double), #x
                            POINTER(c_double), #y
                            POINTER(c_double)] #s
def xys06a(date1, date2):
    """ For a given TT date, compute X, Y coordinates of the celestial
    intermediate pole and the CIO locator *s*, using IAU 2006 precession
    and IAU 2000A nutation models.

    :param date1, date2: TT as a two-part Julian date.
    :type date1, date2: float

    :returns: a 3-tuple:

        * X CIP coordinate
        * Y CIP coordinate
        * the CIO locator *s*.

    .. seealso:: |MANUAL| page 250
    """
    x = c_double()
    y = c_double()
    s = c_double()
    _sofa.iauXys06a(date1, date2, byref(x), byref(y), byref(s))
    return x.value, y.value, s.value


# iauZp
_sofa.iauZp.argtypes = [ndpointer(shape=(1,3), dtype=float)] #p
def zp(p):
    """ Zero a p-vector.

    :param p: p-vector.
    :type p: array-like of shape (1,3)

    :returns: a new p-vector filled with zeros. *p* isn't modified.

    .. seealso:: |MANUAL| page 251
    """
    p2 = asmatrix(p, dtype=float)
    _sofa.iauZp(p2)
    return p2


# iauZpv
_sofa.iauZpv.argtypes = [ndpointer(shape=(2,3), dtype=float)] #pv
def zpv(pv):
    """ Zero a pv-vector.

    :param pv: pv-vector.
    :type pv: array-like of shape (2,3)

    :returns: a new pv-vector filled with zeros. *pv* isn't modified.

    .. seealso:: |MANUAL| page 252
    """
    pv2 = asmatrix(pv, dtype=float)
    _sofa.iauZpv(pv2)
    return pv2


# iauZr
_sofa.iauZr.argtypes = [ndpointer(shape=(3,3), dtype=float)] #r
def zr(r):
    """ Initialize a rotation matrix to the null matrix.

    :param r: rotation matrix.
    :type r: array-like shape (3,3)

    :returns: a new rotation matrix fileld with zeroes. *r* isn't modified.

    .. seealso:: |MANUAL| page 253
    """
    r2 = asmatrix(r, dtype=float)
    _sofa.iauZr(r2)
    return r2

