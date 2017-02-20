#include "sofa.h"
#include "sofam.h"
#include "ruby.h"

#ifndef DBL2NUM
# define DBL2NUM(dbl) rb_float_new(dbl)
#endif

VALUE mCeles;
ID id_status;

static VALUE
celes_s_status(VALUE self){
	return rb_ivar_get(self, id_status);
}

static void
cvec_cp(VALUE vvector, double vector[3]){
	int i;

	Check_Type(vvector, T_ARRAY);
	if(RARRAY_LEN(vvector) != 3)
		rb_raise(rb_eArgError, "vector size is not 3");

	for(i = 0; i < 3; i++)
		vector[i] = NUM2DBL(RARRAY_PTR(vvector)[i]);
}

static void
cmat_cp23(VALUE vmatrix, double matrix[2][3]){
	int i, j;

	Check_Type(vmatrix, T_ARRAY);
	if(RARRAY_LEN(vmatrix) != 2)
		rb_raise(rb_eArgError, "matrix size is not 2x3");

	for(i = 0; i < 2; i++){
		Check_Type(RARRAY_PTR(vmatrix)[i], T_ARRAY);
		if(RARRAY_LEN(RARRAY_PTR(vmatrix)[i]) != 3)
			rb_raise(rb_eArgError, "matrix size is not 2x3");
		
		for(j = 0; j < 3; j++)
			matrix[i][j] = NUM2DBL(RARRAY_PTR(RARRAY_PTR(vmatrix)[i])[j]);
	}
}

static void
cmat_cp33(VALUE vmatrix, double matrix[3][3]){
	int i, j;

	Check_Type(vmatrix, T_ARRAY);
	if(RARRAY_LEN(vmatrix) != 3)
		rb_raise(rb_eArgError, "matrix size is not 3x3");

	for(i = 0; i < 3; i++){
		Check_Type(RARRAY_PTR(vmatrix)[i], T_ARRAY);
		if(RARRAY_LEN(RARRAY_PTR(vmatrix)[i]) != 3)
			rb_raise(rb_eArgError, "matrix size is not 3x3");
		
		for(j = 0; j < 3; j++)
			matrix[i][j] = NUM2DBL(RARRAY_PTR(RARRAY_PTR(vmatrix)[i])[j]);
	}
}

static VALUE
vvec_cp(double vector[3], VALUE vvector){
	int i;

	Check_Type(vvector, T_ARRAY);
	if(RARRAY_LEN(vvector) != 3)
		rb_raise(rb_eArgError, "vector size is not 3");

	for(i = 0; i < 3; i++)
		RARRAY_PTR(vvector)[i] = DBL2NUM(vector[i]);

	return vvector;
}

static VALUE
vmat_cp23(double matrix[2][3], VALUE vmatrix){
	int i, j;

	Check_Type(vmatrix, T_ARRAY);
	if(RARRAY_LEN(vmatrix) != 2)
		rb_raise(rb_eArgError, "matrix size is not 2x3");

	for(i = 0; i < 2; i++){
		Check_Type(RARRAY_PTR(vmatrix)[i], T_ARRAY);
		if(RARRAY_LEN(RARRAY_PTR(vmatrix)[i]) != 3)
			rb_raise(rb_eArgError, "matrix size is not 2x3");
		
		for(j = 0; j < 3; j++)
			RARRAY_PTR(RARRAY_PTR(vmatrix)[i])[j] = DBL2NUM(matrix[i][j]);
	}

	return vmatrix;
}

static VALUE
vmat_cp33(double matrix[3][3], VALUE vmatrix){
	int i, j;

	Check_Type(vmatrix, T_ARRAY);
	if(RARRAY_LEN(vmatrix) != 3)
		rb_raise(rb_eArgError, "matrix size is not 3x3");

	for(i = 0; i < 3; i++){
		Check_Type(RARRAY_PTR(vmatrix)[i], T_ARRAY);
		if(RARRAY_LEN(RARRAY_PTR(vmatrix)[i]) != 3)
			rb_raise(rb_eArgError, "matrix size is not 3x3");
		
		for(j = 0; j < 3; j++)
			RARRAY_PTR(RARRAY_PTR(vmatrix)[i])[j] = DBL2NUM(matrix[i][j]);
	}

	return vmatrix;
}

static VALUE
vvec_new(double vector[3]){
	return rb_ary_new3(3,
			DBL2NUM(vector[0]),
			DBL2NUM(vector[1]),
			DBL2NUM(vector[2]));
}

static VALUE
vmat_new23(double matrix[2][3]){
	return rb_ary_new3(2,
			rb_ary_new3(3,
					DBL2NUM(matrix[0][0]),
					DBL2NUM(matrix[0][1]),
					DBL2NUM(matrix[0][2])),
			rb_ary_new3(3,
					DBL2NUM(matrix[1][0]),
					DBL2NUM(matrix[1][1]),
					DBL2NUM(matrix[1][2])));
}

static VALUE
vmat_new33(double matrix[3][3]){
	return rb_ary_new3(3,
			rb_ary_new3(3,
					DBL2NUM(matrix[0][0]),
					DBL2NUM(matrix[0][1]),
					DBL2NUM(matrix[0][2])),
			rb_ary_new3(3,
					DBL2NUM(matrix[1][0]),
					DBL2NUM(matrix[1][1]),
					DBL2NUM(matrix[1][2])),
			rb_ary_new3(3,
					DBL2NUM(matrix[2][0]),
					DBL2NUM(matrix[2][1]),
					DBL2NUM(matrix[2][2])));
}



static VALUE
celes_s_zp_b(VALUE self, VALUE vp){
	double p[3];

	cvec_cp(vp, p);
	iauZp(p);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_cp(p, vp);
}

static VALUE
celes_s_zp(VALUE self){
	double p[3];

	iauZp(p);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(p);
}

