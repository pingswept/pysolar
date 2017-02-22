#include "sofam.h"
#include <stdlib.h>

int iauAf2a(char s, int ideg, int iamin, double asec, double *rad)
/*
**  - - - - - - - -
**   i a u A f 2 a
**  - - - - - - - -
**
**  Convert degrees, arcminutes, arcseconds to radians.
**
**  Status:  support function.
**
**  Given:
**     s         char    sign:  '-' = negative, otherwise positive
**     ideg      int     degrees
**     iamin     int     arcminutes
**     asec      double  arcseconds
**
**  Returned:
**     rad       double  angle in radians
**
**  Returned (function value):
**               int     status:  0 = OK
**                                1 = ideg outside range 0-359
**                                2 = iamin outside range 0-59
**                                3 = asec outside range 0-59.999...
**
**  Notes:
**
**  1)  The result is computed even if any of the range checks fail.
**
**  2)  Negative ideg, iamin and/or asec produce a warning status, but
**      the absolute value is used in the conversion.
**
**  3)  If there are multiple errors, the status value reflects only the
**      first, the smallest taking precedence.
**
**  This revision:  2012 February 13
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{

/* Compute the interval. */
   *rad  = ( s == '-' ? -1.0 : 1.0 ) *
           ( 60.0 * ( 60.0 * ( (double) abs(ideg) ) +
                             ( (double) abs(iamin) ) ) +
                                        fabs(asec) ) * DAS2R;

/* Validate arguments and return status. */
   if ( ideg < 0 || ideg > 359 ) return 1;
   if ( iamin < 0 || iamin > 59 ) return 2;
   if ( asec < 0.0 || asec >= 60.0 ) return 3;
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
