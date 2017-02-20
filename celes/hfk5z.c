#include "sofam.h"

void iauHfk5z(double rh, double dh, double date1, double date2,
              double *r5, double *d5, double *dr5, double *dd5)
/*
**  - - - - - - - - -
**   i a u H f k 5 z
**  - - - - - - - - -
**
**  Transform a Hipparcos star position into FK5 J2000.0, assuming
**  zero Hipparcos proper motion.
**
**  Status:  support function.
**
**  Given:
**     rh            double    Hipparcos RA (radians)
**     dh            double    Hipparcos Dec (radians)
**     date1,date2   double    TDB date (Note 1)
**
**  Returned (all FK5, equinox J2000.0, date date1+date2):
**     r5            double    RA (radians)
**     d5            double    Dec (radians)
**     dr5           double    FK5 RA proper motion (rad/year, Note 4)
**     dd5           double    Dec proper motion (rad/year, Note 4)
**
**  Notes:
**
**  1) The TT date date1+date2 is a Julian Date, apportioned in any
**     convenient way between the two arguments.  For example,
**     JD(TT)=2450123.7 could be expressed in any of these ways,
**     among others:
**
**            date1          date2
**
**         2450123.7           0.0       (JD method)
**         2451545.0       -1421.3       (J2000 method)
**         2400000.5       50123.2       (MJD method)
**         2450123.5           0.2       (date & time method)
**
**     The JD method is the most natural and convenient to use in
**     cases where the loss of several decimal digits of resolution
**     is acceptable.  The J2000 method is best matched to the way
**     the argument is handled internally and will deliver the
**     optimum resolution.  The MJD method and the date & time methods
**     are both good compromises between resolution and convenience.
**
**  2) The proper motion in RA is dRA/dt rather than cos(Dec)*dRA/dt.
**
**  3) The FK5 to Hipparcos transformation is modeled as a pure rotation
**     and spin;  zonal errors in the FK5 catalogue are not taken into
**     account.
**
**  4) It was the intention that Hipparcos should be a close
**     approximation to an inertial frame, so that distant objects have
**     zero proper motion;  such objects have (in general) non-zero
**     proper motion in FK5, and this function returns those fictitious
**     proper motions.
**
**  5) The position returned by this function is in the FK5 J2000.0
**     reference system but at date date1+date2.
**
**  6) See also iauFk52h, iauH2fk5, iauFk5zhz.
**
**  Called:
**     iauS2c       spherical coordinates to unit vector
**     iauFk5hip    FK5 to Hipparcos rotation and spin
**     iauRxp       product of r-matrix and p-vector
**     iauSxp       multiply p-vector by scalar
**     iauRxr       product of two r-matrices
**     iauTrxp      product of transpose of r-matrix and p-vector
**     iauPxp       vector product of two p-vectors
**     iauPv2s      pv-vector to spherical
**     iauAnp       normalize angle into range 0 to 2pi
**
**  Reference:
**
**     F.Mignard & M.Froeschle, 2000, Astron.Astrophys. 354, 732-739.
**
**  This revision:  2009 December 17
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double t, ph[3], r5h[3][3], s5h[3], sh[3], vst[3],
   rst[3][3], r5ht[3][3], pv5e[2][3], vv[3],
   w, r, v;


/* Time interval from fundamental epoch J2000.0 to given date (JY). */
   t = ((date1 - DJ00) + date2) / DJY;

/* Hipparcos barycentric position vector (normalized). */
   iauS2c(rh, dh, ph);

/* FK5 to Hipparcos orientation matrix and spin vector. */
   iauFk5hip(r5h, s5h);

/* Rotate the spin into the Hipparcos system. */
   iauRxp(r5h, s5h, sh);

/* Accumulated Hipparcos wrt FK5 spin over that interval. */
   iauSxp(t, s5h, vst);

/* Express the accumulated spin as a rotation matrix. */
   iauRv2m(vst, rst);

/* Rotation matrix:  accumulated spin, then FK5 to Hipparcos. */
   iauRxr(r5h, rst, r5ht);

/* De-orient & de-spin the Hipparcos position into FK5 J2000.0. */
   iauTrxp(r5ht, ph, pv5e[0]);

/* Apply spin to the position giving a space motion. */
   iauPxp(sh, ph, vv);

/* De-orient & de-spin the Hipparcos space motion into FK5 J2000.0. */
   iauTrxp(r5ht, vv, pv5e[1]);

/* FK5 position/velocity pv-vector to spherical. */
   iauPv2s(pv5e, &w, d5, &r, dr5, dd5, &v);
   *r5 = iauAnp(w);

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
