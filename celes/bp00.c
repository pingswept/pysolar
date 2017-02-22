#include "sofam.h"

void iauBp00(double date1, double date2,
             double rb[3][3], double rp[3][3], double rbp[3][3])
/*
**  - - - - - - - -
**   i a u B p 0 0
**  - - - - - - - -
**
**  Frame bias and precession, IAU 2000.
**
**  Status:  canonical model.
**
**  Given:
**     date1,date2  double         TT as a 2-part Julian Date (Note 1)
**
**  Returned:
**     rb           double[3][3]   frame bias matrix (Note 2)
**     rp           double[3][3]   precession matrix (Note 3)
**     rbp          double[3][3]   bias-precession matrix (Note 4)
**
**  Notes:
**
**  1) The TT date date1+date2 is a Julian Date, apportioned in any
**     convenient way between the two arguments.  For example,
**     JD(TT)=2450123.7 could be expressed in any of these ways,
**     among others:
**
**             date1         date2
**
**         2450123.7           0.0       (JD method)
**         2451545.0       -1421.3       (J2000 method)
**         2400000.5       50123.2       (MJD method)
**         2450123.5           0.2       (date & time method)
**
**     The JD method is the most natural and convenient to use in
**     cases where the loss of several decimal digits of resolution
**     is acceptable.  The J2000 method is best matched to the way
**     the argument is handled internally and will deliver the
**     optimum resolution.  The MJD method and the date & time methods
**     are both good compromises between resolution and convenience.
**
**  2) The matrix rb transforms vectors from GCRS to mean J2000.0 by
**     applying frame bias.
**
**  3) The matrix rp transforms vectors from J2000.0 mean equator and
**     equinox to mean equator and equinox of date by applying
**     precession.
**
**  4) The matrix rbp transforms vectors from GCRS to mean equator and
**     equinox of date by applying frame bias then precession.  It is
**     the product rp x rb.
**
**  5) It is permissible to re-use the same array in the returned
**     arguments.  The arrays are filled in the order given.
**
**  Called:
**     iauBi00      frame bias components, IAU 2000
**     iauPr00      IAU 2000 precession adjustments
**     iauIr        initialize r-matrix to identity
**     iauRx        rotate around X-axis
**     iauRy        rotate around Y-axis
**     iauRz        rotate around Z-axis
**     iauCr        copy r-matrix
**     iauRxr       product of two r-matrices
**
**  Reference:
**     "Expressions for the Celestial Intermediate Pole and Celestial
**     Ephemeris Origin consistent with the IAU 2000A precession-
**     nutation model", Astron.Astrophys. 400, 1145-1154 (2003)
**
**     n.b. The celestial ephemeris origin (CEO) was renamed "celestial
**          intermediate origin" (CIO) by IAU 2006 Resolution 2.
**
**  This revision:  2010 January 18
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
/* J2000.0 obliquity (Lieske et al. 1977) */
   const double EPS0 = 84381.448 * DAS2R;

   double t, dpsibi, depsbi;
   double dra0, psia77, oma77, chia, dpsipr, depspr, psia, oma,
          rbw[3][3];


/* Interval between fundamental epoch J2000.0 and current date (JC). */
   t = ((date1 - DJ00) + date2) / DJC;

/* Frame bias. */
   iauBi00(&dpsibi, &depsbi, &dra0);

/* Precession angles (Lieske et al. 1977) */
   psia77 = (5038.7784 + (-1.07259 + (-0.001147) * t) * t) * t * DAS2R;
   oma77  =       EPS0 + ((0.05127 + (-0.007726) * t) * t) * t * DAS2R;
   chia   = (  10.5526 + (-2.38064 + (-0.001125) * t) * t) * t * DAS2R;

/* Apply IAU 2000 precession corrections. */
   iauPr00(date1, date2, &dpsipr,  &depspr);
   psia = psia77 + dpsipr;
   oma  = oma77  + depspr;

/* Frame bias matrix: GCRS to J2000.0. */
   iauIr(rbw);
   iauRz(dra0, rbw);
   iauRy(dpsibi * sin(EPS0), rbw);
   iauRx(-depsbi, rbw);
   iauCr(rbw, rb);

/* Precession matrix: J2000.0 to mean of date. */
   iauIr(rp);
   iauRx(EPS0,  rp);
   iauRz(-psia, rp);
   iauRx(-oma,  rp);
   iauRz(chia,  rp);

/* Bias-precession matrix: GCRS to mean of date. */
   iauRxr(rp, rbw, rbp);

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
