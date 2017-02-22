#ifndef SOFAHDEF
#define SOFAHDEF

/*
**  - - - - - - -
**   s o f a . h
**  - - - - - - -
**
**  Prototype function declarations for SOFA library.
**
**  This revision:   2012 February 23
**
**  Original version 2012-03-01
**
**  Copyright (C) 2013 Naoki Arita.  See notes at end.
*/

#include "math.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Astronomy/Calendars */
int iauCal2jd(int iy, int im, int id, double *djm0, double *djm);
double iauEpb(double dj1, double dj2);
void iauEpb2jd(double epb, double *djm0, double *djm);
double iauEpj(double dj1, double dj2);
void iauEpj2jd(double epj, double *djm0, double *djm);
int iauJd2cal(double dj1, double dj2,
                     int *iy, int *im, int *id, double *fd);
int iauJdcalf(int ndp, double dj1, double dj2, int iymdf[4]);

/* Astronomy/Ephemerides */
int iauEpv00(double date1, double date2,
             double pvh[2][3], double pvb[2][3]);
int iauPlan94(double date1, double date2, int np, double pv[2][3]);

/* Astronomy/FundamentalArgs */
double iauFad03(double t);
double iauFae03(double t);
double iauFaf03(double t);
double iauFaju03(double t);
double iauFal03(double t);
double iauFalp03(double t);
double iauFama03(double t);
double iauFame03(double t);
double iauFane03(double t);
double iauFaom03(double t);
double iauFapa03(double t);
double iauFasa03(double t);
double iauFaur03(double t);
double iauFave03(double t);

/* Astronomy/PrecNutPolar */
void iauBi00(double *dpsibi, double *depsbi, double *dra);
void iauBp00(double date1, double date2,
             double rb[3][3], double rp[3][3], double rbp[3][3]);
void iauBp06(double date1, double date2,
             double rb[3][3], double rp[3][3], double rbp[3][3]);
void iauBpn2xy(double rbpn[3][3], double *x, double *y);
void iauC2i00a(double date1, double date2, double rc2i[3][3]);
void iauC2i00b(double date1, double date2, double rc2i[3][3]);
void iauC2i06a(double date1, double date2, double rc2i[3][3]);
void iauC2ibpn(double date1, double date2, double rbpn[3][3],
               double rc2i[3][3]);
void iauC2ixy(double date1, double date2, double x, double y,
              double rc2i[3][3]);
void iauC2ixys(double x, double y, double s, double rc2i[3][3]);
void iauC2t00a(double tta, double ttb, double uta, double utb,
               double xp, double yp, double rc2t[3][3]);
void iauC2t00b(double tta, double ttb, double uta, double utb,
               double xp, double yp, double rc2t[3][3]);
void iauC2t06a(double tta, double ttb, double uta, double utb,
               double xp, double yp, double rc2t[3][3]);
void iauC2tcio(double rc2i[3][3], double era, double rpom[3][3],
               double rc2t[3][3]);
void iauC2teqx(double rbpn[3][3], double gst, double rpom[3][3],
               double rc2t[3][3]);
void iauC2tpe(double tta, double ttb, double uta, double utb,
              double dpsi, double deps, double xp, double yp,
              double rc2t[3][3]);
void iauC2txy(double tta, double ttb, double uta, double utb,
              double x, double y, double xp, double yp,
              double rc2t[3][3]);
double iauEo06a(double date1, double date2);
double iauEors(double rnpb[3][3], double s);
void iauFw2m(double gamb, double phib, double psi, double eps,
             double r[3][3]);
void iauFw2xy(double gamb, double phib, double psi, double eps,
              double *x, double *y);
