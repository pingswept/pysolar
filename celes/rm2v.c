#include "sofam.h"

void iauRm2v(double r[3][3], double w[3])
/*
**  - - - - - - - -
**   i a u R m 2 v
**  - - - - - - - -
**
**  Express an r-matrix as an r-vector.
**
**  Status:  vector/matrix support function.
**
**  Given:
**     r        double[3][3]    rotation matrix
**
**  Returned:
**     w        double[3]       rotation vector (Note 1)
**
**  Notes:
**
**  1) A rotation matrix describes a rotation through some angle about
**     some arbitrary axis called the Euler axis.  The "rotation vector"
**     returned by this function has the same direction as the Euler axis,
**     and its magnitude is the angle in radians.  (The magnitude and
**     direction can be separated by means of the function iauPn.)
**
**  2) If r is null, so is the result.  If r is not a rotation matrix
**     the result is undefined;  r must be proper (i.e. have a positive
**     determinant) and real orthogonal (inverse = transpose).
**
**  3) The reference frame rotates clockwise as seen looking along
**     the rotation vector from the origin.
**
**  This revision:  2010 August 27
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double x, y, z, s2, c2, phi, f;


   x = r[1][2] - r[2][1];
   y = r[2][0] - r[0][2];
   z = r[0][1] - r[1][0];
   s2 = sqrt(x*x + y*y + z*z);
   if (s2 != 0) {
      c2 = r[0][0] + r[1][1] + r[2][2] - 1.0;
      phi = atan2(s2, c2);
      f =  phi / s2;
      w[0] = x * f;
      w[1] = y * f;
      w[2] = z * f;
   } else {
      w[0] = 0.0;
      w[1] = 0.0;
      w[2] = 0.0;
   }

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