static VALUE
celes_s_zr_b(VALUE self, VALUE vr){
	double r[3][3];

	cmat_cp33(vr, r);
	iauZr(r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_cp33(r, vr);
}

static VALUE
celes_s_zr(VALUE self){
	double r[3][3];

	iauZr(r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(r);
}

static VALUE
celes_s_ir_b(VALUE self, VALUE vr){
	double r[3][3];

	cmat_cp33(vr, r);
	iauIr(r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_cp33(r, vr);
}

static VALUE
celes_s_ir(VALUE self){
	double r[3][3];

	iauIr(r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(r);
}

static VALUE
celes_s_cp(VALUE self, VALUE vp){
	double p[3], c[3];

	cvec_cp(vp, p);
	iauCp(p, c);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(c);
}

static VALUE
celes_s_cr(VALUE self, VALUE vr){
	double r[3][3], c[3][3];

	cmat_cp33(vr, r);
	iauCr(r, c);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(c);
}

static VALUE
celes_s_rx_b(VALUE self, VALUE vphi, VALUE vr){
	double r[3][3];
	
	cmat_cp33(vr, r);
	iauRx(NUM2DBL(vphi), r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_cp33(r, vr);
}

static VALUE
celes_s_rx(VALUE self, VALUE vphi, VALUE vr){
	double r[3][3];
	
	cmat_cp33(vr, r);
	iauRx(NUM2DBL(vphi), r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(r);
}

static VALUE
celes_s_ry_b(VALUE self, VALUE vphi, VALUE vr){
	double r[3][3];

	cmat_cp33(vr, r);
	iauRy(NUM2DBL(vphi), r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_cp33(r, vr);
}

static VALUE
celes_s_ry(VALUE self, VALUE vphi, VALUE vr){
	double r[3][3];
	
	cmat_cp33(vr, r);
	iauRy(NUM2DBL(vphi), r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(r);
}

static VALUE
celes_s_rz_b(VALUE self, VALUE vphi, VALUE vr){
	double r[3][3];

	cmat_cp33(vr, r);
	iauRz(NUM2DBL(vphi), r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_cp33(r, vr);
}

static VALUE
celes_s_rz(VALUE self, VALUE vphi, VALUE vr){
	double r[3][3];
	
	cmat_cp33(vr, r);
	iauRz(NUM2DBL(vphi), r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(r);
}

static VALUE
celes_s_s2c(VALUE self, VALUE vtheta, VALUE vphi){
	double c[3];

	iauS2c(NUM2DBL(vtheta), NUM2DBL(vphi), c);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(c);
}

static VALUE
celes_s_c2s(VALUE self, VALUE vp){
	double p[3], theta, phi;

	cvec_cp(vp, p);
	iauC2s(p, &theta, &phi);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(theta), DBL2NUM(phi));
}

static VALUE
celes_s_s2p(VALUE self, VALUE vtheta, VALUE vphi, VALUE vr){
	double p[3];

	iauS2p(NUM2DBL(vtheta), NUM2DBL(vphi), NUM2DBL(vr), p);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(p);
}

static VALUE
celes_s_p2s(VALUE self, VALUE vp){
	double p[3], theta, phi, r;

	cvec_cp(vp, p);
	iauP2s(p, &theta, &phi, &r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(3, DBL2NUM(theta), DBL2NUM(phi), DBL2NUM(r));
}

static VALUE
celes_s_ppp(VALUE self, VALUE va, VALUE vb){
	double a[3], b[3], apb[3];

	cvec_cp(va, a);
	cvec_cp(vb, b);
	iauPpp(a, b, apb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(apb);
}

static VALUE
celes_s_pmp(VALUE self, VALUE va, VALUE vb){
	double a[3], b[3], amb[3];

	cvec_cp(va, a);
	cvec_cp(vb, b);
	iauPmp(a, b, amb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(amb);
}

static VALUE
celes_s_ppsp(VALUE self, VALUE va, VALUE vs, VALUE vb){
	double a[3], b[3], apsb[3];

	cvec_cp(va, a);
	cvec_cp(vb, b);
	iauPpsp(a, NUM2DBL(vs), b, apsb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(apsb);
}

static VALUE
celes_s_pdp(VALUE self, VALUE va, VALUE vb){
	double a[3], b[3];

	cvec_cp(va, a);
	cvec_cp(vb, b);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauPdp(a, b));
}

static VALUE
celes_s_pxp(VALUE self, VALUE va, VALUE vb){
	double a[3], b[3], axb[3];

	cvec_cp(va, a);
	cvec_cp(vb, b);
	iauPxp(a, b, axb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(axb);
}

static VALUE
celes_s_pm(VALUE self, VALUE vp){
	double p[3];

	cvec_cp(vp, p);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauPm(p));
}

static VALUE
celes_s_pn(VALUE self, VALUE vp){
	double p[3], r, u[3];

	cvec_cp(vp, p);
	iauPn(p, &r, u);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(r), vvec_new(u));
}

static VALUE
celes_s_sxp(VALUE self, VALUE vs, VALUE vp){
	double p[3], sp[3];

	cvec_cp(vp, p);
	iauSxp(NUM2DBL(vs), p, sp);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(sp);
}


static VALUE
celes_s_rxr(VALUE self, VALUE va, VALUE vb){
	double a[3][3], b[3][3], atb[3][3];

	cmat_cp33(va, a);
	cmat_cp33(vb, b);
	iauRxr(a, b, atb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(atb);
}

static VALUE
celes_s_tr(VALUE self, VALUE vr){
	double r[3][3], rt[3][3];

	cmat_cp33(vr, r);
	iauTr(r, rt);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rt);
}

static VALUE
celes_s_rxp(VALUE self, VALUE vr, VALUE vp){
	double r[3][3], p[3], rp[3];

	cmat_cp33(vr, r);
	cvec_cp(vp, p);
	iauRxp(r, p, rp);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(rp);
}

static VALUE
celes_s_trxp(VALUE self, VALUE vr, VALUE vp){
	double r[3][3], p[3], trp[3];

	cmat_cp33(vr, r);
	cvec_cp(vp, p);
	iauTrxp(r, p, trp);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(trp);
}

static VALUE
celes_s_sepp(VALUE self, VALUE va, VALUE vb){
	double a[3], b[3];

	cvec_cp(va, a);
	cvec_cp(vb, b);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauSepp(a, b));
}

static VALUE
celes_s_seps(VALUE self, VALUE val, VALUE vap, VALUE vbl, VALUE vbp){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauSeps(NUM2DBL(val), NUM2DBL(vap),
			NUM2DBL(vbl), NUM2DBL(vbp)));
}

static VALUE
celes_s_pap(VALUE self, VALUE va, VALUE vb){
	double a[3], b[3];

	cvec_cp(va, a);
	cvec_cp(vb, b);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauPap(a, b));
}

static VALUE
celes_s_pas(VALUE self, VALUE val, VALUE vap, VALUE vbl, VALUE vbp){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauPas(NUM2DBL(val), NUM2DBL(vap),
			NUM2DBL(vbl), NUM2DBL(vbp)));
}

static VALUE
celes_s_rv2m(VALUE self, VALUE vw){
	double w[3], r[3][3];

	cvec_cp(vw, w);
	iauRv2m(w, r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(r);
}

static VALUE
celes_s_rm2v(VALUE self, VALUE vr){
	double r[3][3], w[3];

	cmat_cp33(vr, r);
	iauRm2v(r, w);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(w);
}

static VALUE
celes_s_zpv_b(VALUE self, VALUE vpv){
	double pv[2][3];

	cmat_cp23(vpv, pv);
	iauZpv(pv);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_cp23(pv, vpv);
}

static VALUE
celes_s_zpv(VALUE self){
	double pv[2][3];

	iauZpv(pv);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(pv);
}

static VALUE
celes_s_cpv(VALUE self, VALUE vpv){
	double pv[2][3], c[2][3];

	cmat_cp23(vpv, pv);
	iauCpv(pv, c);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(c);
}

static VALUE
celes_s_p2pv(VALUE self, VALUE vp){
	double p[3], pv[2][3];

	cvec_cp(vp, p);
	iauP2pv(p, pv);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(pv);
}

static VALUE
celes_s_pv2p(VALUE self, VALUE vpv){
	double pv[2][3], p[3];

	cmat_cp23(vpv, pv);
	iauPv2p(pv, p);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(p);
}

static VALUE
celes_s_s2pv(VALUE self, VALUE vtheta, VALUE vphi, VALUE vr,
		VALUE vtd, VALUE vpd, VALUE vrd){
	double pv[2][3];

	iauS2pv(NUM2DBL(vtheta), NUM2DBL(vphi), NUM2DBL(vr),
			NUM2DBL(vtd), NUM2DBL(vpd), NUM2DBL(vrd), pv);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(pv);
}

static VALUE
celes_s_pv2s(VALUE self, VALUE vpv){
	double pv[2][3], theta, phi, r, td, pd, rd;

	cmat_cp23(vpv, pv);
	iauPv2s(pv, &theta, &phi, &r, &td, &pd, &rd);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(6, DBL2NUM(theta), DBL2NUM(phi),
			DBL2NUM(r), DBL2NUM(td), DBL2NUM(pd), DBL2NUM(rd));
}

static VALUE
celes_s_pvppv(VALUE self, VALUE va, VALUE vb){
	double a[2][3], b[2][3], apb[2][3];

	cmat_cp23(va, a);
	cmat_cp23(vb, b);
	iauPvppv(a, b, apb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(apb);
}

static VALUE
celes_s_pvmpv(VALUE self, VALUE va, VALUE vb){
	double a[2][3], b[2][3], amb[2][3];

	cmat_cp23(va, a);
	cmat_cp23(vb, b);
	iauPvmpv(a, b, amb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(amb);
}

static VALUE
celes_s_pvdpv(VALUE self, VALUE va, VALUE vb){
	double a[2][3], b[2][3], adb[2];

	cmat_cp23(va, a);
	cmat_cp23(vb, b);
	iauPvdpv(a, b, adb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(adb[0]), DBL2NUM(adb[1]));
}

static VALUE
celes_s_pvxpv(VALUE self, VALUE va, VALUE vb){
	double a[2][3], b[2][3], axb[2][3];

	cmat_cp23(va, a);
	cmat_cp23(vb, b);
	iauPvxpv(a, b, axb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(axb);
}

static VALUE
celes_s_pvm(VALUE self, VALUE vpv){
	double pv[2][3], r, s;

	cmat_cp23(vpv, pv);
	iauPvm(pv, &r, &s);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(r), DBL2NUM(s));
}

static VALUE
celes_s_sxpv(VALUE self, VALUE vs, VALUE vpv){
	double pv[2][3], spv[2][3];

	cmat_cp23(vpv, pv);
	iauSxpv(NUM2DBL(vs), pv, spv);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(spv);
}

static VALUE
celes_s_s2xpv(VALUE self, VALUE vs1, VALUE vs2, VALUE vpv){
	double pv[2][3], spv[2][3];

	cmat_cp23(vpv, pv);
	iauS2xpv(NUM2DBL(vs1), NUM2DBL(vs2), pv, spv);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(spv);
}

static VALUE
celes_s_pvu(VALUE self, VALUE vdt, VALUE vpv){
	double pv[2][3], upv[2][3];

	cmat_cp23(vpv, pv);
	iauPvu(NUM2DBL(vdt), pv, upv);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(upv);
}

static VALUE
celes_s_pvup(VALUE self, VALUE vdt, VALUE vpv){
	double pv[2][3], p[3];

	cmat_cp23(vpv, pv);
	iauPvup(NUM2DBL(vdt), pv, p);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vvec_new(p);
}

static VALUE
celes_s_rxpv(VALUE self, VALUE vr, VALUE vpv){
	double r[3][3], pv[2][3], rpv[2][3];

	cmat_cp33(vr, r);
	cmat_cp23(vpv, pv);
	iauRxpv(r, pv, rpv);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(rpv);
}

static VALUE
celes_s_trxpv(VALUE self, VALUE vr, VALUE vpv){
	double r[3][3], pv[2][3], trpv[2][3];

	cmat_cp33(vr, r);
	cmat_cp23(vpv, pv);
	iauTrxpv(r, pv, trpv);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new23(trpv);
}

static VALUE
celes_s_anp(VALUE self, VALUE va){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauAnp(NUM2DBL(va)));
}

static VALUE
celes_s_anpm(VALUE self, VALUE va){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauAnpm(NUM2DBL(va)));
}

static VALUE
celes_s_a2tf(VALUE self, VALUE vndp, VALUE vangle){
	char sign;
	int ihmsf[4];

	iauA2tf(NUM2INT(vndp), NUM2DBL(vangle), &sign, ihmsf);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, rb_str_new(&sign, 1),
			rb_ary_new3(4, INT2NUM(ihmsf[0]), INT2NUM(ihmsf[1]),
				INT2NUM(ihmsf[2]), INT2NUM(ihmsf[3])));
}

static VALUE
celes_s_a2af(VALUE self, VALUE vndp, VALUE vangle){
	char sign;
	int idmsf[4];

	iauA2af(NUM2INT(vndp), NUM2DBL(vangle), &sign, idmsf);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, rb_str_new(&sign, 1),
			rb_ary_new3(4, INT2NUM(idmsf[0]), INT2NUM(idmsf[1]),
				INT2NUM(idmsf[2]), INT2NUM(idmsf[3])));
}

static VALUE
celes_s_af2a(VALUE self, VALUE vs, VALUE vdeg, VALUE vamin, VALUE vasec){
	int ret;
	double rad;

	Check_Type(vs, T_STRING);

	ret = iauAf2a(RSTRING_PTR(vs)[0], NUM2DBL(vdeg),
			NUM2DBL(vamin), NUM2DBL(vasec), &rad);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	return DBL2NUM(rad);
}

static VALUE
celes_s_d2tf(VALUE self, VALUE vndp, VALUE vdays){
	char sign;
	int ihmsf[4];

	iauD2tf(NUM2INT(vndp), NUM2DBL(vdays), &sign, ihmsf);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, rb_str_new(&sign, 1),
			rb_ary_new3(4, INT2NUM(ihmsf[0]), INT2NUM(ihmsf[1]),
				INT2NUM(ihmsf[2]), INT2NUM(ihmsf[3])));
}

static VALUE
celes_s_tf2a(VALUE self, VALUE vs, VALUE vhour, VALUE vmin, VALUE vsec){
	int ret;
	double rad;

	Check_Type(vs, T_STRING);

	ret = iauTf2a(RSTRING_PTR(vs)[0], NUM2DBL(vhour),
			NUM2DBL(vmin), NUM2DBL(vsec), &rad);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	return DBL2NUM(rad);
}

static VALUE
celes_s_tf2d(VALUE self, VALUE vs, VALUE vhour, VALUE vmin, VALUE vsec){
	int ret;
	double days;

	Check_Type(vs, T_STRING);

	ret = iauTf2d(RSTRING_PTR(vs)[0], NUM2DBL(vhour),
			NUM2DBL(vmin), NUM2DBL(vsec), &days);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	return DBL2NUM(days);
}

static VALUE
celes_s_cal2jd(VALUE self, VALUE vy, VALUE vm, VALUE vd){
	int ret;
	double djm0, djm;

	ret = iauCal2jd(NUM2INT(vy), NUM2INT(vm), NUM2INT(vd), &djm0, &djm);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "bad year");
	else if(ret == -2)
		rb_raise(rb_eArgError, "bad month");

	return rb_ary_new3(2, DBL2NUM(djm0), DBL2NUM(djm));
}

static VALUE
celes_s_epb(VALUE self, VALUE vdj1, VALUE vdj2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEpb(NUM2DBL(vdj1), NUM2DBL(vdj2)));
}

static VALUE
celes_s_epb2jd(VALUE self, VALUE vepb){
	double djm0, djm;

	iauEpb2jd(NUM2DBL(vepb), &djm0, &djm);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(djm0), DBL2NUM(djm));
}

static VALUE
celes_s_epj(VALUE self, VALUE vdj1, VALUE vdj2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEpj(NUM2DBL(vdj1), NUM2DBL(vdj2)));
}

static VALUE
celes_s_epj2jd(VALUE self, VALUE vepj){
	double djm0, djm;

	iauEpj2jd(NUM2DBL(vepj), &djm0, &djm);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(djm0), DBL2NUM(djm));
}


