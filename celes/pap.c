#include "sofam.h"

double iauPap(double a[3], double b[3])
/*
**  - - - - - - -
**   i a u P a p
**  - - - - - - -
**
**  Position-angle from two p-vectors.
**
**  Status:  vector/matrix support function.
**
**  Given:
**     a      double[3]  direction of reference point
**     b      double[3]  direction of point whose PA is required
**
**  Returned (function value):
**            double     position angle of b with respect to a (radians)
**
**  Notes:
**
**  1) The result is the position angle, in radians, of direction b with
**     respect to direction a.  It is in the range -pi to +pi.  The
**     sense is such that if b is a small distance "north" of a the
**     position angle is approximately zero, and if b is a small
**     distance "east" of a the position angle is approximately +pi/2.
**
**  2) The vectors a and b need not be of unit length.
**
**  3) Zero is returned if the two directions are the same or if either
**     vector is null.
**
**  4) If vector a is at a pole, the result is ill-defined.
**
**  Called:
**     iauPn        decompose p-vector into modulus and direction
**     iauPm        modulus of p-vector
**     iauPxp       vector product of two p-vectors
**     iauPmp       p-vector minus p-vector
**     iauPdp       scalar product of two p-vectors
**
**  This revision:  2008 May 25
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double am, au[3], bm, st, ct, xa, ya, za, eta[3], xi[3], a2b[3], pa;


/* Modulus and direction of the a vector. */
   iauPn(a, &am, au);

/* Modulus of the b vector. */
   bm = iauPm(b);

/* Deal with the case of a null vector. */
   if ((am == 0.0) || (bm == 0.0)) {
      st = 0.0;
      ct = 1.0;
   } else {

   /* The "north" axis tangential from a (arbitrary length). */
      xa = a[0];
      ya = a[1];
      za = a[2];
      eta[0] = -xa * za;
      eta[1] = -ya * za;
      eta[2] =  xa*xa + ya*ya;

   /* The "east" axis tangential from a (same length). */
      iauPxp(eta, au, xi);

   /* The vector from a to b. */
      iauPmp(b, a, a2b);

   /* Resolve into components along the north and east axes. */
      st = iauPdp(a2b, xi);
      ct = iauPdp(a2b, eta);

   /* Deal with degenerate cases. */
      if ((st == 0.0) && (ct == 0.0)) ct = 1.0;
   }

/* Position angle. */
   pa = atan2(st, ct);

   return pa;

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