void iauNum00a(double date1, double date2, double rmatn[3][3]);
void iauNum00b(double date1, double date2, double rmatn[3][3]);
void iauNum06a(double date1, double date2, double rmatn[3][3]);
void iauNumat(double epsa, double dpsi, double deps, double rmatn[3][3]);
void iauNut00a(double date1, double date2, double *dpsi, double *deps);
void iauNut00b(double date1, double date2, double *dpsi, double *deps);
void iauNut06a(double date1, double date2, double *dpsi, double *deps);
void iauNut80(double date1, double date2, double *dpsi, double *deps);
void iauNutm80(double date1, double date2, double rmatn[3][3]);
double iauObl06(double date1, double date2);
double iauObl80(double date1, double date2);
void iauP06e(double date1, double date2,
             double *eps0, double *psia, double *oma, double *bpa,
             double *bqa, double *pia, double *bpia,
             double *epsa, double *chia, double *za, double *zetaa,
             double *thetaa, double *pa,
             double *gam, double *phi, double *psi);
void iauPb06(double date1, double date2,
             double *bzeta, double *bz, double *btheta);
void iauPfw06(double date1, double date2,
              double *gamb, double *phib, double *psib, double *epsa);
void iauPmat00(double date1, double date2, double rbp[3][3]);
void iauPmat06(double date1, double date2, double rbp[3][3]);
void iauPmat76(double date1, double date2, double rmatp[3][3]);
void iauPn00(double date1, double date2, double dpsi, double deps,
             double *epsa,
             double rb[3][3], double rp[3][3], double rbp[3][3],
             double rn[3][3], double rbpn[3][3]);
void iauPn00a(double date1, double date2,
              double *dpsi, double *deps, double *epsa,
              double rb[3][3], double rp[3][3], double rbp[3][3],
              double rn[3][3], double rbpn[3][3]);
void iauPn00b(double date1, double date2,
              double *dpsi, double *deps, double *epsa,
              double rb[3][3], double rp[3][3], double rbp[3][3],
              double rn[3][3], double rbpn[3][3]);
void iauPn06(double date1, double date2, double dpsi, double deps,
             double *epsa,
             double rb[3][3], double rp[3][3], double rbp[3][3],
             double rn[3][3], double rbpn[3][3]);
void iauPn06a(double date1, double date2,
              double *dpsi, double *deps, double *epsa,
              double rb[3][3], double rp[3][3], double rbp[3][3],
              double rn[3][3], double rbpn[3][3]);
void iauPnm00a(double date1, double date2, double rbpn[3][3]);
void iauPnm00b(double date1, double date2, double rbpn[3][3]);
void iauPnm06a(double date1, double date2, double rnpb[3][3]);
void iauPnm80(double date1, double date2, double rmatpn[3][3]);
void iauPom00(double xp, double yp, double sp, double rpom[3][3]);
void iauPr00(double date1, double date2, double *dpsipr, double *depspr);
void iauPrec76(double ep01, double ep02, double ep11, double ep12,
               double *zeta, double *z, double *theta);
double iauS00(double date1, double date2, double x, double y);
double iauS00a(double date1, double date2);
double iauS00b(double date1, double date2);
double iauS06(double date1, double date2, double x, double y);
double iauS06a(double date1, double date2);
double iauSp00(double date1, double date2);
void iauXy06(double date1, double date2, double *x, double *y);
void iauXys00a(double date1, double date2,
               double *x, double *y, double *s);
void iauXys00b(double date1, double date2,
               double *x, double *y, double *s);
void iauXys06a(double date1, double date2,
               double *x, double *y, double *s);

/* Astronomy/RotationAndTime */
double iauEe00(double date1, double date2, double epsa, double dpsi);
double iauEe00a(double date1, double date2);
double iauEe00b(double date1, double date2);
double iauEe06a(double date1, double date2);
double iauEect00(double date1, double date2);
double iauEqeq94(double date1, double date2);
double iauEra00(double dj1, double dj2);
double iauGmst00(double uta, double utb, double tta, double ttb);
double iauGmst06(double uta, double utb, double tta, double ttb);
double iauGmst82(double dj1, double dj2);
double iauGst00a(double uta, double utb, double tta, double ttb);
double iauGst00b(double uta, double utb);
double iauGst06(double uta, double utb, double tta, double ttb,
                double rnpb[3][3]);
