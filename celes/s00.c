#include "sofam.h"

double iauS00(double date1, double date2, double x, double y)
/*
**  - - - - - - -
**   i a u S 0 0
**  - - - - - - -
**
**  The CIO locator s, positioning the Celestial Intermediate Origin on
**  the equator of the Celestial Intermediate Pole, given the CIP's X,Y
**  coordinates.  Compatible with IAU 2000A precession-nutation.
**
**  Status:  canonical model.
**
**  Given:
**     date1,date2   double    TT as a 2-part Julian Date (Note 1)
**     x,y           double    CIP coordinates (Note 3)
**
**  Returned (function value):
**                   double    the CIO locator s in radians (Note 2)
**
**  Notes:
**
**  1) The TT date date1+date2 is a Julian Date, apportioned in any
**     convenient way between the two arguments.  For example,
**     JD(TT)=2450123.7 could be expressed in any of these ways,
**     among others:
**
**            date1          date2
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
**  2) The CIO locator s is the difference between the right ascensions
**     of the same point in two systems:  the two systems are the GCRS
**     and the CIP,CIO, and the point is the ascending node of the
**     CIP equator.  The quantity s remains below 0.1 arcsecond
**     throughout 1900-2100.
**
**  3) The series used to compute s is in fact for s+XY/2, where X and Y
**     are the x and y components of the CIP unit vector;  this series
**     is more compact than a direct series for s would be.  This
**     function requires X,Y to be supplied by the caller, who is
**     responsible for providing values that are consistent with the
**     supplied date.
**
**  4) The model is consistent with the IAU 2000A precession-nutation.
**
**  Called:
**     iauFal03     mean anomaly of the Moon
**     iauFalp03    mean anomaly of the Sun
**     iauFaf03     mean argument of the latitude of the Moon
**     iauFad03     mean elongation of the Moon from the Sun
**     iauFaom03    mean longitude of the Moon's ascending node
**     iauFave03    mean longitude of Venus
**     iauFae03     mean longitude of Earth
**     iauFapa03    general accumulated precession in longitude
**
**  References:
**
**     Capitaine, N., Chapront, J., Lambert, S. and Wallace, P.,
**     "Expressions for the Celestial Intermediate Pole and Celestial
**     Ephemeris Origin consistent with the IAU 2000A precession-
**     nutation model", Astron.Astrophys. 400, 1145-1154 (2003)
**
**     n.b. The celestial ephemeris origin (CEO) was renamed "celestial
**          intermediate origin" (CIO) by IAU 2006 Resolution 2.
**
**     McCarthy, D. D., Petit, G. (eds.), IERS Conventions (2003),
**     IERS Technical Note No. 32, BKG (2004)
**
**  This revision:  2010 January 18
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
/* Time since J2000.0, in Julian centuries */
   double t;

/* Miscellaneous */
   int i, j;
   double a, w0, w1, w2, w3, w4, w5;

/* Fundamental arguments */
   double fa[8];

/* Returned value */
   double s;

/* --------------------- */
/* The series for s+XY/2 */
/* --------------------- */

   typedef struct {
      int nfa[8];      /* coefficients of l,l',F,D,Om,LVe,LE,pA */
      double s, c;     /* sine and cosine coefficients */
   } TERM;

/* Polynomial coefficients */
   static const double sp[] = {

   /* 1-6 */
          94.00e-6,
        3808.35e-6,
        -119.94e-6,
      -72574.09e-6,
          27.70e-6,
          15.61e-6
   };

