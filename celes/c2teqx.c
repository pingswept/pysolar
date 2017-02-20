#include "sofam.h"

void iauC2teqx(double rbpn[3][3], double gst, double rpom[3][3],
               double rc2t[3][3])
/*
**  - - - - - - - - - -
**   i a u C 2 t e q x
**  - - - - - - - - - -
**
**  Assemble the celestial to terrestrial matrix from equinox-based
**  components (the celestial-to-true matrix, the Greenwich Apparent
**  Sidereal Time and the polar motion matrix).
**
**  Status:  support function.
**
**  Given:
**     rbpn     double[3][3]    celestial-to-true matrix
**     gst      double          Greenwich (apparent) Sidereal Time
**     rpom     double[3][3]    polar-motion matrix
**
**  Returned:
**     rc2t     double[3][3]    celestial-to-terrestrial matrix (Note 2)
**
**  Notes:
**
**  1) This function constructs the rotation matrix that transforms
**     vectors in the celestial system into vectors in the terrestrial
**     system.  It does so starting from precomputed components, namely
**     the matrix which rotates from celestial coordinates to the
**     true equator and equinox of date, the Greenwich Apparent Sidereal
**     Time and the polar motion matrix.  One use of the present function
**     is when generating a series of celestial-to-terrestrial matrices
**     where only the Sidereal Time changes, avoiding the considerable
**     overhead of recomputing the precession-nutation more often than
**     necessary to achieve given accuracy objectives.
**
**  2) The relationship between the arguments is as follows:
**
**        [TRS] = rpom * R_3(gst) * rbpn * [CRS]
**
**              = rc2t * [CRS]
**
**     where [CRS] is a vector in the Geocentric Celestial Reference
**     System and [TRS] is a vector in the International Terrestrial
**     Reference System (see IERS Conventions 2003).
**
**  Called:
**     iauCr        copy r-matrix
**     iauRz        rotate around Z-axis
**     iauRxr       product of two r-matrices
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
   double r[3][3];


/* Construct the matrix. */
   iauCr(rbpn, r);
   iauRz(gst, r);
   iauRxr(rpom, r, rc2t);

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