double iauGst06a(double uta, double utb, double tta, double ttb);
double iauGst94(double uta, double utb);

/* Astronomy/SpaceMotion */
int iauPvstar(double pv[2][3], double *ra, double *dec,
              double *pmr, double *pmd, double *px, double *rv);
int iauStarpv(double ra, double dec,
              double pmr, double pmd, double px, double rv,
              double pv[2][3]);

/* Astronomy/StarCatalogs */
void iauFk52h(double r5, double d5,
              double dr5, double dd5, double px5, double rv5,
              double *rh, double *dh,
              double *drh, double *ddh, double *pxh, double *rvh);
void iauFk5hip(double r5h[3][3], double s5h[3]);
void iauFk5hz(double r5, double d5, double date1, double date2,
              double *rh, double *dh);
void iauH2fk5(double rh, double dh,
              double drh, double ddh, double pxh, double rvh,
              double *r5, double *d5,
              double *dr5, double *dd5, double *px5, double *rv5);
void iauHfk5z(double rh, double dh, double date1, double date2,
              double *r5, double *d5, double *dr5, double *dd5);
int iauStarpm(double ra1, double dec1,
              double pmr1, double pmd1, double px1, double rv1,
              double ep1a, double ep1b, double ep2a, double ep2b,
              double *ra2, double *dec2,
              double *pmr2, double *pmd2, double *px2, double *rv2);

/* Astronomy/Geodetic/Geocentric */
int iauEform(int n, double *a, double *f);
int iauGc2gd(int n, double xyz[3],
             double *elong, double *phi, double *height);
int iauGc2gde(double a, double f, double xyz[3],
              double *elong, double *phi, double *height);
int iauGd2gc(int n, double elong, double phi, double height,
             double xyz[3]);
int iauGd2gce(double a, double f,
              double elong, double phi, double height, double xyz[3]);

/* Astronomy/Timescales */
int iauD2dtf(const char *scale, int ndp, double d1, double d2,
             int *iy, int *im, int *id, int ihmsf[4]);
int iauDat(int iy, int im, int id, double fd, double *deltat);
double iauDtdb(double date1, double date2,
               double ut, double elong, double u, double v);
int iauDtf2d(const char *scale, int iy, int im, int id,
             int ihr, int imn, double sec, double *d1, double *d2);
int iauTaitt(double tai1, double tai2, double *tt1, double *tt2);
int iauTaiut1(double tai1, double tai2, double dta,
              double *ut11, double *ut12);
int iauTaiutc(double tai1, double tai2, double *utc1, double *utc2);
int iauTcbtdb(double tcb1, double tcb2, double *tdb1, double *tdb2);
int iauTcgtt(double tcg1, double tcg2, double *tt1, double *tt2);
int iauTdbtcb(double tdb1, double tdb2, double *tcb1, double *tcb2);
int iauTdbtt(double tdb1, double tdb2, double dtr,
             double *tt1, double *tt2);
int iauTttai(double tt1, double tt2, double *tai1, double *tai2);
int iauTttcg(double tt1, double tt2, double *tcg1, double *tcg2);
int iauTttdb(double tt1, double tt2, double dtr,
             double *tdb1, double *tdb2);
int iauTtut1(double tt1, double tt2, double dt,
             double *ut11, double *ut12);
int iauUt1tai(double ut11, double ut12, double dta,
              double *tai1, double *tai2);
int iauUt1tt(double ut11, double ut12, double dt,
             double *tt1, double *tt2);
int iauUt1utc(double ut11, double ut12, double dut1,
              double *utc1, double *utc2);
int iauUtctai(double utc1, double utc2, double *tai1, double *tai2);
int iauUtcut1(double utc1, double utc2, double dut1,
              double *ut11, double *ut12);