static VALUE
celes_s_jd2cal(VALUE self, VALUE vdj1, VALUE vdj2){
	int ret, iy, im, id;
	double fd;

	ret = iauJd2cal(NUM2DBL(vdj1), NUM2DBL(vdj2), &iy, &im, &id, &fd);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "unacceptable date");

	return rb_ary_new3(4, INT2FIX(iy), INT2FIX(im),
			INT2FIX(id), DBL2NUM(fd));
}

static VALUE
celes_s_jdcalf(VALUE self, VALUE vndp, VALUE vdj1, VALUE vdj2){
	int ret, iymdf[4];

	ret = iauJdcalf(NUM2INT(vndp), NUM2DBL(vdj1), NUM2DBL(vdj2), iymdf);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "date out of range");

	return rb_ary_new3(4, INT2FIX(iymdf[0]), INT2FIX(iymdf[1]),
			INT2FIX(iymdf[2]), INT2NUM(iymdf[3]));
}

static VALUE
celes_s_d2dtf(VALUE self, VALUE vscale, VALUE vndp, VALUE vd1, VALUE vd2){
	int ret;
	int iy, im, id, ihmsf[4];

	if(NIL_P(vscale)) vscale = rb_str_new2("");
	ret = iauD2dtf(RSTRING_PTR(vscale), NUM2INT(vndp),
			NUM2DBL(vd1), NUM2DBL(vd2), &iy, &im, &id, ihmsf);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "unacceptable date");

	return rb_ary_new3(4, INT2FIX(iy), INT2FIX(im), INT2FIX(id),
			rb_ary_new3(4, INT2FIX(ihmsf[0]), INT2FIX(ihmsf[1]),
			INT2FIX(ihmsf[2]), INT2NUM(ihmsf[3])));
}

static VALUE
celes_s_dat(VALUE self, VALUE vy, VALUE vm, VALUE vd, VALUE vfd){
	int ret;
	double deltat;

	ret = iauDat(NUM2INT(vy), NUM2INT(vm),
			NUM2INT(vd), NUM2DBL(vfd), &deltat);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "bad year");
	else if(ret == -2)
		rb_raise(rb_eArgError, "bad month");
	else if(ret == -3)
		rb_raise(rb_eArgError, "bad day");
	else if(ret == -4)
		rb_raise(rb_eArgError, "bad fraction");

	return DBL2NUM(deltat);
}

static VALUE
celes_s_dtdb(VALUE self, VALUE vdate1, VALUE vdate2,
		VALUE vut, VALUE velong, VALUE vu, VALUE vv){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauDtdb(NUM2DBL(vdate1), NUM2DBL(vdate2),
			NUM2DBL(vut), NUM2DBL(velong), NUM2DBL(vu), NUM2DBL(vv)));
}

static VALUE
celes_s_dtf2d(VALUE self, VALUE vscale, VALUE vy, VALUE vm, VALUE vd,
		VALUE vhr, VALUE vmn, VALUE vsec){
	int ret;
	double d1, d2;

	if(NIL_P(vscale)) vscale = rb_str_new2("");
	ret = iauDtf2d(RSTRING_PTR(vscale), NUM2INT(vy), NUM2INT(vm),
			NUM2INT(vd), NUM2INT(vhr), NUM2INT(vmn), NUM2DBL(vsec),
			&d1, &d2);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "bad year");
	else if(ret == -2)
		rb_raise(rb_eArgError, "bad month");
	else if(ret == -3)
		rb_raise(rb_eArgError, "bad day");

	return rb_ary_new3(2, DBL2NUM(d1), DBL2NUM(d2));
}

static VALUE
celes_s_taitt(VALUE self, VALUE vtai1, VALUE vtai2){
	double tt1, tt2;

	iauTaitt(NUM2DBL(vtai1), NUM2DBL(vtai2), &tt1, &tt2);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(tt1), DBL2NUM(tt2));
}

static VALUE
celes_s_taiut1(VALUE self, VALUE vtai1, VALUE vtai2, VALUE vdta){
	double ut11, ut12;

	iauTaiut1(NUM2DBL(vtai1), NUM2DBL(vtai2), NUM2DBL(vdta), &ut11, &ut12);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(ut11), DBL2NUM(ut12));
}

static VALUE
celes_s_taiutc(VALUE self, VALUE vtai1, VALUE vtai2){
	int ret;
	double utc1, utc2;

	ret = iauTaiutc(NUM2DBL(vtai1), NUM2DBL(vtai2), &utc1, &utc2);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "unacceptable date");

	return rb_ary_new3(2, DBL2NUM(utc1), DBL2NUM(utc2));
}

static VALUE
celes_s_tcbtdb(VALUE self, VALUE vtcb1, VALUE vtcb2){
	double tdb1, tdb2;

	iauTcbtdb(NUM2DBL(vtcb1), NUM2DBL(vtcb2), &tdb1, &tdb2);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(tdb1), DBL2NUM(tdb2));
}

static VALUE
celes_s_tcgtt(VALUE self, VALUE vtcg1, VALUE vtcg2){
	double tt1, tt2;

	iauTcgtt(NUM2DBL(vtcg1), NUM2DBL(vtcg2), &tt1, &tt2);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(tt1), DBL2NUM(tt2));
}

static VALUE
celes_s_tdbtcb(VALUE self, VALUE vtdb1, VALUE vtdb2){
	double tcb1, tcb2;

	iauTdbtcb(NUM2DBL(vtdb1), NUM2DBL(vtdb2), &tcb1, &tcb2);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(tcb1), DBL2NUM(tcb2));
}

static VALUE
celes_s_tdbtt(VALUE self, VALUE vtdb1, VALUE vtdb2, VALUE vdtr){
	double tt1, tt2;

	iauTdbtt(NUM2DBL(vtdb1), NUM2DBL(vtdb2), NUM2DBL(vdtr), &tt1, &tt2);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(tt1), DBL2NUM(tt2));
}

static VALUE
celes_s_tttai(VALUE self, VALUE vtt1, VALUE vtt2){
	double tai1, tai2;

	iauTttai(NUM2DBL(vtt1), NUM2DBL(vtt2), &tai1, &tai2);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(tai1), DBL2NUM(tai2));
}

static VALUE
celes_s_tttcg(VALUE self, VALUE vtt1, VALUE vtt2){
	double tcg1, tcg2;

	iauTttcg(NUM2DBL(vtt1), NUM2DBL(vtt2), &tcg1, &tcg2);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(tcg1), DBL2NUM(tcg2));
}

static VALUE
celes_s_tttdb(VALUE self, VALUE vtt1, VALUE vtt2, VALUE vdtr){
	double tdb1, tdb2;

	iauTttdb(NUM2DBL(vtt1), NUM2DBL(vtt2), NUM2DBL(vdtr), &tdb1, &tdb2);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(tdb1), DBL2NUM(tdb2));
}

static VALUE
celes_s_ttut1(VALUE self, VALUE vtt1, VALUE vtt2, VALUE vdt){
	double ut11, ut12;

	iauTtut1(NUM2DBL(vtt1), NUM2DBL(vtt2), NUM2DBL(vdt), &ut11, &ut12);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(ut11), DBL2NUM(ut12));
}

static VALUE
celes_s_ut1tai(VALUE self, VALUE vut11, VALUE vut12, VALUE vdta){
	double tai1, tai2;

	iauUt1tai(NUM2DBL(vut11), NUM2DBL(vut12), NUM2DBL(vdta), &tai1, &tai2);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(tai1), DBL2NUM(tai2));
}

static VALUE
celes_s_ut1tt(VALUE self, VALUE vut11, VALUE vut12, VALUE vdt){
	double tt1, tt2;

	iauUt1tt(NUM2DBL(vut11), NUM2DBL(vut12), NUM2DBL(vdt), &tt1, &tt2);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(tt1), DBL2NUM(tt2));
}

static VALUE
celes_s_ut1utc(VALUE self, VALUE vut11, VALUE vut12, VALUE vdut1){
	int ret;
	double utc1, utc2;

	ret = iauUt1utc(NUM2DBL(vut11), NUM2DBL(vut12),
			NUM2DBL(vdut1), &utc1, &utc2);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "unacceptable date");

	return rb_ary_new3(2, DBL2NUM(utc1), DBL2NUM(utc2));
}

static VALUE
celes_s_utctai(VALUE self, VALUE vutc1, VALUE vutc2){
	int ret;
	double tai1, tai2;

	ret = iauUtctai(NUM2DBL(vutc1), NUM2DBL(vutc2), &tai1, &tai2);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "unacceptable date");

	return rb_ary_new3(2, DBL2NUM(tai1), DBL2NUM(tai2));
}

