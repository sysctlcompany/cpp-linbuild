%define compname xerces-c
%define libname lib%{compname}-3_2
%define develname lib%{compname}-devel
%define utilname %{compname}-bin

Summary: Xerces-C++ validating XML parser
Name: %{libname}
Version: 3.2.4
Release: 2%{?dist}
URL: https://xerces.apache.org/%{compname}/
Source0: https://shibboleth.net/downloads/%{compname}/%{compname}-%{version}.tar.bz2
Provides: %{compname} = %{version}-%{release}
Obsoletes: %{compname} < %{version}-%{release}
License: Apache-2.0
Group: Development/Libraries
BuildRequires: gcc-c++
BuildRequires: pkgconfig
%{?_with_curl:BuildRequires: curl-devel}
%{?_with_icu:BuildRequires: libicu-devel}
%if "%{_vendor}" == "redhat"
BuildRequires: redhat-rpm-config
%endif

%if 0%{?rhel} >= 8 || 0%{?centos_version} >= 800
BuildRequires: gdb
%endif

%description
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

The main package contains just the shared library.

%package -n %{utilname}
Summary: Utilities for Xerces-C++ validating XML parser
Group: Development/Libraries

%description -n %{utilname}
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

This package contains the utility programs.

%package -n %{develname}
Group: Development/Libraries
Summary: Header files for Xerces-C++ validating XML parser
Requires: %{libname} = %{version}-%{release}
Provides: %{compname}-devel = %{version}-%{release}

%description -n %{develname}
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

The static libraries and header files needed for development with Xerces-C++.

%prep
%setup -q -n %{compname}-%{version}

%build
%configure %{?_with_curl:--enable-netaccessor-curl} %{!?_with_curl:--disable-netaccessor-curl} %{?_with_icu:--enable-transcoder-icu --enable-msgloader-icu} %{?xerces_options}
%{__make}

%install
%make_install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n %{utilname}
%defattr(755,root,root)
%{_bindir}/*

%files
%defattr(755,root,root)
%{_libdir}/libxerces-c-*.so

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/xercesc
%{_libdir}/libxerces-c.so
%{_libdir}/libxerces-c.a
%{_libdir}/pkgconfig/xerces-c.pc
%exclude %{_libdir}/libxerces-c.la

%changelog
* Sat Jun 17 2023 John W. O'Brien <john@saltant.com> 3.2.4-2
- Normalize SPEC file whitespace
- Delete obsolete BuildRoot macro
- Limit macro specifications to one per line for diff-ability
- Conform License field to SPDX License List
- Ensure Source is valid and fetchable
- Adopt %make_install
- Drop support for relocatable xerces-c RPM
- Parameterize (sub-)package names
- Replace empty main package with lib sub-package
- Append %dist to Release

* Fri Oct 21 2022 John W. O'Brien <john@saltant.com> 3.2.4-1
- Bump version

* Wed Dec 23 2020 John W. O'Brien <john@saltant.com> 3.2.3-1
- Bump version

* Tue May 1 2018 Scott Cantor <cantor.2@osu.edu> 3.2.0-1
- Bump version

* Thu Feb 19 2015 Scott Cantor <cantor.2@osu.edu> 3.1.2-1
- Bump version, and remove Obsoletes

* Thu Apr 29 2010 Scott Cantor <cantor.2@osu.edu> 3.1.1-1
- Bump version and fix Provides/Obsoletes versioning

* Sun Feb 14 2010 Scott Cantor <cantor.2@osu.edu> 3.1.0-1
- Bump version

* Mon Dec 28 2009 Scott Cantor <cantor.2@osu.edu> 3.0.1-2
- Sync package names for side by side installation

* Wed Aug  5 2009 Scott Cantor <cantor.2@osu.edu> 3.0.1-1
- Disabled curl thanks to Red Hat

* Fri Mar  7 2008 Boris Kolpackov <boris@codesynthesis.com>
- Integrated updates for 3.0.0 from Scott Cantor.

* Fri Jun  6 2003 Tuan Hoang <tqhoang@bigfoot.com>
- updated for new Xerces-C filename and directory format
- fixed date format in changelog section

* Fri Mar 14 2003 Tinny Ng <tng@ca.ibm.com>
- changed to 2.3

* Wed Dec 18 2002 Albert Strasheim <albert@stonethree.com>
- added symlink to libxerces-c.so in lib directory

* Fri Dec 13 2002 Albert Strasheim <albert@stonethree.com>
- added seperate doc package
- major cleanups

* Tue Sep 03 2002  <thomas@linux.de>
- fixed missing DESTDIR in Makefile.util.submodule

* Mon Sep 02 2002  <thomas@linux.de>
- Initial build.
