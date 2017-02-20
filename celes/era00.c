#include "sofam.h"

double iauEra00(double dj1, double dj2)
/*
**  - - - - - - - - -
**   i a u E r a 0 0
**  - - - - - - - - -
**
**  Earth rotation angle (IAU 2000 model).
**
**  Status:  canonical model.
**
**  Given:
**     dj1,dj2   double    UT1 as a 2-part Julian Date (see note)
**
**  Returned (function value):
**               double    Earth rotation angle (radians), range 0-2pi
**
**  Notes:
**
**  1) The UT1 date dj1+dj2 is a Julian Date, apportioned in any
**     convenient way between the arguments dj1 and dj2.  For example,
**     JD(UT1)=2450123.7 could be expressed in any of these ways,
**     among others:
**
**             dj1            dj2
**
**         2450123.7           0.0       (JD method)
**         2451545.0       -1421.3       (J2000 method)
**         2400000.5       50123.2       (MJD method)
**         2450123.5           0.2       (date & time method)
**
**     The JD method is the most natural and convenient to use in
**     cases where the loss of several decimal digits of resolution
**     is acceptable.  The J2000 and MJD methods are good compromises
**     between resolution and convenience.  The date & time method is
**     best matched to the algorithm used:  maximum precision is
**     delivered when the dj1 argument is for 0hrs UT1 on the day in
**     question and the dj2 argument lies in the range 0 to 1, or vice
**     versa.
**
**  2) The algorithm is adapted from Expression 22 of Capitaine et al.
**     2000.  The time argument has been expressed in days directly,
**     and, to retain precision, integer contributions have been
**     eliminated.  The same formulation is given in IERS Conventions
**     (2003), Chap. 5, Eq. 14.
**
**  Called:
**     iauAnp       normalize angle into range 0 to 2pi
**
**  References:
**
**     Capitaine N., Guinot B. and McCarthy D.D, 2000, Astron.
**     Astrophys., 355, 398-405.
**
**     McCarthy, D. D., Petit, G. (eds.), IERS Conventions (2003),
**     IERS Technical Note No. 32, BKG (2004)
**
**  This revision:  2008 May 24
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double d1, d2, t, f, theta;


/* Days since fundamental epoch. */
   if (dj1 < dj2) {
      d1 = dj1;
      d2 = dj2;
   } else {
      d1 = dj2;
      d2 = dj1;
   }
   t = d1 + (d2- DJ00);

/* Fractional part of T (days). */
   f = fmod(d1, 1.0) + fmod(d2, 1.0);

/* Earth rotation angle at this UT1. */
   theta = iauAnp(D2PI * (f + 0.7790572732640
                            + 0.00273781191135448 * t));

   return theta;

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
