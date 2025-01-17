Name: shibboleth
Version: 3.5.0
Release: 2%{?dist}
Summary: Open source system for attribute-based Web SSO
Group: Productivity/Networking/Security
Vendor: Shibboleth Consortium
License: Apache-2.0
URL: http://shibboleth.net/
Source0: https://shibboleth.net/downloads/service-provider/%{version}/%{name}-sp-%{version}.tar.bz2
Obsoletes: shibboleth-sp = 2.5.0
Requires: openssl
%if 0%{?rhel} >= 6 || 0%{?amzn} == 1 || 0%{?amzn} == 2
Requires(pre,preun): xmltooling-schemas%{?_isa} >= 3.3.0
Requires(pre,preun): opensaml-schemas%{?_isa} >= 3.3.0
%else
Requires(pre,preun): xmltooling-schemas >= 3.3.0
Requires(pre,preun): opensaml-schemas >= 3.3.0
%endif
%if 0%{?suse_version} > 1030 && 0%{?suse_version} < 1130
Requires(pre,preun): %{insserv_prereq}
Requires(pre,preun): %{fillup_prereq}
%endif
%if 0%{?rhel} >= 7 || 0%{?amzn2023}
Requires: hostname
BuildRequires: systemd-devel
%else
Requires: net-tools
%endif
%if 0%{?rhel} >= 8
BuildRequires: gdb
%endif
BuildRequires: libxerces-c-devel >= 3.2
BuildRequires: libxml-security-c-devel >= 2.0.0
BuildRequires: libxmltooling-devel >= 3.2.0
BuildRequires: libsaml-devel >= 3.2.0
%{?_with_log4cpp:BuildRequires: liblog4cpp-devel >= 1.0}
%{!?_with_log4cpp:BuildRequires: liblog4shib-devel >= 2}
%if 0%{?rhel} == 6 || 0%{?rhel} == 7 || 0%{?amzn} == 1 || 0%{?amzn} == 2
Requires: libcurl-openssl%{?_isa} >= 7.21.7
BuildRequires: chrpath
%endif
%if 0%{?suse_version} > 1300
BuildRequires: libtool
%endif
BuildRequires: gcc-c++
BuildRequires: pkgconfig
BuildRequires: boost-devel >= 1.32.0
%{!?_without_gssapi:BuildRequires: krb5-devel}
%{!?_without_doxygen:BuildRequires: doxygen}
%{!?_without_odbc:BuildRequires:unixODBC-devel}
%{?_with_fastcgi:BuildRequires: fcgi-devel}
%if 0%{?centos} == 6 || 0%{?centos} == 7 || 0%{?rhel} >= 6 || 0%{?amzn2023}
BuildRequires: libmemcached-devel
%endif
%{?_with_memcached:BuildRequires: libmemcached-devel}
%if "%{_vendor}" == "redhat" || "%{_vendor}" == "amazon"
%if 0%{?rhel} >= 6 || 0%{?amzn} == 1 || 0%{?amzn} == 2
%{!?_without_builtinapache:BuildRequires: httpd-devel%{?_isa}}
%else
%{!?_without_builtinapache:BuildRequires: httpd-devel}
%endif
BuildRequires: redhat-rpm-config
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
%endif
%if "%{_vendor}" == "suse"
Requires(pre): pwdutils
%{!?_without_builtinapache:BuildRequires: apache2-devel}
%{?systemd_requires}
%if 0%{?suse_version} >= 1210
BuildRequires: systemd-rpm-macros
BuildRequires: systemd-devel
%endif
%endif

%define runuser shibd
%if "%{_vendor}" == "suse"
%define pkgdocdir %{_docdir}/shibboleth
%else
%define pkgdocdir %{_docdir}/shibboleth-%{version}
%endif

%description
Shibboleth is a Web Single Sign-On implementations based on OpenSAML
that supports multiple protocols, federated identity, and the extensible
exchange of rich attributes subject to privacy controls.

This package contains the Shibboleth Service Provider runtime libraries,
daemon, default plugins, and Apache module(s).

