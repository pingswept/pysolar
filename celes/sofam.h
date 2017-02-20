#ifndef SOFAMHDEF
#define SOFAMHDEF

/*
**  - - - - - - - -
**   s o f a m . h
**  - - - - - - - -
**
**  Macros used by SOFA library.
**
**  Please note that the constants defined below are to be used only in
**  the context of the SOFA software, and have no other official IAU
**  status.
**
**  This revision:   2012 February 23
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/

#include "sofa.h"


/* Pi */
#define DPI (3.141592653589793238462643)

/* 2Pi */
#define D2PI (6.283185307179586476925287)

/* Degrees to radians */
#define DD2R (1.745329251994329576923691e-2)

/* Radians to arcseconds */
#define DR2AS (206264.8062470963551564734)

/* Arcseconds to radians */
#define DAS2R (4.848136811095359935899141e-6)

/* Seconds of time to radians */
#define DS2R (7.272205216643039903848712e-5)

/* Arcseconds in a full circle */
#define TURNAS (1296000.0)

/* Milliarcseconds to radians */
#define DMAS2R (DAS2R / 1e3)

/* Length of tropical year B1900 (days) */
#define DTY (365.242198781)

/* Seconds per day. */
#define DAYSEC (86400.0)

/* Days per Julian year */
#define DJY (365.25)

/* Days per Julian century */
#define DJC (36525.0)

/* Days per Julian millennium */
#define DJM (365250.0)

/* Reference epoch (J2000.0), Julian Date */
#define DJ00 (2451545.0)

/* Julian Date of Modified Julian Date zero */
#define DJM0 (2400000.5)

/* Reference epoch (J2000.0), Modified Julian Date */
#define DJM00 (51544.5)

/* 1977 Jan 1.0 as MJD */
#define DJM77 (43144.0)

/* TT minus TAI (s) */
#define TTMTAI (32.184)

/* AU (m) */
#define DAU (149597870e3)

/* Speed of light (AU per day) */
#define DC (DAYSEC / 499.004782)

/* L_G = 1 - d(TT)/d(TCG) */
#define ELG (6.969290134e-10)

/* L_B = 1 - d(TDB)/d(TCB), and TDB (s) at TAI 1977/1/1.0 */
#define ELB (1.550519768e-8)
#define TDB0 (-6.55e-5)

/* dint(A) - truncate to nearest whole number towards zero (double) */
#define dint(A) ((A)<0.0?ceil(A):floor(A))

/* dnint(A) - round to nearest whole number (double) */
#define dnint(A) ((A)<0.0?ceil((A)-0.5):floor((A)+0.5))

/* dsign(A,B) - magnitude of A with sign of B (double) */
#define dsign(A,B) ((B)<0.0?-fabs(A):fabs(A))

/* Reference ellipsoids */
#define WGS84 1
#define GRS80 2
#define WGS72 3

#endif

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
