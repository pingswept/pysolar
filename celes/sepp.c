#include "sofam.h"

double iauSepp(double a[3], double b[3])
/*
**  - - - - - - - -
**   i a u S e p p
**  - - - - - - - -
**
**  Angular separation between two p-vectors.
**
**  Status:  vector/matrix support function.
**
**  Given:
**     a      double[3]    first p-vector (not necessarily unit length)
**     b      double[3]    second p-vector (not necessarily unit length)
**
**  Returned (function value):
**            double       angular separation (radians, always positive)
**
**  Notes:
**
**  1) If either vector is null, a zero result is returned.
**
**  2) The angular separation is most simply formulated in terms of
**     scalar product.  However, this gives poor accuracy for angles
**     near zero and pi.  The present algorithm uses both cross product
**     and dot product, to deliver full accuracy whatever the size of
**     the angle.
**
**  Called:
**     iauPxp       vector product of two p-vectors
**     iauPm        modulus of p-vector
**     iauPdp       scalar product of two p-vectors
**
**  This revision:  2008 May 22
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double axb[3], ss, cs, s;


/* Sine of angle between the vectors, multiplied by the two moduli. */
   iauPxp(a, b, axb);
   ss = iauPm(axb);

/* Cosine of the angle, multiplied by the two moduli. */
   cs = iauPdp(a, b);

/* The angle. */
   s = ((ss != 0.0) || (cs != 0.0)) ? atan2(ss, cs) : 0.0;

   return s;

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