%package devel
Summary: Shibboleth Development Headers
Group: Development/Libraries/C and C++
Requires: %{name} = %{version}-%{release}
Obsoletes: shibboleth-sp-devel = 2.5.0
Requires: libxerces-c-devel >= 3.2
Requires: libxml-security-c-devel >= 2.0.0
Requires: libxmltooling-devel >= 3.3.0
Requires: libsaml-devel >= 3.3.0
%{?_with_log4cpp:Requires: liblog4cpp-devel >= 1.0}
%{!?_with_log4cpp:Requires: liblog4shib-devel >= 2}

%description devel
Shibboleth is a Web Single Sign-On implementations based on OpenSAML
that supports multiple protocols, federated identity, and the extensible
exchange of rich attributes subject to privacy controls.

This package includes files needed for development with Shibboleth.

%prep
%setup -q -n %{name}-sp-%{version}

%build
%if 0%{?suse_version} >= 1300
    %configure %{?_without_odbc:--disable-odbc} %{?_without_adfs:--disable-adfs} %{?_with_fastcgi} %{!?_without_gssapi:--with-gssapi} %{!?_without_systemd:--enable-systemd} %{?shib_options} PKG_CONFIG_PATH=./pkgconfig-workarounds/opensuse13
%else
%if 0%{?suse_version} >= 1210
    %configure %{?_without_odbc:--disable-odbc} %{?_without_adfs:--disable-adfs} %{?_with_fastcgi} %{!?_without_gssapi:--with-gssapi} %{!?_without_systemd:--enable-systemd} %{?shib_options}
%else
%if 0%{?amzn2023}
    %configure %{?_without_odbc:--disable-odbc} %{?_without_adfs:--disable-adfs} %{?_with_fastcgi} %{!?_without_gssapi:--with-gssapi} %{?_with_memcached} %{!?_without_systemd:--enable-systemd} %{?shib_options}
%else
%if 0%{?rhel} >= 8
    %configure %{?_without_odbc:--disable-odbc} %{?_without_adfs:--disable-adfs} %{?_with_fastcgi} %{!?_without_gssapi:--with-gssapi} %{?_with_memcached} %{!?_without_systemd:--enable-systemd} %{?shib_options}
%else
%if 0%{?rhel} >= 7
    %configure %{?_without_odbc:--disable-odbc} %{?_without_adfs:--disable-adfs} %{?_with_fastcgi} %{!?_without_gssapi:--with-gssapi} %{!?_without_memcached:--with-memcached} %{!?_without_systemd:--enable-systemd} %{?shib_options} PKG_CONFIG_PATH=/opt/shibboleth/%{_lib}/pkgconfig
%else
%if 0%{?centos} >= 6
    %configure %{?_without_odbc:--disable-odbc} %{?_without_adfs:--disable-adfs} %{?_with_fastcgi} %{!?_without_gssapi:--with-gssapi} %{!?_without_memcached:--with-memcached} %{?shib_options} PKG_CONFIG_PATH=/opt/shibboleth/%{_lib}/pkgconfig:./pkgconfig-workarounds/rh6
%else
%if 0%{?rhel} >= 6
    %configure %{?_without_odbc:--disable-odbc} %{?_without_adfs:--disable-adfs} %{?_with_fastcgi} %{!?_without_gssapi:--with-gssapi} %{?_with-memcached} %{?shib_options} PKG_CONFIG_PATH=/opt/shibboleth/%{_lib}/pkgconfig:./pkgconfig-workarounds/rh6
%else
    %configure %{?_without_odbc:--disable-odbc} %{?_without_adfs:--disable-adfs} %{?_with_fastcgi} %{!?_without_gssapi:--with-gssapi} %{?_with_memcached} %{?shib_options}
%endif
%endif
%endif
%endif
%endif
%endif
%endif
%{__make} pkgdocdir=%{pkgdocdir}

%install
%make_install NOKEYGEN=1 pkgdocdir=%{pkgdocdir}

