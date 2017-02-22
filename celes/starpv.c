#include "sofam.h"

int iauStarpv(double ra, double dec,
              double pmr, double pmd, double px, double rv,
              double pv[2][3])
/*
**  - - - - - - - - - -
**   i a u S t a r p v
**  - - - - - - - - - -
**
**  Convert star catalog coordinates to position+velocity vector.
**
**  Status:  support function.
**
**  Given (Note 1):
**     ra     double        right ascension (radians)
**     dec    double        declination (radians)
**     pmr    double        RA proper motion (radians/year)
**     pmd    double        Dec proper motion (radians/year)
**     px     double        parallax (arcseconds)
**     rv     double        radial velocity (km/s, positive = receding)
**
**  Returned (Note 2):
**     pv     double[2][3]  pv-vector (AU, AU/day)
**
**  Returned (function value):
**            int           status:
**                              0 = no warnings
**                              1 = distance overridden (Note 6)
**                              2 = excessive speed (Note 7)
**                              4 = solution didn't converge (Note 8)
**                           else = binary logical OR of the above
**
**  Notes:
**
**  1) The star data accepted by this function are "observables" for an
**     imaginary observer at the solar-system barycenter.  Proper motion
**     and radial velocity are, strictly, in terms of barycentric
**     coordinate time, TCB.  For most practical applications, it is
**     permissible to neglect the distinction between TCB and ordinary
**     "proper" time on Earth (TT/TAI).  The result will, as a rule, be
**     limited by the intrinsic accuracy of the proper-motion and
**     radial-velocity data;  moreover, the pv-vector is likely to be
**     merely an intermediate result, so that a change of time unit
**     would cancel out overall.
**
**     In accordance with normal star-catalog conventions, the object's
**     right ascension and declination are freed from the effects of
**     secular aberration.  The frame, which is aligned to the catalog
**     equator and equinox, is Lorentzian and centered on the SSB.
**
**  2) The resulting position and velocity pv-vector is with respect to
**     the same frame and, like the catalog coordinates, is freed from
**     the effects of secular aberration.  Should the "coordinate
**     direction", where the object was located at the catalog epoch, be
**     required, it may be obtained by calculating the magnitude of the
**     position vector pv[0][0-2] dividing by the speed of light in
**     AU/day to give the light-time, and then multiplying the space
**     velocity pv[1][0-2] by this light-time and adding the result to
**     pv[0][0-2].
**
**     Summarizing, the pv-vector returned is for most stars almost
**     identical to the result of applying the standard geometrical
**     "space motion" transformation.  The differences, which are the
**     subject of the Stumpff paper referenced below, are:
**
**     (i) In stars with significant radial velocity and proper motion,
**     the constantly changing light-time distorts the apparent proper
**     motion.  Note that this is a classical, not a relativistic,
**     effect.
**
**     (ii) The transformation complies with special relativity.
**
**  3) Care is needed with units.  The star coordinates are in radians
**     and the proper motions in radians per Julian year, but the
**     parallax is in arcseconds; the radial velocity is in km/s, but
**     the pv-vector result is in AU and AU/day.
**
**  4) The RA proper motion is in terms of coordinate angle, not true
**     angle.  If the catalog uses arcseconds for both RA and Dec proper
**     motions, the RA proper motion will need to be divided by cos(Dec)
**     before use.
**
**  5) Straight-line motion at constant speed, in the inertial frame,
**     is assumed.
**
**  6) An extremely small (or zero or negative) parallax is interpreted
**     to mean that the object is on the "celestial sphere", the radius
**     of which is an arbitrary (large) value (see the constant PXMIN).
**     When the distance is overridden in this way, the status,
**     initially zero, has 1 added to it.
**
**  7) If the space velocity is a significant fraction of c (see the
**     constant VMAX), it is arbitrarily set to zero.  When this action
**     occurs, 2 is added to the status.
**
**  8) The relativistic adjustment involves an iterative calculation.
**     If the process fails to converge within a set number (IMAX) of
**     iterations, 4 is added to the status.
**
**  9) The inverse transformation is performed by the function
**     iauPvstar.
**
**  Called:
**     iauS2pv      spherical coordinates to pv-vector
**     iauPm        modulus of p-vector
**     iauZp        zero p-vector
**     iauPn        decompose p-vector into modulus and direction
**     iauPdp       scalar product of two p-vectors
**     iauSxp       multiply p-vector by scalar
**     iauPmp       p-vector minus p-vector
**     iauPpp       p-vector plus p-vector
**
**  Reference:
**
**     Stumpff, P., 1985, Astron.Astrophys. 144, 232-240.
**
**  This revision:  2009 July 6
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
/* Smallest allowed parallax */
   static const double PXMIN = 1e-7;

/* Largest allowed speed (fraction of c) */
   static const double VMAX = 0.5;

/* Maximum number of iterations for relativistic solution */
   static const int IMAX = 100;

   int i, iwarn;
   double w, r, rd, rad, decd, v, x[3], usr[3], ust[3],
          vsr, vst, betst, betsr, bett, betr,
          dd, ddel, ur[3], ut[3],
          d = 0.0, del = 0.0,       /* to prevent */
          odd = 0.0, oddel = 0.0,   /* compiler   */
          od = 0.0, odel = 0.0;     /* warnings   */


/* Distance (AU). */
   if (px >= PXMIN) {
      w = px;
      iwarn = 0;
   } else {
      w = PXMIN;
      iwarn = 1;
   }
   r = DR2AS / w;

/* Radial velocity (AU/day). */
   rd = DAYSEC * rv * 1e3 / DAU;

/* Proper motion (radian/day). */
   rad = pmr / DJY;
   decd = pmd / DJY;

/* To pv-vector (AU,AU/day). */
   iauS2pv(ra, dec, r, rad, decd, rd, pv);

/* If excessive velocity, arbitrarily set it to zero. */
   v = iauPm(pv[1]);
   if (v / DC > VMAX) {
      iauZp(pv[1]);
      iwarn += 2;
   }

/* Isolate the radial component of the velocity (AU/day). */
   iauPn(pv[0], &w, x);
   vsr = iauPdp(x, pv[1]);
   iauSxp(vsr, x, usr);

/* Isolate the transverse component of the velocity (AU/day). */
   iauPmp(pv[1], usr, ust);
   vst = iauPm(ust);

/* Special-relativity dimensionless parameters. */
   betsr = vsr / DC;
   betst = vst / DC;

/* Determine the inertial-to-observed relativistic correction terms. */
   bett = betst;
   betr = betsr;
   for (i = 0; i < IMAX; i++) {
      d = 1.0 + betr;
      del = sqrt(1.0 - betr*betr - bett*bett) - 1.0;
      betr = d * betsr + del;
      bett = d * betst;
      if (i > 0) {
         dd = fabs(d - od);
         ddel = fabs(del - odel);
         if ((i > 1) && (dd >= odd) && (ddel >= oddel)) break;
         odd = dd;
         oddel = ddel;
      }
      od = d;
      odel = del;
   }
   if (i >= IMAX) iwarn += 4;

/* Replace observed radial velocity with inertial value. */
   w = (betsr != 0.0) ? d + del / betsr : 1.0;
   iauSxp(w, usr, ur);

/* Replace observed tangential velocity with inertial value. */
   iauSxp(d, ust, ut);

/* Combine the two to obtain the inertial space velocity. */
   iauPpp(ur, ut, pv[1]);

/* Return the status. */
   return iwarn;

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
