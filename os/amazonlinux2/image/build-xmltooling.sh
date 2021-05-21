arch=$(rpm -E '%{_arch}')
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xerces*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*log4shib*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xml-security-c*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*curl-openssl*
rpmbuild -ba --clean xmltooling.spec
rpmspec -q --rpms xmltooling.spec > ${EXT_BASE}/out/xmltooling.rpms
rpmspec -q --srpm xmltooling.spec > ${EXT_BASE}/out/xmltooling.srpm
createrepo_c ${EXT_BASE}/out/RPMS/${arch}