static VALUE
celes_s_utcut1(VALUE self, VALUE vutc1, VALUE vutc2, VALUE vdut1){
	int ret;
	double ut11, ut12;

	ret = iauUtcut1(NUM2DBL(vutc1), NUM2DBL(vutc2),
			NUM2DBL(vdut1), &ut11, &ut12);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "unacceptable date");

	return rb_ary_new3(2, DBL2NUM(ut11), DBL2NUM(ut12));
}

static VALUE
celes_s_ee00(VALUE self, VALUE vdate1, VALUE vdate2,
		VALUE vepsa, VALUE vdpsi){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEe00(NUM2DBL(vdate1), NUM2DBL(vdate2),
			NUM2DBL(vepsa), NUM2DBL(vdpsi)));
}

static VALUE
celes_s_ee00a(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEe00a(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_ee00b(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEe00b(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_ee06a(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEe06a(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_eect00(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEect00(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_eqeq94(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEqeq94(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_era00(VALUE self, VALUE vdj1, VALUE vdj2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEra00(NUM2DBL(vdj1), NUM2DBL(vdj2)));
}

static VALUE
celes_s_gmst00(VALUE self, VALUE vuta, VALUE vutb, VALUE vtta, VALUE vttb){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauGmst00(NUM2DBL(vuta), NUM2DBL(vutb),
			NUM2DBL(vtta), NUM2DBL(vttb)));
}

static VALUE
celes_s_gmst06(VALUE self, VALUE vuta, VALUE vutb, VALUE vtta, VALUE vttb){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauGmst06(NUM2DBL(vuta), NUM2DBL(vutb),
			NUM2DBL(vtta), NUM2DBL(vttb)));
}

static VALUE
celes_s_gmst82(VALUE self, VALUE vdj1, VALUE vdj2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauGmst82(NUM2DBL(vdj1), NUM2DBL(vdj2)));
}

static VALUE
celes_s_gst00a(VALUE self, VALUE vuta, VALUE vutb, VALUE vtta, VALUE vttb){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauGst00a(NUM2DBL(vuta), NUM2DBL(vutb),
			NUM2DBL(vtta), NUM2DBL(vttb)));
}

static VALUE
celes_s_gst00b(VALUE self, VALUE vuta, VALUE vutb){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauGst00b(NUM2DBL(vuta), NUM2DBL(vutb)));
}

static VALUE
celes_s_gst06(VALUE self, VALUE vuta, VALUE vutb,
		VALUE vtta, VALUE vttb, VALUE vrnpb){
	double rnpb[3][3];

	rb_ivar_set(self, id_status, INT2FIX(0));

	cmat_cp33(vrnpb, rnpb);

	return DBL2NUM(iauGst06(NUM2DBL(vuta), NUM2DBL(vutb),
			NUM2DBL(vtta), NUM2DBL(vttb), rnpb));
}

static VALUE
celes_s_gst06a(VALUE self, VALUE vuta, VALUE vutb, VALUE vtta, VALUE vttb){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauGst06a(NUM2DBL(vuta), NUM2DBL(vutb),
			NUM2DBL(vtta), NUM2DBL(vttb)));
}

static VALUE
celes_s_gst94(VALUE self, VALUE vuta, VALUE vutb){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauGst94(NUM2DBL(vuta), NUM2DBL(vutb)));
}

static VALUE
celes_s_epv00(VALUE self, VALUE vdate1, VALUE vdate2){
	int ret;
	double pvh[2][3], pvb[2][3];

	ret = iauEpv00(NUM2DBL(vdate1), NUM2DBL(vdate2), pvh, pvb);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	return rb_ary_new3(2, vmat_new23(pvh), vmat_new23(pvb));
}

static VALUE
celes_s_plan94(VALUE self, VALUE vdate1, VALUE vdate2, VALUE vnp){
	int ret;
	double pv[2][3];

	ret = iauPlan94(NUM2DBL(vdate1), NUM2DBL(vdate2), NUM2INT(vnp), pv);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "illegal NP (outside 1-8)");

	return vmat_new23(pv);
}
static VALUE
celes_s_bi00(VALUE self){
	double dpsibi, depsbi, dra;

	iauBi00(&dpsibi, &depsbi, &dra);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(3, DBL2NUM(dpsibi), DBL2NUM(depsbi), DBL2NUM(dra));
}

static VALUE
celes_s_bp00(VALUE self, VALUE vdate1, VALUE vdate2){
	double rb[3][3], rp[3][3], rbp[3][3];

	iauBp00(NUM2DBL(vdate1), NUM2DBL(vdate2), rb, rp, rbp);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(3, vmat_new33(rb), vmat_new33(rp), vmat_new33(rbp));
}

static VALUE
celes_s_bp06(VALUE self, VALUE vdate1, VALUE vdate2){
	double rb[3][3], rp[3][3], rbp[3][3];

	iauBp06(NUM2DBL(vdate1), NUM2DBL(vdate2), rb, rp, rbp);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(3, vmat_new33(rb), vmat_new33(rp), vmat_new33(rbp));
}

static VALUE
celes_s_bpn2xy(VALUE self, VALUE vrbpn){
	double rbpn[3][3], x, y;

	cmat_cp33(vrbpn, rbpn);
	iauBpn2xy(rbpn, &x, &y);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(x), DBL2NUM(y));
}

static VALUE
celes_s_c2i00a(VALUE self, VALUE vdate1, VALUE vdate2){
	double rc2i[3][3];

	iauC2i00a(NUM2DBL(vdate1), NUM2DBL(vdate2), rc2i);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2i);
}

static VALUE
celes_s_c2i00b(VALUE self, VALUE vdate1, VALUE vdate2){
	double rc2i[3][3];

	iauC2i00b(NUM2DBL(vdate1), NUM2DBL(vdate2), rc2i);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2i);
}

static VALUE
celes_s_c2i06a(VALUE self, VALUE vdate1, VALUE vdate2){
	double rc2i[3][3];

	iauC2i06a(NUM2DBL(vdate1), NUM2DBL(vdate2), rc2i);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2i);
}

static VALUE
celes_s_c2ibpn(VALUE self, VALUE vdate1, VALUE vdate2, VALUE vrbpn){
	double rbpn[3][3], rc2i[3][3];

	cmat_cp33(vrbpn, rbpn);
	iauC2ibpn(NUM2DBL(vdate1), NUM2DBL(vdate2), rbpn, rc2i);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2i);
}

static VALUE
celes_s_c2ixy(VALUE self, VALUE vdate1, VALUE vdate2, VALUE vx, VALUE vy){
	double rc2i[3][3];

	iauC2ixy(NUM2DBL(vdate1), NUM2DBL(vdate2),
			NUM2DBL(vx), NUM2DBL(vy), rc2i);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2i);
}

static VALUE
celes_s_c2ixys(VALUE self, VALUE vx, VALUE vy, VALUE vs){
	double rc2i[3][3];

	iauC2ixys(NUM2DBL(vx), NUM2DBL(vy), NUM2DBL(vs), rc2i);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2i);
}

static VALUE
celes_s_c2t00a(VALUE self, VALUE vtta, VALUE vttb,
		VALUE vuta, VALUE vutb, VALUE vxp, VALUE vyp){
	double rc2t[3][3];

	iauC2t00a(NUM2DBL(vtta), NUM2DBL(vttb), NUM2DBL(vuta), NUM2DBL(vutb), 
			NUM2DBL(vxp), NUM2DBL(vyp), rc2t);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2t);
}

static VALUE
celes_s_c2t00b(VALUE self, VALUE vtta, VALUE vttb,
		VALUE vuta, VALUE vutb, VALUE vxp, VALUE vyp){
	double rc2t[3][3];

	iauC2t00b(NUM2DBL(vtta), NUM2DBL(vttb), NUM2DBL(vuta), NUM2DBL(vutb), 
			NUM2DBL(vxp), NUM2DBL(vyp), rc2t);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2t);
}

static VALUE
celes_s_c2t06a(VALUE self, VALUE vtta, VALUE vttb,
		VALUE vuta, VALUE vutb, VALUE vxp, VALUE vyp){
	double rc2t[3][3];

	iauC2t06a(NUM2DBL(vtta), NUM2DBL(vttb), NUM2DBL(vuta), NUM2DBL(vutb), 
			NUM2DBL(vxp), NUM2DBL(vyp), rc2t);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2t);
}

static VALUE
celes_s_c2tcio(VALUE self, VALUE vrc2i, VALUE vera, VALUE vrpom){
	double rc2i[3][3], rpom[3][3], rc2t[3][3];

	cmat_cp33(vrc2i, rc2i);
	cmat_cp33(vrpom, rpom);
	iauC2tcio(rc2i, NUM2DBL(vera), rpom, rc2t);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2t);
}

static VALUE
celes_s_c2teqx(VALUE self, VALUE vrbpn, VALUE vgst, VALUE vrpom){
	double rbpn[3][3], rpom[3][3], rc2t[3][3];

	cmat_cp33(vrbpn, rbpn);
	cmat_cp33(vrpom, rpom);
	iauC2teqx(rbpn, NUM2DBL(vgst), rpom, rc2t);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2t);
}

static VALUE
celes_s_c2tpe(VALUE self, VALUE vtta, VALUE vttb, VALUE vuta, VALUE vutb,
		VALUE vdpsi, VALUE vdeps, VALUE vxp, VALUE vyp){
	double rc2t[3][3];

	iauC2tpe(NUM2DBL(vtta), NUM2DBL(vttb), NUM2DBL(vuta), NUM2DBL(vutb),
			NUM2DBL(vdpsi), NUM2DBL(vdeps), NUM2DBL(vxp), NUM2DBL(vyp),
			rc2t);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2t);
}

static VALUE
celes_s_c2txy(VALUE self, VALUE vtta, VALUE vttb, VALUE vuta, VALUE vutb,
		VALUE vx, VALUE vy, VALUE vxp, VALUE vyp){
	double rc2t[3][3];

	iauC2txy(NUM2DBL(vtta), NUM2DBL(vttb), NUM2DBL(vuta), NUM2DBL(vutb),
			NUM2DBL(vx), NUM2DBL(vy), NUM2DBL(vxp), NUM2DBL(vyp), rc2t);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rc2t);
}

