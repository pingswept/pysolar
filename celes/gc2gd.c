#include "sofam.h"

int iauGc2gd ( int n, double xyz[3],
               double *elong, double *phi, double *height )
/*
**  - - - - - - - - -
**   i a u G c 2 g d
**  - - - - - - - - -
**
**  Transform geocentric coordinates to geodetic using the specified
**  reference ellipsoid.
**
**  Status:  canonical transformation.
**
**  Given:
**     n       int        ellipsoid identifier (Note 1)
**     xyz     double[3]  geocentric vector (Note 2)
**
**  Returned:
**     elong   double     longitude (radians, east +ve)
**     phi     double     latitude (geodetic, radians, Note 3)
**     height  double     height above ellipsoid (geodetic, Notes 2,3)
**
**  Returned (function value):
**            int         status:  0 = OK
**                                -1 = illegal identifier (Note 3)
**                                -2 = internal error (Note 3)
**
**  Notes:
**
**  1) The identifier n is a number that specifies the choice of
**     reference ellipsoid.  The following are supported:
**
**        n    ellipsoid
**
**        1     WGS84
**        2     GRS80
**        3     WGS72
**
**     The n value has no significance outside the SOFA software.  For
**     convenience, symbols WGS84 etc. are defined in sofam.h.
**
**  2) The geocentric vector (xyz, given) and height (height, returned)
**     are in meters.
**
**  3) An error status -1 means that the identifier n is illegal.  An
**     error status -2 is theoretically impossible.  In all error cases,
**     phi and height are both set to -1e9.
**
**  4) The inverse transformation is performed in the function iauGd2gc.
**
**  Called:
**     iauEform     Earth reference ellipsoids
**     iauGc2gde    geocentric to geodetic transformation, general
**
**  This revision:  2012 Febuary 23
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   int j;
   double a, f;


/* Obtain reference ellipsoid parameters. */
   j = iauEform ( n, &a, &f );

/* If OK, transform x,y,z to longitude, geodetic latitude, height. */
   if ( j == 0 ) {
      j = iauGc2gde ( a, f, xyz, elong, phi, height );
      if ( j < 0 ) j = -2;
   }

/* Deal with any errors. */
   if ( j < 0 ) {
      *phi = -1e9;
      *height = -1e9;
   }

/* Return the status. */
   return j;

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
