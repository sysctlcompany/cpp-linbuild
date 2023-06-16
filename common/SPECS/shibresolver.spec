%define compname shibresolver
%define distname shibboleth-resolver
%define libname lib%{compname}6
%define develname lib%{compname}-devel

Name: %{distname}
Version: 3.4.0
Summary: Shibboleth SP Attribute Resolver Library
Release: 1
Vendor: Shibboleth Consortium
Group: System Environment/Libraries
License: Apache-2.0
URL: https://www.shibboleth.net/
Source0: https://shibboleth.net/downloads/service-provider/extensions/%{compname}/%{version}/%{distname}-%{version}.tar.bz2
BuildRequires: libxerces-c-devel >= 3.2
BuildRequires: libxml-security-c-devel >= 2.0.0
BuildRequires: libxmltooling-devel >= 3.2.0
BuildRequires: libsaml-devel >= 3.2.0
BuildRequires: shibboleth-devel >= 3.4.0
%{?_with_log4cpp:BuildRequires: liblog4cpp-devel >= 1.0}
%{!?_with_log4cpp:BuildRequires: liblog4shib-devel >= 1.0.4}
%{!?_without_gssapi:BuildRequires: krb5-devel}
BuildRequires: gcc-c++
BuildRequires: pkgconfig
%if "%{_vendor}" == "redhat"
BuildRequires: redhat-rpm-config
%endif

%if "%{_vendor}" == "suse"
%define pkgdocdir %{_docdir}/%{name}
%else
%define pkgdocdir %{_docdir}/%{name}-%{version}
%endif

%description
This package contains a Shibboleth SP Extension that provides
externally accessible attribute resolver functionality for processing
local and remote sources of federated attribute information.

%package -n %{libname}
Summary: Shibboleth SP Attribute Resolver library
Group: Development/Libraries
Provides: %{distname} = %{version}-%{release}
Obsoletes: %{distname} < %{version}-%{release}

%description -n %{libname}
This package contains a Shibboleth SP Extension that provides
externally accessible attribute resolver functionality for processing
local and remote sources of federated attribute information.

This package contains just the shared library.

%package -n %{develname}
Summary: Shibboleth SP Attribute Resolver development Headers
Group: Development/Libraries
Requires: %{libname} = %{version}-%{release}
Provides: %{distname}-devel = %{version}-%{release}
Obsoletes: %{distname}-devel < %{version}-%{release}
Requires: libxerces-c-devel >= 3.2
Requires: libxml-security-c-devel >= 2.0.0
Requires: libxmltooling-devel >= 3.2.0
Requires: libsaml-devel >= 3.2.0
Requires: shibboleth-devel >= 3.4.0
%{?_with_log4cpp:Requires: liblog4cpp-devel >= 1.0}
%{!?_with_log4cpp:Requires: liblog4shib-devel >= 1.0.4}

%description -n %{develname}
This package contains a Shibboleth SP Extension that provides
externally accessible attribute resolver functionality for processing
local and remote sources of federated attribute information.

This package includes files needed for development.

%prep
%setup -q

%build
%if 0%{?suse_version} >= 1300
    %configure --with-gssapi %{?shib_options} PKG_CONFIG_PATH=./pkgconfig-workarounds/opensuse13
%else
%if 0%{?suse_version} >= 1210
    %configure --with-gssapi %{?shib_options}
%else
%if 0%{?rhel} >= 7
    %configure --with-gssapi %{?shib_options} PKG_CONFIG_PATH=/opt/shibboleth/%{_lib}/pkgconfig
%else
%if 0%{?rhel} >= 6
    %configure --with-gssapi %{?shib_options} PKG_CONFIG_PATH=/opt/shibboleth/%{_lib}/pkgconfig:./pkgconfig-workarounds/rh6
%else
    %configure --with-gssapi %{?shib_options}
%endif
%endif
%endif
%endif
%{__make} pkgdocdir=%{pkgdocdir}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT
%make_install pkgdocdir=%{pkgdocdir}

%check
%{__make} check

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libshibresolver-lite.so.*
%{_libdir}/libshibresolver.so.*
%exclude %{_libdir}/*.la

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/shibresolver.pc
%{_libdir}/pkgconfig/shibresolver-lite.pc
%doc %{pkgdocdir}

%changelog
* Mon Oct 24 2022 Scott Cantor <cantor.2@osu.edu> - 3.4.0-1
- Bump version

* Thu Oct 28 2021 Scott Cantor  <cantor.2@osu.edu> - 3.3.0-1
- Bump version

* Mon Dec 7 2020  Scott Cantor  <cantor.2@osu.edu> - 3.2.0-1
- Bump version

* Thu Apr 2 2020  Scott Cantor  <cantor.2@osu.edu> - 3.1.0-1
- Bump version

* Mon Sep 30 2019  Scott Cantor  <cantor.2@osu.edu>  - 3.0.0-2
- CentOS 8 changes

* Fri Jul 20 2018  Scott Cantor  <cantor.2@osu.edu>  - 3.0.0-1
- Redo package for SP 3 release

* Wed Jan 25 2017  Scott Cantor  <cantor.2@osu.edu>  - 1.0.0-2
- Apply fixes to make this available via official package sets

* Wed Aug 27 2014  Scott Cantor  <cantor.2@osu.edu>  - 1.0-1
- Update specfile for release, with RH7 changes

* Tue Sep 14 2010  Scott Cantor  <cantor.2@osu.edu>  - 0.1-1
- Initial specfile
