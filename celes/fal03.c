#include "sofam.h"

double iauFal03(double t)
/*
**  - - - - - - - - -
**   i a u F a l 0 3
**  - - - - - - - - -
**
**  Fundamental argument, IERS Conventions (2003):
**  mean anomaly of the Moon.
**
**  Status:  canonical model.
**
**  Given:
**     t     double    TDB, Julian centuries since J2000.0 (Note 1)
**
**  Returned (function value):
**           double    l, radians (Note 2)
**
**  Notes:
**
**  1) Though t is strictly TDB, it is usually more convenient to use
**     TT, which makes no significant difference.
**
**  2) The expression used is as adopted in IERS Conventions (2003) and
**     is from Simon et al. (1994).
**
**  References:
**
**     McCarthy, D. D., Petit, G. (eds.), IERS Conventions (2003),
**     IERS Technical Note No. 32, BKG (2004)
**
**     Simon, J.-L., Bretagnon, P., Chapront, J., Chapront-Touze, M.,
**     Francou, G., Laskar, J. 1994, Astron.Astrophys. 282, 663-683
**
**  This revision:  2009 December 16
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double a;


/* Mean anomaly of the Moon (IERS Conventions 2003). */
   a = fmod(           485868.249036  +
             t * ( 1717915923.2178 +
             t * (         31.8792 +
             t * (          0.051635 +
             t * (        - 0.00024470 ) ) ) ), TURNAS ) * DAS2R;

   return a;

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