static VALUE
celes_s_eo06a(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEo06a(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_eors(VALUE self, VALUE vrnpb, VALUE vs){
	double rnpb[3][3];

	cmat_cp33(vrnpb, rnpb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauEors(rnpb, NUM2DBL(vs)));
}

static VALUE
celes_s_fw2m(VALUE self, VALUE vgamb, VALUE vphib, VALUE vpsi, VALUE veps){
	double r[3][3];

	iauFw2m(NUM2DBL(vgamb), NUM2DBL(vphib),
			NUM2DBL(vpsi), NUM2DBL(veps), r);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(r);
}

static VALUE
celes_s_fw2xy(VALUE self, VALUE vgamb,
		VALUE vphib, VALUE vpsi, VALUE veps){
	double x, y;

	iauFw2xy(NUM2DBL(vgamb), NUM2DBL(vphib),
			NUM2DBL(vpsi), NUM2DBL(veps), &x, &y);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(x), DBL2NUM(y));
}

static VALUE
celes_s_num00a(VALUE self, VALUE vdate1, VALUE vdate2){
	double rmatn[3][3];

	iauNum00a(NUM2DBL(vdate1), NUM2DBL(vdate2), rmatn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rmatn);
}

static VALUE
celes_s_num00b(VALUE self, VALUE vdate1, VALUE vdate2){
	double rmatn[3][3];

	iauNum00b(NUM2DBL(vdate1), NUM2DBL(vdate2), rmatn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rmatn);
}

static VALUE
celes_s_num06a(VALUE self, VALUE vdate1, VALUE vdate2){
	double rmatn[3][3];

	iauNum06a(NUM2DBL(vdate1), NUM2DBL(vdate2), rmatn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rmatn);
}

static VALUE
celes_s_numat(VALUE self, VALUE vepsa, VALUE vdpsi, VALUE vdeps){
	double rmatn[3][3];

	iauNumat(NUM2DBL(vepsa), NUM2DBL(vdpsi), NUM2DBL(vdeps), rmatn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rmatn);
}

static VALUE
celes_s_nut00a(VALUE self, VALUE vdate1, VALUE vdate2){
	double dpsi, deps;

	iauNut00a(NUM2DBL(vdate1), NUM2DBL(vdate2), &dpsi, &deps);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(dpsi), DBL2NUM(deps));
}

static VALUE
celes_s_nut00b(VALUE self, VALUE vdate1, VALUE vdate2){
	double dpsi, deps;

	iauNut00b(NUM2DBL(vdate1), NUM2DBL(vdate2), &dpsi, &deps);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(dpsi), DBL2NUM(deps));
}

static VALUE
celes_s_nut06a(VALUE self, VALUE vdate1, VALUE vdate2){
	double dpsi, deps;

	iauNut06a(NUM2DBL(vdate1), NUM2DBL(vdate2), &dpsi, &deps);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(dpsi), DBL2NUM(deps));
}

static VALUE
celes_s_nut80(VALUE self, VALUE vdate1, VALUE vdate2){
	double dpsi, deps;

	iauNut80(NUM2DBL(vdate1), NUM2DBL(vdate2), &dpsi, &deps);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(dpsi), DBL2NUM(deps));
}

static VALUE
celes_s_nutm80(VALUE self, VALUE vdate1, VALUE vdate2){
	double rmatn[3][3];

	iauNutm80(NUM2DBL(vdate1), NUM2DBL(vdate2), rmatn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rmatn);
}

static VALUE
celes_s_obl06(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauObl06(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_obl80(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauObl80(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_pb06(VALUE self, VALUE vdate1, VALUE vdate2){
	double bzeta, bz, btheta;

	iauPb06(NUM2DBL(vdate1), NUM2DBL(vdate2), &bzeta, &bz, &btheta);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(3, DBL2NUM(bzeta), DBL2NUM(bz), DBL2NUM(btheta));
}

static VALUE
celes_s_pfw06(VALUE self, VALUE vdate1, VALUE vdate2){
	double gamb, phib, psib, epsa;

	iauPfw06(NUM2DBL(vdate1), NUM2DBL(vdate2), &gamb, &phib, &psib, &epsa);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(4, DBL2NUM(gamb),
			DBL2NUM(phib), DBL2NUM(psib), DBL2NUM(epsa));
}

static VALUE
celes_s_pmat00(VALUE self, VALUE vdate1, VALUE vdate2){
	double rbp[3][3];

	iauPmat00(NUM2DBL(vdate1), NUM2DBL(vdate2), rbp);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rbp);
}

static VALUE
celes_s_pmat06(VALUE self, VALUE vdate1, VALUE vdate2){
	double rbp[3][3];

	iauPmat06(NUM2DBL(vdate1), NUM2DBL(vdate2), rbp);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rbp);
}

static VALUE
celes_s_pmat76(VALUE self, VALUE vdate1, VALUE vdate2){
	double rmatp[3][3];

	iauPmat76(NUM2DBL(vdate1), NUM2DBL(vdate2), rmatp);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rmatp);
}

static VALUE
celes_s_pn00(VALUE self, VALUE vdate1, VALUE vdate2,
		VALUE vdpsi, VALUE vdeps){
	double epsa, rb[3][3], rp[3][3], rbp[3][3], rn[3][3], rbpn[3][3];

	iauPn00(NUM2DBL(vdate1), NUM2DBL(vdate2),
			NUM2DBL(vdpsi), NUM2DBL(vdeps), &epsa,
			rb, rp, rbp, rn, rbpn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(6, DBL2NUM(epsa), vmat_new33(rb),
			vmat_new33(rp), vmat_new33(rbp), vmat_new33(rn), vmat_new33(rbpn));
}

static VALUE
celes_s_pn00a(VALUE self, VALUE vdate1, VALUE vdate2){
	double dpsi, deps, epsa, rb[3][3],
			rp[3][3], rbp[3][3], rn[3][3], rbpn[3][3];

	iauPn00a(NUM2DBL(vdate1), NUM2DBL(vdate2), &dpsi, &deps, &epsa,
			rb, rp, rbp, rn, rbpn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(8, DBL2NUM(dpsi), DBL2NUM(deps), DBL2NUM(epsa),
			vmat_new33(rb), vmat_new33(rp), vmat_new33(rbp),
			vmat_new33(rn), vmat_new33(rbpn));
}

static VALUE
celes_s_pn00b(VALUE self, VALUE vdate1, VALUE vdate2){
	double dpsi, deps, epsa, rb[3][3],
			rp[3][3], rbp[3][3], rn[3][3], rbpn[3][3];

	iauPn00b(NUM2DBL(vdate1), NUM2DBL(vdate2), &dpsi, &deps, &epsa,
			rb, rp, rbp, rn, rbpn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(8, DBL2NUM(dpsi), DBL2NUM(deps), DBL2NUM(epsa),
			vmat_new33(rb), vmat_new33(rp), vmat_new33(rbp),
			vmat_new33(rn), vmat_new33(rbpn));
}

static VALUE
celes_s_pn06(VALUE self, VALUE vdate1, VALUE vdate2,
		VALUE vdpsi, VALUE vdeps){
	double epsa, rb[3][3], rp[3][3], rbp[3][3], rn[3][3], rbpn[3][3];

	iauPn06(NUM2DBL(vdate1), NUM2DBL(vdate2),
			NUM2DBL(vdpsi), NUM2DBL(vdeps), &epsa,
			rb, rp, rbp, rn, rbpn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(6, DBL2NUM(epsa), vmat_new33(rb),
			vmat_new33(rp), vmat_new33(rbp), vmat_new33(rn), vmat_new33(rbpn));
}

static VALUE
celes_s_pn06a(VALUE self, VALUE vdate1, VALUE vdate2){
	double dpsi, deps, epsa, rb[3][3],
			rp[3][3], rbp[3][3], rn[3][3], rbpn[3][3];

	iauPn06a(NUM2DBL(vdate1), NUM2DBL(vdate2), &dpsi, &deps, &epsa,
			rb, rp, rbp, rn, rbpn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(8, DBL2NUM(dpsi), DBL2NUM(deps), DBL2NUM(epsa),
			vmat_new33(rb), vmat_new33(rp), vmat_new33(rbp),
			vmat_new33(rn), vmat_new33(rbpn));
}

static VALUE
celes_s_pnm00a(VALUE self, VALUE vdate1, VALUE vdate2){
	double rbpn[3][3];

	iauPnm00a(NUM2DBL(vdate1), NUM2DBL(vdate2), rbpn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rbpn);
}

static VALUE
celes_s_pnm00b(VALUE self, VALUE vdate1, VALUE vdate2){
	double rbpn[3][3];

	iauPnm00b(NUM2DBL(vdate1), NUM2DBL(vdate2), rbpn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rbpn);
}

static VALUE
celes_s_pnm06a(VALUE self, VALUE vdate1, VALUE vdate2){
	double rnpb[3][3];

	iauPnm06a(NUM2DBL(vdate1), NUM2DBL(vdate2), rnpb);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rnpb);
}

static VALUE
celes_s_pnm80(VALUE self, VALUE vdate1, VALUE vdate2){
	double rmatpn[3][3];

	iauPnm80(NUM2DBL(vdate1), NUM2DBL(vdate2), rmatpn);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rmatpn);
}

static VALUE
celes_s_p06e(VALUE self, VALUE vdate1, VALUE vdate2){
	double eps0, psia, oma, bpa, bqa, pia, bpia,
			epsa, chia, za, zetaa, thetaa, pa, gam, phi, psi;
	
	iauP06e(NUM2DBL(vdate1), NUM2DBL(vdate2), &eps0, &psia,
			&oma, &bpa, &bqa, &pia, &bpia, &epsa, &chia, &za,
			&zetaa, &thetaa, &pa, &gam, &phi, &psi);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(16, DBL2NUM(eps0), DBL2NUM(psia),
			DBL2NUM(oma), DBL2NUM(bpa), DBL2NUM(bqa), DBL2NUM(pia),
			DBL2NUM(bpia), DBL2NUM(epsa), DBL2NUM(chia), DBL2NUM(za),
			DBL2NUM(zetaa), DBL2NUM(thetaa), DBL2NUM(pa), DBL2NUM(gam),
			DBL2NUM(phi), DBL2NUM(psi));
}

static VALUE
celes_s_pom00(VALUE self, VALUE vxp, VALUE vyp, VALUE vsp){
	double rpom[3][3];

	iauPom00(NUM2DBL(vxp), NUM2DBL(vyp), NUM2DBL(vsp), rpom);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return vmat_new33(rpom);
}

static VALUE
celes_s_pr00(VALUE self, VALUE vdate1, VALUE vdate2){
	double dpsipr, depspr;

	iauPr00(NUM2DBL(vdate1), NUM2DBL(vdate2), &dpsipr, &depspr);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(dpsipr), DBL2NUM(depspr));
}

static VALUE
celes_s_prec76(VALUE self, VALUE vep01, VALUE vep02,
		VALUE vep11, VALUE vep12){
	double zeta, z, theta;

	iauPrec76(NUM2DBL(vep01), NUM2DBL(vep02),
			NUM2DBL(vep11), NUM2DBL(vep12), &zeta, &z, &theta);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(3, DBL2NUM(zeta), DBL2NUM(z), DBL2NUM(theta));
}

static VALUE
celes_s_s00(VALUE self, VALUE vdate1, VALUE vdate2, VALUE vx, VALUE vy){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauS00(NUM2DBL(vdate1), NUM2DBL(vdate2),
			NUM2DBL(vx), NUM2DBL(vy)));
}

static VALUE
celes_s_s00a(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauS00a(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_s00b(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauS00b(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_s06(VALUE self, VALUE vdate1, VALUE vdate2, VALUE vx, VALUE vy){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauS06(NUM2DBL(vdate1), NUM2DBL(vdate2),
			NUM2DBL(vx), NUM2DBL(vy)));
}

static VALUE
celes_s_s06a(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauS06a(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_sp00(VALUE self, VALUE vdate1, VALUE vdate2){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauSp00(NUM2DBL(vdate1), NUM2DBL(vdate2)));
}

static VALUE
celes_s_xy06(VALUE self, VALUE vdate1, VALUE vdate2){
	double x, y;

	iauXy06(NUM2DBL(vdate1), NUM2DBL(vdate2), &x, &y);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(x), DBL2NUM(y));
}

static VALUE
celes_s_xys00a(VALUE self, VALUE vdate1, VALUE vdate2){
	double x, y, s;

	iauXys00a(NUM2DBL(vdate1), NUM2DBL(vdate2), &x, &y, &s);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(3, DBL2NUM(x), DBL2NUM(y), DBL2NUM(s));
}

static VALUE
celes_s_xys00b(VALUE self, VALUE vdate1, VALUE vdate2){
	double x, y, s;

	iauXys00b(NUM2DBL(vdate1), NUM2DBL(vdate2), &x, &y, &s);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(3, DBL2NUM(x), DBL2NUM(y), DBL2NUM(s));
}

static VALUE
celes_s_xys06a(VALUE self, VALUE vdate1, VALUE vdate2){
	double x, y, s;

	iauXys06a(NUM2DBL(vdate1), NUM2DBL(vdate2), &x, &y, &s);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(3, DBL2NUM(x), DBL2NUM(y), DBL2NUM(s));
}

static VALUE
celes_s_fad03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFad03(NUM2DBL(vt)));
}

static VALUE
celes_s_fae03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFae03(NUM2DBL(vt)));
}

static VALUE
celes_s_faf03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFaf03(NUM2DBL(vt)));
}

