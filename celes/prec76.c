#include "sofam.h"

void iauPrec76(double ep01, double ep02, double ep11, double ep12,
               double *zeta, double *z, double *theta)
/*
**  - - - - - - - - - -
**   i a u P r e c 7 6
**  - - - - - - - - - -
**
**  IAU 1976 precession model.
**
**  This function forms the three Euler angles which implement general
**  precession between two epochs, using the IAU 1976 model (as for
**  the FK5 catalog).
**
**  Status:  canonical model.
**
**  Given:
**     ep01,ep02   double    TDB starting epoch (Note 1)
**     ep11,ep12   double    TDB ending epoch (Note 1)
**
**  Returned:
**     zeta        double    1st rotation: radians cw around z
**     z           double    3rd rotation: radians cw around z
**     theta       double    2nd rotation: radians ccw around y
**
**  Notes:
**
**  1) The epochs ep01+ep02 and ep11+ep12 are Julian Dates, apportioned
**     in any convenient way between the arguments epn1 and epn2.  For
**     example, JD(TDB)=2450123.7 could be expressed in any of these
**     ways, among others:
**
**             epn1          epn2
**
**         2450123.7           0.0       (JD method)
**         2451545.0       -1421.3       (J2000 method)
**         2400000.5       50123.2       (MJD method)
**         2450123.5           0.2       (date & time method)
**
**     The JD method is the most natural and convenient to use in cases
**     where the loss of several decimal digits of resolution is
**     acceptable.  The J2000 method is best matched to the way the
**     argument is handled internally and will deliver the optimum
**     optimum resolution.  The MJD method and the date & time methods
**     are both good compromises between resolution and convenience.
**     The two epochs may be expressed using different methods, but at
**     the risk of losing some resolution.
**
**  2) The accumulated precession angles zeta, z, theta are expressed
**     through canonical polynomials which are valid only for a limited
**     time span.  In addition, the IAU 1976 precession rate is known to
**     be imperfect.  The absolute accuracy of the present formulation
**     is better than 0.1 arcsec from 1960AD to 2040AD, better than
**     1 arcsec from 1640AD to 2360AD, and remains below 3 arcsec for
**     the whole of the period 500BC to 3000AD.  The errors exceed
**     10 arcsec outside the range 1200BC to 3900AD, exceed 100 arcsec
**     outside 4200BC to 5600AD and exceed 1000 arcsec outside 6800BC to
**     8200AD.
**
**  3) The three angles are returned in the conventional order, which
**     is not the same as the order of the corresponding Euler
**     rotations.  The precession matrix is
**     R_3(-z) x R_2(+theta) x R_3(-zeta).
**
**  Reference:
**
**     Lieske, J.H., 1979, Astron.Astrophys. 73, 282, equations
**     (6) & (7), p283.
**
**  This revision:  2009 December 17
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double t0, t, tas2r, w;


/* Interval between fundamental epoch J2000.0 and start epoch (JC). */
   t0 = ((ep01 - DJ00) + ep02) / DJC;

/* Interval over which precession required (JC). */
   t = ((ep11 - ep01) + (ep12 - ep02)) / DJC;

/* Euler angles. */
   tas2r = t * DAS2R;
   w = 2306.2181 + (1.39656 - 0.000139 * t0) * t0;

   *zeta = (w + ((0.30188 - 0.000344 * t0) + 0.017998 * t) * t) * tas2r;

   *z = (w + ((1.09468 + 0.000066 * t0) + 0.018203 * t) * t) * tas2r;

   *theta = ((2004.3109 + (-0.85330 - 0.000217 * t0) * t0)
          + ((-0.42665 - 0.000217 * t0) - 0.041833 * t) * t) * tas2r;

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
