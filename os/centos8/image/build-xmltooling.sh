rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xerces*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*log4shib*
rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xml-security-c*
rpmbuild -ba --clean xmltooling.spec
rpmspec -q --rpms xmltooling.spec > ${EXT_BASE}/out/xmltooling.rpms
rpmspec -q --srpm xmltooling.spec > ${EXT_BASE}/out/xmltooling.srpm
