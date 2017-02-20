#include "sofam.h"

void iauC2s(double p[3], double *theta, double *phi)
/*
**  - - - - - - -
**   i a u C 2 s
**  - - - - - - -
**
**  P-vector to spherical coordinates.
**
**  Status:  vector/matrix support function.
**
**  Given:
**     p      double[3]    p-vector
**
**  Returned:
**     theta  double       longitude angle (radians)
**     phi    double       latitude angle (radians)
**
**  Notes:
**
**  1) The vector p can have any magnitude; only its direction is used.
**
**  2) If p is null, zero theta and phi are returned.
**
**  3) At either pole, zero theta is returned.
**
**  This revision:  2008 May 11
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double x, y, z, d2;


   x  = p[0];
   y  = p[1];
   z  = p[2];
   d2 = x*x + y*y;

   *theta = (d2 == 0.0) ? 0.0 : atan2(y, x);
   *phi = (z == 0.0) ? 0.0 : atan2(z, sqrt(d2));

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
