#include "sofam.h"

int iauCal2jd(int iy, int im, int id, double *djm0, double *djm)
/*
**  - - - - - - - - - -
**   i a u C a l 2 j d
**  - - - - - - - - - -
**
**  Gregorian Calendar to Julian Date.
**
**  Status:  support function.
**
**  Given:
**     iy,im,id  int     year, month, day in Gregorian calendar (Note 1)
**
**  Returned:
**     djm0      double  MJD zero-point: always 2400000.5
**     djm       double  Modified Julian Date for 0 hrs
**
**  Returned (function value):
**               int     status:
**                           0 = OK
**                          -1 = bad year   (Note 3: JD not computed)
**                          -2 = bad month  (JD not computed)
**                          -3 = bad day    (JD computed)
**
**  Notes:
**
**  1) The algorithm used is valid from -4800 March 1, but this
**     implementation rejects dates before -4799 January 1.
**
**  2) The Julian Date is returned in two pieces, in the usual SOFA
**     manner, which is designed to preserve time resolution.  The
**     Julian Date is available as a single number by adding djm0 and
**     djm.
**
**  3) In early eras the conversion is from the "Proleptic Gregorian
**     Calendar";  no account is taken of the date(s) of adoption of
**     the Gregorian Calendar, nor is the AD/BC numbering convention
**     observed.
**
**  Reference:
**
**     Explanatory Supplement to the Astronomical Almanac,
**     P. Kenneth Seidelmann (ed), University Science Books (1992),
**     Section 12.92 (p604).
**
**  This revision:  2009 October 19
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   int j, ly, my;
   long iypmy;

/* Earliest year allowed (4800BC) */
   const int IYMIN = -4799;

/* Month lengths in days */
   static const int mtab[]
                     = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};


/* Preset status. */
   j = 0;

/* Validate year and month. */
   if (iy < IYMIN) return -1;
   if (im < 1 || im > 12) return -2;

/* If February in a leap year, 1, otherwise 0. */
   ly = ((im == 2) && !(iy%4) && (iy%100 || !(iy%400)));

/* Validate day, taking into account leap years. */
   if ( (id < 1) || (id > (mtab[im-1] + ly))) j = -3;

/* Return result. */
   my = (im - 14) / 12;
   iypmy = (long) (iy + my);
   *djm0 = 2400000.5;
   *djm = (double)((1461L * (iypmy + 4800L)) / 4L
                 + (367L * (long) (im - 2 - 12 * my)) / 12L
                 - (3L * ((iypmy + 4900L) / 100L)) / 4L
                 + (long) id - 2432076L);

/* Return status. */
   return j;

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
