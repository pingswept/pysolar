
SHELL = /bin/sh

# V=0 quiet, V=1 verbose.  other values don't work.
V = 0
Q1 = $(V:1=)
Q = $(Q1:0=@)
ECHO1 = $(V:1=@:)
ECHO = $(ECHO1:0=@echo)
NULLCMD = :

#### Start of system configuration section. ####

srcdir = .
topdir = /C/Ruby226/include/ruby-2.2.0
hdrdir = $(topdir)
arch_hdrdir = C:/Ruby226/include/ruby-2.2.0/x64-mingw32
PATH_SEPARATOR = :
VPATH = $(srcdir):$(arch_hdrdir)/ruby:$(hdrdir)/ruby
prefix = $(DESTDIR)/C/Ruby226
rubysitearchprefix = $(rubylibprefix)/$(sitearch)
rubyarchprefix = $(rubylibprefix)/$(arch)
rubylibprefix = $(libdir)/$(RUBY_BASE_NAME)
exec_prefix = $(prefix)
vendorarchhdrdir = $(vendorhdrdir)/$(sitearch)
sitearchhdrdir = $(sitehdrdir)/$(sitearch)
rubyarchhdrdir = $(rubyhdrdir)/$(arch)
vendorhdrdir = $(rubyhdrdir)/vendor_ruby
sitehdrdir = $(rubyhdrdir)/site_ruby
rubyhdrdir = $(includedir)/$(RUBY_VERSION_NAME)
vendorarchdir = $(vendorlibdir)/$(sitearch)
vendorlibdir = $(vendordir)/$(ruby_version)
vendordir = $(rubylibprefix)/vendor_ruby
sitearchdir = $(DESTDIR)./.gem.20170129-5540-nxuw03
sitelibdir = $(DESTDIR)./.gem.20170129-5540-nxuw03
sitedir = $(rubylibprefix)/site_ruby
rubyarchdir = $(rubylibdir)/$(arch)
rubylibdir = $(rubylibprefix)/$(ruby_version)
sitearchincludedir = $(includedir)/$(sitearch)
archincludedir = $(includedir)/$(arch)
sitearchlibdir = $(libdir)/$(sitearch)
archlibdir = $(libdir)/$(arch)
ridir = $(datarootdir)/$(RI_BASE_NAME)
mandir = $(datarootdir)/man
localedir = $(datarootdir)/locale
libdir = $(exec_prefix)/lib
psdir = $(docdir)
pdfdir = $(docdir)
dvidir = $(docdir)
htmldir = $(docdir)
infodir = $(datarootdir)/info
docdir = $(datarootdir)/doc/$(PACKAGE)
oldincludedir = $(DESTDIR)/usr/include
includedir = $(prefix)/include
localstatedir = $(prefix)/var
sharedstatedir = $(prefix)/com
sysconfdir = $(prefix)/etc
datadir = $(datarootdir)
datarootdir = $(prefix)/share
libexecdir = $(exec_prefix)/libexec
sbindir = $(exec_prefix)/sbin
bindir = $(exec_prefix)/bin
archdir = $(rubyarchdir)


CC = x86_64-w64-mingw32-gcc
CXX = x86_64-w64-mingw32-g++
LIBRUBY = lib$(RUBY_SO_NAME).dll.a
LIBRUBY_A = lib$(RUBY_SO_NAME)-static.a
LIBRUBYARG_SHARED = -l$(RUBY_SO_NAME)
LIBRUBYARG_STATIC = -l$(RUBY_SO_NAME)-static
empty =
OUTFLAG = -o $(empty)
COUTFLAG = -o $(empty)

