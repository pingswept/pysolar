#include "sofam.h"

void iauPv2s(double pv[2][3],
             double *theta, double *phi, double *r,
             double *td, double *pd, double *rd)
/*
**  - - - - - - - -
**   i a u P v 2 s
**  - - - - - - - -
**
**  Convert position/velocity from Cartesian to spherical coordinates.
**
**  Status:  vector/matrix support function.
**
**  Given:
**     pv       double[2][3]  pv-vector
**
**  Returned:
**     theta    double        longitude angle (radians)
**     phi      double        latitude angle (radians)
**     r        double        radial distance
**     td       double        rate of change of theta
**     pd       double        rate of change of phi
**     rd       double        rate of change of r
**
**  Notes:
**
**  1) If the position part of pv is null, theta, phi, td and pd
**     are indeterminate.  This is handled by extrapolating the
**     position through unit time by using the velocity part of
**     pv.  This moves the origin without changing the direction
**     of the velocity component.  If the position and velocity
**     components of pv are both null, zeroes are returned for all
**     six results.
**
**  2) If the position is a pole, theta, td and pd are indeterminate.
**     In such cases zeroes are returned for all three.
**
**  This revision:  2008 October 28
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double x, y, z, xd, yd, zd, rxy2, rxy, r2, rtrue, rw, xyp;


/* Components of position/velocity vector. */
   x  = pv[0][0];
   y  = pv[0][1];
   z  = pv[0][2];
   xd = pv[1][0];
   yd = pv[1][1];
   zd = pv[1][2];

/* Component of r in XY plane squared. */
   rxy2 = x*x + y*y;

/* Modulus squared. */
   r2 = rxy2 + z*z;

/* Modulus. */
   rtrue = sqrt(r2);

/* If null vector, move the origin along the direction of movement. */
   rw = rtrue;
   if (rtrue == 0.0) {
       x = xd;
       y = yd;
       z = zd;
       rxy2 = x*x + y*y;
       r2 = rxy2 + z*z;
       rw = sqrt(r2);
   }

/* Position and velocity in spherical coordinates. */
   rxy = sqrt(rxy2);
   xyp = x*xd + y*yd;
   if (rxy2 != 0.0) {
       *theta = atan2(y, x);
       *phi = atan2(z, rxy);
       *td = (x*yd - y*xd) / rxy2;
       *pd = (zd*rxy2 - z*xyp) / (r2*rxy);
   } else {
       *theta = 0.0;
       *phi = (z != 0.0) ? atan2(z, rxy) : 0.0;
       *td = 0.0;
       *pd = 0.0;
   }
   *r = rtrue;
   *rd = (rw != 0.0) ? (xyp + z*zd) / rw : 0.0;

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
