%define compname log4shib
%define libname lib%{compname}2
%define develname lib%{compname}-devel

Name: %{libname}
Version: 2.0.1
Release: 2%{?dist}
Summary: Log for C++, Shibboleth Edition
License: LGPL-2.1-only
Group: Development/Libraries
Vendor: Shibboleth Consortium
URL: https://shibboleth.net/downloads/%{compname}/%{version}
Source0: https://shibboleth.net/downloads/%{compname}/%{version}/%{compname}-%{version}.tar.bz2
Provides: %{compname} = %{version}-%{release}
Obsoletes: %{compname} < %{version}-%{release}
BuildRequires: gcc-c++
BuildRequires: pkgconfig
%{!?_without_doxygenrpm:BuildRequires: doxygen}
%if "%{_vendor}" == "redhat"
BuildRequires: redhat-rpm-config
%endif

%if 0%{?rhel} >= 8 || 0%{?centos_version} >= 800
BuildRequires: gdb
%endif

%if "%{_vendor}" == "suse"
%define pkgdocdir %{_docdir}/%{compname}
%else
%define pkgdocdir %{_docdir}/%{compname}-%{version}
%endif

%description
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.

The main package contains just the shared library.

%package -n %{develname}
Summary: Development tools for Log for C++
Group: Development/Libraries
Requires: %{libname} = %{version}-%{release}
Provides: %{compname}-devel = %{version}-%{release}
Obsoletes: %{compname}-devel < %{version}-%{release}

%description -n %{develname}
The static libraries and header files needed for development with log4shib.

%prep
%setup -q -n %{compname}-%{version}

%build
%configure %{!?_without_doxygenrpm:--enable-doxygen} %{?_without_doxygenrpm:--disable-doxygen}
%{__make}

%install
%make_install apidir=$RPM_BUILD_ROOT%{pkgdocdir}/api
# If we use %%doc down below to package the README files from the build tree,
# it will blow away the package's docdir folder, and the installed API docs with it.
# Instead, copy the README files manually into the platform's docdir.
config/install-sh -d $RPM_BUILD_ROOT%{pkgdocdir}
config/install-sh -m 644 -c AUTHORS COPYING INSTALL NEWS README THANKS ChangeLog $RPM_BUILD_ROOT%{pkgdocdir}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post -n %{develname}
if test "x$RPM_INSTALL_PREFIX0" != "x" ; then
    %{__perl} -pi -e"s|^prefix=\"[^\"]*\"|prefix=\"$RPM_INSTALL_PREFIX0\"|" $RPM_INSTALL_PREFIX0/bin/log4shib-config
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-,root,root,755)
%{_includedir}/*
%{!?_without_doxygenrpm:%{_mandir}/man?/*}
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/pkgconfig/log4shib.pc
%exclude %{_libdir}/*.la
%doc %{pkgdocdir}

%changelog
* Sat Jun 17 2023 John W. O'Brien <john@saltant.com> - 2.0.1-2
- Normalize SPEC file whitespace
- Delete obsolete BuildRoot macro
- Limit macro specifications to one per line for diff-ability
- Conform License field to SPDX License List
- Escape macros in comments
- Ensure Source is valid and fetchable
- Adopt %make_install
- Parameterize (sub-)package names
- Replace empty main package with lib sub-package
- Append %dist to Release

* Thu Oct 28 2021 Scott Cantor <cantor.2@osu.edu> - 2.0.1-1
- Remove static library from manifest.

* Fri Sep 27 2019 Scott Cantor <cantor.2@osu.edu> - 2.0.0-2
- Remove old Solaris exclusions
- Add CentOS 8 gdb dependency

* Mon Jun 25 2018 Scott Cantor <cantor.2@osu.edu> - 2.0.0-1
- Bump version
- Switch to bzipped source

* Thu May 23 2013  Scott Cantor  <cantor.2@osu.edu>  - 1.0.6-1
- Patch to limit file handle leakage from prop-based configs

* Sat Jul 21 2012  Scott Cantor  <cantor.2@osu.edu>  - 1.0.5-1
- Fix Provides/Obsoletes versioning
- Update Vendor and URL

* Mon Dec 28 2009  Scott Cantor  <cantor.2@osu.edu>  - 1.0.4-1
- Sync package naming to support side by side installs

* Sat Oct 24 2009  Scott Cantor  <cantor.2@osu.edu>  - 1.0.3-2
- Cleaned up specfile for OpenSUSE build service

* Wed Aug 5 2009  Scott Cantor  <cantor.2@osu.edu>  - 1.0.3-1
- Cleaned up specfile for OpenSUSE build service