RUBY_EXTCONF_H = 
cflags   =  $(optflags) $(debugflags) $(warnflags)
optflags = -O3 -fno-omit-frame-pointer -fno-fast-math
debugflags = -g
warnflags = -Wall -Wextra -Wno-unused-parameter -Wno-parentheses -Wno-long-long -Wno-missing-field-initializers -Wunused-variable -Wpointer-arith -Wwrite-strings -Wdeclaration-after-statement -Wimplicit-function-declaration -Wdeprecated-declarations -Wno-packed-bitfield-compat
CCDLFLAGS = 
CFLAGS   = $(CCDLFLAGS) $(cflags) $(ARCH_FLAG)
INCFLAGS = -I. -I$(arch_hdrdir) -I$(hdrdir)/ruby/backward -I$(hdrdir) -I$(srcdir)
DEFS     = -D_FILE_OFFSET_BITS=64
CPPFLAGS =  -DFD_SETSIZE=2048 -D_WIN32_WINNT=0x0501 -D__MINGW_USE_VC2005_COMPAT $(DEFS) $(cppflags)
CXXFLAGS = $(CCDLFLAGS) $(cxxflags) $(ARCH_FLAG)
ldflags  = -L. 
dldflags =  -Wl,--enable-auto-image-base,--enable-auto-import $(DEFFILE) 
ARCH_FLAG = 
DLDFLAGS = $(ldflags) $(dldflags) $(ARCH_FLAG)
LDSHARED = $(CC) -shared $(if $(filter-out -g -g0,$(debugflags)),,-s)
LDSHAREDXX = $(CXX) -shared $(if $(filter-out -g -g0,$(debugflags)),,-s)
AR = ar
EXEEXT = .exe

RUBY_INSTALL_NAME = $(RUBY_BASE_NAME)
RUBY_SO_NAME = x64-msvcrt-ruby220
RUBYW_INSTALL_NAME = $(RUBYW_BASE_NAME)
RUBY_VERSION_NAME = $(RUBY_BASE_NAME)-$(ruby_version)
RUBYW_BASE_NAME = rubyw
RUBY_BASE_NAME = ruby

arch = x64-mingw32
sitearch = x64-msvcrt
ruby_version = 2.2.0
ruby = $(bindir)/$(RUBY_BASE_NAME)
RUBY = $(ruby)
ruby_headers = $(hdrdir)/ruby.h $(hdrdir)/ruby/ruby.h $(hdrdir)/ruby/defines.h $(hdrdir)/ruby/missing.h $(hdrdir)/ruby/intern.h $(hdrdir)/ruby/st.h $(hdrdir)/ruby/subst.h $(arch_hdrdir)/ruby/config.h

RM = rm -f
RM_RF = $(RUBY) -run -e rm -- -rf
RMDIRS = rmdir --ignore-fail-on-non-empty -p
MAKEDIRS = /usr/bin/mkdir -p
INSTALL = /usr/bin/install -c
INSTALL_PROG = $(INSTALL) -m 0755
INSTALL_DATA = $(INSTALL) -m 644
COPY = cp
TOUCH = exit >

#### End of system configuration section. ####

preload = 

libpath = . $(libdir)
LIBPATH =  -L. -L$(libdir)
DEFFILE = $(TARGET)-$(arch).def

CLEANFILES = mkmf.log $(DEFFILE)
DISTCLEANFILES = 
DISTCLEANDIRS = 