/* Terms of order t^0 */
   static const TERM s0[] = {

   /* 1-10 */
      {{ 0,  0,  0,  0,  1,  0,  0,  0}, -2640.73e-6,   0.39e-6 },
      {{ 0,  0,  0,  0,  2,  0,  0,  0},   -63.53e-6,   0.02e-6 },
      {{ 0,  0,  2, -2,  3,  0,  0,  0},   -11.75e-6,  -0.01e-6 },
      {{ 0,  0,  2, -2,  1,  0,  0,  0},   -11.21e-6,  -0.01e-6 },
      {{ 0,  0,  2, -2,  2,  0,  0,  0},     4.57e-6,   0.00e-6 },
      {{ 0,  0,  2,  0,  3,  0,  0,  0},    -2.02e-6,   0.00e-6 },
      {{ 0,  0,  2,  0,  1,  0,  0,  0},    -1.98e-6,   0.00e-6 },
      {{ 0,  0,  0,  0,  3,  0,  0,  0},     1.72e-6,   0.00e-6 },
      {{ 0,  1,  0,  0,  1,  0,  0,  0},     1.41e-6,   0.01e-6 },
      {{ 0,  1,  0,  0, -1,  0,  0,  0},     1.26e-6,   0.01e-6 },

   /* 11-20 */
      {{ 1,  0,  0,  0, -1,  0,  0,  0},     0.63e-6,   0.00e-6 },
      {{ 1,  0,  0,  0,  1,  0,  0,  0},     0.63e-6,   0.00e-6 },
      {{ 0,  1,  2, -2,  3,  0,  0,  0},    -0.46e-6,   0.00e-6 },
      {{ 0,  1,  2, -2,  1,  0,  0,  0},    -0.45e-6,   0.00e-6 },
      {{ 0,  0,  4, -4,  4,  0,  0,  0},    -0.36e-6,   0.00e-6 },
      {{ 0,  0,  1, -1,  1, -8, 12,  0},     0.24e-6,   0.12e-6 },
      {{ 0,  0,  2,  0,  0,  0,  0,  0},    -0.32e-6,   0.00e-6 },
      {{ 0,  0,  2,  0,  2,  0,  0,  0},    -0.28e-6,   0.00e-6 },
      {{ 1,  0,  2,  0,  3,  0,  0,  0},    -0.27e-6,   0.00e-6 },
      {{ 1,  0,  2,  0,  1,  0,  0,  0},    -0.26e-6,   0.00e-6 },

   /* 21-30 */
      {{ 0,  0,  2, -2,  0,  0,  0,  0},     0.21e-6,   0.00e-6 },
      {{ 0,  1, -2,  2, -3,  0,  0,  0},    -0.19e-6,   0.00e-6 },
      {{ 0,  1, -2,  2, -1,  0,  0,  0},    -0.18e-6,   0.00e-6 },
      {{ 0,  0,  0,  0,  0,  8,-13, -1},     0.10e-6,  -0.05e-6 },
      {{ 0,  0,  0,  2,  0,  0,  0,  0},    -0.15e-6,   0.00e-6 },
      {{ 2,  0, -2,  0, -1,  0,  0,  0},     0.14e-6,   0.00e-6 },
      {{ 0,  1,  2, -2,  2,  0,  0,  0},     0.14e-6,   0.00e-6 },
      {{ 1,  0,  0, -2,  1,  0,  0,  0},    -0.14e-6,   0.00e-6 },
      {{ 1,  0,  0, -2, -1,  0,  0,  0},    -0.14e-6,   0.00e-6 },
      {{ 0,  0,  4, -2,  4,  0,  0,  0},    -0.13e-6,   0.00e-6 },

   /* 31-33 */
      {{ 0,  0,  2, -2,  4,  0,  0,  0},     0.11e-6,   0.00e-6 },
      {{ 1,  0, -2,  0, -3,  0,  0,  0},    -0.11e-6,   0.00e-6 },
      {{ 1,  0, -2,  0, -1,  0,  0,  0},    -0.11e-6,   0.00e-6 }
   };

/* Terms of order t^1 */
   static const TERM s1[] ={

   /* 1-3 */
      {{ 0,  0,  0,  0,  2,  0,  0,  0},    -0.07e-6,   3.57e-6 },
      {{ 0,  0,  0,  0,  1,  0,  0,  0},     1.71e-6,  -0.03e-6 },
      {{ 0,  0,  2, -2,  3,  0,  0,  0},     0.00e-6,   0.48e-6 }
   };

/* Terms of order t^2 */
   static const TERM s2[] ={

   /* 1-10 */
      {{ 0,  0,  0,  0,  1,  0,  0,  0},   743.53e-6,  -0.17e-6 },
      {{ 0,  0,  2, -2,  2,  0,  0,  0},    56.91e-6,   0.06e-6 },
      {{ 0,  0,  2,  0,  2,  0,  0,  0},     9.84e-6,  -0.01e-6 },
      {{ 0,  0,  0,  0,  2,  0,  0,  0},    -8.85e-6,   0.01e-6 },
      {{ 0,  1,  0,  0,  0,  0,  0,  0},    -6.38e-6,  -0.05e-6 },
      {{ 1,  0,  0,  0,  0,  0,  0,  0},    -3.07e-6,   0.00e-6 },
      {{ 0,  1,  2, -2,  2,  0,  0,  0},     2.23e-6,   0.00e-6 },
      {{ 0,  0,  2,  0,  1,  0,  0,  0},     1.67e-6,   0.00e-6 },
      {{ 1,  0,  2,  0,  2,  0,  0,  0},     1.30e-6,   0.00e-6 },
      {{ 0,  1, -2,  2, -2,  0,  0,  0},     0.93e-6,   0.00e-6 },

   /* 11-20 */
      {{ 1,  0,  0, -2,  0,  0,  0,  0},     0.68e-6,   0.00e-6 },
      {{ 0,  0,  2, -2,  1,  0,  0,  0},    -0.55e-6,   0.00e-6 },
      {{ 1,  0, -2,  0, -2,  0,  0,  0},     0.53e-6,   0.00e-6 },
      {{ 0,  0,  0,  2,  0,  0,  0,  0},    -0.27e-6,   0.00e-6 },
      {{ 1,  0,  0,  0,  1,  0,  0,  0},    -0.27e-6,   0.00e-6 },
      {{ 1,  0, -2, -2, -2,  0,  0,  0},    -0.26e-6,   0.00e-6 },
      {{ 1,  0,  0,  0, -1,  0,  0,  0},    -0.25e-6,   0.00e-6 },
      {{ 1,  0,  2,  0,  1,  0,  0,  0},     0.22e-6,   0.00e-6 },
      {{ 2,  0,  0, -2,  0,  0,  0,  0},    -0.21e-6,   0.00e-6 },
      {{ 2,  0, -2,  0, -1,  0,  0,  0},     0.20e-6,   0.00e-6 },

   /* 21-25 */
      {{ 0,  0,  2,  2,  2,  0,  0,  0},     0.17e-6,   0.00e-6 },
      {{ 2,  0,  2,  0,  2,  0,  0,  0},     0.13e-6,   0.00e-6 },
      {{ 2,  0,  0,  0,  0,  0,  0,  0},    -0.13e-6,   0.00e-6 },
      {{ 1,  0,  2, -2,  2,  0,  0,  0},    -0.12e-6,   0.00e-6 },
      {{ 0,  0,  2,  0,  0,  0,  0,  0},    -0.11e-6,   0.00e-6 }
   };