%if "%{_vendor}" == "suse"
    %{__sed} -i "s/\/var\/log\/httpd/\/var\/log\/apache2/g" \
        $RPM_BUILD_ROOT%{_sysconfdir}/shibboleth/native.logger
%endif

# Plug the SP into the built-in Apache on a recognized system.
touch rpm.filelist
APACHE_CONFIG="no"
if [ -f $RPM_BUILD_ROOT%{_libdir}/shibboleth/mod_shib_13.so ] ; then
    APACHE_CONFIG="apache.config"
fi
if [ -f $RPM_BUILD_ROOT%{_libdir}/shibboleth/mod_shib_20.so ] ; then
    APACHE_CONFIG="apache2.config"
fi
if [ -f $RPM_BUILD_ROOT%{_libdir}/shibboleth/mod_shib_22.so ] ; then
    APACHE_CONFIG="apache22.config"
fi
if [ -f $RPM_BUILD_ROOT%{_libdir}/shibboleth/mod_shib_24.so ] ; then
    APACHE_CONFIG="apache24.config"
fi
%{?_without_builtinapache:APACHE_CONFIG="no"}
if [ "$APACHE_CONFIG" != "no" ] ; then
    APACHE_CONFD="no"
    if [ -d %{_sysconfdir}/httpd/conf.d ] ; then
        APACHE_CONFD="%{_sysconfdir}/httpd/conf.d"
    fi
    if [ -d %{_sysconfdir}/apache2/conf.d ] ; then
        APACHE_CONFD="%{_sysconfdir}/apache2/conf.d"
    fi
    if [ "$APACHE_CONFD" != "no" ] ; then
        %{__mkdir} -p $RPM_BUILD_ROOT$APACHE_CONFD
        %{__cp} -p $RPM_BUILD_ROOT%{_sysconfdir}/shibboleth/$APACHE_CONFIG $RPM_BUILD_ROOT$APACHE_CONFD/shib.conf
        echo "%config(noreplace) $APACHE_CONFD/shib.conf" >> rpm.filelist
    fi
fi