extout = 
extout_prefix = 
target_prefix = 
LOCAL_LIBS = 
LIBS = $(LIBRUBYARG_SHARED)  -lshell32 -lws2_32 -liphlpapi -limagehlp -lshlwapi  
ORIG_SRCS = a2af.c a2tf.c af2a.c anp.c anpm.c bi00.c bp00.c bp06.c bpn2xy.c c2i00a.c c2i00b.c c2i06a.c c2ibpn.c c2ixy.c c2ixys.c c2s.c c2t00a.c c2t00b.c c2t06a.c c2tcio.c c2teqx.c c2tpe.c c2txy.c cal2jd.c celes_core.c cp.c cpv.c cr.c d2dtf.c d2tf.c dat.c dtdb.c dtf2d.c ee00.c ee00a.c ee00b.c ee06a.c eect00.c eform.c eo06a.c eors.c epb.c epb2jd.c epj.c epj2jd.c epv00.c eqeq94.c era00.c fad03.c fae03.c faf03.c faju03.c fal03.c falp03.c fama03.c fame03.c fane03.c faom03.c fapa03.c fasa03.c faur03.c fave03.c fk52h.c fk5hip.c fk5hz.c fw2m.c fw2xy.c gc2gd.c gc2gde.c gd2gc.c gd2gce.c gmst00.c gmst06.c gmst82.c gst00a.c gst00b.c gst06.c gst06a.c gst94.c h2fk5.c hfk5z.c ir.c jd2cal.c jdcalf.c num00a.c num00b.c num06a.c numat.c nut00a.c nut00b.c nut06a.c nut80.c nutm80.c obl06.c obl80.c p06e.c p2pv.c p2s.c pap.c pas.c pb06.c pdp.c pfw06.c plan94.c pm.c pmat00.c pmat06.c pmat76.c pmp.c pn.c pn00.c pn00a.c pn00b.c pn06.c pn06a.c pnm00a.c pnm00b.c pnm06a.c pnm80.c pom00.c ppp.c ppsp.c pr00.c prec76.c pv2p.c pv2s.c pvdpv.c pvm.c pvmpv.c pvppv.c pvstar.c pvu.c pvup.c pvxpv.c pxp.c rm2v.c rv2m.c rx.c rxp.c rxpv.c rxr.c ry.c rz.c s00.c s00a.c s00b.c s06.c s06a.c s2c.c s2p.c s2pv.c s2xpv.c sepp.c seps.c sp00.c starpm.c starpv.c sxp.c sxpv.c taitt.c taiut1.c taiutc.c tcbtdb.c tcgtt.c tdbtcb.c tdbtt.c tf2a.c tf2d.c tr.c trxp.c trxpv.c tttai.c tttcg.c tttdb.c ttut1.c ut1tai.c ut1tt.c ut1utc.c utctai.c utcut1.c xy06.c xys00a.c xys00b.c xys06a.c zp.c zpv.c zr.c
SRCS = $(ORIG_SRCS) 
OBJS = a2af.o a2tf.o af2a.o anp.o anpm.o bi00.o bp00.o bp06.o bpn2xy.o c2i00a.o c2i00b.o c2i06a.o c2ibpn.o c2ixy.o c2ixys.o c2s.o c2t00a.o c2t00b.o c2t06a.o c2tcio.o c2teqx.o c2tpe.o c2txy.o cal2jd.o celes_core.o cp.o cpv.o cr.o d2dtf.o d2tf.o dat.o dtdb.o dtf2d.o ee00.o ee00a.o ee00b.o ee06a.o eect00.o eform.o eo06a.o eors.o epb.o epb2jd.o epj.o epj2jd.o epv00.o eqeq94.o era00.o fad03.o fae03.o faf03.o faju03.o fal03.o falp03.o fama03.o fame03.o fane03.o faom03.o fapa03.o fasa03.o faur03.o fave03.o fk52h.o fk5hip.o fk5hz.o fw2m.o fw2xy.o gc2gd.o gc2gde.o gd2gc.o gd2gce.o gmst00.o gmst06.o gmst82.o gst00a.o gst00b.o gst06.o gst06a.o gst94.o h2fk5.o hfk5z.o ir.o jd2cal.o jdcalf.o num00a.o num00b.o num06a.o numat.o nut00a.o nut00b.o nut06a.o nut80.o nutm80.o obl06.o obl80.o p06e.o p2pv.o p2s.o pap.o pas.o pb06.o pdp.o pfw06.o plan94.o pm.o pmat00.o pmat06.o pmat76.o pmp.o pn.o pn00.o pn00a.o pn00b.o pn06.o pn06a.o pnm00a.o pnm00b.o pnm06a.o pnm80.o pom00.o ppp.o ppsp.o pr00.o prec76.o pv2p.o pv2s.o pvdpv.o pvm.o pvmpv.o pvppv.o pvstar.o pvu.o pvup.o pvxpv.o pxp.o rm2v.o rv2m.o rx.o rxp.o rxpv.o rxr.o ry.o rz.o s00.o s00a.o s00b.o s06.o s06a.o s2c.o s2p.o s2pv.o s2xpv.o sepp.o seps.o sp00.o starpm.o starpv.o sxp.o sxpv.o taitt.o taiut1.o taiutc.o tcbtdb.o tcgtt.o tdbtcb.o tdbtt.o tf2a.o tf2d.o tr.o trxp.o trxpv.o tttai.o tttcg.o tttdb.o ttut1.o ut1tai.o ut1tt.o ut1utc.o utctai.o utcut1.o xy06.o xys00a.o xys00b.o xys06a.o zp.o zpv.o zr.o
HDRS = $(srcdir)/sofa.h $(srcdir)/sofam.h
TARGET = celes_core
TARGET_NAME = celes_core
TARGET_ENTRY = Init_$(TARGET_NAME)
DLLIB = $(TARGET).so
EXTSTATIC = 
STATIC_LIB = 

