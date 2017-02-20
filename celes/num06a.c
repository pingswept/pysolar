#include "sofam.h"

void iauNum06a(double date1, double date2, double rmatn[3][3])
/*
**  - - - - - - - - - -
**   i a u N u m 0 6 a
**  - - - - - - - - - -
**
**  Form the matrix of nutation for a given date, IAU 2006/2000A model.
**
**  Status:  support function.
**
**  Given:
**     date1,date2   double          TT as a 2-part Julian Date (Note 1)
**
**  Returned:
**     rmatn         double[3][3]    nutation matrix
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
**  2) The matrix operates in the sense V(true) = rmatn * V(mean), where
**     the p-vector V(true) is with respect to the true equatorial triad
**     of date and the p-vector V(mean) is with respect to the mean
**     equatorial triad of date.
**
**  Called:
**     iauObl06     mean obliquity, IAU 2006
**     iauNut06a    nutation, IAU 2006/2000A
**     iauNumat     form nutation matrix
**
**  Reference:
**
**     Explanatory Supplement to the Astronomical Almanac,
**     P. Kenneth Seidelmann (ed), University Science Books (1992),
**     Section 3.222-3 (p114).
**
**  This revision:  2008 May 12
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double eps, dp, de;


/* Mean obliquity. */
   eps = iauObl06(date1, date2);

/* Nutation components. */
   iauNut06a(date1, date2, &dp, &de);

/* Nutation matrix. */
   iauNumat(eps, dp, de, rmatn);

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
