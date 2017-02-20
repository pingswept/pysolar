#include "sofam.h"

void iauRy(double theta, double r[3][3])
/*
**  - - - - - -
**   i a u R y
**  - - - - - -
**
**  Rotate an r-matrix about the y-axis.
**
**  Status:  vector/matrix support function.
**
**  Given:
**     theta  double          angle (radians)
**
**  Given and returned:
**     r      double[3][3]    r-matrix, rotated
**
**  Notes:
**
**  1) Calling this function with positive theta incorporates in the
**     supplied r-matrix r an additional rotation, about the y-axis,
**     anticlockwise as seen looking towards the origin from positive y.
**
**  2) The additional rotation can be represented by this matrix:
**
**         (  + cos(theta)     0      - sin(theta)  )
**         (                                        )
**         (       0           1           0        )
**         (                                        )
**         (  + sin(theta)     0      + cos(theta)  )
**
**  This revision:  2012 April 3
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/
{
   double s, c, a00, a01, a02, a20, a21, a22;


   s = sin(theta);
   c = cos(theta);

   a00 = c*r[0][0] - s*r[2][0];
   a01 = c*r[0][1] - s*r[2][1];
   a02 = c*r[0][2] - s*r[2][2];
   a20 = s*r[0][0] + c*r[2][0];
   a21 = s*r[0][1] + c*r[2][1];
   a22 = s*r[0][2] + c*r[2][2];

   r[0][0] = a00;
   r[0][1] = a01;
   r[0][2] = a02;
   r[2][0] = a20;
   r[2][1] = a21;
   r[2][2] = a22;

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