TIMESTAMP_DIR = .
BINDIR        = $(bindir)
RUBYCOMMONDIR = $(sitedir)$(target_prefix)
RUBYLIBDIR    = $(sitelibdir)$(target_prefix)
RUBYARCHDIR   = $(sitearchdir)$(target_prefix)
HDRDIR        = $(rubyhdrdir)/ruby$(target_prefix)
ARCHHDRDIR    = $(rubyhdrdir)/$(arch)/ruby$(target_prefix)

TARGET_SO     = $(DLLIB)
CLEANLIBS     = $(TARGET).so 
CLEANOBJS     = *.o  *.bak

all:    $(DLLIB)
static: $(STATIC_LIB)
.PHONY: all install static install-so install-rb
.PHONY: clean clean-so clean-static clean-rb

clean-static::
clean-rb-default::
clean-rb::
clean-so::
clean: clean-so clean-static clean-rb-default clean-rb
		-$(Q)$(RM) $(CLEANLIBS) $(CLEANOBJS) $(CLEANFILES) .*.time

distclean-rb-default::
distclean-rb::
distclean-so::
distclean-static::
distclean: clean distclean-so distclean-static distclean-rb-default distclean-rb
		-$(Q)$(RM) Makefile $(RUBY_EXTCONF_H) conftest.* mkmf.log
		-$(Q)$(RM) core ruby$(EXEEXT) *~ $(DISTCLEANFILES)
		-$(Q)$(RMDIRS) $(DISTCLEANDIRS) 2> /dev/null || true

realclean: distclean
install: install-so install-rb

install-so: $(DLLIB) $(TIMESTAMP_DIR)/.RUBYARCHDIR.time
	$(INSTALL_PROG) $(DLLIB) $(RUBYARCHDIR)
clean-static::
	-$(Q)$(RM) $(STATIC_LIB)
install-rb: pre-install-rb install-rb-default
install-rb-default: pre-install-rb-default
pre-install-rb: Makefile
pre-install-rb-default: Makefile
pre-install-rb-default:
	@$(NULLCMD)
$(TIMESTAMP_DIR)/.RUBYARCHDIR.time:
	$(Q) $(MAKEDIRS) $(@D) $(RUBYARCHDIR)
	$(Q) $(TOUCH) $@

site-install: site-install-so site-install-rb
site-install-so: install-so
site-install-rb: install-rb

.SUFFIXES: .c .m .cc .mm .cxx .cpp .o .S

.cc.o:
	$(ECHO) compiling $(<)
	$(Q) $(CXX) $(INCFLAGS) $(CPPFLAGS) $(CXXFLAGS) $(COUTFLAG)$@ -c $<

.cc.S:
	$(ECHO) translating $(<)
	$(Q) $(CXX) $(INCFLAGS) $(CPPFLAGS) $(CXXFLAGS) $(COUTFLAG)$@ -S $<

.mm.o:
	$(ECHO) compiling $(<)
	$(Q) $(CXX) $(INCFLAGS) $(CPPFLAGS) $(CXXFLAGS) $(COUTFLAG)$@ -c $<

.mm.S:
	$(ECHO) translating $(<)
	$(Q) $(CXX) $(INCFLAGS) $(CPPFLAGS) $(CXXFLAGS) $(COUTFLAG)$@ -S $<

.cxx.o:
	$(ECHO) compiling $(<)
	$(Q) $(CXX) $(INCFLAGS) $(CPPFLAGS) $(CXXFLAGS) $(COUTFLAG)$@ -c $<

.cxx.S:
	$(ECHO) translating $(<)
	$(Q) $(CXX) $(INCFLAGS) $(CPPFLAGS) $(CXXFLAGS) $(COUTFLAG)$@ -S $<

.cpp.o:
	$(ECHO) compiling $(<)
	$(Q) $(CXX) $(INCFLAGS) $(CPPFLAGS) $(CXXFLAGS) $(COUTFLAG)$@ -c $<

.cpp.S:
	$(ECHO) translating $(<)
	$(Q) $(CXX) $(INCFLAGS) $(CPPFLAGS) $(CXXFLAGS) $(COUTFLAG)$@ -S $<