/* Terms of order t^3 */
   static const TERM s3[] ={

   /* 1-4 */
      {{ 0,  0,  0,  0,  1,  0,  0,  0},     0.30e-6, -23.51e-6 },
      {{ 0,  0,  2, -2,  2,  0,  0,  0},    -0.03e-6,  -1.39e-6 },
      {{ 0,  0,  2,  0,  2,  0,  0,  0},    -0.01e-6,  -0.24e-6 },
      {{ 0,  0,  0,  0,  2,  0,  0,  0},     0.00e-6,   0.22e-6 }
   };

/* Terms of order t^4 */
   static const TERM s4[] ={

   /* 1-1 */
      {{ 0,  0,  0,  0,  1,  0,  0,  0},    -0.26e-6,  -0.01e-6 }
   };

/* Number of terms in the series */
   const int NS0 = (int) (sizeof s0 / sizeof (TERM));
   const int NS1 = (int) (sizeof s1 / sizeof (TERM));
   const int NS2 = (int) (sizeof s2 / sizeof (TERM));
   const int NS3 = (int) (sizeof s3 / sizeof (TERM));
   const int NS4 = (int) (sizeof s4 / sizeof (TERM));

/*--------------------------------------------------------------------*/

/* Interval between fundamental epoch J2000.0 and current date (JC). */
   t = ((date1 - DJ00) + date2) / DJC;

/* Fundamental Arguments (from IERS Conventions 2003) */

/* Mean anomaly of the Moon. */
   fa[0] = iauFal03(t);

/* Mean anomaly of the Sun. */
   fa[1] = iauFalp03(t);

/* Mean longitude of the Moon minus that of the ascending node. */
   fa[2] = iauFaf03(t);

/* Mean elongation of the Moon from the Sun. */
   fa[3] = iauFad03(t);

/* Mean longitude of the ascending node of the Moon. */
   fa[4] = iauFaom03(t);

/* Mean longitude of Venus. */
   fa[5] = iauFave03(t);

/* Mean longitude of Earth. */
   fa[6] = iauFae03(t);

/* General precession in longitude. */
   fa[7] = iauFapa03(t);

/* Evaluate s. */
   w0 = sp[0];
   w1 = sp[1];
   w2 = sp[2];
   w3 = sp[3];
   w4 = sp[4];
   w5 = sp[5];

   for (i = NS0-1; i >= 0; i--) {
   a = 0.0;
   for (j = 0; j < 8; j++) {
       a += (double)s0[i].nfa[j] * fa[j];
   }
   w0 += s0[i].s * sin(a) + s0[i].c * cos(a);
   }

   for (i = NS1-1; i >= 0; i--) {
   a = 0.0;
   for (j = 0; j < 8; j++) {
       a += (double)s1[i].nfa[j] * fa[j];
   }
   w1 += s1[i].s * sin(a) + s1[i].c * cos(a);
   }

   for (i = NS2-1; i >= 0; i--) {
   a = 0.0;
   for (j = 0; j < 8; j++) {
       a += (double)s2[i].nfa[j] * fa[j];
   }
   w2 += s2[i].s * sin(a) + s2[i].c * cos(a);
   }

   for (i = NS3-1; i >= 0; i--) {
   a = 0.0;
   for (j = 0; j < 8; j++) {
       a += (double)s3[i].nfa[j] * fa[j];
   }
   w3 += s3[i].s * sin(a) + s3[i].c * cos(a);
   }

   for (i = NS4-1; i >= 0; i--) {
   a = 0.0;
   for (j = 0; j < 8; j++) {
       a += (double)s4[i].nfa[j] * fa[j];
   }
   w4 += s4[i].s * sin(a) + s4[i].c * cos(a);
   }

   s = (w0 +
       (w1 +
       (w2 +
       (w3 +
       (w4 +
        w5 * t) * t) * t) * t) * t) * DAS2R - x*y/2.0;

   return s;

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
