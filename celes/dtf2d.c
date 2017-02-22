#include "sofam.h"
#include <string.h>

int iauDtf2d(const char *scale, int iy, int im, int id,
             int ihr, int imn, double sec, double *d1, double *d2)
/*
**  - - - - - - - - -
**   i a u D t f 2 d
**  - - - - - - - - -
**
**  Encode date and time fields into 2-part Julian Date (or in the case
**  of UTC a quasi-JD form that includes special provision for leap
**  seconds).
**
**  Status:  support function.
**
**  Given:
**     scale     char[]  time scale ID (Note 1)
**     iy,im,id  int     year, month, day in Gregorian calendar (Note 2)
**     ihr,imn   int     hour, minute
**     sec       double  seconds
**
**  Returned:
**     d1,d2     double  2-part Julian Date (Notes 3,4)
**
**  Returned (function value):
**               int     status: +3 = both of next two
**                               +2 = time is after end of day (Note 5)
**                               +1 = dubious year (Note 6)
**                                0 = OK
**                               -1 = bad year
**                               -2 = bad month
**                               -3 = bad day
**                               -4 = bad hour
**                               -5 = bad minute
**                               -6 = bad second (<0)
**
**  Notes:
**
**  1) scale identifies the time scale.  Only the value "UTC" (in upper
**     case) is significant, and enables handling of leap seconds (see
**     Note 4).
**
**  2) For calendar conventions and limitations, see iauCal2jd.
**
**  3) The sum of the results, d1+d2, is Julian Date, where normally d1
**     is the Julian Day Number and d2 is the fraction of a day.  In the
**     case of UTC, where the use of JD is problematical, special
**     conventions apply:  see the next note.
**
**  4) JD cannot unambiguously represent UTC during a leap second unless
**     special measures are taken.  The SOFA internal convention is that
**     the quasi-JD day represents UTC days whether the length is 86399,
**     86400 or 86401 SI seconds.
**
**  5) The warning status "time is after end of day" usually means that
**     the sec argument is greater than 60.0.  However, in a day ending
**     in a leap second the limit changes to 61.0 (or 59.0 in the case
**     of a negative leap second).
**
**  6) The warning status "dubious year" flags UTCs that predate the
**     introduction of the time scale and that are too far in the future
**     to be trusted.  See iauDat for further details.
**
**  7) Only in the case of continuous and regular time scales (TAI, TT,
**     TCG, TCB and TDB) is the result d1+d2 a Julian Date, strictly
**     speaking.  In the other cases (UT1 and UTC) the result must be
**     used with circumspection;  in particular the difference between
**     two such results cannot be interpreted as a precise time
**     interval.
**
**  Called:
**     iauCal2jd    Gregorian calendar to JD
**     iauDat       delta(AT) = TAI-UTC
**     iauJd2cal    JD to Gregorian calendar
**
**  This revision:  2012 February 12
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   int js, iy2, im2, id2;
   double dj, w, day, seclim, dat1, dat2, ddt, time;


/* Today's Julian Day Number. */
   js = iauCal2jd(iy, im, id, &dj, &w);
   if ( js ) return js;
   dj += w;

/* Day length and final minute length in seconds (provisional). */
   day = DAYSEC;
   seclim = 60;

/* Deal with the UTC leap second case. */
   if ( ! strcmp(scale,"UTC") ) {

   /* TAI-UTC today. */
      js = iauDat(iy, im, id, 0.0, &dat1);
      if ( js < 0 ) return js;

   /* TAI-UTC tomorrow. */
      js = iauJd2cal ( dj, 1.0, &iy2, &im2, &id2, &w);
      if ( js ) return js;
      js = iauDat(iy2, im2, id2, 0.0, &dat2);
      if ( js < 0 ) return js;

   /* The change in TAI-UTC (seconds). */
      ddt = dat2 - dat1;

   /* If leap second day, correct the day and final minute lengths. */
      if ( fabs(ddt) > 0.5 ) {
         day += ddt;
         if ( ihr == 23 && imn == 59 ) seclim += ddt;
      }
   }

/* Validate the time. */
   if ( ihr >= 0 && ihr <= 23 ) {
      if ( imn >= 0 && imn <= 59 ) {
         if ( sec >= 0 ) {
            if ( sec >= seclim ) {
               js += 2;
            }
         } else {
            js = -6;
         }
      } else {
         js = -5;
      }
   } else {
      js = -4;
   }
   if ( js < 0 ) return js;

/* The time in days. */
   time  = ( 60.0 * ( (double) ( 60 * ihr + imn ) ) + sec ) / day;

/* Return the date and time. */
   *d1 = dj;
   *d2 = time;

/* Status. */
   return js;

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
