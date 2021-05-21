arch=$(rpm -E '%{_arch}')
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xerces*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xml-security-c*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*log4shib*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*curl-openssl*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xmltooling*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*libsaml*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*opensaml*
rpmbuild -ba --clean shibboleth.spec
rpmspec -q --rpms shibboleth.spec > ${EXT_BASE}/out/shibboleth.rpms
rpmspec -q --srpm shibboleth.spec > ${EXT_BASE}/out/shibboleth.srpm
createrepo_c ${EXT_BASE}/out/RPMS/${arch}
