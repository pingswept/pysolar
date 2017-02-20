#include "sofam.h"

void iauFk52h(double r5, double d5,
              double dr5, double dd5, double px5, double rv5,
              double *rh, double *dh,
              double *drh, double *ddh, double *pxh, double *rvh)
/*
**  - - - - - - - - -
**   i a u F k 5 2 h
**  - - - - - - - - -
**
**  Transform FK5 (J2000.0) star data into the Hipparcos system.
**
**  Status:  support function.
**
**  Given (all FK5, equinox J2000.0, epoch J2000.0):
**     r5      double    RA (radians)
**     d5      double    Dec (radians)
**     dr5     double    proper motion in RA (dRA/dt, rad/Jyear)
**     dd5     double    proper motion in Dec (dDec/dt, rad/Jyear)
**     px5     double    parallax (arcsec)
**     rv5     double    radial velocity (km/s, positive = receding)
**
**  Returned (all Hipparcos, epoch J2000.0):
**     rh      double    RA (radians)
**     dh      double    Dec (radians)
**     drh     double    proper motion in RA (dRA/dt, rad/Jyear)
**     ddh     double    proper motion in Dec (dDec/dt, rad/Jyear)
**     pxh     double    parallax (arcsec)
**     rvh     double    radial velocity (km/s, positive = receding)
**
**  Notes:
**
**  1) This function transforms FK5 star positions and proper motions
**     into the system of the Hipparcos catalog.
**
**  2) The proper motions in RA are dRA/dt rather than
**     cos(Dec)*dRA/dt, and are per year rather than per century.
**
**  3) The FK5 to Hipparcos transformation is modeled as a pure
**     rotation and spin;  zonal errors in the FK5 catalog are not
**     taken into account.
**
**  4) See also iauH2fk5, iauFk5hz, iauHfk5z.
**
**  Called:
**     iauStarpv    star catalog data to space motion pv-vector
**     iauFk5hip    FK5 to Hipparcos rotation and spin
**     iauRxp       product of r-matrix and p-vector
**     iauPxp       vector product of two p-vectors
**     iauPpp       p-vector plus p-vector
**     iauPvstar    space motion pv-vector to star catalog data
**
**  Reference:
**
**     F.Mignard & M.Froeschle, Astron. Astrophys. 354, 732-739 (2000).
**
**  This revision:  2009 December 17
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   int i;
   double pv5[2][3], r5h[3][3], s5h[3], wxp[3], vv[3], pvh[2][3];


/* FK5 barycentric position/velocity pv-vector (normalized). */
   iauStarpv(r5, d5, dr5, dd5, px5, rv5, pv5);

/* FK5 to Hipparcos orientation matrix and spin vector. */
   iauFk5hip(r5h, s5h);

/* Make spin units per day instead of per year. */
   for ( i = 0; i < 3; s5h[i++] /= 365.25 );

/* Orient the FK5 position into the Hipparcos system. */
   iauRxp(r5h, pv5[0], pvh[0]);

/* Apply spin to the position giving an extra space motion component. */
   iauPxp(pv5[0], s5h, wxp);

/* Add this component to the FK5 space motion. */
   iauPpp(wxp, pv5[1], vv);

/* Orient the FK5 space motion into the Hipparcos system. */
   iauRxp(r5h, vv, pvh[1]);

/* Hipparcos pv-vector to spherical. */
   iauPvstar(pvh, rh, dh, drh, ddh, pxh, rvh);

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
