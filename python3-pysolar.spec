# what it's called on pypi
%global srcname Pysolar
# what it's imported asn
%global libname pysolar
# name of egg info directory
%global eggname pysolar
# package name fragment
%global pkgname pysolar

Name:           python3-%{pkgname}
Version:        0.8
Release:        2%{?dist}
Summary:        Python library to perform solar calculations
License:        LGPLv3+
URL:            http://pysolar.org/
Source0:        https://github.com/pingswept/pysolar/archive/0.8.tar.gz
BuildArch:      noarch

%description
Pysolar is a collection of Python libraries for simulating the irradiation of
any point on earth by the sun. It includes code for extremely precise ephemeris
calculations.

BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-numpy

Provides:       python3-%{srcname} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{pkgname}}

%prep
%autosetup -p 1 -n %{pkgname}-%{version}

rm -rf %{py3dir}
cp -a . %{py3dir}

%build
pushd %{py3dir}
%py3_build
popd

make -C doc html

%install
pushd %{py3dir}
%py3_install
popd

%check
pushd %{py3dir}
%{__python3} setup.py test
popd

%files -n python%{python3_pkgversion}-%{pkgname}
%license COPYING
%doc doc/_build/html
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info

%changelog
* Fri Jun 19 2020 Johan Heikkila <johan.heikkila@gmail.com> - 0.8-2
- Removed python2
- Added BuildRequires python3-numpy

* Mon Sep 16 2019 Elliot Lee <sopwith@gmail.com> - 0.8-1
- Initial version
