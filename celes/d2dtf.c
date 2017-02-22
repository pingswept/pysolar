#include "sofam.h"
#include <string.h>

int iauD2dtf(const char *scale, int ndp, double d1, double d2,
             int *iy, int *im, int *id, int ihmsf[4])
/*
**  - - - - - - - - -
**   i a u D 2 d t f
**  - - - - - - - - -
**
**  Format for output a 2-part Julian Date (or in the case of UTC a
**  quasi-JD form that includes special provision for leap seconds).
**
**  Status:  support function.
**
**  Given:
**     scale     char[]  time scale ID (Note 1)
**     ndp       int     resolution (Note 2)
**     d1,d2     double  time as a 2-part Julian Date (Notes 3,4)
**
**  Returned:
**     iy,im,id  int     year, month, day in Gregorian calendar (Note 5)
**     ihmsf     int[4]  hours, minutes, seconds, fraction (Note 1)
**
**  Returned (function value):
**               int     status: +1 = dubious year (Note 5)
**                                0 = OK
**                               -1 = unacceptable date (Note 6)
**
**  Notes:
**
**  1) scale identifies the time scale.  Only the value "UTC" (in upper
**     case) is significant, and enables handling of leap seconds (see
**     Note 4).
**
**  2) ndp is the number of decimal places in the seconds field, and can
**     have negative as well as positive values, such as:
**
**     ndp         resolution
**     -4            1 00 00
**     -3            0 10 00
**     -2            0 01 00
**     -1            0 00 10
**      0            0 00 01
**      1            0 00 00.1
**      2            0 00 00.01
**      3            0 00 00.001
**
**     The limits are platform dependent, but a safe range is -5 to +9.
**
**  3) d1+d2 is Julian Date, apportioned in any convenient way between
**     the two arguments, for example where d1 is the Julian Day Number
**     and d2 is the fraction of a day.  In the case of UTC, where the
**     use of JD is problematical, special conventions apply:  see the
**     next note.
**
**  4) JD cannot unambiguously represent UTC during a leap second unless
**     special measures are taken.  The SOFA internal convention is that
**     the quasi-JD day represents UTC days whether the length is 86399,
**     86400 or 86401 SI seconds.
**
**  5) The warning status "dubious year" flags UTCs that predate the
**     introduction of the time scale and that are too far in the future
**     to be trusted.  See iauDat for further details.
**
**  6) For calendar conventions and limitations, see iauCal2jd.
**
**  Called:
**     iauJd2cal    JD to Gregorian calendar
**     iauD2tf      decompose days to hms
**     iauDat       delta(AT) = TAI-UTC
**
**  This revision:  2012 February 12
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   int leap;
   char s;
   int iy1, im1, id1, js, iy2, im2, id2, ihmsf1[4], i;
   double a1, b1, fd, dat1, w, dat2, ddt;


/* The two-part JD. */
   a1 = d1;
   b1 = d2;

/* Provisional calendar date. */
   js = iauJd2cal(a1, b1, &iy1, &im1, &id1, &fd);
   if ( js ) return js < 0 ? -1 : js;

/* Is this a leap second day? */
   leap = 0;
   if ( ! strcmp(scale,"UTC") ) {

   /* TAI-UTC today. */
      js = iauDat(iy1, im1, id1, fd, &dat1);
      if ( js < 0 ) return -1;

   /* TAI-UTC tomorrow (at noon, to avoid rounding effects). */
      js = iauJd2cal(a1+1.5, b1-fd, &iy2, &im2, &id2, &w);
      js = iauDat(iy2, im2, id2, 0.0, &dat2);
      if ( js < 0 ) return -1;

   /* The change in TAI-UTC (seconds). */
      ddt = dat2 - dat1;

   /* If leap second day, scale the fraction of a day into SI. */
      leap = fabs(ddt) > 0.5;
      if (leap) fd += fd * ddt/DAYSEC;
   }

/* Provisional time of day. */
   iauD2tf ( ndp, fd, &s, ihmsf1 );

/* Is this a leap second day? */
   if ( ! leap ) {

   /* No.  Has the time rounded up to 24h? */
      if ( ihmsf1[0] > 23 ) {

      /* Yes.  We will need tomorrow's calendar date. */
         js = iauJd2cal(a1+1.5, b1-fd, &iy2, &im2, &id2, &w);

      /* Use 0h tomorrow. */
         iy1 = iy2;
         im1 = im2;
         id1 = id2;
         for ( i = 0; i < 4; i++ ) {
            ihmsf1[i] = 0;
         }
      }
   } else {

   /* This is a leap second day.  Has the time reached or passed 24h? */
      if ( ihmsf1[0] > 23 ) {

      /* Yes.  Use 23 59 60... */
         ihmsf1[0] = 23;
         ihmsf1[1] = 59;
         ihmsf1[2] = 60;
      }
   }

/* Results. */
   *iy = iy1;
   *im = im1;
   *id = id1;
   for ( i = 0; i < 4; i++ ) {
      ihmsf[i] = ihmsf1[i];
   }

/* Status. */
   return js < 0 ? -1 : js;

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
