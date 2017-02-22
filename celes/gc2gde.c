#include "sofam.h"

int iauGc2gde ( double a, double f, double xyz[3],
                double *elong, double *phi, double *height )
/*
**  - - - - - - - - - -
**   i a u G c 2 g d e
**  - - - - - - - - - -
**
**  Transform geocentric coordinates to geodetic for a reference
**  ellipsoid of specified form.
**
**  Status:  support function.
**
**  Given:
**     a       double     equatorial radius (Notes 2,4)
**     f       double     flattening (Note 3)
**     xyz     double[3]  geocentric vector (Note 4)
**
**  Returned:
**     elong   double     longitude (radians, east +ve)
**     phi     double     latitude (geodetic, radians)
**     height  double     height above ellipsoid (geodetic, Note 4)
**
**  Returned (function value):
**             int        status:  0 = OK
**                                -1 = illegal f
**                                -2 = illegal a
**
**  Notes:
**
**  1) This function is based on the GCONV2H Fortran subroutine by
**     Toshio Fukushima (see reference).
**
**  2) The equatorial radius, a, can be in any units, but meters is
**     the conventional choice.
**
**  3) The flattening, f, is (for the Earth) a value around 0.00335,
**     i.e. around 1/298.
**
**  4) The equatorial radius, a, and the geocentric vector, xyz,
**     must be given in the same units, and determine the units of
**     the returned height, height.
**
**  5) If an error occurs (status < 0), elong, phi and height are
**     unchanged.
**
**  6) The inverse transformation is performed in the function
**     iauGd2gce.
**
**  7) The transformation for a standard ellipsoid (such as WGS84) can
**     more conveniently be performed by calling iauGc2gd, which uses a
**     numerical code to identify the required A and F values.
**
**  Reference:
**
**     Fukushima, T., "Transformation from Cartesian to geodetic
**     coordinates accelerated by Halley's method", J.Geodesy (2006)
**     79: 689-693
**
**  This revision:  2012 February 23
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double aeps2, e2, e4t, ec2, ec, b, x, y, z, p2, absz, p, s0, pn, zc,
                 c0, c02, c03, s02, s03, a02, a0, a03, d0, f0, b0, s1,
                 cc, s12, cc2;


/* ------------- */
/* Preliminaries */
/* ------------- */

/* Validate ellipsoid parameters. */
   if ( f < 0.0 || f >= 1.0 ) return -1;
   if ( a <= 0.0 ) return -2;

/* Functions of ellipsoid parameters (with further validation of f). */
   aeps2 = a*a * 1e-32;
   e2 = (2.0 - f) * f;
   e4t = e2*e2 * 1.5;
   ec2 = 1.0 - e2;
   if ( ec2 <= 0.0 ) return -1;
   ec = sqrt(ec2);
   b = a * ec;

/* Cartesian components. */
   x = xyz[0];
   y = xyz[1];
   z = xyz[2];

/* Distance from polar axis squared. */
   p2 = x*x + y*y;

/* Longitude. */
   *elong = p2 != 0.0 ? atan2(y, x) : 0.0;

/* Unsigned z-coordinate. */
   absz = fabs(z);

/* Proceed unless polar case. */
   if ( p2 > aeps2 ) {

   /* Distance from polar axis. */
      p = sqrt(p2);

   /* Normalization. */
      s0 = absz / a;
      pn = p / a;
      zc = ec * s0;

   /* Prepare Newton correction factors. */
      c0 = ec * pn;
      c02 = c0 * c0;
      c03 = c02 * c0;
      s02 = s0 * s0;
      s03 = s02 * s0;
      a02 = c02 + s02;
      a0 = sqrt(a02);
      a03 = a02 * a0;
      d0 = zc*a03 + e2*s03;
      f0 = pn*a03 - e2*c03;

   /* Prepare Halley correction factor. */
      b0 = e4t * s02 * c02 * pn * (a0 - ec);
      s1 = d0*f0 - b0*s0;
      cc = ec * (f0*f0 - b0*c0);

   /* Evaluate latitude and height. */
      *phi = atan(s1/cc);
      s12 = s1 * s1;
      cc2 = cc * cc;
      *height = (p*cc + absz*s1 - a * sqrt(ec2*s12 + cc2)) /
                                                        sqrt(s12 + cc2);
   } else {

   /* Exception: pole. */
      *phi = DPI / 2.0;
      *height = absz - b;
   }

/* Restore sign of latitude. */
   if ( z < 0 ) *phi = -*phi;

/* OK status. */
   return 0;

/*----------------------------------------------------------------------
**
**  Celes is a wrapper of the SOFA Library for Ruby.
**
**  This file is redistributed and relicensed in accordance with 
**  the SOFA Software License (http://www.iausofa.org/tandc.html).
**
**  The original library is available from IAU Standards of
**  Fundamental Astronomy (http://www.iausofa.org/).
**
**
**
**
**
**  Copyright (C) 2013, Naoki Arita
**  All rights reserved.
**
**  Redistribution and use in source and binary forms, with or without
**  modification, are permitted provided that the following conditions
**  are met:
**
**  1 Redistributions of source code must retain the above copyright
**    notice, this list of conditions and the following disclaimer.
**
**  2 Redistributions in binary form must reproduce the above copyright
**    notice, this list of conditions and the following disclaimer in
**    the documentation and/or other materials provided with the
**    distribution.
**
**  3 Neither the name of the Standards Of Fundamental Astronomy Board,
**    the International Astronomical Union nor the names of its
**    contributors may be used to endorse or promote products derived
**    from this software without specific prior written permission.
**
**  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
**  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
**  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
**  FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
**  COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
**  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
**  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
**  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
**  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
**  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
**  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
**  POSSIBILITY OF SUCH DAMAGE.
**
**--------------------------------------------------------------------*/

}