static VALUE
celes_s_faju03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFaju03(NUM2DBL(vt)));
}

static VALUE
celes_s_fal03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFal03(NUM2DBL(vt)));
}

static VALUE
celes_s_falp03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFalp03(NUM2DBL(vt)));
}

static VALUE
celes_s_fama03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFama03(NUM2DBL(vt)));
}

static VALUE
celes_s_fame03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFame03(NUM2DBL(vt)));
}

static VALUE
celes_s_fane03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFane03(NUM2DBL(vt)));
}

static VALUE
celes_s_faom03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFaom03(NUM2DBL(vt)));
}

static VALUE
celes_s_fapa03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFapa03(NUM2DBL(vt)));
}

static VALUE
celes_s_fasa03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFasa03(NUM2DBL(vt)));
}

static VALUE
celes_s_faur03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFaur03(NUM2DBL(vt)));
}

static VALUE
celes_s_fave03(VALUE self, VALUE vt){
	rb_ivar_set(self, id_status, INT2FIX(0));

	return DBL2NUM(iauFave03(NUM2DBL(vt)));
}
static VALUE
celes_s_pvstar(VALUE self, VALUE vpv){
	int ret;
	double pv[2][3], ra, dec, pmr, pmd, px, rv;

	cmat_cp23(vpv, pv);
	ret = iauPvstar(pv, &ra, &dec, &pmr, &pmd, &px, &rv);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "superluminal speed");
	else if(ret == -2)
		rb_raise(rb_eArgError, "null position vector");
	
	return rb_ary_new3(6, DBL2NUM(ra), DBL2NUM(dec),
			DBL2NUM(pmr), DBL2NUM(pmd), DBL2NUM(px), DBL2NUM(rv));
}

static VALUE
celes_s_starpv(VALUE self, VALUE vra, VALUE vdec,
		VALUE vpmr, VALUE vpmd, VALUE vpx, VALUE vrv){
	int ret;
	double pv[2][3];

	ret = iauStarpv(NUM2DBL(vra), NUM2DBL(vdec), NUM2DBL(vpmr),
			NUM2DBL(vpmd), NUM2DBL(vpx), NUM2DBL(vrv), pv);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	return vmat_new23(pv);
}
static VALUE
celes_s_fk52h(VALUE self, VALUE vr5, VALUE vd5,
		VALUE vdr5, VALUE vdd5, VALUE vpx5, VALUE vrv5){
	double rh, dh, drh, ddh, pxh, rvh;

	iauFk52h(NUM2DBL(vr5), NUM2DBL(vd5), NUM2DBL(vdr5),
			NUM2DBL(vdd5), NUM2DBL(vpx5), NUM2DBL(vrv5),
			&rh, &dh, &drh, &ddh, &pxh, &rvh);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(6, DBL2NUM(rh), DBL2NUM(dh),
			DBL2NUM(drh), DBL2NUM(ddh), DBL2NUM(pxh), DBL2NUM(rvh));
}

static VALUE
celes_s_fk5hip(VALUE self){
	double r5h[3][3], s5h[3];

	iauFk5hip(r5h, s5h);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, vmat_new33(r5h), vvec_new(s5h));
}

static VALUE
celes_s_fk5hz(VALUE self, VALUE vr5, VALUE vd5,
		VALUE vdate1, VALUE vdate2){
	double rh, dh;

	iauFk5hz(NUM2DBL(vr5), NUM2DBL(vd5),
			NUM2DBL(vdate1), NUM2DBL(vdate2), &rh, &dh);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(2, DBL2NUM(rh), DBL2NUM(dh));
}

static VALUE
celes_s_h2fk5(VALUE self, VALUE vrh, VALUE vdh,
		VALUE vdrh, VALUE vddh, VALUE vpxh, VALUE vrvh){
	double r5, d5, dr5, dd5, px5, rv5;

	iauH2fk5(NUM2DBL(vrh), NUM2DBL(vdh), NUM2DBL(vdrh),
			NUM2DBL(vddh), NUM2DBL(vpxh), NUM2DBL(vrvh),
			&r5, &d5, &dr5, &dd5, &px5, &rv5);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(6, DBL2NUM(r5), DBL2NUM(d5),
			DBL2NUM(dr5), DBL2NUM(dd5), DBL2NUM(px5), DBL2NUM(rv5));
}

static VALUE
celes_s_hfk5z(VALUE self, VALUE vrh, VALUE vdh,
		VALUE vdate1, VALUE vdate2){
	double r5, d5, dr5, dd5;

	iauHfk5z(NUM2DBL(vrh), NUM2DBL(vdh), NUM2DBL(vdate1), NUM2DBL(vdate2),
			&r5, &d5, &dr5, &dd5);
	rb_ivar_set(self, id_status, INT2FIX(0));

	return rb_ary_new3(4, DBL2NUM(r5), DBL2NUM(d5),
			DBL2NUM(dr5), DBL2NUM(dd5));
}

static VALUE
celes_s_starpm(VALUE self, VALUE vra1, VALUE vdec1,
		VALUE vpmr1, VALUE vpmd1, VALUE vpx1, VALUE vrv1,
		VALUE vep1a, VALUE vep1b, VALUE vep2a, VALUE vep2b){
	int ret;
	double ra2, dec2, pmr2, pmd2, px2, rv2;

	ret = iauStarpm(NUM2DBL(vra1), NUM2DBL(vdec1),
			NUM2DBL(vpmr1), NUM2DBL(vpmd1), NUM2DBL(vpx1), NUM2DBL(vrv1),
			NUM2DBL(vep1a), NUM2DBL(vep1b), NUM2DBL(vep2a), NUM2DBL(vep2b),
			&ra2, &dec2, &pmr2, &pmd2, &px2, &rv2);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "system error");
	
	return rb_ary_new3(6,
			DBL2NUM(ra2), DBL2NUM(dec2), DBL2NUM(pmr2),
			DBL2NUM(pmd2), DBL2NUM(px2), DBL2NUM(rv2));
}
static VALUE
celes_s_eform(VALUE self, VALUE vn){
	int ret;
	double a, f;

	ret = iauEform(NUM2INT(vn), &a, &f);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "illegal identifier");

	return rb_ary_new3(2, DBL2NUM(a), DBL2NUM(f));
}

static VALUE
celes_s_gc2gd(VALUE self, VALUE vn, VALUE vxyz){
	int ret;
	double xyz[3], elong, phi, height;

	cvec_cp(vxyz, xyz);
	ret = iauGc2gd(NUM2INT(vn), xyz, &elong, &phi, &height);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "illegal identifier");
	else if(ret == -2)
		rb_raise(rb_eArgError, "internal error");

	return rb_ary_new3(3, DBL2NUM(elong), DBL2NUM(phi), DBL2NUM(height));
}