.c.o:
	$(ECHO) compiling $(<)
	$(Q) $(CC) $(INCFLAGS) $(CPPFLAGS) $(CFLAGS) $(COUTFLAG)$@ -c $<

.c.S:
	$(ECHO) translating $(<)
	$(Q) $(CC) $(INCFLAGS) $(CPPFLAGS) $(CFLAGS) $(COUTFLAG)$@ -S $<

.m.o:
	$(ECHO) compiling $(<)
	$(Q) $(CC) $(INCFLAGS) $(CPPFLAGS) $(CFLAGS) $(COUTFLAG)$@ -c $<

.m.S:
	$(ECHO) translating $(<)
	$(Q) $(CC) $(INCFLAGS) $(CPPFLAGS) $(CFLAGS) $(COUTFLAG)$@ -S $<

$(DLLIB): $(DEFFILE) $(OBJS) Makefile
	$(ECHO) linking shared-object $(DLLIB)
	-$(Q)$(RM) $(@)
	$(Q) $(LDSHARED) -o $@ $(OBJS) $(LIBPATH) $(DLDFLAGS) $(LOCAL_LIBS) $(LIBS)



$(DEFFILE): 
	$(ECHO) generating $(@)
	$(Q) $(RUBY) -e "puts 'EXPORTS', '$(TARGET_ENTRY)'"  > $@

###
celes_core.o: celes_core.c sofa.h sofam.h a2af.c a2tf.c af2a.c \
		anp.c anpm.c bi00.c bp00.c bp06.c bpn2xy.c c2i00a.c c2i00b.c \
		c2i06a.c c2ibpn.c c2ixy.c c2ixys.c c2s.c c2t00a.c c2t00b.c \
		c2t06a.c c2tcio.c c2teqx.c c2tpe.c c2txy.c cal2jd.c cp.c cpv.c \
		cr.c d2dtf.c d2tf.c dat.c dtdb.c dtf2d.c ee00.c ee00a.c ee00b.c \
		ee06a.c eect00.c eform.c eo06a.c eors.c epb.c epb2jd.c epj.c \
		epj2jd.c epv00.c eqeq94.c era00.c fad03.c fae03.c faf03.c \
		faju03.c fal03.c falp03.c fama03.c fame03.c fane03.c faom03.c \
		fapa03.c fasa03.c faur03.c fave03.c fk52h.c fk5hip.c fk5hz.c \
		fw2m.c fw2xy.c gc2gd.c gc2gde.c gd2gc.c gd2gce.c gmst00.c \
		gmst06.c gmst82.c gst00a.c gst00b.c gst06.c gst06a.c gst94.c \
		h2fk5.c hfk5z.c ir.c jd2cal.c jdcalf.c num00a.c num00b.c \
		num06a.c numat.c nut00a.c nut00b.c nut06a.c nut80.c nutm80.c \
		obl06.c obl80.c p06e.c p2pv.c p2s.c pap.c pas.c pb06.c pdp.c \
		pfw06.c plan94.c pm.c pmat00.c pmat06.c pmat76.c pmp.c pn.c \
		pn00.c pn00a.c pn00b.c pn06.c pn06a.c pnm00a.c pnm00b.c \
		pnm06a.c pnm80.c pom00.c ppp.c ppsp.c pr00.c prec76.c pv2p.c \
		pv2s.c pvdpv.c pvm.c pvmpv.c pvppv.c pvstar.c pvu.c pvup.c \
		pvxpv.c pxp.c rm2v.c rv2m.c rx.c rxp.c rxpv.c rxr.c ry.c \
		rz.c s00.c s00a.c s00b.c s06.c s06a.c s2c.c s2p.c s2pv.c \
		s2xpv.c sepp.c seps.c sp00.c starpm.c starpv.c sxp.c sxpv.c \
		taitt.c taiut1.c taiutc.c tcbtdb.c tcgtt.c tdbtcb.c tdbtt.c \
		tf2a.c tf2d.c tr.c trxp.c trxpv.c tttai.c tttcg.c tttdb.c \
		ttut1.c ut1tai.c ut1tt.c ut1utc.c utctai.c utcut1.c xy06.c \
		xys00a.c xys00b.c xys06a.c zp.c zpv.c zr.c