# Establish location of systemd file, if any.
SYSTEMD_SHIBD="no"
%if 0%{?suse_version} >= 1210 || 0%{?rhel} >= 7 || 0%{?amzn2023}
    %{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
    echo "%attr(0444,-,-) %{_unitdir}/shibd.service" >> rpm.filelist
    SYSTEMD_SHIBD="$RPM_BUILD_ROOT%{_unitdir}/shibd.service"

    # Get run directory created at boot time.
    %{__mkdir} -p $RPM_BUILD_ROOT%{_tmpfilesdir}
    echo "%attr(0444,-,-) %{_tmpfilesdir}/%{name}.conf" >> rpm.filelist
    cat > $RPM_BUILD_ROOT%{_tmpfilesdir}/%{name}.conf <<EOF
d /run/%{name} 755 %{runuser} %{runuser} -
EOF
%endif

# Otherwise, establish location of sysconfig file, if any.
SYSCONFIG_SHIBD="no"
if [ "$SYSTEMD_SHIBD" == "no" ] ; then
%if "%{_vendor}" == "redhat" || "%{_vendor}" == "amazon"
    %{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
    echo "%config(noreplace) %{_sysconfdir}/sysconfig/shibd" >> rpm.filelist
    SYSCONFIG_SHIBD="$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/shibd"
%endif
%if "%{_vendor}" == "suse"
    %{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/adm/fillup-templates
    echo "%{_localstatedir}/adm/fillup-templates/sysconfig.shibd" >> rpm.filelist
    SYSCONFIG_SHIBD="$RPM_BUILD_ROOT%{_localstatedir}/adm/fillup-templates/sysconfig.shibd"
%endif
fi

if [ "$SYSTEMD_SHIBD" != "no" ] ; then
    # Populate the systemd file
    cat > $SYSTEMD_SHIBD <<EOF
[Unit]
Description=Shibboleth Service Provider Daemon
Documentation=https://wiki.shibboleth.net/confluence/display/SP3/Home
After=network-online.target
Before=httpd.service

[Service]
Type=notify
NotifyAccess=main
User=%{runuser}
%if 0%{?rhel} == 6 || 0%{?rhel} == 7 || 0%{?amzn} == 1 || 0%{?amzn} == 2
Environment=LD_LIBRARY_PATH=/opt/shibboleth/%{_lib}
%endif
ExecStart=%{_sbindir}/shibd -f -F
StandardInput=null
StandardOutput=null
StandardError=journal
TimeoutStopSec=1m
TimeoutStartSec=5m
Restart=on-failure
RestartSec=30s

[Install]
WantedBy=multi-user.target
EOF
elif [ "$SYSCONFIG_SHIBD" != "no" ] ; then
    # Populate the sysconfig file.
    cat > $SYSCONFIG_SHIBD <<EOF
# Shibboleth SP init script customization

# User account for shibd
SHIBD_USER=%{runuser}

# Umask for shibd
# SHIBD_UMASK=022

# Wait period (secs) for configuration (and metadata) to load
SHIBD_WAIT=30
EOF
    %if 0%{?rhel} == 6 || 0%{?rhel} == 7 || 0%{?amzn} == 1 || 0%{?amzn} == 2
        cat >> $SYSCONFIG_SHIBD <<EOF

# Override OS-supplied libcurl
export LD_LIBRARY_PATH=/opt/shibboleth/%{_lib}
EOF
    %endif
fi

%if 0%{?rhel} == 6 || 0%{?rhel} == 7 || 0%{?amzn} == 1 || 0%{?amzn} == 2
    # Strip existing rpath to libcurl.
    chrpath -d $RPM_BUILD_ROOT%{_sbindir}/shibd
    chrpath -d $RPM_BUILD_ROOT%{_bindir}/mdquery
    chrpath -d $RPM_BUILD_ROOT%{_bindir}/resolvertest
%endif

%if "%{_vendor}" == "redhat" || "%{_vendor}" == "amazon" || "%{_vendor}" == "suse"
if [ "$SYSTEMD_SHIBD" == "no" ] ; then
    install -d -m 0755 $RPM_BUILD_ROOT%{_initddir}
    install -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/shibboleth/shibd-%{_vendor} $RPM_BUILD_ROOT%{_initddir}/shibd
%if "%{_vendor}" == "suse"
    install -d -m 0755 $RPM_BUILD_ROOT/%{_sbindir}
    %{__ln_s} -f %{_initddir}/shibd $RPM_BUILD_ROOT%{_sbindir}/rcshibd
%endif
fi
%endif

%check
%{__make} check

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group %{runuser} >/dev/null || groupadd -r %{runuser}
getent passwd %{runuser} >/dev/null || useradd -r -g %{runuser} \
    -d  %{_localstatedir}/run/shibboleth -s /sbin/nologin -c "Shibboleth SP daemon" %{runuser}
%if 0%{?suse_version} >= 1210
    %service_add_pre shibd.service
%endif
exit 0

%post
/sbin/ldconfig

# Generate two keys on new installs.
if [ $1 -eq 1 ] ; then
    cd %{_sysconfdir}/shibboleth
    /bin/sh ./keygen.sh -b -n sp-signing -u %{runuser} -g %{runuser}
    /bin/sh ./keygen.sh -b -n sp-encrypt -u %{runuser} -g %{runuser}
fi

%if "%{_vendor}" == "redhat" || "%{_vendor}" == "amazon"
if [ $1 -gt 1 ] ; then
        # On Red Hat with shib.conf installed, clean up old Alias commands
        # by pointing them at new version-independent /usr/share/share tree.
        # Any Aliases we didn't create we assume are custom files.
        # This is to accomodate making shib.conf a noreplace config file.
        # We can't do this for SUSE, because they disallow changes to
        # packaged files in scriplets.
        APACHE_CONF="no"
        if [ -f %{_sysconfdir}/httpd/conf.d/shib.conf ] ; then
            APACHE_CONF="%{_sysconfdir}/httpd/conf.d/shib.conf"
        fi
        if [ "$APACHE_CONF" != "no" ] ; then
            %{__sed} -i "s/\/usr\/share\/doc\/shibboleth\(\-\(.\)\{1,\}\)\{0,1\}\/main\.css/\/usr\/share\/shibboleth\/main.css/g" \
                $APACHE_CONF
            %{__sed} -i "s/\/usr\/share\/doc\/shibboleth\(\-\(.\)\{1,\}\)\{0,1\}\/logo\.jpg/\/usr\/share\/shibboleth\/logo.jpg/g" \
                $APACHE_CONF
        fi
    fi

%if 0%{?rhel} >= 7 || 0%{?amzn2023}
    # Initial prep for systemd
    %systemd_post shibd.service
    if [ $1 -gt 1 ] ; then
        systemctl daemon-reload
    fi
%else
    # Add the proper /etc/rc*.d links for the script
    /sbin/chkconfig --add shibd
%endif
%endif
%if "%{_vendor}" == "suse"
%if 0%{?suse_version} >= 1210
    %service_add_post shibd.service
    systemd-tmpfiles --create %{_tmpfilesdir}/%{name}.conf
%else
    # This adds the proper /etc/rc*.d links for the script
    # and populates the sysconfig/shibd file.
    cd /
    %{fillup_only -n shibd}
    %insserv_force_if_yast shibd
%endif
%endif

%preun
# On final removal, stop shibd and remove service, restart Apache if running.
%if "%{_vendor}" == "redhat" || "%{_vendor}" == "amazon"
%if 0%{?rhel} >= 7 || 0%{?amzn2023}
    %systemd_preun shibd.service
%else
    if [ $1 -eq 0 ] ; then
        /sbin/service shibd stop >/dev/null 2>&1
        /sbin/chkconfig --del shibd
    fi
%endif
    if [ $1 -eq 0 ] ; then
        %{!?_without_builtinapache:/sbin/service httpd status 1>/dev/null && /sbin/service httpd restart 1>/dev/null}
        exit 0
    fi
%endif
%if "%{_vendor}" == "suse"
%if 0%{?suse_version} >= 1210
        %service_del_preun shibd.service
%else
    %stop_on_removal shibd
%endif
    if [ $1 -eq 0 ] ; then
        %{!?_without_builtinapache:/sbin/service apache2 status 1>/dev/null && /sbin/service apache2 restart 1>/dev/null}
        exit 0
    fi
%endif
exit 0

%postun
/sbin/ldconfig
%if "%{_vendor}" == "redhat" || "%{_vendor}" == "amazon"
# On upgrade, restart components if they're already running.
%if 0%{?rhel} >= 7 || 0%{?amzn2023}
    %systemd_postun_with_restart shibd.service
%else
    if [ $1 -ge 1 ] ; then
        /sbin/service shibd status 1>/dev/null && /sbin/service shibd restart 1>/dev/null
    fi
%endif
    if [ $1 -ge 1 ] ; then
        %{!?_without_builtinapache:/sbin/service httpd status 1>/dev/null && /sbin/service httpd restart 1>/dev/null}
        exit 0
    fi
%endif
%if "%{_vendor}" == "suse"
%if 0%{?suse_version} >= 1210
    %service_del_postun shibd.service
%else
    cd /
    %restart_on_update shibd
    %{insserv_cleanup}
%endif
    %{!?_without_builtinapache:%restart_on_update apache2}
%endif

%posttrans
# One-time extra restart of shibd and Apache to work around
# SUSE bug that breaks old %%restart_on_update macro.
# If we remove, upgrades from pre-systemd to post-systemd
# will stop doing the final restart.
%if "%{_vendor}" == "suse" && 0%{?suse_version} >= 1210
    /usr/bin/systemctl try-restart shibd >/dev/null 2>&1 || :
    /usr/bin/systemctl try-restart apache2 >/dev/null 2>&1 || :
%endif
exit 0

%files -f rpm.filelist
%defattr(-,root,root,-)
%{_sbindir}/shibd
%{_bindir}/mdquery
%{_bindir}/resolvertest
%{_libdir}/libshibsp.so.*
%{_libdir}/libshibsp-lite.so.*
%exclude %{_libdir}/*.la
%dir %{_libdir}/shibboleth
%{_libdir}/shibboleth/*.so
%exclude %{_libdir}/shibboleth/*.la
%{?_with_fastcgi:%{_libdir}/shibboleth/shibauthorizer}
%{?_with_fastcgi:%{_libdir}/shibboleth/shibresponder}
%attr(0750,%{runuser},%{runuser}) %dir %{_localstatedir}/log/shibboleth
%if 0%{?suse_version} < 1300
%attr(0755,%{runuser},%{runuser}) %dir %{_localstatedir}/run/shibboleth
%endif
%attr(0755,%{runuser},%{runuser}) %dir %{_localstatedir}/cache/shibboleth
%dir %{_datadir}/xml/shibboleth
%{_datadir}/xml/shibboleth/*
%dir %{_datadir}/shibboleth
%{_datadir}/shibboleth/*
%dir %{_sysconfdir}/shibboleth
%config(missingok, noreplace) %{_sysconfdir}/shibboleth/shibboleth2.xml
%config(noreplace) %{_sysconfdir}/shibboleth/attribute-map.xml
%config(noreplace) %{_sysconfdir}/shibboleth/attribute-policy.xml
%config(noreplace) %{_sysconfdir}/shibboleth/example-metadata.xml
%config(noreplace) %{_sysconfdir}/shibboleth/protocols.xml
%config(noreplace) %{_sysconfdir}/shibboleth/security-policy.xml
%config(noreplace) %{_sysconfdir}/shibboleth/*.html
%config(noreplace) %{_sysconfdir}/shibboleth/*.logger
%if "%{_vendor}" == "redhat"
%if 0%{?rhel} >= 7
%else
%config %{_initddir}/shibd
%endif
%endif
%if "%{_vendor}" == "amazon" && 0%{?amzn} == 2
%config %{_initddir}/shibd
%endif
%if "%{_vendor}" == "suse" && 0%{?suse_version} < 1210
%config %{_initddir}/shibd
%{_sbindir}/rcshibd
%endif
%if 0%{?suse_version} >= 1210 || 0%{?rhel} >= 7 || 0%{?amzn2023}
%{_tmpfilesdir}/%{name}.conf
%endif
%{_sysconfdir}/shibboleth/example-shibboleth2.xml
%{_sysconfdir}/shibboleth/*.dist
%{_sysconfdir}/shibboleth/apache*.config
%{_sysconfdir}/shibboleth/shibd-*
%attr(0755,root,root) %{_sysconfdir}/shibboleth/keygen.sh
%attr(0755,root,root) %{_sysconfdir}/shibboleth/metagen.sh
%attr(0755,root,root) %{_sysconfdir}/shibboleth/seckeygen.sh
%doc %{pkgdocdir}
%exclude %{pkgdocdir}/api

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libshibsp.so
%{_libdir}/libshibsp-lite.so
%{_libdir}/pkgconfig/*.pc
%doc %{pkgdocdir}/api

%changelog
* Tue Oct 22 2024 Scott Cantor <cantor.2@osu.edu> - 3.5.0-2
- Turn off memcache option for newer platforms

* Wed Oct 16 2024 Scott Cantor <cantor.2@osu.edu> - 3.5.0-1
- Bump version and xmltooling/opensaml dependencies

* Wed Jul 31 2024 Scott Cantor <cantor.2@osu.edu> - 3.4.1-6
- SSPCPP-990 - Add dedicated configure for AL2023
- Fix missing memcache dep. on newer platforms

* Tue Jul 30 2024 John W. O'Brien <john@saltant.com> - 3.4.1-5
- SSPCPP-989 Fix add'l SysV/SystemD mismatches on AL2023

* Sun Jun 30 2024 John W. O'Brien <john@saltant.com> - 3.4.1-4
- SSPCPP-987 Include missed conversion from SysV to SystemD for AL2023

* Sat Jun 17 2023 John W. O'Brien <john@saltant.com> - 3.4.1-3
- Normalize SPEC file whitespace
- Delete obsolete BuildRoot macro
- Limit macro specifications to one per line for diff-ability
- Escape macros in comments
- Avoid hardcoding library path
- Replace deprecated PreReq
- Run %setup quietly
- Ensure Source is valid and fetchable
- Adopt %make_install
- Drop support for RHEL 5
- Append %dist to Release

* Fri Mar 24 2023 John W. O'Brien <john@saltant.com> 3.4.1-2
- Build with memcached on RHEL 8 and later and derivatives

* Wed Nov 2 2022 Scott Cantor <cantor.2@osu.edu> - 3.4.0-1
- Version bump

* Thu Apr 22 2021 Scott Cantor <cantor.2@osu.edu> - 3.2.2-1
- Fix devel dependency versions

* Tue Dec 1 2020 Scott Cantor <cantor.2@osu.edu> - 3.2.0-1
- Version and lib bump

* Mon Feb 3 2020 Scott Cantor <cantor.2@osu.edu> - 3.1.0-1
- Version and lib bump
- Add hostname dependency for keygen script

* Mon Sep 30 2019 Scott Cantor <cantor.2@osu.edu> - 3.0.4-1
- CentOS 8 cleanup

* Mon Apr 30 2018 Scott Cantor <cantor.2@osu.edu> - 3.0.0-1
- Bump dependency versions
- Require updated libraries across the board
- Generate two keys on new installs

* Tue May 03 2016 Scott Cantor <cantor.2@osu.edu> - 2.6.0-1
- Bump opensaml dependency version
- Bump max wait time for shibd systemd unit file

* Thu Jul 23 2015 Scott Cantor <cantor.2@osu.edu> - 2.5.5-2
- Fix use of /var/run/shibboleth on newer tmpfs platforms

* Thu Jul 2 2015 Scott Cantor <cantor.2@osu.edu> - 2.5.5-1
- Revamp with systemd support for RH/CentOS 7+ and SUSE 12.1+

* Mon Mar 9 2015 Scott Cantor <cantor.2@osu.edu> - 2.5.4-1
- Add Amazon VM support
- Add a separate native logging directory
- Remove hard-coded init.d usage
- Switch to bz2 sources to prevent future issues with SuSE

* Mon Nov 17 2014 Scott Cantor <cantor.2@osu.edu> - 2.5.3-2
- Add libtool dep for OpenSUSE 13
- Remove /var/run/shibboleth for OpenSUSE 13

* Tue May 13 2014 Ian Young <ian@iay.org.uk> - 2.5.3-1.2
- Update package dependencies for RHEL/CentOS 7
- Fix bogus dates in changelog

* Sat Jun 8 2013   Scott Cantor  <cantor.2@osu.edu>  - 2.5.2-1
- Add --with-gssapi using MIT K5 by default

* Tue Sep 25 2012  Scott Cantor  <cantor.2@osu.edu>  - 2.5.1-1
- Merge back various changes used in released packages
- Prep for 2.5.1 by pulling extra restart out

* Tue Aug 7 2012  Scott Cantor  <cantor.2@osu.edu>  - 2.5.0-2
- Changed package name back to shibboleth because of upgrade bugs
- Put back extra restart for this release only.

* Thu Mar 1 2012  Scott Cantor  <cantor.2@osu.edu>  - 2.5.0-1
- Move logo and stylesheet to version-independent tree
- Make shib.conf noreplace
- Post-fixup of Alias commands in older shib.conf
- Changes to run shibd as non-root shibboleth user
- Move init customizations to /etc/sysconfig/shibd
- Copy shibd restart for Red Hat to postun
- Add boost-devel dependency
- Build memcache plugin on RH6
- Add cachedir to install
- Add Apache 2.4 to install

* Sun Jun 26 2011  Scott Cantor  <cantor.2@osu.edu>  - 2.4.3-1
- Log files shouldn't be world readable.
- Explicit requirement for libcurl-openssl on RHEL6
- Uncomment LD_LIBRARY_PATH in init script for RHEL6
- Remove rpath from binaries for RHEL6

* Fri Dec 25 2009  Scott Cantor  <cantor.2@osu.edu>  - 2.4-1
- Update dependencies.

* Mon Nov 23 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.3.1-1
- Reset revision for 2.3.1 release

* Wed Aug 19 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.2.1-2
- SuSE init script changes
- Restart Apache on removal, not just upgrade
- Fix scriptlet exit values when Apache is stopped

* Mon Aug 10 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.2.1-1
- Doc handling changes
- SuSE init script

* Tue Aug 4 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.2.1-1
- Initial version for 2.2.1, with shibd/httpd restart on upgrade

* Thu Jun 25 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.2-3
- Add additional cleanup to posttrans fix

* Tue Jun 23 2009 Scott Cantor  <cantor.2@osu.edu>  - 2.2-2
- Reverse without_builtinapache macro test
- Fix init script handling on Red Hat to handle upgrades

* Wed Dec 3 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.2-1
- Bump minor version.
- Make keygen.sh executable.
- Fixing SUSE Xerces dependency name.
- Optionally package shib.conf.

* Tue Jun 10 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.1-1
- Change shib.conf handling to treat as config file.

* Mon Mar 17 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.0-6
- Official release.

* Fri Jan 18 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.0-5
- Release candidate 1.

* Sun Oct 21 2007 Scott Cantor  <cantor.2@osu.edu>  - 2.0-4
- libexec -> lib/shibboleth changes
- Added doc subpackage

* Thu Aug 16 2007 Scott Cantor  <cantor.2@osu.edu>  - 2.0-3
- First public beta.

* Fri Jul 13 2007 Scott Cantor  <cantor.2@osu.edu>  - 2.0-2
- Second alpha release.

* Sun Jun 10 2007 Scott Cantor  <cantor.2@osu.edu>  - 2.0-1
- First alpha release.

* Mon Oct 2 2006 Scott Cantor   <cantor.2@osu.edu>  - 1.3-11
- Applied fix for secadv 20061002
- Fix for metadata loader loop

* Thu Jun 15 2006 Scott Cantor  <cantor.2@osu.edu>  - 1.3-10
- Applied fix for sec 20060615

* Sat Apr 15 2006 Scott Cantor  <cantor.2@osu.edu>  - 1.3-9
- Misc. patches, SuSE, Apache 2.2, gcc 4.1, and 64-bit support

* Mon Jan 9 2006 Scott Cantor  <cantor.2@osu.edu>  - 1.3-8
- Applied new fix for secadv 20060109

* Tue Nov 8 2005 Scott Cantor  <cantor.2@osu.edu>  - 1.3-7
- Applied new fix for secadv 20050901 plus rollup

* Fri Sep 23 2005 Scott Cantor  <cantor.2@osu.edu>  - 1.3-6
- Minor patches and default config changes
- pidfile patch
- Fix shib.conf creation
- Integrated init.d script
- Prevent replacement of config files

* Thu Sep 1 2005  Scott Cantor  <cantor.2@osu.edu>  - 1.3-5
- Applied fix for secadv 20050901 plus rollup of NSAPI fixes

* Sun Apr 24 2005  Scott Cantor  <cantor.2@osu.edu>  - 1.3-1
- Updated test programs and location of schemas.
- move siterefresh to to sbindir

* Fri Apr  1 2005  Derek Atkins  <derek@ihtfp.com>  - 1.3-1
- Add selinux-targeted-policy package
- move shar to sbindir

* Tue Oct 19 2004  Derek Atkins  <derek@ihtfp.com>  - 1.2-1
- Create SPEC file based on various versions in existence.