/* VectorMatrix/AngleOps */
void iauA2af(int ndp, double angle, char *sign, int idmsf[4]);
void iauA2tf(int ndp, double angle, char *sign, int ihmsf[4]);
int iauAf2a(char s, int ideg, int iamin, double asec, double *rad);
double iauAnp(double a);
double iauAnpm(double a);
void iauD2tf(int ndp, double days, char *sign, int ihmsf[4]);
int iauTf2a(char s, int ihour, int imin, double sec, double *rad);
int iauTf2d(char s, int ihour, int imin, double sec, double *days);

/* VectorMatrix/BuildRotations */
void iauRx(double phi, double r[3][3]);
void iauRy(double theta, double r[3][3]);
void iauRz(double psi, double r[3][3]);

/* VectorMatrix/CopyExtendExtract */
void iauCp(double p[3], double c[3]);
void iauCpv(double pv[2][3], double c[2][3]);
void iauCr(double r[3][3], double c[3][3]);
void iauP2pv(double p[3], double pv[2][3]);
void iauPv2p(double pv[2][3], double p[3]);

/* VectorMatrix/Initialization */
void iauIr(double r[3][3]);
void iauZp(double p[3]);
void iauZpv(double pv[2][3]);
void iauZr(double r[3][3]);

/* VectorMatrix/MatrixOps */
void iauRxr(double a[3][3], double b[3][3], double atb[3][3]);
void iauTr(double r[3][3], double rt[3][3]);

/* VectorMatrix/MatrixVectorProducts */
void iauRxp(double r[3][3], double p[3], double rp[3]);
void iauRxpv(double r[3][3], double pv[2][3], double rpv[2][3]);
void iauTrxp(double r[3][3], double p[3], double trp[3]);
void iauTrxpv(double r[3][3], double pv[2][3], double trpv[2][3]);

/* VectorMatrix/RotationVectors */
void iauRm2v(double r[3][3], double w[3]);
void iauRv2m(double w[3], double r[3][3]);

/* VectorMatrix/SeparationAndAngle */
double iauPap(double a[3], double b[3]);
double iauPas(double al, double ap, double bl, double bp);
double iauSepp(double a[3], double b[3]);
double iauSeps(double al, double ap, double bl, double bp);

/* VectorMatrix/SphericalCartesian */
void iauC2s(double p[3], double *theta, double *phi);
void iauP2s(double p[3], double *theta, double *phi, double *r);
void iauPv2s(double pv[2][3],
             double *theta, double *phi, double *r,
             double *td, double *pd, double *rd);
void iauS2c(double theta, double phi, double c[3]);
void iauS2p(double theta, double phi, double r, double p[3]);
void iauS2pv(double theta, double phi, double r,
             double td, double pd, double rd,
             double pv[2][3]);

/* VectorMatrix/VectorOps */
double iauPdp(double a[3], double b[3]);
double iauPm(double p[3]);
void iauPmp(double a[3], double b[3], double amb[3]);
void iauPn(double p[3], double *r, double u[3]);
void iauPpp(double a[3], double b[3], double apb[3]);
void iauPpsp(double a[3], double s, double b[3], double apsb[3]);
void iauPvdpv(double a[2][3], double b[2][3], double adb[2]);
void iauPvm(double pv[2][3], double *r, double *s);
void iauPvmpv(double a[2][3], double b[2][3], double amb[2][3]);
void iauPvppv(double a[2][3], double b[2][3], double apb[2][3]);
void iauPvu(double dt, double pv[2][3], double upv[2][3]);
void iauPvup(double dt, double pv[2][3], double p[3]);
void iauPvxpv(double a[2][3], double b[2][3], double axb[2][3]);
void iauPxp(double a[3], double b[3], double axb[3]);
void iauS2xpv(double s1, double s2, double pv[2][3], double spv[2][3]);
void iauSxp(double s, double p[3], double sp[3]);
void iauSxpv(double s, double pv[2][3], double spv[2][3]);

#ifdef __cplusplus
}
#endif

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
