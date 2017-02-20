#include "sofam.h"

int iauTcbtdb(double tcb1, double tcb2, double *tdb1, double *tdb2)
/*
**  - - - - - - - - - -
**   i a u T c b t d b
**  - - - - - - - - - -
**
**  Time scale transformation:  Barycentric Coordinate Time, TCB, to
**  Barycentric Dynamical Time, TDB.
**
**  Status:  canonical.
**
**  Given:
**     tcb1,tcb2  double    TCB as a 2-part Julian Date
**
**  Returned:
**     tdb1,tdb2  double    TDB as a 2-part Julian Date
**
**  Returned (function value):
**                int       status:  0 = OK
**
**  Notes:
**
**  1) tcb1+tcb2 is Julian Date, apportioned in any convenient way
**     between the two arguments, for example where tcb1 is the Julian
**     Day Number and tcb2 is the fraction of a day.  The returned
**     tdb1,tdb2 follow suit.
**
**  2) The 2006 IAU General Assembly introduced a conventional linear
**     transformation between TDB and TCB.  This transformation
**     compensates for the drift between TCB and terrestrial time TT,
**     and keeps TDB approximately centered on TT.  Because the
**     relationship between TT and TCB depends on the adopted solar
**     system ephemeris, the degree of alignment between TDB and TT over
**     long intervals will vary according to which ephemeris is used.
**     Former definitions of TDB attempted to avoid this problem by
**     stipulating that TDB and TT should differ only by periodic
**     effects.  This is a good description of the nature of the
**     relationship but eluded precise mathematical formulation.  The
**     conventional linear relationship adopted in 2006 sidestepped
**     these difficulties whilst delivering a TDB that in practice was
**     consistent with values before that date.
**
**  3) TDB is essentially the same as Teph, the time argument for the
**     JPL solar system ephemerides.
**
**  Reference:
**
**     IAU 2006 Resolution B3
**
**  This revision:  2011 May 14
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{

/* 1977 Jan 1 00:00:32.184 TT, as two-part JD */
   static const double t77td = DJM0 + DJM77;
   static const double t77tf = TTMTAI/DAYSEC;

/* TDB (days) at TAI 1977 Jan 1.0 */
   static const double tdb0 = TDB0/DAYSEC;

   double d;


/* Result, safeguarding precision. */
   if ( tcb1 > tcb2 ) {
      d = tcb1 - t77td;
      *tdb1 = tcb1;
      *tdb2 = tcb2 + tdb0 - ( d + ( tcb2 - t77tf ) ) * ELB;
   } else {
      d = tcb2 - t77td;
      *tdb1 = tcb1 + tdb0 - ( d + ( tcb1 - t77tf ) ) * ELB;
      *tdb2 = tcb2;
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
