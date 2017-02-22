#include "sofam.h"

void iauS2pv(double theta, double phi, double r,
             double td, double pd, double rd,
             double pv[2][3])
/*
**  - - - - - - - -
**   i a u S 2 p v
**  - - - - - - - -
**
**  Convert position/velocity from spherical to Cartesian coordinates.
**
**  Status:  vector/matrix support function.
**
**  Given:
**     theta    double          longitude angle (radians)
**     phi      double          latitude angle (radians)
**     r        double          radial distance
**     td       double          rate of change of theta
**     pd       double          rate of change of phi
**     rd       double          rate of change of r
**
**  Returned:
**     pv       double[2][3]    pv-vector
**
**  This revision:  2008 May 25
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double st, ct, sp, cp, rcp, x, y, rpd, w;


   st = sin(theta);
   ct = cos(theta);
   sp = sin(phi);
   cp = cos(phi);
   rcp = r * cp;
   x = rcp * ct;
   y = rcp * st;
   rpd = r * pd;
   w = rpd*sp - cp*rd;

   pv[0][0] = x;
   pv[0][1] = y;
   pv[0][2] = r * sp;
   pv[1][0] = -y*td - w*ct;
   pv[1][1] =  x*td - w*st;
   pv[1][2] = rpd*cp + sp*rd;

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
