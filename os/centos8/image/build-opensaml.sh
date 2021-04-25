rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xerces*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xml-security-c*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*log4shib*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xmltooling*
rpmbuild -ba --clean opensaml.spec
rpmspec -q --rpms opensaml.spec > ${EXT_BASE}/out/opensaml.rpms
rpmspec -q --srpm opensaml.spec > ${EXT_BASE}/out/opensaml.srpm
