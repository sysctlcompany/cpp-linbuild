rpm --install ${EXT_BASE}/out/RPMS/x86_64/*xerces*
rpmbuild -ba --clean xml-security-c.spec
rpmspec -q --rpms xml-security-c.spec > ${EXT_BASE}/out/xml-security-c.rpms
rpmspec -q --srpm xml-security-c.spec > ${EXT_BASE}/out/xml-security-c.srpm
