#include "sofam.h"

int iauUtcut1(double utc1, double utc2, double dut1,
              double *ut11, double *ut12)
/*
**  - - - - - - - - - -
**   i a u U t c u t 1
**  - - - - - - - - - -
**
**  Time scale transformation:  Coordinated Universal Time, UTC, to
**  Universal Time, UT1.
**
**  Status:  canonical.
**
**  Given:
**     utc1,utc2  double   UTC as a 2-part quasi Julian Date (Notes 1-4)
**     dut1       double   Delta UT1 = UT1-UTC in seconds (Note 5)
**
**  Returned:
**     ut11,ut12  double   UT1 as a 2-part Julian Date (Note 6)
**
**  Returned (function value):
**                int      status: +1 = dubious year (Note 7)
**                                  0 = OK
**                                 -1 = unacceptable date
**
**  Notes:
**
**  1) utc1+utc2 is quasi Julian Date (see Note 2), apportioned in any
**     convenient way between the two arguments, for example where utc1
**     is the Julian Day Number and utc2 is the fraction of a day.
**
**  2) JD cannot unambiguously represent UTC during a leap second unless
**     special measures are taken.  The convention in the present
**     function is that the JD day represents UTC days whether the
**     length is 86399, 86400 or 86401 SI seconds.
**
**  3) The warning status "dubious year" flags UTCs that predate the
**     introduction of the time scale and that are too far in the future
**     to be trusted.  See iauDat  for further details.
**
**  4) The function iauDtf2d  converts from calendar date and time of
**     day into 2-part Julian Date, and in the case of UTC implements
**     the leap-second-ambiguity convention described above.
**
**  5) Delta UT1 can be obtained from tabulations provided by the
**     International Earth Rotation and Reference Systems Service.  It
**     It is the caller's responsibility to supply a DUT argument
**     containing the UT1-UTC value that matches the given UTC.
**
**  6) The returned ut11,ut12 are such that their sum is the UT1 Julian
**     Date.
**
**  7) The warning status "dubious year" flags UTCs that predate the
**     introduction of the time scale and that are too far in the future
**     to be trusted.  See iauDat for further details.
**
**  References:
**
**     McCarthy, D. D., Petit, G. (eds.), IERS Conventions (2003),
**     IERS Technical Note No. 32, BKG (2004)
**
**     Explanatory Supplement to the Astronomical Almanac,
**     P. Kenneth Seidelmann (ed), University Science Books (1992)
**
**  Called:
**     iauJd2cal    JD to Gregorian calendar
**     iauDat       delta(AT) = TAI-UTC
**     iauUtctai    UTC to TAI
**     iauTaiut1    TAI to UT1
**
**  This revision:  2010 May 16
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   int iy, im, id, js, jw;
   double w, dat, dta, tai1, tai2;


/* Look up TAI-UTC. */
   if ( iauJd2cal(utc1, utc2, &iy, &im, &id, &w) ) return -1;
   js = iauDat ( iy, im, id, 0.0, &dat);
   if ( js < 0 ) return -1;

/* Form UT1-TAI. */
   dta = dut1 - dat;

/* UTC to TAI to UT1. */
   jw = iauUtctai(utc1, utc2, &tai1, &tai2);
   if ( jw < 0 ) {
      return -1;
   } else if ( jw > 0 ) {
      js = jw;
   }
   if ( iauTaiut1(tai1, tai2, dta, ut11, ut12) ) return -1;

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
