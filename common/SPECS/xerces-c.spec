Summary: Xerces-C++ validating XML parser
Name: xerces-c
Version: 3.2.4
Release: 1
URL: http://xerces.apache.org/xerces-c/
Source0: https://shibboleth.net/downloads/%{name}/%{name}-%{version}.tar.bz2
License: Apache-2.0
Group: Libraries
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

%package -n xerces-c-bin
Summary: Utilities for Xerces-C++ validating XML parser
Group: Development/Libraries

%description -n xerces-c-bin
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

This package contains the utility programs.

%package -n libxerces-c-3_2
Summary: Shared library for Xerces-C++ validating XML parser
Group: Development/Libraries
Provides: xerces-c = %{version}-%{release}

%description -n libxerces-c-3_2
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

This package contains just the shared library.

%package -n libxerces-c-devel
Group: Development/Libraries
Summary: Header files for Xerces-C++ validating XML parser
Requires: libxerces-c-3_2 = %{version}-%{release}
Provides: xerces-c-devel = %{version}-%{release}

%description -n libxerces-c-devel
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

The static libraries and header files needed for development with Xerces-C++.

%prep
%setup -q

%build
%configure %{?_with_curl:--enable-netaccessor-curl} %{!?_with_curl:--disable-netaccessor-curl} %{?_with_icu:--enable-transcoder-icu --enable-msgloader-icu} %{?xerces_options}
%{__make}

%install
%make_install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%post -n libxerces-c-3_2 -p /sbin/ldconfig

%postun -n libxerces-c-3_2 -p /sbin/ldconfig

%files -n xerces-c-bin
%defattr(755,root,root)
%{_bindir}/*

%files -n libxerces-c-3_2
%defattr(755,root,root)
%{_libdir}/libxerces-c-*.so

%files -n libxerces-c-devel
%defattr(-,root,root)
%{_includedir}/xercesc
%{_libdir}/libxerces-c.so
%{_libdir}/libxerces-c.a
%{_libdir}/pkgconfig/xerces-c.pc
%exclude %{_libdir}/libxerces-c.la

%changelog
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
