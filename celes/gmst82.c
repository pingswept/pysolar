#include "sofam.h"

double iauGmst82(double dj1, double dj2)
/*
**  - - - - - - - - - -
**   i a u G m s t 8 2
**  - - - - - - - - - -
**
**  Universal Time to Greenwich mean sidereal time (IAU 1982 model).
**
**  Status:  canonical model.
**
**  Given:
**     dj1,dj2    double    UT1 Julian Date (see note)
**
**  Returned (function value):
**                double    Greenwich mean sidereal time (radians)
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
**         2450123.7D0        0D0        (JD method)
**          2451545D0      -1421.3D0     (J2000 method)
**         2400000.5D0     50123.2D0     (MJD method)
**         2450123.5D0       0.2D0       (date & time method)
**
**     The JD method is the most natural and convenient to use in
**     cases where the loss of several decimal digits of resolution
**     is acceptable.  The J2000 and MJD methods are good compromises
**     between resolution and convenience.  The date & time method is
**     best matched to the algorithm used:  maximum accuracy (or, at
**     least, minimum noise) is delivered when the dj1 argument is for
**     0hrs UT1 on the day in question and the dj2 argument lies in the
**     range 0 to 1, or vice versa.
**
**  2) The algorithm is based on the IAU 1982 expression.  This is
**     always described as giving the GMST at 0 hours UT1.  In fact, it
**     gives the difference between the GMST and the UT, the steady
**     4-minutes-per-day drawing-ahead of ST with respect to UT.  When
**     whole days are ignored, the expression happens to equal the GMST
**     at 0 hours UT1 each day.
**
**  3) In this function, the entire UT1 (the sum of the two arguments
**     dj1 and dj2) is used directly as the argument for the standard
**     formula, the constant term of which is adjusted by 12 hours to
**     take account of the noon phasing of Julian Date.  The UT1 is then
**     added, but omitting whole days to conserve accuracy.
**
**  Called:
**     iauAnp       normalize angle into range 0 to 2pi
**
**  References:
**
**     Transactions of the International Astronomical Union,
**     XVIII B, 67 (1983).
**
**     Aoki et al., Astron. Astrophys. 105, 359-361 (1982).
**
**  This revision:  2008 May 24
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
/* Coefficients of IAU 1982 GMST-UT1 model */
   double A = 24110.54841  -  DAYSEC / 2.0;
   double B = 8640184.812866;
   double C = 0.093104;
   double D =  -6.2e-6;

/* Note: the first constant, A, has to be adjusted by 12 hours */
/* because the UT1 is supplied as a Julian date, which begins  */
/* at noon.                                                    */

   double d1, d2, t, f, gmst;


/* Julian centuries since fundamental epoch. */
   if (dj1 < dj2) {
      d1 = dj1;
      d2 = dj2;
   } else {
      d1 = dj2;
      d2 = dj1;
   }
   t = (d1 + (d2 - DJ00)) / DJC;

/* Fractional part of JD(UT1), in seconds. */
   f = DAYSEC * (fmod(d1, 1.0) + fmod(d2, 1.0));

/* GMST at this UT1. */
   gmst = iauAnp(DS2R * ((A + (B + (C + D * t) * t) * t) + f));

   return gmst;

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
