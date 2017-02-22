#include "sofam.h"

int iauTttcg(double tt1, double tt2, double *tcg1, double *tcg2)
/*
**  - - - - - - - - -
**   i a u T t t c g
**  - - - - - - - - -
**
**  Time scale transformation:  Terrestrial Time, TT, to Geocentric
**  Coordinate Time, TCG.
**
**  Status:  canonical.
**
**  Given:
**     tt1,tt2    double    TT as a 2-part Julian Date
**
**  Returned:
**     tcg1,tcg2  double    TCG as a 2-part Julian Date
**
**  Returned (function value):
**                int       status:  0 = OK
**
**  Note:
**
**     tt1+tt2 is Julian Date, apportioned in any convenient way between
**     the two arguments, for example where tt1 is the Julian Day Number
**     and tt2 is the fraction of a day.  The returned tcg1,tcg2 follow
**     suit.
**
**  References:
**
**     McCarthy, D. D., Petit, G. (eds.), IERS Conventions (2003),
**     IERS Technical Note No. 32, BKG (2004)
**
**     IAU 2000 Resolution B1.9
**
**  This revision:  2010 May 13
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{

/* 1977 Jan 1 00:00:32.184 TT, as MJD */
   static const double t77t = DJM77 + TTMTAI/DAYSEC;

/* TT to TCG rate */
   static const double elgg = ELG/(1.0-ELG);


/* Result, safeguarding precision. */
   if ( tt1 > tt2 ) {
      *tcg1 = tt1;
      *tcg2 = tt2 + ( ( tt1 - DJM0 ) + ( tt2 - t77t ) ) * elgg;
   } else {
      *tcg1 = tt1 + ( ( tt2 - DJM0 ) + ( tt1 - t77t ) ) * elgg;
      *tcg2 = tt2;
   }

/* Status (always OK). */
   return 0;

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
