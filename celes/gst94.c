#include "sofa.h"

double iauGst94(double uta, double utb)
/*
**  - - - - - - - - -
**   i a u G s t 9 4
**  - - - - - - - - -
**
**  Greenwich apparent sidereal time (consistent with IAU 1982/94
**  resolutions).
**
**  Status:  support function.
**
**  Given:
**     uta,utb    double    UT1 as a 2-part Julian Date (Notes 1,2)
**
**  Returned (function value):
**                double    Greenwich apparent sidereal time (radians)
**
**  Notes:
**
**  1) The UT1 date uta+utb is a Julian Date, apportioned in any
**     convenient way between the argument pair.  For example,
**     JD=2450123.7 could be expressed in any of these ways, among
**     others:
**
**             uta            utb
**
**         2450123.7           0.0       (JD method)
**         2451545.0       -1421.3       (J2000 method)
**         2400000.5       50123.2       (MJD method)
**         2450123.5           0.2       (date & time method)
**
**     The JD method is the most natural and convenient to use in cases
**     where the loss of several decimal digits of resolution is
**     acceptable.  The J2000 and MJD methods are good compromises
**     between resolution and convenience.  For UT, the date & time
**     method is best matched to the algorithm that is used by the Earth
**     Rotation Angle function, called internally:  maximum precision is
**     delivered when the uta argument is for 0hrs UT1 on the day in
**     question and the utb argument lies in the range 0 to 1, or vice
**     versa.
**
**  2) The result is compatible with the IAU 1982 and 1994 resolutions,
**     except that accuracy has been compromised for the sake of
**     convenience in that UT is used instead of TDB (or TT) to compute
**     the equation of the equinoxes.
**
**  3) This GAST must be used only in conjunction with contemporaneous
**     IAU standards such as 1976 precession, 1980 obliquity and 1982
**     nutation.  It is not compatible with the IAU 2000 resolutions.
**
**  4) The result is returned in the range 0 to 2pi.
**
**  Called:
**     iauGmst82    Greenwich mean sidereal time, IAU 1982
**     iauEqeq94    equation of the equinoxes, IAU 1994
**     iauAnp       normalize angle into range 0 to 2pi
**
**  References:
**
**     Explanatory Supplement to the Astronomical Almanac,
**     P. Kenneth Seidelmann (ed), University Science Books (1992)
**
**     IAU Resolution C7, Recommendation 3 (1994)
**
**  This revision:  2008 May 16
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double gmst82, eqeq94, gst;


   gmst82 = iauGmst82(uta, utb);
   eqeq94 = iauEqeq94(uta, utb);
   gst = iauAnp(gmst82  + eqeq94);

   return gst;

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
