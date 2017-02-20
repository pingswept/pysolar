#include "sofam.h"

void iauC2ixys(double x, double y, double s, double rc2i[3][3])
/*
**  - - - - - - - - - -
**   i a u C 2 i x y s
**  - - - - - - - - - -
**
**  Form the celestial to intermediate-frame-of-date matrix given the CIP
**  X,Y and the CIO locator s.
**
**  Status:  support function.
**
**  Given:
**     x,y      double         Celestial Intermediate Pole (Note 1)
**     s        double         the CIO locator s (Note 2)
**
**  Returned:
**     rc2i     double[3][3]   celestial-to-intermediate matrix (Note 3)
**
**  Notes:
**
**  1) The Celestial Intermediate Pole coordinates are the x,y
**     components of the unit vector in the Geocentric Celestial
**     Reference System.
**
**  2) The CIO locator s (in radians) positions the Celestial
**     Intermediate Origin on the equator of the CIP.
**
**  3) The matrix rc2i is the first stage in the transformation from
**     celestial to terrestrial coordinates:
**
**        [TRS] = RPOM * R_3(ERA) * rc2i * [CRS]
**
**              = RC2T * [CRS]
**
**     where [CRS] is a vector in the Geocentric Celestial Reference
**     System and [TRS] is a vector in the International Terrestrial
**     Reference System (see IERS Conventions 2003), ERA is the Earth
**     Rotation Angle and RPOM is the polar motion matrix.
**
**  Called:
**     iauIr        initialize r-matrix to identity
**     iauRz        rotate around Z-axis
**     iauRy        rotate around Y-axis
**
**  Reference:
**
**     McCarthy, D. D., Petit, G. (eds.), IERS Conventions (2003),
**     IERS Technical Note No. 32, BKG (2004)
**
**  This revision:  2008 May 11
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double r2, e, d;


/* Obtain the spherical angles E and d. */
   r2 = x*x + y*y;
   e = (r2 != 0.0) ? atan2(y, x) : 0.0;
   d = atan(sqrt(r2 / (1.0 - r2)));

/* Form the matrix. */
   iauIr(rc2i);
   iauRz(e, rc2i);
   iauRy(d, rc2i);
   iauRz(-(e+s), rc2i);

   return;

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