static VALUE
celes_s_gc2gde(VALUE self, VALUE va, VALUE vf, VALUE vxyz){
	int ret;
	double xyz[3], elong, phi, height;

	cvec_cp(vxyz, xyz);
	ret = iauGc2gde(NUM2DBL(va), NUM2DBL(vf), xyz, &elong, &phi, &height);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "illegal f");
	else if(ret == -2)
		rb_raise(rb_eArgError, "illegal a");

	return rb_ary_new3(3, DBL2NUM(elong), DBL2NUM(phi), DBL2NUM(height));
}

static VALUE
celes_s_gd2gc(VALUE self, VALUE vn,
		VALUE velong, VALUE vphi, VALUE vheight){
	int ret;
	double xyz[3];

	ret = iauGd2gc(NUM2INT(vn), NUM2DBL(velong),
			NUM2DBL(vphi), NUM2DBL(vheight), xyz);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "illegal identifier");
	else if(ret == -2)
		rb_raise(rb_eArgError, "illegal case");

	return vvec_new(xyz);
}

static VALUE
celes_s_gd2gce(VALUE self, VALUE va, VALUE vf,
		VALUE velong, VALUE vphi, VALUE vheight){
	int ret;
	double xyz[3];

	ret = iauGd2gce(NUM2DBL(va), NUM2DBL(vf),
			NUM2DBL(velong), NUM2DBL(vphi), NUM2DBL(vheight), xyz);
	rb_ivar_set(self, id_status, INT2FIX(ret));

	if(ret == -1)
		rb_raise(rb_eArgError, "illegal case");

	return vvec_new(xyz);
}


