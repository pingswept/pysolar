# what it's called on pypi
%global srcname Pysolar
# what it's imported asn
%global libname pysolar
# name of egg info directory
%global eggname pysolar
# package name fragment
%global pkgname pysolar

%if %{defined rhel} || (%{defined fedora} && 0%{?fedora} < 30)
%bcond_without python2
%endif
%bcond_without python3

Name:           python-%{pkgname}
Version:        0.8
Release:        1%{?dist}
Summary:        Python library to perform solar calculations
License:        LGPLv3+
URL:            http://pysolar.org/
Source0:        https://github.com/pingswept/pysolar/archive/0.8.tar.gz
BuildArch:      noarch

%global _description \
Pysolar is a collection of Python libraries for simulating the irradiation of any point on earth by the sun. It includes code for extremely precise ephemeris calculations.

%description %{_description}

%if %{with python2}
%package -n     python2-%{pkgname}
Summary:        %{summary}
BuildRequires:  make
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
Provides:       python-%{srcname} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %{_description}
%endif

%if %{with python3}
%package -n     python%{python3_pkgversion}-%{pkgname}
Summary:        %{summary}
BuildRequires:  make
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-sphinx
Provides:       python%{python3_pkgversion}-%{srcname} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pkgname}}

%description -n python%{python3_pkgversion}-%{pkgname} %{_description}
%endif

%prep
%autosetup -p 1 -n %{pkgname}-%{version}

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if %{with python2}
%py2_build
%endif

%if %{with python3}
pushd %{py3dir}
%py3_build
popd
%endif

make -C doc html

%install
%if %{with python2}
%py2_install
%endif

%if %{with python3}
pushd %{py3dir}
%py3_install
popd
%endif

%check
%if %{with python2}
%{__python2} setup.py test
%endif

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%if %{with python2}
%files -n python2-%{pkgname}
%license COPYING
%doc doc/_build/html
%{python2_sitelib}/%{libname}
%{python2_sitelib}/%{eggname}-%{version}-py%{python2_version}.egg-info
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-%{pkgname}
%license COPYING
%doc doc/_build/html
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info
%endif

%changelog
* Mon Sep 16 2019 Elliot Lee <sopwith@gmail.com> - 0.8-1
- Initial version

