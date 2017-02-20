#include "sofam.h"

void iauFk5hip(double r5h[3][3], double s5h[3])
/*
**  - - - - - - - - - -
**   i a u F k 5 h i p
**  - - - - - - - - - -
**
**  FK5 to Hipparcos rotation and spin.
**
**  Status:  support function.
**
**  Returned:
**     r5h   double[3][3]  r-matrix: FK5 rotation wrt Hipparcos (Note 2)
**     s5h   double[3]     r-vector: FK5 spin wrt Hipparcos (Note 3)
**
**  Notes:
**
**  1) This function models the FK5 to Hipparcos transformation as a
**     pure rotation and spin;  zonal errors in the FK5 catalogue are
**     not taken into account.
**
**  2) The r-matrix r5h operates in the sense:
**
**           P_Hipparcos = r5h x P_FK5
**
**     where P_FK5 is a p-vector in the FK5 frame, and P_Hipparcos is
**     the equivalent Hipparcos p-vector.
**
**  3) The r-vector s5h represents the time derivative of the FK5 to
**     Hipparcos rotation.  The units are radians per year (Julian,
**     TDB).
**
**  Called:
**     iauRv2m      r-vector to r-matrix
**
**  Reference:
**
**     F.Mignard & M.Froeschle, Astron. Astrophys. 354, 732-739 (2000).
**
**  This revision:  2009 March 14
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double v[3];

/* FK5 wrt Hipparcos orientation and spin (radians, radians/year) */
   double epx, epy, epz;
   double omx, omy, omz;


   epx = -19.9e-3 * DAS2R;
   epy =  -9.1e-3 * DAS2R;
   epz =  22.9e-3 * DAS2R;

   omx = -0.30e-3 * DAS2R;
   omy =  0.60e-3 * DAS2R;
   omz =  0.70e-3 * DAS2R;

/* FK5 to Hipparcos orientation expressed as an r-vector. */
   v[0] = epx;
   v[1] = epy;
   v[2] = epz;

/* Re-express as an r-matrix. */
   iauRv2m(v, r5h);

/* Hipparcos wrt FK5 spin expressed as an r-vector. */
   s5h[0] = omx;
   s5h[1] = omy;
   s5h[2] = omz;

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