void
Init_celes_core(void){
	mCeles = rb_define_module("Celes");
	id_status = rb_intern("@status");

	rb_define_module_function(mCeles, "status", celes_s_status, 0);

	rb_define_module_function(mCeles, "zp!",    celes_s_zp_b,   1);
	rb_define_module_function(mCeles, "zp",     celes_s_zp,     0);
	rb_define_module_function(mCeles, "zr!",    celes_s_zr_b,   1);
	rb_define_module_function(mCeles, "zr",     celes_s_zr,     0);
	rb_define_module_function(mCeles, "ir!",    celes_s_ir_b,   1);
	rb_define_module_function(mCeles, "ir",     celes_s_ir,     0);
	rb_define_module_function(mCeles, "cp",     celes_s_cp,     1);
	rb_define_module_function(mCeles, "cr",     celes_s_cr,     1);
	rb_define_module_function(mCeles, "rx!",    celes_s_rx_b,   2);
	rb_define_module_function(mCeles, "rx",     celes_s_rx,     2);
	rb_define_module_function(mCeles, "ry!",    celes_s_ry_b,   2);
	rb_define_module_function(mCeles, "ry",     celes_s_ry,     2);
	rb_define_module_function(mCeles, "rz!",    celes_s_rz_b,   2);
	rb_define_module_function(mCeles, "rz",     celes_s_rz,     2);
	rb_define_module_function(mCeles, "s2c",    celes_s_s2c,    2);
	rb_define_module_function(mCeles, "c2s",    celes_s_c2s,    1);
	rb_define_module_function(mCeles, "s2p",    celes_s_s2p,    3);
	rb_define_module_function(mCeles, "p2s",    celes_s_p2s,    1);
	rb_define_module_function(mCeles, "ppp",    celes_s_ppp,    2);
	rb_define_module_function(mCeles, "pmp",    celes_s_pmp,    2);
	rb_define_module_function(mCeles, "ppsp",   celes_s_ppsp,   3);
	rb_define_module_function(mCeles, "pdp",    celes_s_pdp,    2);
	rb_define_module_function(mCeles, "pxp",    celes_s_pxp,    2);
	rb_define_module_function(mCeles, "pm",     celes_s_pm,     1);
	rb_define_module_function(mCeles, "pn",     celes_s_pn,     1);
	rb_define_module_function(mCeles, "sxp",    celes_s_sxp,    2);
	rb_define_module_function(mCeles, "rxr",    celes_s_rxr,    2);
	rb_define_module_function(mCeles, "tr",     celes_s_tr,     1);
	rb_define_module_function(mCeles, "rxp",    celes_s_rxp,    2);
	rb_define_module_function(mCeles, "trxp",   celes_s_trxp,   2);
	rb_define_module_function(mCeles, "sepp",   celes_s_sepp,   2);
	rb_define_module_function(mCeles, "seps",   celes_s_seps,   4);
	rb_define_module_function(mCeles, "pap",    celes_s_pap,    2);
	rb_define_module_function(mCeles, "pas",    celes_s_pas,    4);
	rb_define_module_function(mCeles, "rv2m",   celes_s_rv2m,   1);
	rb_define_module_function(mCeles, "rm2v",   celes_s_rm2v,   1);
	rb_define_module_function(mCeles, "zpv!",   celes_s_zpv_b,  1);
	rb_define_module_function(mCeles, "zpv",    celes_s_zpv,    0);
	rb_define_module_function(mCeles, "cpv",    celes_s_cpv,    1);
	rb_define_module_function(mCeles, "p2pv",   celes_s_p2pv,   1);
	rb_define_module_function(mCeles, "pv2p",   celes_s_pv2p,   1);
	rb_define_module_function(mCeles, "s2pv",   celes_s_s2pv,   6);
	rb_define_module_function(mCeles, "pv2s",   celes_s_pv2s,   1);
	rb_define_module_function(mCeles, "pvppv",  celes_s_pvppv,  2);
	rb_define_module_function(mCeles, "pvmpv",  celes_s_pvmpv,  2);
	rb_define_module_function(mCeles, "pvdpv",  celes_s_pvdpv,  2);
	rb_define_module_function(mCeles, "pvxpv",  celes_s_pvxpv,  2);
	rb_define_module_function(mCeles, "pvm",    celes_s_pvm,    1);
	rb_define_module_function(mCeles, "sxpv",   celes_s_sxpv,   2);
	rb_define_module_function(mCeles, "s2xpv",  celes_s_s2xpv,  3);
	rb_define_module_function(mCeles, "pvu",    celes_s_pvu,    2);
	rb_define_module_function(mCeles, "pvup",   celes_s_pvup,   2);
	rb_define_module_function(mCeles, "rxpv",   celes_s_rxpv,   2);
	rb_define_module_function(mCeles, "trxpv",  celes_s_trxpv,  2);

	rb_define_module_function(mCeles, "anp",    celes_s_anp,    1);
	rb_define_module_function(mCeles, "anpm",   celes_s_anpm,   1);
	rb_define_module_function(mCeles, "a2tf",   celes_s_a2tf,   2);
	rb_define_module_function(mCeles, "a2af",   celes_s_a2af,   2);
	rb_define_module_function(mCeles, "af2a",   celes_s_af2a,   4);
	rb_define_module_function(mCeles, "d2tf",   celes_s_d2tf,   2);
	rb_define_module_function(mCeles, "tf2a",   celes_s_tf2a,   4);
	rb_define_module_function(mCeles, "tf2d",   celes_s_tf2d,   4);

	rb_define_module_function(mCeles, "cal2jd", celes_s_cal2jd, 3);
	rb_define_module_function(mCeles, "epb",    celes_s_epb,    2);
	rb_define_module_function(mCeles, "epb2jd", celes_s_epb2jd, 1);
	rb_define_module_function(mCeles, "epj",    celes_s_epj,    2);
	rb_define_module_function(mCeles, "epj2jd", celes_s_epj2jd, 1);
	rb_define_module_function(mCeles, "jd2cal", celes_s_jd2cal, 2);
	rb_define_module_function(mCeles, "jdcalf", celes_s_jdcalf, 3);

	rb_define_module_function(mCeles, "d2dtf",  celes_s_d2dtf,  4);
	rb_define_module_function(mCeles, "dat",    celes_s_dat,    4);
	rb_define_module_function(mCeles, "dtdb",   celes_s_dtdb,   6);
	rb_define_module_function(mCeles, "dtf2d",  celes_s_dtf2d,  7);
	rb_define_module_function(mCeles, "taitt",  celes_s_taitt,  2);
	rb_define_module_function(mCeles, "taiut1", celes_s_taiut1, 3);
	rb_define_module_function(mCeles, "taiutc", celes_s_taiutc, 2);
	rb_define_module_function(mCeles, "tcbtdb", celes_s_tcbtdb, 2);
	rb_define_module_function(mCeles, "tcgtt" , celes_s_tcgtt,  2);
	rb_define_module_function(mCeles, "tdbtcb", celes_s_tdbtcb, 2);
	rb_define_module_function(mCeles, "tdbtt" , celes_s_tdbtt,  3);
	rb_define_module_function(mCeles, "tttai" , celes_s_tttai,  2);
	rb_define_module_function(mCeles, "tttcg" , celes_s_tttcg,  2);
	rb_define_module_function(mCeles, "tttdb" , celes_s_tttdb,  3);
	rb_define_module_function(mCeles, "ttut1" , celes_s_ttut1,  3);
	rb_define_module_function(mCeles, "ut1tai", celes_s_ut1tai, 3);
	rb_define_module_function(mCeles, "ut1tt",  celes_s_ut1tt,  3);
	rb_define_module_function(mCeles, "ut1utc", celes_s_ut1utc, 3);
	rb_define_module_function(mCeles, "utctai", celes_s_utctai, 2);
	rb_define_module_function(mCeles, "utcut1", celes_s_utcut1, 3);

	rb_define_module_function(mCeles, "ee00",   celes_s_ee00,   4);
	rb_define_module_function(mCeles, "ee00a",  celes_s_ee00a,  2);
	rb_define_module_function(mCeles, "ee00b",  celes_s_ee00b,  2);
	rb_define_module_function(mCeles, "ee06a",  celes_s_ee06a,  2);
	rb_define_module_function(mCeles, "eect00", celes_s_eect00, 2);
	rb_define_module_function(mCeles, "eqeq94", celes_s_eqeq94, 2);
	rb_define_module_function(mCeles, "era00",  celes_s_era00,  2);
	rb_define_module_function(mCeles, "gmst00", celes_s_gmst00, 4);
	rb_define_module_function(mCeles, "gmst06", celes_s_gmst06, 4);
	rb_define_module_function(mCeles, "gmst82", celes_s_gmst82, 2);
	rb_define_module_function(mCeles, "gst00a", celes_s_gst00a, 4);
	rb_define_module_function(mCeles, "gst00b", celes_s_gst00b, 2);
	rb_define_module_function(mCeles, "gst06",  celes_s_gst06,  5);
	rb_define_module_function(mCeles, "gst06a", celes_s_gst06a, 4);
	rb_define_module_function(mCeles, "gst94",  celes_s_gst94,  2);

	rb_define_module_function(mCeles, "epv00",  celes_s_epv00,  2);
	rb_define_module_function(mCeles, "plan94", celes_s_plan94, 3);

	rb_define_module_function(mCeles, "bi00",   celes_s_bi00,   0);
	rb_define_module_function(mCeles, "bp00",   celes_s_bp00,   2);
	rb_define_module_function(mCeles, "bp06",   celes_s_bp06,   2);
	rb_define_module_function(mCeles, "bpn2xy", celes_s_bpn2xy, 1);
	rb_define_module_function(mCeles, "c2i00a", celes_s_c2i00a, 2);
	rb_define_module_function(mCeles, "c2i00b", celes_s_c2i00b, 2);
	rb_define_module_function(mCeles, "c2i06a", celes_s_c2i06a, 2);
	rb_define_module_function(mCeles, "c2ibpn", celes_s_c2ibpn, 3);
	rb_define_module_function(mCeles, "c2ixy",  celes_s_c2ixy,  4);
	rb_define_module_function(mCeles, "c2ixys", celes_s_c2ixys, 3);
	rb_define_module_function(mCeles, "c2t00a", celes_s_c2t00a, 6);
	rb_define_module_function(mCeles, "c2t00b", celes_s_c2t00b, 6);
	rb_define_module_function(mCeles, "c2t06a", celes_s_c2t06a, 6);
	rb_define_module_function(mCeles, "c2tcio", celes_s_c2tcio, 3);
	rb_define_module_function(mCeles, "c2teqx", celes_s_c2teqx, 3);
	rb_define_module_function(mCeles, "c2tpe",  celes_s_c2tpe,  8);
	rb_define_module_function(mCeles, "c2txy",  celes_s_c2txy,  8);
	rb_define_module_function(mCeles, "eo06a",  celes_s_eo06a,  2);
	rb_define_module_function(mCeles, "eors",   celes_s_eors,   2);
	rb_define_module_function(mCeles, "fw2m",   celes_s_fw2m,   4);
	rb_define_module_function(mCeles, "fw2xy",  celes_s_fw2xy,  4);
	rb_define_module_function(mCeles, "num00a", celes_s_num00a, 2);
	rb_define_module_function(mCeles, "num00b", celes_s_num00b, 2);
	rb_define_module_function(mCeles, "num06a", celes_s_num06a, 2);
	rb_define_module_function(mCeles, "numat",  celes_s_numat,  3);
	rb_define_module_function(mCeles, "nut00a", celes_s_nut00a, 2);
	rb_define_module_function(mCeles, "nut00b", celes_s_nut00b, 2);
	rb_define_module_function(mCeles, "nut06a", celes_s_nut06a, 2);
	rb_define_module_function(mCeles, "nut80",  celes_s_nut80,  2);
	rb_define_module_function(mCeles, "nutm80", celes_s_nutm80, 2);
	rb_define_module_function(mCeles, "obl06",  celes_s_obl06,  2);
	rb_define_module_function(mCeles, "obl80",  celes_s_obl80,  2);
	rb_define_module_function(mCeles, "pb06",   celes_s_pb06,   2);
	rb_define_module_function(mCeles, "pfw06",  celes_s_pfw06,  2);
	rb_define_module_function(mCeles, "pmat00", celes_s_pmat00, 2);
	rb_define_module_function(mCeles, "pmat06", celes_s_pmat06, 2);
	rb_define_module_function(mCeles, "pmat76", celes_s_pmat76, 2);
	rb_define_module_function(mCeles, "pn00",   celes_s_pn00,   4);
	rb_define_module_function(mCeles, "pn00a",  celes_s_pn00a,  2);
	rb_define_module_function(mCeles, "pn00b",  celes_s_pn00b,  2);
	rb_define_module_function(mCeles, "pn06",   celes_s_pn06,   4);
	rb_define_module_function(mCeles, "pn06a",  celes_s_pn06a,  2);
	rb_define_module_function(mCeles, "pnm00a", celes_s_pnm00a, 2);
	rb_define_module_function(mCeles, "pnm00b", celes_s_pnm00b, 2);
	rb_define_module_function(mCeles, "pnm06a", celes_s_pnm06a, 2);
	rb_define_module_function(mCeles, "pnm80",  celes_s_pnm80,  2);
	rb_define_module_function(mCeles, "p06e",   celes_s_p06e,   2);
	rb_define_module_function(mCeles, "pom00",  celes_s_pom00,  3);
	rb_define_module_function(mCeles, "pr00",   celes_s_pr00,   2);
	rb_define_module_function(mCeles, "prec76", celes_s_prec76, 4);
	rb_define_module_function(mCeles, "s00",    celes_s_s00,    4);
	rb_define_module_function(mCeles, "s00a",   celes_s_s00a,   2);
	rb_define_module_function(mCeles, "s00b",   celes_s_s00b,   2);
	rb_define_module_function(mCeles, "s06",    celes_s_s06,    4);
	rb_define_module_function(mCeles, "s06a",   celes_s_s06a,   2);
	rb_define_module_function(mCeles, "sp00",   celes_s_sp00,   2);
	rb_define_module_function(mCeles, "xy06",   celes_s_xy06,   2);
	rb_define_module_function(mCeles, "xys00a", celes_s_xys00a, 2);
	rb_define_module_function(mCeles, "xys00b", celes_s_xys00b, 2);
	rb_define_module_function(mCeles, "xys06a", celes_s_xys06a, 2);

	rb_define_module_function(mCeles, "fad03",  celes_s_fad03,  1);
	rb_define_module_function(mCeles, "fae03",  celes_s_fae03,  1);
	rb_define_module_function(mCeles, "faf03",  celes_s_faf03,  1);
	rb_define_module_function(mCeles, "faju03", celes_s_faju03, 1);
	rb_define_module_function(mCeles, "fal03",  celes_s_fal03,  1);
	rb_define_module_function(mCeles, "falp03", celes_s_falp03, 1);
	rb_define_module_function(mCeles, "fama03", celes_s_fama03, 1);
	rb_define_module_function(mCeles, "fame03", celes_s_fame03, 1);
	rb_define_module_function(mCeles, "fane03", celes_s_fane03, 1);
	rb_define_module_function(mCeles, "faom03", celes_s_faom03, 1);
	rb_define_module_function(mCeles, "fapa03", celes_s_fapa03, 1);
	rb_define_module_function(mCeles, "fasa03", celes_s_fasa03, 1);
	rb_define_module_function(mCeles, "faur03", celes_s_faur03, 1);
	rb_define_module_function(mCeles, "fave03", celes_s_fave03, 1);

	rb_define_module_function(mCeles, "pvstar", celes_s_pvstar, 1);
	rb_define_module_function(mCeles, "starpv", celes_s_starpv, 6);

	rb_define_module_function(mCeles, "fk52h",  celes_s_fk52h,  6);
	rb_define_module_function(mCeles, "fk5hip", celes_s_fk5hip, 0);
	rb_define_module_function(mCeles, "fk5hz",  celes_s_fk5hz,  4);
	rb_define_module_function(mCeles, "h2fk5",  celes_s_h2fk5,  6);
	rb_define_module_function(mCeles, "hfk5z",  celes_s_hfk5z,  4);
	rb_define_module_function(mCeles, "starpm", celes_s_starpm, 10);

	rb_define_module_function(mCeles, "eform",  celes_s_eform,  1);
	rb_define_module_function(mCeles, "gc2gd",  celes_s_gc2gd,  2);
	rb_define_module_function(mCeles, "gc2gde", celes_s_gc2gde, 3);
	rb_define_module_function(mCeles, "gd2gc",  celes_s_gd2gc,  4);
	rb_define_module_function(mCeles, "gd2gce", celes_s_gd2gce, 5);

	rb_define_const(mCeles, "DPI",    DBL2NUM(DPI));
	rb_define_const(mCeles, "D2PI",   DBL2NUM(D2PI));
	rb_define_const(mCeles, "DD2R",   DBL2NUM(DD2R));
	rb_define_const(mCeles, "DR2AS",  DBL2NUM(DR2AS));
	rb_define_const(mCeles, "DAS2R",  DBL2NUM(DAS2R));
	rb_define_const(mCeles, "DS2R",   DBL2NUM(DS2R));
	rb_define_const(mCeles, "TURNAS", DBL2NUM(TURNAS));
	rb_define_const(mCeles, "DMAS2R", DBL2NUM(DMAS2R));
	rb_define_const(mCeles, "DTY",    DBL2NUM(DTY));
	rb_define_const(mCeles, "DAYSEC", DBL2NUM(DAYSEC));
	rb_define_const(mCeles, "DJY",    DBL2NUM(DJY));
	rb_define_const(mCeles, "DJC",    DBL2NUM(DJC));
	rb_define_const(mCeles, "DJM",    DBL2NUM(DJM));
	rb_define_const(mCeles, "DJ00",   DBL2NUM(DJ00));
	rb_define_const(mCeles, "DJM0",   DBL2NUM(DJM0));
	rb_define_const(mCeles, "DJM00",  DBL2NUM(DJM00));
	rb_define_const(mCeles, "DJM77",  DBL2NUM(DJM77));
	rb_define_const(mCeles, "TTMTAI", DBL2NUM(TTMTAI));
	rb_define_const(mCeles, "DAU",    DBL2NUM(DAU));
	rb_define_const(mCeles, "DC",     DBL2NUM(DC));
	rb_define_const(mCeles, "ELG",    DBL2NUM(ELG));
	rb_define_const(mCeles, "ELB",    DBL2NUM(ELB));
	rb_define_const(mCeles, "TDB0",   DBL2NUM(TDB0));
	rb_define_const(mCeles, "WGS84",  INT2NUM(WGS84));
	rb_define_const(mCeles, "GRS80",  INT2NUM(GRS80));
	rb_define_const(mCeles, "WGS72",  INT2NUM(WGS72));
}




/*----------------------------------------------------------------------
**
**  Celes is a wrapper of the SOFA Library for Ruby.
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
